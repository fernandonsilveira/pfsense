.PHONY: build run

DOCKER_IMAGE = secops-pfsense
WORK_DIR     = /app
CURRENT_PATH = $(shell pwd)

build:
		docker build -t $(DOCKER_IMAGE) .

run: build
		docker run --rm --env-file variaveis.txt --name $(DOCKER_IMAGE) -v $(CURRENT_PATH)/app:$(WORK_DIR) $(DOCKER_IMAGE) python $(WORK_DIR)/start.py
