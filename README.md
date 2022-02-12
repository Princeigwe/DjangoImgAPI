# DjangoImgAPI

## Hello, My name is Prince, and I'm a Python back-end developer.

This repo is concerning an API blog I'm currently writing, and any other API blog I'll write in the future. The README.md file will be updated as the project progresses. 

Thank you.


## THE BUILD PROCESS:

This web application is built in a Docker container. It is possible to build this application outside a container, yeah, but I'm just practicing good building practice.

* Run the following in your terminal to create a new project folder: 
    > $ mkdir djImgAPI 

    You can use your desired project name here.

* Call the directory in your favourite IDE [in this case, mine is VSCode]:
    > $ cd djImgAPI

* Run the following in the project root folder terminal to install Django:
    > $ pipenv install django

    This installs the latest Django 4. After installation, the Pipfile and the Pipfile.lock should be created automatically.

* Activate the pipenv virtual environment by running:
    > $ pipenv shell

    The best thing I love about the pipenv package, is the combination of a package manager and a virtual environment. It is so world class :ok_hand:.

* To start our django image API project, we run:
    > $ django-admin startproject DjangoImageAPI .

    This create a `DjangoImageAPI` project in the current directory.

### Containerizing the project with a Docker container
Create a `Dockerfile` and a `docker-compose.yml` file in the root folder.


* **Content of the Dockerfile:**
    
    FROM python:3.8

    ENV PYTHONDONTWRITEBYTECODE=1

    ENV PYTHONUNBUFFERED=1

    RUN mkdir /code 

    WORKDIR /code

    RUN pip install --upgrade pip

    COPY Pipfile Pipfile.lock /code/

    RUN pip install pipenv && pipenv install --system


* **Content of docker-compose.yml**:
    
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

* Build and run the container:
    > $ docker-compose up -d --build