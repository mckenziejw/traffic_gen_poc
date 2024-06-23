FROM ubuntu:20.04
COPY requirements.txt requirements.txt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip firefox
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dkpg -i google-chrome-stable_current_amd64.deb
RUN pip3 install -r requirements.txt
ENV DISPLAY=:0
COPY . . 
COPY geckodriver /usr/bin
COPY chrome-driver /usr/bin
CMD ["python3", "app.py"]


# FROM python:3.8-slim-buster
# WORKDIR /python-docker
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev
# COPY . . 
# COPY geckodriver /usr/bin
# CMD ["python3", "app.py"]