.PHONY: help


## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo "${YELLOW} make ${RESET} ${GREEN}<target> [options]${RESET}"
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
    	message = match(lastLine, /^## (.*)/); \
		if (message) { \
			command = substr($$1, 0, index($$1, ":")-1); \
			message = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW_S}%-$(TARGET_MAX_CHAR_NUM)s${RESET} %s\n", command, message; \
		} \
	} \
    { lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''


## Add a production package to the application. e.g make add-package-prod package=package_name
add-package-prod:
	pip install $(package) ; pip freeze | grep $(package) >> prod.requirements.txt
## Add a development package to the application. e.g make add-package-dev package=package_name
add-package-dev:
	pip install $(package) ; pip freeze | grep $(package) >> dev.requirements.txt


ifeq (test,$(firstword $(MAKECMDGOALS)))
  TAG_ARGS := $(word 2, $(MAKECMDGOALS))
  $(eval $(TAG_ARGS):;@:)
endif

# COLORS
GREEN  := `tput setaf 2`
YELLOW := `tput setaf 3`
WHITE  := `tput setaf 7`
YELLOW_S := $(shell tput -Txterm setaf 3)
NC := "\e[0m"
RESET  := $(shell tput -Txterm sgr0)

INFO := @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE
SUCCESS := @bash -c 'printf $(GREEN); echo "===> $$1"; printf $(NC)' SOME_VALUE