# coding:utf-8

import os
from typing import Optional
from typing import Sequence

from .actuator import add_command
from .actuator import commands
from .actuator import run_command
from .attribute import __author__
from .attribute import __author_email__
from .attribute import __prog_project__
from .attribute import __url_home__
from .attribute import __version__
from .parser import argp


class project:

    def __init__(self, name: str, license: str, allow_update: bool = False):
        self.__name: str = name
        self.__license: str = license
        self.__allow_update: bool = allow_update

    @property
    def name(self) -> str:
        return self.__name

    @property
    def license(self) -> str:
        return self.__license

    @property
    def allow_update(self) -> bool:
        return self.__allow_update

    def write(self, path: str, content: str) -> bool:
        if not os.path.exists(path) or self.allow_update:
            with open(path, "w", encoding="utf-8") as hdl:
                if content[-1] != "\n":
                    content += "\n"
                hdl.write(content)
        return True

    def init_pylintrc(self):
        self.write(".pylintrc", '''[MASTER]
disable=
    C0114,   # missing-module-docstring
    C0115,   # missing-class-docstring
    C0116,   # missing-function-docstring
''')

    def init_makefile(self):
        self.write("Makefile", f'''MAKEFLAGS += --always-make

all: build install test


clean-cover:
	rm -rf cover .coverage
clean-tox: clean-cover
	rm -rf .stestr .tox
clean: build-clean clean-tox


upload:
	xpip-upload --config-file .pypirc dist/*


build-clean:
	xpip-build --debug setup --clean
build: build-clean
	xpip-build --debug setup --all


install:
	pip3 install --force-reinstall --no-deps dist/*.whl
uninstall:
	pip3 uninstall -y {self.name}
reinstall: uninstall install


prepare-test:
	pip3 install --upgrade pylint flake8 pytest
pylint:
	pylint $$(git ls-files {self.name}/*.py test/*.py example/*.py)
flake8:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest:
	pytest
test: prepare-test pylint flake8 pytest
''')

    def init_readme(self):
        self.write("README.md", f'''# {self.name}

> Automatically created by {__prog_project__}.''')

    def init_requirements(self):
        self.write("requirements.txt", f'''xarg-python >= {__version__}''')

    def init_setup(self):
        # create setup.cfg
        self.write("setup.cfg", f'''[metadata]
keywords = command-line, argparse, argcomplete
long_description = file: README.md
long_description_content_type = text/markdown
license = {self.license}
license_files = LICENSE
platforms = any
classifiers =
    Programming Language :: Python
    Programming Language :: Python :: 3

[options]
zip_safe = True
include_package_data = True
python_requires = >=3.8

[options.entry_points]
console_scripts =
    {self.name} = {self.name}.command:main
''')

        # create setup.py
        self.write("setup.py", f'''# coding=utf-8

from setuptools import find_packages
from setuptools import setup

from {self.name}.attribute import __author__
from {self.name}.attribute import __author_email__
from {self.name}.attribute import __description__
from {self.name}.attribute import __project__
from {self.name}.attribute import __url_bugs__
from {self.name}.attribute import __url_code__
from {self.name}.attribute import __url_docs__
from {self.name}.attribute import __url_home__
from {self.name}.attribute import __version__


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements("requirements.txt")
    return requirements


setup(
    name=__project__,
    version=__version__,
    description=__description__,
    url=__url_home__,
    author=__author__,
    author_email=__author_email__,
    project_urls={{"Source Code": __url_code__,
                  "Bug Tracker": __url_bugs__,
                  "Documentation": __url_docs__}},
    packages=find_packages(include=["{self.name}*"], exclude=["tests"]),
    install_requires=all_requirements())
''')

    def init_project(self):
        os.makedirs(self.name, exist_ok=True)
        self.write(os.path.join(self.name, "__init__.py"),
                   '''# coding:utf-8''')
        self.write(os.path.join(self.name, "attribute.py"),
                   f'''# coding:utf-8

from urllib.parse import urljoin

__project__ = "{self.name}"
__version__ = "0.1.alpha.1"
__description__ = "Automatically created by {__prog_project__}."
__url_home__ = "{__url_home__}"
__url_code__ = __url_home__
__url_docs__ = __url_home__
__url_bugs__ = urljoin(__url_home__, "issues")

# author
__author__ = "{__author__}"
__author_email__ = "{__author_email__}"
''')
        self.write(os.path.join(self.name, "command.py"),
                   f'''# coding:utf-8

from typing import Optional
from typing import Sequence

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from .attribute import __url_home__
from .attribute import __project__
from .attribute import __version__


@add_command(__project__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description="Automatically created by {__prog_project__}.",
        epilog=f"For more, please visit {{__url_home__}}.")
''')

    def create(self) -> int:
        self.init_pylintrc()
        self.init_makefile()
        self.init_readme()
        self.init_requirements()
        self.init_setup()
        self.init_project()
        return 0


@add_command("init", help="Initialize a command-line project.")
def add_cmd_init(_arg: argp):
    _arg.add_opt_on("--update", help="allow updating existing files")
    _arg.add_argument("--license", type=str, nargs=1, metavar="LICENSE",
                      default=["MIT"], help="select license, default to MIT")
    _arg.add_pos("project_name", type=str, metavar="PROJECT")


@run_command(add_cmd_init)
def run_cmd_init(cmds: commands) -> int:
    return project(name=cmds.args.project_name,
                   license=cmds.args.license[0],
                   allow_update=cmds.args.update
                   ).create()


@add_command(__prog_project__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, add_cmd_init)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description="Create a command-line project.",
        epilog=f"For more, please visit {__url_home__}.")
