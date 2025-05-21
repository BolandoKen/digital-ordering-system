import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from PIL import Image
import shutil

class PixmapRepo() :
    def __init__(self):
        self.repo = {}
    
    def get_pixmap(self, img_path) :
        if img_path not in self.repo :
            temp_pixmap = QPixmap(img_path)
            self.repo[img_path] = temp_pixmap.scaled(
                                    QSize(200,150), 
                                    Qt.AspectRatioMode.KeepAspectRatio, 
                                    Qt.TransformationMode.SmoothTransformation
                                    )
            return self.repo[img_path]
        return self.repo[img_path]
    
    def update_imgPath_key(self, img_path) :
        temp_pixmap = QPixmap(img_path)
        self.repo[img_path] = temp_pixmap.scaled(
                                    QSize(200,150), 
                                    Qt.AspectRatioMode.KeepAspectRatio, 
                                    Qt.TransformationMode.SmoothTransformation
                                    )

    
    

pixmapRepo = PixmapRepo()

def getImgPath(imgFileName, assetFolder) :
     return os.path.join(os.path.abspath(f"assets/{assetFolder}"), imgFileName) 


def setPixMapOf(label, imgFileName, folder) : # folder :  temp | icon | food | category | profile
    if imgFileName is None: # set default icon
        destFolder = "icons"
        imgFileName = "placeholder_img.svg" if folder != "profile" else "pfp_icon.svg"
        path = os.path.join(os.path.abspath(f"assets/{destFolder}"), imgFileName) 

        pixmap = pixmapRepo.get_pixmap(path)
        label.setPixmap(pixmap)
        # label.setFixedSize(125,125)
        # label.setScaledContents(True)
        obj = {
            "path" : None,
            "pixmap" : pixmap, # unnecessary after memoization, refactor later, no ty im lazy
        }
        return obj
    if folder == "temp" :
        destFolder = "temp"
        # label.setFixedSize(150,150) # preferably remove these setfixsizes please!
        # label.setScaledContents(True)
    elif folder == "icon" :
        destFolder = "icons"
    else :
        destFolder = folder + "img" #folder is either 'category' or 'food'
        # label.setMaximumHeight(125)
        # label.setFixedSize(125,125) 
        # label.setScaledContents(True)

    path = os.path.join(os.path.abspath(f"assets/{destFolder}"), imgFileName) 
    if folder == "temp" :
        pixmapRepo.update_imgPath_key(path)

    pixmap = pixmapRepo.get_pixmap(path)

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
    # from edits, when img is saved as is, it basically moves the same image in place.
    if panelName == "category" :
        destPath = os.path.abspath("assets/categoryimg")
        os.makedirs(destPath, exist_ok=True)
        destPath = os.path.join(destPath, ImgRename)
        shutil.move(imgFilePath, destPath)
        print(imgFilePath, destPath)
        pixmapRepo.update_imgPath_key(destPath)

    elif panelName == "food" :
        destPath = os.path.abspath("assets/foodimg")
        os.makedirs(destPath, exist_ok=True)
        destPath = os.path.join(destPath, ImgRename)
        shutil.move(imgFilePath, destPath)
        pixmapRepo.update_imgPath_key(destPath)

    elif panelName == "profile" :
        destPath = os.path.abspath("assets/profileimg")
        os.makedirs(destPath, exist_ok=True)
        destPath = os.path.join(destPath, ImgRename)
        shutil.move(imgFilePath, destPath)
        pixmapRepo.update_imgPath_key(destPath)

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