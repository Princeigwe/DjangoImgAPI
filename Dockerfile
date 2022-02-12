# from the python image version in my computer
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create a code directory
RUN mkdir /code 

# make the code directory the working directory for DOcker
WORKDIR /code

RUN pip install --upgrade pip

# copying the Pipfile and Pipfile.lock in to the code dorectory
COPY Pipfile Pipfile.lock /code/

# using pipenv to manage the dependencies
RUN pip install pipenv && pipenv install --system

# copy the whole directory into Docker container
COPY . /code/