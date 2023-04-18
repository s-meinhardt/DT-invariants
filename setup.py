from setuptools import find_packages, setup  # type: ignore[import]

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(package_dir={"": "app"}, packages=find_packages(where="app"))
