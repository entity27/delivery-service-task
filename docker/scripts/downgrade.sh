#!/usr/bin/env bash

set -e
set -x

docker compose exec api alembic downgrade -1
