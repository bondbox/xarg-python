MAKEFLAGS += --always-make

all: build install


upgrade-xpip.build:
	pip3 install -i https://pypi.org/simple --upgrade xpip.build

upgrade-xpip.upload:
	pip3 install -i https://pypi.org/simple --upgrade xpip.upload

upgrade-xpip: upgrade-xpip.build upgrade-xpip.upload
	pip3 install -i https://pypi.org/simple --upgrade xpip.mirror


upload:
	xpip-upload --config-file .pypirc dist/*


build:
	xpip-build setup --clean --all


install:
	pip3 install --force-reinstall --no-deps dist/*.whl


uninstall:
	pip3 uninstall -y xarg-python
