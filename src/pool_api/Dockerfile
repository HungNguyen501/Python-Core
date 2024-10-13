FROM python:3.11-slim

WORKDIR /app

COPY src/pool_api/ /app/src/pool_api/

RUN  apt-get update \
    && apt-get install gcc -y \
    && apt-get clean \
    && pip install -r /app/src/pool_api/requirements.txt \
    && rm -rf /root/.cache/pip \
    && mkdir -p /app/src/common/calculate_quantile/

ADD src/common/calculate_quantile/calculate_quantile.py /app/src/common/calculate_quantile/
