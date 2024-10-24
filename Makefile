ROOT_DIR = $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))/

.PHONY: Generate models
init:
	@echo "Generating models..."
	mkdir -p ${ROOT_DIR}src/migration/versions/
	cd ${ROOT_DIR}src && alembic revision --autogenerate -m "init"
	@echo "Done generating models."

.PHONY: Deploy api
api:
	$Q flyctl deploy -c ci/fly.toml

.PHONY: Deploy ui
ui:
	$Q cd ui/news-ui && pnpm dlx @cloudflare/next-on-pages
	$Q cd ui/news-ui && pnpm wrangler pages deploy .vercel/output/static --branch master --commit-dirty=true