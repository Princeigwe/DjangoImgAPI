# DjangoImgAPI

This repo is concerning an API blog I'm currently writing, and any other API blog I'll write in the future. The README.md file will be updated as the project progresses.

For any problem concerning this documentation, you can reach me [here](igwep297@gmail.com).

Thank you.


## THE BUILD PROCESS:

This web application is built in a Docker container. It is possible to build this application outside a container, yeah, but I'm just practicing good building practice.

* Run the following in your terminal to create a new project folder: 

    `$ mkdir djImgAPI`

    You can use your desired project name here.

* Call the directory in your favourite IDE [in this case, mine is VSCode]:

    `$ cd djImgAPI`

* Run the following in the project root folder terminal to install Django:

    `$ pipenv install django`

    This installs the latest Django 4. After installation, the Pipfile and the Pipfile.lock should be created automatically.

* Activate the pipenv virtual environment by running:

    `$ pipenv shell`

    The best thing I love about the pipenv package, is the combination of a package manager and a virtual environment. It is so world class :ok_hand:.

* To start our django image API project, we run:

    `$ django-admin startproject DjangoImageAPI .`

    This create a `DjangoImageAPI` project in the current directory.

### Containerizing the project with a Docker container
Create a `Dockerfile` and a `docker-compose.yml` file in the root folder.


* **Content of the Dockerfile:**
    
    ```
    FROM python:3.8

    ENV PYTHONDONTWRITEBYTECODE=1

    ENV PYTHONUNBUFFERED=1

    RUN mkdir /code 

    WORKDIR /code

    RUN pip install --upgrade pip

    COPY Pipfile Pipfile.lock /code/

    RUN pip install pipenv && pipenv install --system
    ```


* **Content of docker-compose.yml**:
    
   ```
    version: '3'

    services:
    
        db:
            image: postgres:13.4-alpine
            container_name: 'DjangoImgAPI_DB'
            volumes:
            - ./data/db:/var/lib/postgresql/data
            environment:
            - POSTGRES_NAME=postgres
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=postgres
    
        web:
            build: .
            container_name: 'DjangoImgAPI_WEB'
            command: python /code/manage.py runserver 0.0.0.0:8000
            volumes:
            - .:/code
            ports:
            - 8000:8000
            
            depends_on:
            - db

   ```
* Build and run the container:

    `$ docker-compose up -d --build`

### **Setting up media and static folders**

    ```
    # settings.py

    STATIC_URL = '/static/'

    STATICFILES_DIR = os.path.join(BASE_DIR, 'static')
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    MEDIA_URL = '/media/'  
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


    # urls.py [from root folder]
    from django.conf import settings
    from django.contrib import admin
    from django.urls import path
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,       document_root=settings.MEDIA_ROOT)

    ```
### **Setting up PostgreSQL database and downloading djangorestframework**

* Install pyscopg2 for PostgreSQL database adapter Python

    `$ docker-compose exec web pipenv install psycopg2 djangorestframework` 

* Stop all containers and build them again, to add pyscopg2 to the environment

    ```
    $ docker-compose down
    $ docker-compose up -d --build
    ```

* Make changes to settings.py for PostgreSQL database

    ```
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_NAME'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD')
        }
    ```

### Setting up the framework in Django framework
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd party apps
    'rest_framework', # new
    
]
```
### **Creating the Image Resource Application**

`$ docker-compose exec web python manage.py startapp images`

* Setting up the image application:
    ```
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        
        # local apps
        'images.apps.ImagesConfig', # new
        
        # 3rd party apps
        'rest_framework',
        
    ]

    ```

* Setting up the image model
    ```
    from django.db import models

    class Image(models.Model):
        title = models.CharField(max_length=50)
        image = models.ImageField(upload_to='media/')
        caption = models.TextField(blank=True)
    
        def __str__(self):
            return self.title
    ```

    **_NOTE: IF A PERMISSION ERROR OCCURS AFTER THE CREATION OF A NEW APPLICATION, IT CAN BE RESOLVED BY RUNNING THE FOLLOWING_**

    `$ sudo chown -R $USER:$USER .`

* Creating migrations and migrating:

    ```
    $ docker-compose exec web python manage.py makemigrations images
    $ docker-compose exec web python manage.py migrate
    ```

* Create Image serializer:
    ```
    from . models import Image
    from rest_framework import serializers


    class ImageSerializer(serializers.ModelSerializer):
        class Meta:
            model = Image
            fields = ('id' ,'title', 'image', 'caption')
    ```
    This makes it possible to transmit the image object data from one party to another.

* Adding HTTP methods:
    Here API views are created which executes certain HTTP methods on the Image resource.
    Look at [images/views.py](https://github.com/Princeigwe/DjangoImgAPI/blob/main/images/views.py) for more details.

    API endpoints are created at: [images/urls.py](https://github.com/Princeigwe/DjangoImgAPI/blob/main/images/urls.py)



### **USER AUTHENTICATION AND AUTHORIZATION**
* Create a users app, and add to 'INSTALLED_APPS' list:


    ```
    $ docker-compose exec web python manage.py startapp users

    ```

* Create a CustomUser model in users app:

    ``` 
    from django.db import models
    from django.contrib.auth.models import AbstractUser
    from django.utils import timezone
    from django.contrib.auth.base_user import  BaseUserManager

    ## Model Manager for CustomUser
    class CustomUserManager(BaseUserManager):
    """The customer user manager is used to
    make emails the unique identifiers for authentication,
    instead of username
    """
    
    def create_user(self, email, password, **extra_fields):
        """function to create a save a user"""
        if not email:
            raise ValueError("The Email must be given")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """function to create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


    ## Custom User
    class CustomUser(AbstractUser):
        username = None
        email = models.EmailField('email address', unique=True)
        first_name = models.CharField(max_length=50, blank=True)
        last_name = models.CharField(max_length=50, blank=True)
        age = models.PositiveSmallIntegerField(blank=True, default=0)
        image = models.ImageField(upload_to='profile_pictures/', blank=True)
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []
        
        objects = CustomUserManager()
        
        def __str__(self):
            return self.email

    ```
    [Don't forget to migrate the model]

    ```
    $ docker-compose exec web python manage.py makemigrations users

    $ docker-compose exec web python manage.py migrate
    ```
#### **Installing the application for OAuth authorization**

    ``` 
    $ docker-compose exec web pipenv install django-oauth-toolkit
    ```

* Add the app to INSTALLED_APP list:
    ```
    ## settings.py
    INSTALLED_APPS = [
        ...,
        ...,
        'oauth2_provider', # Django OAuth2 app
    ]
    ```

    [stop and build Docker for it to recognize the new app]
    ``` 
    $ docker-compose down
    $ docker-compose build
    ```
    [Start up the containers again]