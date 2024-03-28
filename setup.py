# coding=utf-8

from setuptools import find_packages
from setuptools import setup

from xarg.util import __author__
from xarg.util import __author_email__
from xarg.util import __description__
from xarg.util import __project__
from xarg.util import __url_bugs__
from xarg.util import __url_code__
from xarg.util import __url_docs__
from xarg.util import __url_home__
from xarg.util import __version__

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    url=__url_home__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __url_code__,
                  "Bug Tracker": __url_bugs__,
                  "Documentation": __url_docs__},
    packages=find_packages(include=["xarg*"], exclude=["tests"]))
