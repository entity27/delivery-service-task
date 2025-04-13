FROM python:3.11.12-alpine

WORKDIR /app

COPY [ \
    "./requirements/requirements.txt", \
    "./alembic.ini", \
    "./" \
]

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["celery"]
CMD [ \
    "-A", \
    "src.backgrounds", \
    "worker", \
    "-B", \
    "-l", \
    "INFO", \
    "--queues", \
    "register_package" \
]
