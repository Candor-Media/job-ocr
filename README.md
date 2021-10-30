```sh
docker build -t ocr-tesseract-docker .
docker run -d -p 5000:5000 ocr-tesseract-docker
```