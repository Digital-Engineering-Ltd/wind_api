FROM python:3.12-slim
LABEL maintainer="zzontou"

ENV PYTHONBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN pip install flake8

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin proj-bin libgeos-dev curl

# Install pyproj
RUN pip install pyproj

RUN pip install -r /tmp/requirements.txt
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

COPY ./windapi /windapi
WORKDIR /windapi
EXPOSE 8000

ENV PATH="/py/bin:$PATH"

USER django-user

ENTRYPOINT [ "sh", "/windapi/entrypoint.sh" ]