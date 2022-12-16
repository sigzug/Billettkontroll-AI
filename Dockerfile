FROM python:3.8.15-slim 

ENV APP_HOME /app
WORKDIR ${APP_HOME}

COPY . ./

RUN pip install pip pipenv --upgrade
# RUN pip install -r requirements.txt
RUN pipenv install --skip-lock --system --dev

CMD ["./scripts/entrypoint.sh"]
