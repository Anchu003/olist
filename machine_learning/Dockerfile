FROM python:3.10-slim


COPY requirements.txt /requirements.txt


RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

COPY models /models


COPY src /src