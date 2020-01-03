import cv2
import os
import numpy as np
from PIL import Image
from mysql_operations import *

def Face_capture(Id):
    face_cascade = cv2.CascadeClassifier(
        "C:\\Users\\rohit gupta\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    sampleN = 0;
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            sampleN = sampleN + 1;
            cv2.imwrite("C:\\MiniProject\\Attendance_management_system\\Images\\User." + str(Id) +  "." + str(sampleN)+".jpg",
                        gray[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.waitKey(100)

        cv2.imshow('img', img)
        cv2.waitKey(1)
        if sampleN > 20:
            break

    cap.release()

    cv2.destroyAllWindows()

    Image_processing()


def Image_processing():
    recognizer = cv2.face.LBPHFaceRecognizer_create();
    path = "C:\\MiniProject\\Attendance_management_system\\Images"

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

        faces = []

        IDs = []

        for imagePath in imagePaths:
            facesImg = Image.open(imagePath).convert('L')

            faceNP = np.array(facesImg, 'uint8')

            ID = int(os.path.split(imagePath)[-1].split(".")[1])

            faces.append(faceNP)

            IDs.append(ID)

            cv2.imshow("Adding faces for traning", faceNP)

            cv2.waitKey(10)

        return np.array(IDs), faces

    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, Ids)
    recognizer.save("C:\\MiniProject\\Attendance_management_system\\training\\trainingdata.yml")
    cv2.destroyAllWindows()

def livefeed_attendance():
    face_cascade = cv2.CascadeClassifier(
        'C:\\Users\\rohit gupta\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    rec = cv2.face.LBPHFaceRecognizer_create();
    rec.read("C:\\MiniProject\\Attendance_management_system\\training\\trainingdata.yml")
    name=get_face_database()
    font = cv2.FONT_HERSHEY_SIMPLEX
    My_Face_ids=[]
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            id, conf = rec.predict(gray[y:y + h, x:x + w])
            name_of_person = name[id].split(":")[1]
            predicted_name = name_of_person
            if name[id].split(":")[0] not in My_Face_ids:
                My_Face_ids.append(name[id].split(":")[0])
            if (conf < 60):
                cv2.putText(img, predicted_name, (x, y + h), font, 0.55, (0, 255, 0), 1)
        cv2.imshow('img', img)

        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()

    cv2.destroyAllWindows()
    return update_idx(My_Face_ids,get_period())
