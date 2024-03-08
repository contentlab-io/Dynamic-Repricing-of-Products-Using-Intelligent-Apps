FROM python:3.11-slim

WORKDIR /usr/src/app

RUN pip install --no-cache-dir Flask

COPY . .

CMD ["flask", "run"]