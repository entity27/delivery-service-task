#!/usr/bin/env bash

set -e
set -x

poetry export --without-hashes --with test --format=requirements.txt > requirements/requirements.tests.txt
