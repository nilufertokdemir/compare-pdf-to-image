import cv2 as cv
import numpy as np
import os
from PIL import Image
from wand.image import Image
from PyPDF2 import PdfFileReader
import PyPDF2
import shutil

def fileOpen():
    pdffiles = []

    for file in os.listdir('/home/nilufer/Downloads/problem2/pdf'):
        try:
            if file.endswith(".pdf"):
                pdffiles.append(str(file))
        except Exception as e:
            raise e
            print "No files found here!"
    return pdffiles

def pdfFinder(filename, f ) :
    fname = f
    f = f.split(".",1)
    foldername = f[0]
    if not os.path.exists('/home/nilufer/Desktop/%s' % foldername):
        os.makedirs('/home/nilufer/Desktop/%s' % foldername)
    path = '/home/nilufer/Desktop/{}/{}.pdf' .format(foldername,fname)
    shutil.copy2('/home/nilufer/Downloads/problem2/pdf/%s' % filename,path)

def PageNumber(nameofpdf) :
    pdfs = []
    pdfs = fileOpen()
    pdf = pdfFinder(nameofpdf)
    pdf = PdfFileReader(open('/home/nilufer/Downloads/problem2/pdf/%s.pdf' % nameofpdf, 'rb'))
    pages = pdf.getNumPages()

    return pages

def GetFirstP (filename ) :
    pdfWriter = PyPDF2.PdfFileWriter()

    pdfFileObj = open('/home/nilufer/Downloads/problem2/pdf/%s' % filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    pdfWriter.addPage(pageObj)


    with open("/home/nilufer/Desktop/firstPages/%s" % filename, "wb") as output:
        pdfWriter.write(output)

    with Image(filename='/home/nilufer/Desktop/firstPages/%s' % filename, resolution=150) as image:
        image.alpha_channel = False
        image.save(filename='/home/nilufer/Desktop/FirstPagesPng/%s.png' % filename)

def fileMatch(filename) :

    pdf = []
    pdf = fileOpen()
    output_filename = '{}.png'.format(filename)
    img_rgb = cv.imread('/home/nilufer/Desktop/FirstPagesPng/%s' % output_filename)

    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    path = '/home/nilufer/Desktop/templates'
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        path2 = os.path.join(path, f)
        template = cv.imread(path2, 0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            pdfFinder(filename,f)

def run():
    pdffile = []
    pdffile = fileOpen()
    pdfpath = '/home/nilufer/Downloads/problem2/pdf'
    for f in os.listdir(pdfpath):
        GetFirstP(f)
    firstPages = []
    path = '/home/nilufer/Desktop/firstPages'
    for f in os.listdir(path):
      firstPages.append(f)
    for i in range(len(firstPages)) :
        fileMatch(firstPages[i])
run()
