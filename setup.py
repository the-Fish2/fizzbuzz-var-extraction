from setuptools import setup, find_packages

setup(
    name="fizzbuzz-var-extraction",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "pyright>=1.1.386",
    ],
    author="Nishka",
    description="FizzBuzz implementation with state extraction capabilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.12",
    ],
)