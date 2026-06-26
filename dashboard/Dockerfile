FROM python:3.10-slim


COPY requirements.txt /requirements.txt


RUN pip install --no-cache-dir pip --upgrade && \
    pip install --no-cache-dir wheel setuptools && \
    pip install --no-cache-dir numpy==1.23.5 pandas==1.5.3 && \
    pip install --no-cache-dir -r /requirements.txt

COPY ./src /src