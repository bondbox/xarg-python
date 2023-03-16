xarg
====

Simple command-line tool based on argparse.

build
-----

fast build via [xpip](https://github.com/bondbox/xpip-python):

```shell
xpip-build setup --all && ls -lh dist/*
```

or build in linux:

```shell
rm -rf "build" "dist" "*.egg-info"
python setup.py check sdist bdist_wheel --universal
```
