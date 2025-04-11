#!/bin/sh -e
set -x

ruff check src tests scripts --fix
ruff format src tests scripts
