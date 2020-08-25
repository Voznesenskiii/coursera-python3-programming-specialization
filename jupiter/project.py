from zipfile import ZipFile 

from PIL import Image

import pytesseract

import cv2 as cv

import numpy as np



# loading the face detection classifier

face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')



def init(fileName):

    database = {}

    with ZipFile(fileName, 'r') as archive:

        for entry in archive.infolist():

            with archive.open(entry) as file:

                img = Image.open(file)

                gray_img= img.convert("L")



                text = pytesseract.image_to_string(gray_img) 



                np_img = np.array(gray_img)

                faces = face_cascade.detectMultiScale(np_img, 1.35)

                database[entry.filename] = {'image': img, 'text': text, 'faces': faces}

    return database

                

def createContactSheet(img, faces):

    SIZE = 100

    MAX_COL = 5

    MAX_ROW = (len(faces) - 1 + MAX_COL) // MAX_COL

    contact_sheet = Image.new(img.mode, (SIZE * MAX_COL, SIZE * MAX_ROW))

    

    px = 0

    py = 0

    

    np_img = np.array(img)     

    for x,y,w,h in faces:

        f = np_img[y:y+h, x:x+w]

        face = Image.fromarray(f)

        face.thumbnail((SIZE, SIZE)) 

        

        contact_sheet.paste(face, (px, py))

        if px + SIZE == contact_sheet.width:

            px = 0

            py = py + SIZE

        else:

            px = px + SIZE

    return contact_sheet



def search(word, database):

    for (fileName, info) in database.items():        

        if word in info["text"]:

            print("Result found in ", fileName)

            if len(info["faces"]) > 0:

                contact_sheet = createContactSheet(info["image"], info["faces"])

                display(contact_sheet)

            else:

                print("But there were no faces in that file!")



print("=== File: small_img.zip ===")

database = init("readonly/small_img.zip")

print("=== Search: Christopher ===")

search("Christopher", database)



print("\n")

print("=== File: images.zip ===")

database = init("readonly/images.zip")

print("=== Search: Mark ===")

search("Mark", database)