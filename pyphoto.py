import os, math
from tkinter import *
from tkinter.filedialog import SaveAs, Directory
from tkinter.messagebox import showinfo
from PIL import Image
from PIL.ImageTk import PhotoImage

APP_NAME = 'Image Search'

class scrolledCanvas(Canvas):
    """
    a canvas in a container that automatically makes vertical
    and horizontal scroll bars for itself
    """
    def __init__(self, container):
        super().__init__(container)
        self.config(borderwidth=0)
        vbar = Scrollbar(container)
        hbar = Scrollbar(container, orient='horizontal')
        vbar.pack(side=RIGHT, fill=Y)
        hbar.pack(side=BOTTOM, fill=X)
        self.pack(side=TOP, fill=BOTH, expand=YES)
        vbar.config(command=self.yview)
        hbar.config(command=self.xview)
        self.config(yscrollcommand=vbar.set)
        self.config(xscrollcommand=hbar.set)

class viewOne(Toplevel):
    """
    Open a single image in a pop-up window when created;
    scroll if image is too big for display;
    resizes window's height or width on mouse click;
    stretches or shrinks; zooms in/out
    """
    def __init__(self, imgpath, forcesize=()):
        super().__init__()
        helptext = """
            Click the thumbnail to have a better view.

            Press i to zoom in, and o to zoom out.

            The title bar shows the path to the image.
        """
        Button(self, text='Help', command=(lambda:showinfo(APP_NAME, helptext))).pack()
        self.title(imgpath+' - '+APP_NAME)
        imgpil = Image.open(imgpath)
        self.canvas = scrolledCanvas(self)
        self.canvas.focus_set()
        self.drawImage(imgpil, forcesize)
        self.canvas.bind('<Button-1>', self.onSizeToDisplayHeight)
        self.canvas.bind('<Button-3>', self.onSizeToDisplayWidth)
        self.canvas.bind('<KeyPress-i>', self.onZoomIn)
        self.canvas.bind('<KeyPress-o>',  self.onZoomOut)

    def drawImage(self, imgpil, forcesize=()):
        imgtk = PhotoImage(image=imgpil)
        scrwide, scrhigh = forcesize or self.maxsize()
        imgwide = imgtk.width()
        imghigh = imgtk.height()

        fullsize = (0, 0, imgwide, imghigh)
        viewwide = min(imgwide, scrwide)
        viewhigh = min(imghigh, scrhigh)

        canvas = self.canvas
        canvas.delete('all')
        canvas.config(height=viewhigh, width=viewwide)
        canvas.config(scrollregion=fullsize)
        canvas.create_image(0, 0, image=imgtk, anchor=NW)

        if imgwide <= scrwide and imghigh <= scrhigh:
            self.state('normal')
        elif sys.platform[:3] == 'win':
            self.state('zoomed')
        self.saveimage = imgpil
        self.savephoto = imgtk
        self.update()

    def sizeToDisplaySide(self, scaler):
        # resize to fill one side of the display
        imgpil = self.saveimage
        scrwide, scrhigh = self.maxsize()
        imgwide, imghigh = imgpil.size
        newwide, newhigh = scaler(scrwide, scrhigh, imgwide, imghigh)
        if (newwide * newhigh < imgwide * imghigh):
            filter = Image.ANTIALIAS
        else:
            filter = Image.BICUBIC
        imgnew = imgpil.resize((newwide, newhigh), filter)
        self.drawImage(imgnew)

    def onSizeToDisplayHeight(self, event):
        def scaleHigh(scrwide, scrhigh, imgwide, imghigh):
            newhigh = scrhigh
            newwide = int(scrhigh * (imgwide/imghigh))
            return (newwide, newhigh)
        self.sizeToDisplaySide(scaleHigh)

    def onSizeToDisplayWidth(self, event):
        def scaleWide(scrwide, scrhigh, imgwide, imghigh):
            newwide = scrwide
            newhigh = int(scrwide * (imghigh/imgwide))
            return (newwide, newhigh)
        self.sizeToDisplaySide(scaleWide)

    def zoom(self, factor):
        # zoom in or out in increments
        imgpil = self.saveimage
        wide, high = imgpil.size
        if factor < 1.0:
            filter = Image.ANTIALIAS
        else:
            filter = Image.BICUBIC
        new = imgpil.resize((int(wide * factor), int(high * factor)), filter)
        self.drawImage(new)

    def onZoomIn(self, event, incr=0.10):
        self.zoom(1.0 + incr)

    def onZoomOut(self, event, decr=0.10):
        self.zoom(1.0-decr)


def makeThumbs(imgdirs, size=(100, 100), subdir='thumbs'):
    """
    Generate thumbnails for images in imgdirs. The thumbnails are saved in the
    current working directory and cleaned up when the main window is closed.
    """
    thumbdir = os.path.join(os.getcwd(), subdir)
    if not os.path.exists(thumbdir):
        os.mkdir(thumbdir)

    thumbs = []
    for score,imgpath in imgdirs:
        thumbpath = os.path.join(thumbdir, os.path.basename(imgpath))
        if os.path.exists(thumbpath):
            thumbobj = Image.open(thumbpath)
            thumbs.append((imgpath, thumbobj))
        else:
            try:
                imgobj = Image.open(imgpath)
                imgobj.thumbnail(size, Image.ANTIALIAS)
                imgobj.save(thumbpath)
                thumbs.append((imgpath, imgobj))
            except:
                print('Skipping: ', imgpath)
    return thumbs

def viewThumbs(imgdirs, kind=Toplevel, numcols=None, height=400, width=500):
    """
    The main window for viewing the thumbnails. This fumction is also responsible
    for calling the callback hamdler when the thumbnails are clicked.
    """
    win = kind()
    win.title(APP_NAME)
    helptxt = "Click on the thumbnail to have a better view."
    Button(win, text='Help', command=(lambda:showinfo(APP_NAME, helptxt))).pack()
    Button(win, text='Quit', command=win.quit).pack(side=BOTTOM, expand=YES)
    canvas = scrolledCanvas(win)
    canvas.config(height=height, width=width)
    thumbs = makeThumbs(imgdirs)
    numthumbs = len(thumbs)
    if not numcols:
        numcols = int(math.ceil(math.sqrt(numthumbs)))
    numrows= int(math.ceil(numthumbs/numcols))
    linksize = max(max(thumb[1].size) for thumb in thumbs)
    fullsize = (0, 0,
                (linksize * numcols), (linksize * numrows))
    canvas.config(scrollregion=fullsize)

    rowpos = 0
    savephotos = []
    while thumbs:
        thumbsrow, thumbs = thumbs[:numcols], thumbs[numcols:]
        colpos = 0
        for (imgpath, imgobj) in thumbsrow:
            photo = PhotoImage(imgobj)
            link = Button(canvas, image=photo)
            def handler(savefile=imgpath):
                viewOne(savefile)
            link.configure(command=handler, width=linksize, height=linksize)
            link.pack(side=LEFT, expand=YES)
            canvas.create_window(colpos, rowpos, anchor=NW, window=link, width=linksize, height=linksize)
            colpos += linksize
            savephotos.append(photo)
        rowpos += linksize
    win.savephotos = savephotos
    return win
