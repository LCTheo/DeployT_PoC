FROM python:buster
WORKDIR /code
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  gcc && apt-get install git

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]