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
        obj = {
            "path" : path,
            "pixmap" : pixmap,
        }
        return obj
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
       
    obj = {
        "path" : path,
        "pixmap" : pixmap,
    }

    return obj

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


def deleteImageOfCategory(catid) :
    destPath = os.path.abspath("assets/categoryimg")
    imgToDelete = f"{catid}.png"
    filePathToDelete = os.path.join(destPath,imgToDelete)
    if os.path.exists(filePathToDelete) :
        os.remove(filePathToDelete)

def deleteImageOfFood(foodid) :
    destPath = os.path.abspath("assets/foodimg")
    imgToDelete = f"{foodid}.png"
    filePathToDelete = os.path.join(destPath,imgToDelete)
    if os.path.exists(filePathToDelete) :
        print(filePathToDelete)
        os.remove(filePathToDelete)


# path = os.path.join(os.path.abspath("assets/foodimg"), "test.png")
# print(path)

# moveImageToAssets(path, "category")