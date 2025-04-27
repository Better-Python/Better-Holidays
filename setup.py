from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A better way to get market holidays"

def read(path):
    with open(path, "r") as f:
        return f.read()

setup(
    name="Better-Holidays",
    version=VERSION,
    author="R5dan",
    description=DESCRIPTION,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude="tests"),
    install_requires=[
        "better-md>=0.3.4"
    ],
    extras_require={},
    keywords=["python", "better holidays", "better", "market", "stocks", "finance", "holidays", "better python"],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    url="https://github.com/Better/better-holidays"
)
