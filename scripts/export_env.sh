#!/usr/bin/env bash

# Экспортирует переменные из .env файла
# Необходимо запускать через "source ./scripts/export_env.sh"
export $(grep -v ^# envs/delivery.env | xargs)
