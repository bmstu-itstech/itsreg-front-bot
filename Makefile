DEFAULT_GOAL := services/api

.PHONY: services/api
services/api: services/api/bots services/api/auth

.PHONY: services/api/bots
services/api/bots:
	@poetry run python3 -m openapi_python_client generate \
		--overwrite \
		--path resources/bots.yaml \
		--output-path services/bots \
		--meta none

.PHONY: services/api/auth
services/api/auth:
	@poetry run python3 -m openapi_python_client generate \
		--overwrite \
		--path resources/auth.yaml \
		--output-path services/auth \
		--meta none

