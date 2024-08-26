from os import getenv

import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

requirements_list = [
    "pydantic==2.5.3",
]

LIB_NAME: str = "presentation-python"

env_version = getenv("VERSION")
if env_version is None:
    raise RuntimeError("Environment variable 'VERSION' must be declared")
VERSION = env_version.split(".")
__version__ = VERSION
__version_str__ = ".".join(map(str, VERSION))

setuptools.setup(
    name=LIB_NAME,
    version=__version_str__,
    author="Luis Gerardo Fosado Baños",
    author_email="yeralway1@gmail.com",
    description="Presentation Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/GerardoX1/{LIB_NAME}.git",
    include_package_data=True,
    keywords="presentation, library, python",
    packages=setuptools.find_packages(include=["presentation", "presentation.*"]),
    namespace_packages=["presentation"],
    package_data={"": ["*.json"]},
    install_requires=requirements_list,
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.9",
    zip_safe=True,
    test_suite="tests",
)
