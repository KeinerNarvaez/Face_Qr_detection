import cv2
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if (cv2.waitKey(1) == 27 ): #Esc
        break
    qrDetect = cv2.QRCodeDetector()
    data, bbox, rectifiedImage = qrDetect.detectAndDecode(frame)
    if len(data) > 0:
        print(f'Dato: {data}')
        rectifiedImage = cv2.resize(rectifiedImage, (300,300), interpolation = cv2.INTER_AREA)
        cv2.imshow("Detectar Qr",rectifiedImage)
        cv2.waitKey(3000)
    else:
        cv2.imshow("Detectar Qr",frame)
cap.release()
cv2.destroyAllWindows()