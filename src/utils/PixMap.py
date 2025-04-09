import os
from PyQt6.QtGui import QPixmap
from PIL import Image, ImageFilter
import shutil

def setPixMapOf(label, imgFileName, folder) :
    if imgFileName is None:
        return 0
        # imgFileName = "icecream.png"
    if folder == "temp" :
        destFolder = "temp"
    else :
        destFolder = folder + "img"
    path = os.path.join(os.path.abspath(f"assets/{destFolder}"), imgFileName) 
    pixmap = QPixmap(path)
    label.setPixmap(pixmap)
    label.setFixedSize(50,50)
    label.setScaledContents(True)

    return path

def checkImgSize(imgFilePath) :
    filesize = os.path.getsize(imgFilePath)
    return filesize

def saveImageToLocalTemp(imgFilePath, fileName) :
    img = Image.open(imgFilePath)
    pathToSave = os.path.join(os.path.abspath("assets/temp"), fileName)
    img.save(pathToSave)
    return pathToSave

def moveImageToAssets(imgFilePath, panelName, ImgRename) :
    if panelName == "category" :
        destPath = os.path.abspath("assets/categoryimg")
        os.makedirs(destPath, exist_ok=True)
        destPath = os.path.join(destPath, ImgRename)
        shutil.move(imgFilePath, destPath)
    elif panelName == "food" :
        destPath = os.path.abspath("assets/foodimg")
        os.makedirs(destPath, exist_ok=True)
        destPath = os.path.join(destPath, ImgRename)
        shutil.move(imgFilePath, destPath)


# path = os.path.join(os.path.abspath("assets/foodimg"), "test.png")
# print(path)

# moveImageToAssets(path, "category")
