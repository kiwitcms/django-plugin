.PHONY: doc8
doc8:
	doc8 README.rst

.PHONY: flake8
flake8:
	@flake8 --exclude=.git *.py tcms_django_plugin testapp tests testsite

.PHONY: pylint
pylint:
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=testsite.settings pylint --load-plugins=pylint_django -d missing-docstring tcms_django_plugin/ tests/ testapp/ testsite/ manage.py

.PHONY: check-build
check-build:
	./tests/check-build.sh

.PHONY: integration_test
integration_test:
	./tests/test-run.sh
