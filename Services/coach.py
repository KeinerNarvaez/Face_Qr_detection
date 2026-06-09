import cv2
import os
import numpy as np

dataPath = "../Data/recognition/"
peopleList = os.listdir(dataPath)
print('Lista de personas',peopleList)
labels=[]
facesData = []
label=0

for nameDir in peopleList:
    personPath = dataPath + '/' + nameDir
    print('Leyendo imagenes')
    for fileName in os.listdir(personPath):
        print('Rostros: ', nameDir+'/'+fileName)
        labels.append(label)
        facesData.append(cv2.imread(personPath+'/'+fileName,0))
        image= cv2.imread(personPath+'/'+fileName,0)
        cv2.putText(image, f'Leyendo imagenes', (10, 30), cv2.FONT_ITALIC, 1, (255, 255, 255), 1)
        cv2.putText(image, f'Rostros: {nameDir}', (10, 290), cv2.FONT_ITALIC, 1, (255, 255, 255), 1)
        if image is None:
            continue
        image = cv2.resize(image, (300, 300))
        facesData.append(image)
        labels.append(label)
        cv2.imshow('image',image)
        cv2.waitKey(10)
    label+=1
cv2.destroyAllWindows()
#face_recognizer = cv2.face.EigenFaceRecognizer_create()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
print('Entrenando...')
imagen = np.zeros((300,300,3),dtype=np.uint8)
cv2.rectangle(imagen,(0,0),(300,300),(0,0,225),-1)
cv2.putText(imagen,'Entrenando',(10,30),cv2.FONT_ITALIC,1,(255,255,255),1)

cv2.imshow("Entrenando",imagen)
cv2.waitKey(100)
face_recognizer.train(facesData, np.array(labels))
face_recognizer.write('../Data/models/Model.xml')
print('Modelo almacenado...')
imagen[:] = (0,150,30)
cv2.putText(imagen,'Modelo',(10,30),cv2.FONT_ITALIC,1,(255,255,255),1)
cv2.putText(imagen,'almacenado...',(10,60),cv2.FONT_ITALIC,1,(255,255,255),1)
cv2.imshow("Entrenando",imagen)
cv2.waitKey(3000)
cv2.destroyAllWindows()