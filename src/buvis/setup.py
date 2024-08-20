import os

from setuptools import find_packages, setup

dependencies = ["PyYAML", "rich", "tzlocal", "inflection"]

if os.name == "nt":
    dependencies.extend(["pywin32"])

setup(
    name="buvis",
    version="0.1.0",
    packages=find_packages(include=["buvis", "buvis.*"]),
    install_requires=dependencies,
)
