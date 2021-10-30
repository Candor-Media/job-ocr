# https://github.com/ricktorzynski/ocr-tesseract-docker
FROM ubuntu:latest
RUN apt-get update -y

# Install python & pip
RUN apt-get install -y python-pip python-dev build-essential
RUN apt update && apt install -y libsm6 libxext6

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

ENTRYPOINT ["python"]
CMD ["main.py"]
