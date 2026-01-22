from setuptools import setup, find_packages

setup(
    name="wikiscraper",
    version="0.1.0",
    description="WikiScraper project",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    python_requires=">=3.10",
)
