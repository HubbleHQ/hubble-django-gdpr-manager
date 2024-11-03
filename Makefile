.PHONY: dev-build
dev-build: ## Create the docker image for you dev environment
	docker compose build

.PHONY: dev-run
dev-run: ## Run a local instance of pass
	docker compose up --build --remove-orphans

.PHONY: dev-stop ## Shutdown the running container and remove any intermediate images. Useful for when you think the container is stopped but docker doesn’t
dev-stop:
	docker compose down --remove-orphans

.PHONY: dev-clean
dev-clean: ## Remove all the docker containers for this project
	docker compose down --rmi local --volumes

.PHONY: dev-ssh
dev-ssh: ## Open a shell on the current running docker image of pass
	docker compose exec dev zsh

.PHONY: dev-test
dev-test: ## Run the tests. If this fails with a message saying unable to connect … try make dev-stop then rerun this target.
	docker compose exec dev python tests_run.py

.PHONY: dev-test-makemigrations
dev-test-makemigrations: ## Makes migrations for the tests, without the migrations the tests won't create the tables and will error.
	docker compose exec dev python tests_makemigrations.py

.PHONY: build
build: # Build the dist package
	docker compose exec dev python -m build

.PHONY: test-deploy
test-deploy: # Deploy dist package to testpypi
	docker compose exec dev python -m twine upload --repository testpypi dist/*

.PHONY: help
help: ## This message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help