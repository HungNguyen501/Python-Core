FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get clean

COPY src/pool_api/ /app/src/pool_api/

RUN  pip install -r /app/src/pool_api/requirements.txt \
    && rm -rf /root/.cache/pip \
    && mkdir -p /app/src/common/calculate_quantile/

ADD src/common/calculate_quantile/calculate_quantile.py /app/src/common/calculate_quantile/
