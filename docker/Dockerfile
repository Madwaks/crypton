FROM python:3.9.5-buster


RUN apt-get update && apt-get install -y gettext build-essential git wget
RUN wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add - \
 && echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" >> /etc/apt/sources.list.d/pgdg.list \
 && apt-get update && apt-get install -y postgresql-client-11

RUN mkdir -p /app/requirements

WORKDIR /app

COPY requirements/ /app/requirements/.

RUN pip install --no-cache-dir -U pip setuptools \
 && pip install --no-cache-dir -r requirements/base.txt

COPY src/. /app/.
COPY scripts/run_crypton.sh /app/.


RUN chmod +x /app/run_crypton.sh

EXPOSE 80

ENTRYPOINT ["bash", "/app/run_crypton.sh"]
CMD ["runserver"]
