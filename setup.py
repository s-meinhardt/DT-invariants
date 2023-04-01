from setuptools import find_packages, setup  # type: ignore[import]

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="dt-invariants",
    version="0.2.0",
    description="A set of tools to compute DT invariants of quivers",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s-meinhardt/dt-invariants",
    author="Sven Meinhardt",
    author_email="sven@meinhardt.ai",
    license="GNU GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=["sympy >= 1.11.1"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.9",
)
