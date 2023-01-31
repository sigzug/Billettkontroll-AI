FROM python:3.10.9

WORKDIR /ai-app
COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]