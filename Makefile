MAKEFLAGS += --always-make

all: build install test


clean-cover:
	rm -rf cover .coverage
clean-tox: clean-cover
	rm -rf .stestr .tox
clean: build-clean test-clean clean-tox


upgrade-xpip.build:
	pip3 install -i https://pypi.org/simple --upgrade xpip.build
upgrade-xpip.upload:
	pip3 install -i https://pypi.org/simple --upgrade xpip.upload
upgrade-xpip: upgrade-xpip.build upgrade-xpip.upload
	pip3 install -i https://pypi.org/simple --upgrade xpip.mirror


upload:
	xpip-upload --config-file .pypirc dist/*


build-clean:
	xpip-build --debug setup --clean
build: build-clean
	xpip-build --debug setup --all


install:
	pip3 install --force-reinstall --no-deps dist/*.whl
uninstall:
	pip3 uninstall -y xarg-python
reinstall: uninstall install


prepare-test:
	pip3 install --upgrade pylint flake8 pytest
pylint:
	pylint $$(git ls-files xarg/*.py test/*.py example/*.py)
flake8:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest:
	pytest
pytest-clean:
	rm -rf .pytest_cache
test: prepare-test pylint flake8 pytest
test-clean: pytest-clean
