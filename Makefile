.PHONY: build plotly post
SHELL := /bin/bash

build:
	docker build -t myplotly -f plotly.Dockerfile . && \
	echo "✅ `myplotly` image created!"

plotly: build
	docker stop myplotly && \
	docker run -d -v $$(pwd):/work -p 8888:8888 --rm --name myplotly myplotly && \
	sleep 2 && \
	URL=$$(docker logs myplotly 2>&1 | grep "http://127.0.0.1:8888/lab?token=" | egrep -o 'https?://[^ ]+') && \
	open $$URL && \
	docker logs -t myplotly

post:
	DATE="$$(date +'%Y-%m-%d')" && \
	SLUG="$$(echo "$$title" | iconv -c -t ascii//TRANSLIT | sed -E 's/[~^]+//g' | sed -E 's/[^a-zA-Z0-9]+/-/g' | sed -E 's/^-+|-+$$//g' | tr A-Z a-z)" && \
	hugo new "blog/$$DATE-$$SLUG/index.md" && \
	open $$(pwd)/content/blog/$$DATE-$$SLUG/ -a Visual\ Studio\ Code
