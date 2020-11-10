FROM python:3.7

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /home/ePortalService

ADD . /app

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
# Install system dependencies with OpenCV
RUN apt-get update && apt-get install -y \
        tzdata \
        libopencv-dev \ 
        build-essential \
        libssl-dev \
        libpq-dev \
        libcurl4-gnutls-dev \
        libexpat1-dev \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        gunicorn \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt 
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pip3 install opencv-contrib-python

#selenium
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb

#chromedriver
RUN curl https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip -o /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

# RUN pipenv install --skip-lock --system --dev

CMD gunicorn main:app 