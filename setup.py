from setuptools import setup

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(
    name="img-search",
    version="0.0.1",
    author="pauli__h",
    author_email="oyelabipaul@gmail.com",
    url="https://github.com/yodeman/img-search",
    description="Searches for similar images and displays result in the terminal/gui",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "OperatingSystem::OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    py_modules=["__init__", "cli", "searchEngine", "pyphoto"],
    python_requires=">=3.7",
    install_requires=["pillow", "opencv-python"],
    entry_points={
        "console_scripts": ["img-search=cli:main"],
    },
)
