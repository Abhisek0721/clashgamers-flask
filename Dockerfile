# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /app

#copy to work directory
COPY requirements.txt requirements.txt

#set environment variables
ENV PYTHONUNBUFFERED 1

#install requirements
RUN pip3 install -r requirements.txt

#copy files of current directory to work directory
COPY . .

#final command
CMD ["gunicorn --bind 0.0.0.0:5000 wsgi:app"]