#!/usr/bin/env bash

set -e

docker-compose -f docker/docker-compose.services.yml down -v
docker-compose -f docker/docker-compose.services.yml up -d

sleep 3

python src/manage.py makemigrations crypto
python src/manage.py makemigrations decision_maker

python src/manage.py migrate

python src/manage.py importpairs
#
python src/manage.py importquotes --time-unit=4h --symbol=ETHBTC
python src/manage.py importquotes --symbol=BTCUSDT --time-unit=4h

python src/manage.py computeindicators --time-unit=4h --symbol=ETHBTC
python src/manage.py computeindicators --symbol=BTCUSDT --time-unit=4h
