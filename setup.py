import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="denbi.nova.filter",
    version="0.0.1",
    author="de.NBI Cloud admins",
    author_email="cloud@denbi.de",
    description="Collection of additional nova filters developed for the de.NBI cloud"
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deNBI/nova-filter-collection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
