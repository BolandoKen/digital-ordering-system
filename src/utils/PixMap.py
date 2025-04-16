import os
from PyQt6.QtGui import QPixmap
from PIL import Image
import shutil

def setPixMapOf(label, imgFileName, folder) :
    if imgFileName is None:
        destFolder = "icons"
        imgFileName = "placeholder_img"
        path = os.path.join(os.path.abspath(f"assets/{destFolder}"), imgFileName) 
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setFixedSize(125,125)
        label.setScaledContents(True)
        return None
    if folder == "temp" :
        destFolder = "temp"
        label.setFixedSize(150,150)
        label.setScaledContents(True)
    elif folder == "icon" :
        destFolder = "icons"
    else :
        destFolder = folder + "img"
        label.setFixedSize(125,125)
        label.setScaledContents(True)

    path = os.path.join(os.path.abspath(f"assets/{destFolder}"), imgFileName) 
    pixmap = QPixmap(path)
    label.setPixmap(pixmap)
       


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
