#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

printf "\n## Performing Migrations\n\n"
python3 /app/manage.py makemigrations
python3 manage.py migrate

printf "\n## Building css"
sass /app/lib/scss/maindefault.scss:/app/lib/assets/css/maindefault.css

printf "\n## Starting Server\n\n"

python3 manage.py runserver_plus 0.0.0.0:8000
