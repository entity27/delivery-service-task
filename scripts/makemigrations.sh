#!/usr/bin/env bash

set -e
set -x

if [ "$#" -ne 1 ]; then
    echo "Необходимо передать название: $0 <название>"
    exit 1
fi

alembic revision --autogenerate -m "$1"
