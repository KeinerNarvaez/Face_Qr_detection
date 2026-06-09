import cv2
import os
import imutils
import numpy as np

PersonName = "Keiner"
dataPath = "../Data/recognition"
personPath = dataPath + '/' + PersonName
if not os.path.exists(personPath):
    print("Creando el archivos necesarios")
    os.mkdir(personPath)
cap = cv2.VideoCapture(0)
#faceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#Cambio por dnn porque es mas precisa
net = cv2.dnn.readNetFromCaffe('../Data/models/deploy.prototxt.txt', '../Data/models/res10_300x300_ssd_iter_140000.caffemodel')
count = 0
while True:
    ret, frame = cap.read()
    if ret == False:break
    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        1.0,
        (300, 300),
        (104.0, 177.0, 123.0)
    )
    net.setInput(blob)
    detections = net.forward()
    #faces = faceClassifier.detectMultiScale(gray, 1.3, 5)
    #for (x, y, w, h) in faces:
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * \
                  np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            cv2.rectangle(frame,(x1, y1),(x2, y2),(255, 0, 0), 2)
            rostro = auxFrame[y1:y2, x1:x2]
            if rostro.size > 0:
                rostro = cv2.resize(rostro,(300, 300),interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(
                    personPath + '/rostro_{}.jpg'.format(count),
                    rostro
                )
                count += 1
    cv2.imshow("frame", frame)
    k= cv2.waitKey(1)
    if k == 27 or count >=300:
        break
cap.release()
cv2.destroyAllWindows()

