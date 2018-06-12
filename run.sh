#!/usr/bin/env bash

## Ajuste o caminho do arquivo variaveis conforme local
## de clone do repositorio.

set -e
set -u

docker run -it --rm \
	--env-file variaveis.txt \
    secops-pfsense python /app/start.py
