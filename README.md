Build Image:
```sh
docker build -t ocr-tesseract-docker .
```

Run Prod:
```sh
docker run -d -p 5000:5000 ocr-tesseract-docker
```

Run Dev:
```sh
docker run -ti -p 5000:5000 -v /$(pwd):/app ocr-tesseract-docker 
```