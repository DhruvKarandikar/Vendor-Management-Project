# Generated by Django 4.0.10 on 2024-05-06 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VendorDetail',
            fields=[
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('creation_by', models.TextField()),
                ('updation_date', models.DateTimeField(auto_now=True, null=True)),
                ('updation_by', models.TextField(blank=True, null=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('vendor_name', models.TextField()),
                ('contact_details', models.TextField()),
                ('vendor_code', models.CharField(max_length=100, unique=True)),
                ('on_time_delivery_rate', models.PositiveIntegerField()),
                ('quality_rating_avg', models.PositiveIntegerField()),
                ('average_response_time', models.PositiveIntegerField()),
                ('fulfillment_rate', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'vm_vendor_detail',
            },
        ),
        migrations.CreateModel(
            name='VendorPerformance',
            fields=[
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('creation_by', models.TextField()),
                ('updation_date', models.DateTimeField(auto_now=True, null=True)),
                ('updation_by', models.TextField(blank=True, null=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('on_time_delivery_rate', models.IntegerField()),
                ('quality_rating_avg', models.IntegerField()),
                ('average_response_time', models.IntegerField()),
                ('fulfillment_rate', models.IntegerField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='performance', to='vendor_app.vendordetail')),
            ],
            options={
                'db_table': 'vm_vendor_performance',
            },
        ),
        migrations.CreateModel(
            name='VendorDetailLog',
            fields=[
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('creation_by', models.TextField()),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('vendor_name', models.TextField()),
                ('contact_details', models.TextField()),
                ('vendor_code', models.CharField(max_length=100, unique=True)),
                ('on_time_delivery_rate', models.PositiveIntegerField()),
                ('quality_rating_avg', models.PositiveIntegerField()),
                ('average_response_time', models.PositiveIntegerField()),
                ('fulfillment_rate', models.PositiveIntegerField()),
                ('vendor_detail_log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logs', to='vendor_app.vendordetail')),
            ],
            options={
                'db_table': 'vm_vendor_detail_log',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('creation_by', models.TextField()),
                ('updation_date', models.DateTimeField(auto_now=True, null=True)),
                ('updation_by', models.TextField(blank=True, null=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('po_number', models.CharField(max_length=100, unique=True)),
                ('order_date', models.DateTimeField()),
                ('delivery_date', models.DateTimeField()),
                ('items', models.JSONField()),
                ('quantity', models.IntegerField(null=True)),
                ('current_status', models.IntegerField()),
                ('quality_rating', models.IntegerField(null=True)),
                ('issue_date', models.DateTimeField(null=True)),
                ('acknowledgment_date', models.DateTimeField(null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='vendor_purchase_orders', to='vendor_app.vendordetail')),
            ],
            options={
                'db_table': 'vm_purchase_order',
            },
        ),
    ]