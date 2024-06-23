FROM python:3.8-slim-buster
WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . . 
COPY geckodriver /usr/bin
CMD ["python3", "app.py"]