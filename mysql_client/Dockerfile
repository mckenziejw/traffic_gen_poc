FROM python:3.8-slim-buster
WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
RUN pip3 install -r requirements.txt
COPY . . 
CMD ["python3", "app.py"]