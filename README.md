# #img-search

### A simple image search engine.

This program searches for similar images on a computer using histogram comparison (color distribution), given the path to a reference image and a path to the directory to be searched. The user can specify the search limits.

**NOTE: This utility program does not find similar images based on the objects contained in the image, instead, it uses the color distribution to find similar images. This is to be executed on the terminal, although some of its functionalities can be imported.**

### Installation

To get this package functioning, execute the following commands:

```shell
git clone https://github.com/yodeman/img-search.git
cd img-search

pip install -r requirements.txt
pip install --upgrade setuptools
python setup.py install
```






### Quick Start

The package is easy to use. Below is an example of how to search for similar image:

```shell
img-search --ref-img path/to/reference/image --dir path/to/directory
```



https://user-images.githubusercontent.com/59335237/152560324-a4ac70f8-c948-41dd-8f32-4ed9d6585223.mp4
