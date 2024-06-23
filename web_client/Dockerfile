FROM ubuntu:20.04
COPY requirements.txt requirements.txt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip wget firefox
RUN apt-get install libcurl3-gnutls libcurl3-nss libcurl4 libcurl4 libdrm2 libbgm1 libnspr4 libnss3 libu2f-udev libvulkan1 xdg-utils
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN pip3 install -r requirements.txt
ENV DISPLAY=:0
COPY . . 
COPY geckodriver /usr/bin
COPY chromedriver /usr/bin
CMD ["python3", "app.py"]


# FROM python:3.8-slim-buster
# WORKDIR /python-docker
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev
# COPY . . 
# COPY geckodriver /usr/bin
# CMD ["python3", "app.py"]