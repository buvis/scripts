import os
from setuptools import find_packages, setup

dependencies=["pyyam", "rich"]

if os.name == "nt":
    dependencies.extend(["pywin32"])

setup(
    name="buvis",
    version="0.1.0",
    packages=find_packages(include=["buvis", "buvis.*"]),
    install_requires=dependencies,
)
