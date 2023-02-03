FROM python:3.10.9-slim

WORKDIR /ai-app
COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["gunicorn"]
CMD ["--workers=4", "--bind=0.0.0.0:8080", "main:app"]