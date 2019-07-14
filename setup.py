"""AWS SSM parameter store utility."""
import os
from setuptools import setup, find_packages


def get_description(file_name="README.md"):
    """Get contents of a file as a string or empty string if none exists."""
    path = os.path.join(os.path.dirname(__file__), file_name)

    if os.path.exists(path):
        with open(path) as in_file:
            return in_file.read()

    return __doc__


install_requires = []
tests_require = install_requires + ["pytest==3.3.1"]
setup_requires = ["pytest-runner>=2.0"]


setup(
    name="dfsmpy",
    version="0.0.1",
    liscense="MIT",
    url="https://github.com/jg75/dfsmpy",
    description=__doc__,
    long_description=get_description(),
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    packages=find_packages()
)
