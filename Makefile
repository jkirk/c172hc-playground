.DEFAULT_GOAL:=help

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

virtualenv:  ## Create virtual enviroment + install requirements
	python3 -m venv venv3
	venv3/bin/pip install pip setuptools --upgrade
ifeq ($(wildcard requirements.txt),'')
	venv3/bin/pip install -r requirements.txt
	venv3/bin/pip install -r requirements.txt --upgrade
endif

upgrade:  ## Update/upgrade virtual enviroment
ifeq ($(wildcard requirements.txt),'')
	venv3/bin/pip install -r requirements.txt --upgrade
endif

codecheck: pythoncheck  ## Alias for pythoncheck

.ONESHELL:
pythoncheck: ## Run pythoncheck (flakecheck, isortcheck + blackcheck)
	@RETURN=0
	@for pythonfile in *.py; do
		flake8 --max-line-length 88 "$${pythonfile}" || RETURN=1
		isort --check "$${pythonfile}" || RETURN=1
		black --check "$${pythonfile}" || RETURN=1
	@done
	@exit $${RETURN}

.ONESHELL:
flakecheck: ## Run flake8 only
	@RETURN=0
	@for pythonfile in *.py; do
		flake8 --max-line-length 88 "$${pythonfile}" || RETURN=1
	@done
	@exit $${RETURN}

.ONESHELL:
isortcheck: ## Run isort --check only
	@RETURN=0
	@for pythonfile in *.py; do
		isort --check "$${pythonfile}" || RETURN=1
	@done
	@exit $${RETURN}

.ONESHELL:
blackcheck: ## Run black --check only
	@RETURN=0
	@for pythonfile in *.py; do
		black --check "$${pythonfile}" || RETURN=1
	@done
	@exit $${RETURN}
