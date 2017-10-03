#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

celery -A web worker --concurrency=4 --loglevel=info
