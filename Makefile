.PHONY: build plotly
SHELL := /bin/bash

build:
	docker build -t myplotly -f plotly.Dockerfile . && \
	echo "✅ `myplotly` image created!"

plotly:
	docker stop myplotly && \
	docker run -d -v $$(pwd):/work -p 8888:8888 --rm --name myplotly myplotly && \
	sleep 2 && \
	URL=$$(docker logs myplotly 2>&1 | head -n10 | grep "http://127.0.0.1:8888/?token=" | egrep -o 'https?://[^ ]+') && \
	open $$URL && \
	docker logs -t myplotly


# Get last tagged version that was pushed to repository or if non existent, use first commit of tree
# Then get logs from $TAG until now and run then through our generate-changelog.py script
changelog:
	touch CHANGELOG.md && \
	LAST_TAG="$$(git --no-pager tag --sort=-v:refname --list | head -n1)" && \
	FIRST_COMMIT="$$(git rev-list --max-parents=0 HEAD)" && \
	TAG=$${LAST_TAG:-$$FIRST_COMMIT} && \
	LOGS=$$(git --no-pager log $$TAG..HEAD --pretty=format:"%h %B") && \
	echo "👉 Pulling logs from \"$$TAG\" to \"$$(git --no-pager log --pretty=format:'%h' -n 1)\"..." && \
	printf "$$LOGS" | python3 .gitlab/scripts/generate-changelog.py && \
	rm CHANGELOG.md

# Bump project version to give $VERSION argument. With new version, create new tag and start deployment process
# by tagging and pushing this commit with new label.
check-tag:
ifndef VERSION
	$(error VERSION is undefined)
endif

tag: check-tag
	TAG_MESSAGE="$$VERSION - $$(date '+%Y-%m-%d')" && \
	git tag -a "$$VERSION" -m "$$TAG_MESSAGE" && \
	git push origin --tags && \
	echo "✅ Updated project to version \"$$VERSION\""
