import os
import cv2 as cv

class ImageSearchEngine:

    def __init__(self, query : str, dir : str, limit : int)-> None:
        self.search_query = query
        self.img_dir = dir
        self.limit = limit

    def histogram(self, img_path):
        """
        Computes the 3D histogram in the RGB color space, normalizes
        the histogram to ensure similar images have similar histogram
        values.
        """
        img = cv.imread(img_path)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        hist = cv.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256]*3)
        hist = cv.normalize(hist, hist)
        return hist.flatten()

    def get_file_hist(self)->str:
        """
        Traverses the given directory and subdirectories, searching
        for images with accepted file extensions.

        Returns:    a tuple containing the path to and the 3D HLS 
        --------    histogram of the images found in the directory
                    and subdirectories.
        """
        lim = 0
        for (dir, sub_dirs, files) in os.walk(self.img_dir):
            for fname in files:
                if os.path.splitext(fname)[-1] in (".jpg", ".jpeg", ".png"):
                    if lim == self.limit: break
                    lim += 1
                    yield (self.histogram(os.path.join(dir, fname)), os.path.join(dir, fname))

    def search(self)->None:
        storage = []
        ref_img = self.histogram(self.search_query)
        for hist_value, fname in self.get_file_hist():
            score = cv.compareHist(ref_img, hist_value, cv.HISTCMP_CORREL)
            if score > 0.3: storage.append((score, fname))
        
        return sorted(storage, reverse=True)

        
