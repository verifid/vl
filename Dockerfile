FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY uwsgi.ini /usr/src/app/
COPY nginx.conf /usr/src/app/
COPY requirements.txt /usr/src/app/
COPY start.sh /usr/src/app/

RUN apt-get -y update
RUN apt-get install -y software-properties-common
RUN apt-get install -y --fix-missing \
    nginx \
    redis-server \
    build-essential \
    cmake \
    libtesseract-dev \
    libleptonica-dev \
    tesseract-ocr \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS
RUN pip3 install -r requirements.txt --upgrade

COPY . /usr/src/app

EXPOSE 5000

COPY nginx.conf /etc/nginx

RUN chmod +x ./start.sh

CMD ["./start.sh"]
