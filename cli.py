import os, argparse
from searchEngine import ImageSearchEngine
from pyphoto import viewThumbs, APP_NAME
from tkinter import Tk, Button

def arg_parser():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
                description="""
                Given a refrence image '--ref-img', the program searches the given
                directory '--dir' for similar images in terms of the differences 
                in the pixels of the image (i.e. the color distribution of the image.)\n
                NOTE: The program does not search based on the objects in the images.
                The supported images include jpg, jpeg, png files.
                """,
                prog="img-search"
            )
    parser.add_argument(
                "--ref-img", dest="ref_img", type=str, default=None,
                help="""
                The path to the reference image with which other images are to be
                compared.\n
                E.g. C:/users/user/downloads/sample.jpg
                """
            )
    parser.add_argument(
                "--dir", dest="dir", type=str, default=None,
                help="""
                This is the path to the directory that contains images to be comapared
                to the reference image.\n
                E.g. C:/users/user/pictures/
                """
            )
    parser.add_argument(
                "--limit", dest="limit", type=int, default=1000,
                help="""
                The number of image files to consider while searching.
                """
            )
    return parser.parse_args()

def cleanup(path : str):
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))

def main():
    args = arg_parser()
    if (not args.ref_img or not args.dir):
        print("Both --ref-img and --dir arguments are required!!!\n\ntype img-search --help")
        exit()
    engine = ImageSearchEngine(args.ref_img, args.dir, args.limit)
    print("Searching...")
    imgpaths = engine.search()
    print(f"Done searching... found {len(imgpaths)} similar images.\nLoading {len(imgpaths)} images...")
    if (len(imgpaths) == 0):
        print("exiting...")
        exit()
    try:
        mainwin = viewThumbs(imgpaths, kind=Tk)
        mainwin.mainloop()
        print("cleaning up...")
        if os.path.exists(os.path.join(os.getcwd(), "thumbs")):
            cleanup(os.path.join(os.getcwd(), "thumbs"))
            os.rmdir(os.path.join(os.getcwd(), "thumbs"))
    except Exception:
        print("cleaning up and exiting...")
        if os.path.exists(os.path.join(os.getcwd(), "thumbs")):
            cleanup(os.path.join(os.getcwd(), "thumbs"))
            os.rmdir(os.path.join(os.getcwd(), "thumbs"))


