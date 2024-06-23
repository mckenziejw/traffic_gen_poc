FROM python:3.8-slim-buster
WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev
COPY . . 
COPY geckodriver /usr/bin
CMD ["python3", "app.py"]