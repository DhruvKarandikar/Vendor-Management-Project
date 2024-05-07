from django.db.models.query import QuerySet, Q
from django.db import models
from django.utils import timezone
import datetime
from functools import wraps
from django.db import models
from django.core.exceptions import FieldError
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField, ManyToOneRel, ManyToManyRel, OneToOneRel
import copy
from vendor_app.custom_helpers.consts import *
from typing import Any, Type
from vendor_app.custom_helpers.jwt_token import get_request
from vendor_app.custom_helpers.status_code import *



def add_log_model(logModel, modelInstance, modelName, creation=False, status_change=False):
    """_summary_
    Args:
        logModel (_type_): Log Model that want to create/update 
        modelInstance (_type_): Model from which the data will be added
        modelName (_type_): Model Name use in error showing
    """
    try:
        logModel = logModel()
        logModel.__dict__ = modelInstance.__dict__.copy()
        logModel.id = None
        logModel.log = modelInstance
        request = get_request()
        logModel.creation_by = request.user_id if request else CREATION_BY
        logModel.creation_date = datetime.datetime.now()
        logModel.save()
        return logModel
    except Exception as e:
        raise CustomExceptionHandler(f'{modelName} Log')



class CustomExceptionHandler(Exception):
    def __init__(self, message=''):
        # Call the base class constructor with the parameters it needs
        super(CustomExceptionHandler, self).__init__(message)


class CustomUpdateManager(QuerySet):
    logModel_config = {}

    @staticmethod
    def set_logModel(logModel, model):
        # map model with its respective log model
        CustomUpdateManager.logModel_config[model] = logModel   

    def update(self, *args, **kwargs):

        logModel_name = CustomUpdateManager.logModel_config.get(self.model.__name__)
        logModel = None
        from django.apps import apps
        for app in apps.get_app_configs():      
            # iterate over all models in an app configuration and get its log model
            for model in app.get_models():          
                if model.__name__ == logModel_name:
                    logModel = model
                    break

        if logModel:
            instances = [instance.id for instance in self]
            super().update(*args, **kwargs)        # updation
            instances = self.model.objects.filter(id__in=instances)

            for instance in instances:
                # add its log by storing the object
                add_log_model(logModel, instance, logModel.__name__)       
        else:
            # if log model not found
            raise CustomExceptionHandler(invalid_log_model(self.model.__name__))   


class ActiveQuerySetManager(CustomUpdateManager):
    @staticmethod
    def _extract_fields_from_Q_object(q: Q):
        """
        Extract fields from the keyword arguments provided during the initialization of Q objects.
        """
        for child in q.children:
            # contains keyword argument as tuples or Q object
            # Inside tuple the first element will be key of keyword argument which will be returned
            if isinstance(child, tuple):
                child = child[0]
                yield child
            if isinstance(q, Q):
                ActiveQuerySetManager._extract_fields_from_Q_object(child)

    @staticmethod
    def get_status_active_kwargs_for_kwarg(model:Type[models.Model],field,exclude,*args,**kwargs) -> dict:
        """
        This function returns a dictionary of keyword arguments which contains all the required status fields set to active .
        """
        reserved_nonfield_keywords = ["exact","iexact","contains","icontains","in","gt","gte","lt","lte","startswith","istartswith","endswith","iendswith","range","date","year","iso_year","month","day","week","week_day","iso_week_day","quarter","time","hour","minute","second","isnull","regex","iregex"]
        # get all related fields from current model
        related_fields = {field.name: field for field in model._meta.get_fields() if isinstance(field, (ForeignKey, ManyToManyField, OneToOneField, ManyToOneRel, ManyToManyRel, OneToOneRel))}

        if "__" in field:
            first, *rest = field.split("__")
            if first in related_fields and rest[0] not in reserved_nonfield_keywords and f"{first}__status" not in kwargs.keys():
                # Makes sure that status is not already provided in keyword arguments
                status_active_kwargs = {f"{first}__status": 1} if not exclude else {f"{first}__status": 0}
                recursive_status_active_kwargs = ActiveQuerySetManager.get_status_active_kwargs_for_kwarg(related_fields.get(first).related_model, "__".join(rest),exclude,**kwargs)
                relative_recursive_status_active_kwargs = {
                    f"{first}__{key}": value for key, value in recursive_status_active_kwargs.items()
                }
                return {
                    **status_active_kwargs,
                    **relative_recursive_status_active_kwargs
                }
                
        return {}
    
    def _inject_status_active_in_kwargs(function):
        """
        This decorator replaces the kwargs with new set of kwargs which contains the status active kwargs
        """
        @wraps(function)
        def wrapper(instance, *args, **kwargs):
            Qs = [arg for arg in args if isinstance(arg, Q)]
            fields_extracted_from_Q = []

            for q in Qs:
                # If arguments has Q model objects
                fields_extracted_from_Q += list(ActiveQuerySetManager._extract_fields_from_Q_object(q))

            new_kwargs = copy.deepcopy(kwargs)
            exclude = False
            if function.__name__=="exclude":
                exclude = True

            status_active_kwargs = {"status": 1} if not exclude else {"status": 0}

            if 'status' in new_kwargs and new_kwargs['status']==0:
                # If user provides the status of object as INACTIVE [ALLOWS OVERRIDING]
                status_active_kwargs['status']=0
            for kwarg in [*kwargs.keys(), *fields_extracted_from_Q]:
                status_active_kwargs = {
                    **status_active_kwargs,
                    **ActiveQuerySetManager.get_status_active_kwargs_for_kwarg(instance.model,kwarg,exclude,**kwargs)
                }
            try:
                new_kwargs = {
                    **new_kwargs,
                    **status_active_kwargs
                }
                return function(instance, *args, **new_kwargs)
            except FieldError as field_error:
                return function(instance, *args, **kwargs)
        return wrapper
    
    @_inject_status_active_in_kwargs
    def filter(self, *args: Any, **kwargs: Any):
        """
        Custom filter(): which by default contains statuses as ACTIVE set.
        """
        return super().filter(*args, **kwargs)
    
    def prefetch_related(self, *lookups, **filter_kwargs):
        """
        Custom prefetch_related(): which by default has query as status ACTIVE set.
        """
        filtered_qs = self.filter(**filter_kwargs)
        # call prefetch_related on the filtered QuerySet
        return super(filtered_qs.__class__, filtered_qs).prefetch_related(*lookups)

    @_inject_status_active_in_kwargs
    def get(self, *args: Any, **kwargs: Any):
        """
        Custom get(): status is set to ACTIVE in the query by default.
        """
        return super().get(*args, **kwargs)

    @_inject_status_active_in_kwargs
    def get_or_create(self, defaults=None, **kwargs):
        """
        Custom get_or_create(): status is set to ACTIVE in the query by default.
        """
        return super().get_or_create(defaults,**kwargs)
    
    @_inject_status_active_in_kwargs
    def update_or_create(self, defaults=None, **kwargs):
        """
        Custom update_or_create(): status is set to ACTIVE in the query by default.
        """
        return super().update_or_create(defaults, **kwargs)
    
    def first(self):
        """Custom first(): First object in the list with status ACTIVE"""
        queryset_value=self
        if not self.ordered:
            queryset_value = self.order_by('id','-status')
        for obj in queryset_value:
            return obj
    
    def last(self):
        """Custom last(): Last object in the list with status ACTIVE"""
        queryset_value=self
        if not self.ordered:
            queryset_value = self.order_by('id','-status')
        last_object=None
        for obj in queryset_value:
            last_object = obj
        return last_object



