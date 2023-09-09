# Makefile for Docker Compose commands

# Define Docker Compose executable
DOCKER_COMPOSE = docker-compose

# Stop and remove containers
down:
	$(DOCKER_COMPOSE) down

# Build containers
build:
	$(DOCKER_COMPOSE) build

# Start specific services (e.g., db and users)
up:
	$(DOCKER_COMPOSE) up 

# Target to run all commands (down, build, and up)
all: down build up

.PHONY: down build up all