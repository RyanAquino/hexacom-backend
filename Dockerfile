FROM python:3.7.9-alpine
RUN apk add build-base
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD ["python", "app.py"]
