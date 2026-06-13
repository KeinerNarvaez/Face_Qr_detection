# region Importaciones
import cv2
import numpy as np
from Services.face.face_base import FaceBase
# endregion
# region Clase
class Recognition(FaceBase):
    # region Constructor
    def __init__(self,camera):
        super().__init__(camera)
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_recognizer.read(self.model_path) # model_path es la dirección donde esta el modelo
    # endregion
    # region Metodos
    def get_face_coordinates(self,detections,i,w,h):
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x1, y1, x2, y2) = box.astype("int")
        # Esto para evitar cordenadas fuera de camara y tome el rostro
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        return (x1, y1, x2, y2)

    def draw_prediction(self,frame,result,x1,y1,x2,y2):
        if result[1] < 70: # 70 Valor de error al detecter, entre menor valor
            cv2.putText(frame, self.people_list[result[0]], (x1, y1 - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Desconocido', (x1, y1 - 20), 1, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    def process_detections(self,detections,frame,auxFrame,w,h):
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.8: # Nivel de confianza 0.5 = moderadamente seguro 0.8 = bastante seguro
                x1, y1, x2, y2 =self.get_face_coordinates(detections,i,w,h)
                rostro = auxFrame[y1:y2, x1:x2]
                if rostro.size == 0:
                    continue
                try:
                    rostro = cv2.resize(rostro, (300, 300), interpolation=cv2.INTER_CUBIC)
                except Exception:
                    continue
                result = self.face_recognizer.predict(rostro)
                print(result)
                cv2.putText(frame, '{}'.format(result[1]), (x1, y1 - 5), 1, 1.2, (255, 255, 0), 1, cv2.LINE_AA)
                self.draw_prediction(frame,result,x1,y1,x2,y2)

    def detect(self):
        try:
            #Este ejecuta el metodo de Coach que buscando los nombres de las carpetas hace un array people_list
            self.detect_name_person()
            error = self.open_camera()
            if error:
                return error
            net = self.load_detector()
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                auxFrame = gray.copy()
                (h, w) = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),1.0,(300, 300),(104.0, 177.0, 123.0))
                net.setInput(blob)
                detections = net.forward()
                self.process_detections(detections,frame,auxFrame,w,h)
                cv2.imshow('frame',frame)
                k = cv2.waitKey(1)
                if k == 27:
                    break
        except Exception as ex:
            return f'Error inesperado: {ex}'
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
    #endregion
# endregion