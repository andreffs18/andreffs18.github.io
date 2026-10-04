.PHONY: help build plotly post project
SHELL := /bin/bash

.DEFAULT_GOAL := help

help: ## Show this help
	@echo "Usage: make <target> [title=\"...\"]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

build: ## Build the myplotly Docker image
	docker build -t myplotly -f plotly.Dockerfile . && \
	echo "✅ `myplotly` image created!"

plotly: build ## Run the myplotly Jupyter container and open it in the browser
	docker stop myplotly && \
	docker run -d -v $$(pwd):/work -p 8888:8888 --rm --name myplotly myplotly && \
	sleep 2 && \
	URL=$$(docker logs myplotly 2>&1 | grep "http://127.0.0.1:8888/lab?token=" | egrep -o 'https?://[^ ]+') && \
	open $$URL && \
	docker logs -t myplotly

post: ## Create a new blog post: make post title="My Post Title"
	DATE="$$(date +'%Y-%m-%d')" && \
	SLUG="$$(echo "$$title" | iconv -c -t ascii//TRANSLIT | sed -E 's/[~^]+//g' | sed -E 's/[^a-zA-Z0-9]+/-/g' | sed -E 's/^-+|-+$$//g' | tr A-Z a-z)" && \
	hugo new --king blog "blog/$$DATE-$$SLUG/index.md" && \
	open $$(pwd)/content/blog/$$DATE-$$SLUG/ -a Visual\ Studio\ Code

project: ## Create a new project: make project title="My Project Name" [year=YYYY]
	YEAR="$${year:-$$(date +'%Y')}" && \
	SLUG="$$(echo "$$title" | iconv -c -t ascii//TRANSLIT | sed -E 's/[~^]+//g' | sed -E 's/[^a-zA-Z0-9]+/-/g' | sed -E 's/^-+|-+$$//g' | tr A-Z a-z)" && \
	hugo new --kind projects "projects/$$YEAR-$$SLUG.md" && \
	open $$(pwd)/content/projects/$$YEAR-$$SLUG.md -a Visual\ Studio\ Code
