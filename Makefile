.PHONY: build plotly deploy post
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

# Deploy codebase by ammending and force pushing the freshly generated /docs folder
# Validates first if we are in "master" to generate the new version
deploy:
	if [[ "$$(git rev-parse --abbrev-ref HEAD)" != "master" ]]; then \
		echo "❌ Not master branch."; \
		exit; \
	else \
		echo "⏳ Deploying"; \
		hugo --baseUrl https://www.andreffs.com; \
		touch docs/.nojekyll; \
		git add docs/; \
		git commit --amend --no-edit; \
		git push -f origin master; \
		echo "✅ Deployed"; \
	fi; \

# Get last tagged version that was pushed to repository or if non existent, use first commit of tree
# Then get logs from $TAG until now and run then through our generate-changelog.py script
changelog:
	touch CHANGELOG.md && \
	LAST_TAG="$$(git --no-pager tag --sort=-v:refname --list | head -n1)" && \
	FIRST_COMMIT="$$(git rev-list --max-parents=0 HEAD)" && \
	TAG=$${LAST_TAG:-$$FIRST_COMMIT} && \
	LOGS=$$(git --no-pager log $$TAG..HEAD --no-merges --pretty=format:"%h %s") && \
	echo "👉 Pulling logs from \"$$TAG\" to \"$$(git --no-pager log --no-merges --pretty=format:'%h %s' -n 1)\"..." && \
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


post:
	DATE="$$(date +'%Y-%m-%d')" && \
	SLUG="$$(echo "$$title" | iconv -c -t ascii//TRANSLIT | sed -E 's/[~^]+//g' | sed -E 's/[^a-zA-Z0-9]+/-/g' | sed -E 's/^-+|-+$$//g' | tr A-Z a-z)" && \
	hugo new "blog/$$DATE-$$SLUG/index.md" && \
	open $$(pwd)/content/blog/$$DATE-$$SLUG/ -a Visual\ Studio\ Code
