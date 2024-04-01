MAKEFLAGS += --always-make

all: build install


clean-cover:
	rm -rf cover .coverage

clean-tox: clean-cover
	rm -rf .stestr .tox

clean: build-clean clean-tox


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
