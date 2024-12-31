from setuptools import setup, find_packages

setup(
    name="gomoku",
    version="1.0.0",
    description="A simple text-based Gomoku game.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/martinreinhardt01/gomoku",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

