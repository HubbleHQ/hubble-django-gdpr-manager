.PHONY: dev-build
dev-build: ## Create the docker image for you dev environment
	docker compose --profile dev build

.PHONY: dev-run
dev-run: ## Run a local instance of pass
	docker compose --profile dev up  --build --remove-orphans

.PHONY: dev-stop ## Shutdown the running container and remove any intermediate images. Useful for when you think the container is stopped but docker doesn’t
dev-stop:
	docker compose --profile dev down --remove-orphans
	docker compose --profile release down --remove-orphans

.PHONY: dev-clean
dev-clean: ## Remove all the docker containers for this project
	docker compose --profile dev down --rmi local --volumes
	docker compose --profile release down --rmi local --volumes

.PHONY: dev-shell
dev-shell: ## Open a shell on the current running docker image of pass
	docker compose --profile dev run --rm --remove-orphans dev zsh

.PHONY: dev-test
dev-test: ## Run the tests. If this fails with a message saying unable to connect … try make dev-stop then rerun this target.
	docker compose --profile dev run dev python tests_run.py

.PHONY: dev-test-makemigrations
dev-test-makemigrations: ## Makes migrations for the tests, without the migrations the tests won't create the tables and will error.
	docker compose --profile dev run  dev python tests_makemigrations.py
.PHONY: build
build: # Build the dist package
	docker compose --profile release run --rm release python -m build
.PHONY: deploy
deploy: # Deploy dist package to testpypi
	make build
	docker compose --profile release run release python -m twine upload --verbose

.PHONY: test-deploy
test-deploy: # Deploy dist package to testpypi
	make build
	docker compose --profile release run release python -m twine upload --verbose --repository testpypi dist/*

.PHONY: help
help: ## This message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
