FROM python:3.11.12-alpine

WORKDIR /app

COPY [ \
    "./requirements/requirements.txt", \
    "./alembic.ini", \
    "./" \
]

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["uvicorn"]
CMD [ \
    "src.main:app", \
    "--host", \
    "0.0.0.0", \
    "--port", \
    "8000", \
    "--reload" \
]
