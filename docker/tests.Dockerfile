FROM python:3.11.12-alpine

WORKDIR /app

COPY [ \
    "./requirements/requirements.tests.txt", \
    "./alembic.ini", \
    "./pyproject.toml", \
    "./" \
]

RUN pip install --no-cache-dir -r requirements.tests.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["pytest"]
