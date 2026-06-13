# region importaciones
import cv2
import os
import imutils
import numpy as np
from Services.face.face_base import FaceBase
# endregion
# region Clase
class ScannerPerson(FaceBase):
    # region Constructor
    def __init__(self,person_name,camera):
        super().__init__(camera)
        if not person_name.strip():
            raise ValueError("El nombre no puede estar vacío")
        self.person_name = person_name.strip().title()
        self.person_path = os.path.join(self.data_path, self.person_name)
        self.count = 0
        self.net = self.load_detector()
    # endregion
    # region Métodos
    def folder_creation(self):
        try:
            if not os.path.exists(self.person_path):
                print("Creando archivos necesarios")
                os.mkdir(self.person_path)
        except Exception as ex:
            return f'Error creando archivos necesarios: {ex}'

    def detect_and_save_faces(self,blob,frame,w,h,auxFrame):
        try:

            self.net.setInput(blob)
            detections = self.net.forward()
            # faces = faceClassifier.detectMultiScale(gray, 1.3, 5)
            # for (x, y, w, h) in faces:
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    box = detections[0, 0, i, 3:7] * \
                          np.array([w, h, w, h])
                    (x1, y1, x2, y2) = box.astype("int")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    rostro = auxFrame[y1:y2, x1:x2]
                    if rostro.size > 0:
                        rostro = cv2.resize(rostro, (300, 300), interpolation=cv2.INTER_CUBIC)
                        cv2.imwrite(
                            os.path.join(self.person_path, f"rostro_{self.count}.jpg"),
                            rostro
                        )
                        self.count += 1
        except Exception as ex:
            return f'Error al guardar los archivos necesarios: {ex}'

    def detect_face(self):
        try:

            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame = imutils.resize(frame, width=640)
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                auxFrame = frame.copy()
                (h, w) = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(
                    cv2.resize(frame, (300, 300)),
                    1.0,
                    (300, 300),
                    (104.0, 177.0, 123.0)
                )
                error = self.detect_and_save_faces(blob,frame,w,h,auxFrame)
                if error:
                    return error
                cv2.imshow("Reconocimiento", frame)
                k = cv2.waitKey(1)
                if k == 27 or self.count >= 300:
                    break
        except Exception as ex:
            return f'Error al detectar rostro: {ex}'

    def detect_person(self):
        try:
            error = self.open_camera()
            if error:
                return error
            error = self.folder_creation()
            if error:
                return error
            error = self.detect_face()
            if error:
                return error
        except Exception as ex:
            return f'Error inesperado: {ex}'
        finally:
            if self.cap is not None:
                self.cap.release()
            cv2.destroyAllWindows()
    # endregion
# endregion