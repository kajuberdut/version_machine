import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

version_path = HERE / "version_machine" / "__version__.py"
with open(version_path, "r") as fh:
    version_dict = {}
    exec(fh.read(), version_dict)
    VERSION = version_dict["__version__"]

setup(
    name="version_machine",
    version=VERSION,
    author="Patrick Shechet",
    author_email="patrick.shechet@gmail.com",
    description=(""),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kajuberdut/version_machine",
    license=None,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "version_machine=version_machine.core:cli",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
