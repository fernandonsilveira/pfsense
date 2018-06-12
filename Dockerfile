FROM alpine:latest

RUN apk add --update && \
    apk add --no-cache python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -r /root/.cache

RUN mkdir -p /app
WORKDIR /app
COPY app/ /app

RUN pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT python start.py
