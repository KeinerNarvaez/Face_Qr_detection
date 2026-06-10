import cv2
import os
import numpy as np
dataPath = "../../Data/recognition"
imagePaths = os.listdir(dataPath)
print('imagePaths',imagePaths)
#face_recognizer = cv2.face.EigenFaceRecognizer_create()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('../../Data/models/Model.xml')
cap = cv2.VideoCapture(0)
#faceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
net = cv2.dnn.readNetFromCaffe('../../Data/models/deploy.prototxt.txt', '../../Data/models/res10_300x300_ssd_iter_140000.caffemodel')
while True:
    ret, frame = cap.read()
    if ret == False: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()
    #faces = faceClassifier.detectMultiScale(gray, 1.3, 5)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),1.0,(300, 300),(104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    #for (x,y,w,h) in faces:
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        #rostro = auxFrame[y:y+h,x:x+w]
        #rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        #result = face_recognizer.predict(rostro)
        #cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(225,225,0),1,cv2.LINE_AA)
        #if result[1] < 5700:
        #    cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y - 25), 2, 1.1, (0, 225, 0), 1, cv2.LINE_AA)
        #    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225,0), 2)
        #else:
        #    cv2.putText(frame, 'Desconocido', (x, y - 20), 1, 0.8, (0, 0, 225), 1, cv2.LINE_AA)
        #    cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,225), 2)
        if confidence > 0.8:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            # Esto para evitar cordenadas fuera de camara y tome el rostro
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)

            rostro = auxFrame[y1:y2, x1:x2]
            if rostro.size == 0:
                continue
            try:
                rostro = cv2.resize(rostro,(300, 300),interpolation=cv2.INTER_CUBIC)
            except:
                continue
            result = face_recognizer.predict(rostro)
            print(result)
            cv2.putText(frame,'{}'.format(result[1]),(x1, y1 - 5),1,1.2,(255, 255, 0),1,cv2.LINE_AA)

            if result[1] < 70:
                cv2.putText(frame,imagePaths[result[0]],(x1, y1 - 25),2,1.1,(0, 255, 0),1,cv2.LINE_AA)
                cv2.rectangle(frame,(x1, y1),(x2, y2),(0, 255, 0),2)
            else:
                cv2.putText(frame,'Desconocido',(x1, y1 - 20),1,0.8,(0, 0, 255),1,cv2.LINE_AA)
                cv2.rectangle(frame,(x1, y1),(x2, y2),(0, 0, 255),2)
    cv2.imshow('frame',frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()