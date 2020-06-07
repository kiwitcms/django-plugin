.PHONY: flake8
flake8:
	@flake8 --exclude=.git *.py tcms_django_plugin testapp tests testsite

.PHONY: doc8
doc8:
	doc8 README.rst

.PHONY: pylint
pylint:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) pylint --load-plugins=pylint_django -d missing-docstring tcms_django_plugin/ tests/ testapp/ testsite/ manage.py

.PHONY: build
build:
	./tests/check-build.sh

