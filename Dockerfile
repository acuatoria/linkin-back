FROM python:3.11
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8000
# EXPOSE 8002

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:8080 --access-logfile - linkin.wsgi:application
