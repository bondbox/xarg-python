xarg
====

Simple command-line tool based on argparse.

build
-----

fast build via [xpip](https://github.com/bondbox/xpip-python):

```shell
xpip-build setup --all && ls -lh dist/*
```

or build via Shell:

```shell
rm -rf "build" "dist" "*.egg-info"
python setup.py check sdist bdist_wheel --universal
```

xargcomplete
------------

Xarg is based on [argcomplete](https://kislyuk.github.io/argcomplete/) and provides easy command line tab completion of arguments for your Python application.

Requires:

- bash or zsh
- package requires xarg and install via pip

Enable completion:

```shell
xargcomplete init
```

Updated completion for all xarg-based python packages:

```shell
xargcomplete update
```
