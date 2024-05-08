About Vendor Management Project:

The Vendor Management System developed using Django and Django REST Framework is a comprehensive solution designed to streamline vendor-related operations within an organization. This project facilitates efficient management of vendor profiles, purchase orders, and performance metrics, offering a centralized platform for monitoring and analyzing vendor interactions.
This system allows for the creation, retrieval, updating, and deletion of vendor profiles, each identified by a unique vendor code.
Through a RESTful API design, this project ensures seamless integration with other systems and applications, promoting interoperability and ease of use. 
Token-based authentication secures API endpoints, safeguarding sensitive vendor and purchase order information.

Note: Read the documentation.txt file before Interacting with API's 

Setting Up the project in you Local System:

Firstly, Use git clone and copy the project ssh into your terminal
command - python3 -m venv {yourenvfilename} for creating the python env file for the project 
command - pip install -r requirements.txt

For Databases connections Postgres is used as the Engine
Kindly, create the Database in Postgres

Hardcode the given values in the settings.py file 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_NAME"),  
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

Making a database schema in your local system 

Command - python manage.py migrate 
command - python manage.py runserver

After going to the localhost server in default browser
Swagger Settings are made in the API to make API interactive with UI UX 

Features:
- Custom Middleware
- Generic API's
- Jwt Authentication
- Override Django Methods
- Reduced API vulnerability
- Interactive API's using Swagger

