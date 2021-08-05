FROM python:3.9

WORKDIR /app

#ENV FLASK_APP api.py

ENV FLASK_RUN_HOST 0.0.0.0
ENV DATABASE_HOST postgres-db
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && apt-get install -y procps \
    && apt-get install net-tools

COPY req.txt req.txt

RUN pip install -r req.txt

COPY . .
#ENTRYPOINT ["gunicorn", "-b", ":8080"]
#CMD python jugadores_apirest/api.py

CMD gunicorn --chdir jugadores_apirest  api:app -w 2 --threads 2 -b 0.0.0.0:8080
