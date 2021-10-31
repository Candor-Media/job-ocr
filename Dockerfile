# https://github.com/ricktorzynski/ocr-tesseract-docker
FROM ubuntu:latest
RUN apt-get update -y
RUN apt install -y software-properties-common

# Install python & pip
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python python-dev python3.6 python3.6-dev virtualenv libssl-dev libpq-dev git build-essential libfontconfig1 libfontconfig1-dev
RUN apt update && apt install -y python3-pip libsm6 libxext6 ffmpeg libgl1

# Install pipenv and compilation dependencies | https://sourcery.ai/blog/python-docker/
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install tesserect
RUN apt-get -y install tesseract-ocr

# Workdirp
COPY . /app
WORKDIR /app

# Install python dependencies
RUN pipenv install --skip-lock

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

RUN apt-get install wget
RUN wget -O /usr/share/tesseract-ocr/4.00/tessdata/hin.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/hin.traineddata

ENTRYPOINT ["pipenv", "run", "python"]
CMD ["src/main.py"]
