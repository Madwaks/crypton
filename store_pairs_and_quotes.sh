#!/usr/bin/env bash

set -e

docker-compose -f docker/docker-compose.services.yml down -v && docker-compose -f docker/docker-compose.services.yml up -d

sleep 5

python src/manage.py makemigrations crypto
python src/manage.py makemigrations decision_maker

python src/manage.py migrate

python src/manage.py importpairs
#
python src/manage.py importquotes --time-unit=4h --symbol=ETHBTC

python src/manage.py computeindicators --time-unit=4h --symbol=ETHBTC
