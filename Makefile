.PHONY: flake8
flake8:
	@flake8 --exclude=.git *.py tcms_django_plugin testapp tests testsite

.PHONY: pylint
pylint:
	pylint -d missing-docstring -d duplicate-code tcms_django_plugin/ tests/
	PYTHONPATH=.:./tcms/ DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) pylint --load-plugins=pylint_django -d missing-docstring -d duplicate-code testapp/ testsite/ manage.py

.PHONY: build
build:
	./tests/check-build.sh

