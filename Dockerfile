FROM python:3.6.0
LABEL Maintainer "Ankur Agrawal"

# set environment variables

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1 

#  Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# Install Python and Package Libraries
RUN apt-get update && apt-get autoremove && apt-get autoclean
RUN apt-get install libpq-dev  -y
RUN apt-get install -y --no-install-recommends  postgresql postgresql-contrib 
# RUN virtualenv -p python3.6 /env

# ENV VIRTUAL_ENV /env
# ENV PATH /env/bin:$PATH

#RUN mkdir /code
WORKDIR /code

# COPY requirements.txt /code/requirements.txt
# COPY docker_entry.sh /code/docker_entry.sh

ADD . /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt


# RUN python manage.py migrate --noinput
EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Changing permission 
RUN ["chmod", "+x", "docker_entry.sh"]
CMD ["sh", "docker_entry.sh"]
# ENTRYPOINT [ "docker_entry.sh" ]