class AddCommonField(models.Model):
    objects = CustomUpdateManager.as_manager()

    status = models.PositiveSmallIntegerField(null=False, default=STATUS_ACTIVE)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    creation_by = models.TextField(null=False)
    updation_date = models.DateTimeField(null=True, auto_now=True)
    updation_by = models.TextField(null=True, blank=True)
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Set the ‘updated_by’ field to the specified username or email
        update_field = kwargs.get('update_fields')
        if update_field:
            if "id" in update_field:
                update_field.remove('id')
            update_field.extend(["creation_date","creation_by",'updation_by',"updation_date"])
            
        if request := get_request():
            if not self.pk:
                self.creation_by = request.user_id
        else:
            self.creation_by = "Not API request"
            self.updation_by = "Not API request"
        super().save(*args, **kwargs)
        if not self.__dict__.get('log_id') and hasattr(self,'logs'):
            self.log_object = add_log_model(self.logs.model, self, self.__class__.__name__)


def dict_get_key_from_value(dict_obj, dict_val):
    try:
        if dict_val is not None:
            key_list = list(dict_obj.keys())
            val_list = list(dict_obj.values())
            try:
                position = val_list.index(int(dict_val))
            except:
                position = val_list.index(dict_val)
            return key_list[position]
        else: 
            return None 
    except:
        return None
    
def help_text_for_dict(dict_value):
    """
    Args:
        dict_value (_type_): Dict type

    Returns:
        _type_: String Format help text
    """
    return f'Enter value from this list - {list(dict_value.keys())}'


def get_datetime_to_str(datetime_obj, format, idx=0, format_type=COMMON_CHECK_FORMAT_TYPE[DATE_FORMAT]):
    from datetime import datetime
    
    if datetime_obj:
        if 'T' in datetime_obj:
            date = datetime_obj.split("T")[idx] 
        else:
            date = datetime_obj.split(" ")[idx]
        
        if COMMON_CHECK_FORMAT_TYPE[TIME_FORMAT] == format_type:
            date = datetime.strptime(date, TIME_HH_MM_SS)
        else:
            date = datetime.strptime(date, DATE_YYYY_MM_DD)
        if date:
            return datetime.strftime(date, format)
    return None


def common_checking_and_passing_value_from_list_dict(value, list_dict, error_label):
    """
    merged two functions common_dict_checking_and_passing_value, common_list_checking
    """
    if value == "":
        return None

    if value:
        if type(list_dict) == list:
            if value not in list_dict:
                raise CustomExceptionHandler(error_label)
            return value
        else:
            if type(value) == list:
                list_value = []
                for single_value in value:
                    if single_value not in list_dict.keys():
                        raise CustomExceptionHandler(error_label)
                    list_value.append(list_dict[single_value])
                return list_value
            
            if value not in list_dict.keys():
                raise CustomExceptionHandler(error_label)
                    
            return list_dict[value]
    return value
