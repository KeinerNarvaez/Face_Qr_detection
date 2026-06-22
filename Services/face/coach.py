# region Importaciones
import cv2
import os
import numpy as np
from Services.face.face_base import FaceBase
# endregion
# region Clase
class Coach(FaceBase):
    # region Constructor
    def __init__(self):
        super().__init__(None)
        self.labels = []
        self.faces_data = []
    # endregion
    # region Metodos
    def detect_person(self):
        try:
            label = 0
            for name_dir in self.people_list:
                person_path = os.path.join(self.data_path,name_dir)
                print('Leyendo imagenes')
                for file_name in os.listdir(person_path):
                    print('Rostros: ', name_dir+'/'+file_name)
                    image = cv2.imread(os.path.join(person_path,file_name),0)
                    if image is None:
                        continue
                    cv2.putText(image, 'Leyendo imagenes', (10, 30), cv2.FONT_ITALIC, 1, (255, 255, 255), 1)
                    cv2.putText(image, f'Rostros: {name_dir}', (10, 290), cv2.FONT_ITALIC, 1, (255, 255, 255), 1)
                    image = cv2.resize(image, (300, 300))
                    self.faces_data.append(image)
                    self.labels.append(label)
                    cv2.imshow('Reconocimiento',image)
                    cv2.waitKey(10)
                label+=1
            cv2.destroyAllWindows()
        except Exception as ex:
            return f'Error al detectar las personas: {ex}'

    def train_model(self):
        try:
            face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            print('Entrenando...')
            imagen = np.zeros((300,300,3),dtype=np.uint8)
            cv2.rectangle(imagen,(0,0),(300,300),(0,0,225),-1)
            cv2.putText(imagen,'Entrenando',(10,30),cv2.FONT_ITALIC,1,(255,255,255),1)

            cv2.imshow("Entrenando",imagen)
            cv2.waitKey(100)
            face_recognizer.train(self.faces_data, np.array(self.labels))
            face_recognizer.write(self.model_path) #model_path es la direccion donde esta el modelo
            print('Modelo almacenado...')
            imagen[:] = (0,150,30)
            cv2.putText(imagen,'Modelo',(10,30),cv2.FONT_ITALIC,1,(255,255,255),1)
            cv2.putText(imagen,'almacenado...',(10,60),cv2.FONT_ITALIC,1,(255,255,255),1)
            cv2.imshow("Entrenando",imagen)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
        except Exception as ex:
            return f'Error al entrenar modelo: {ex}'
    # region orquestador
    def load_training_data(self):
        try:
            error = self.detect_name_person()
            if error:
                return error
            error = self.detect_person()
            if error:
                return error
            error = self.train_model()
            if error:
                return error
        except Exception as ex:
            return f'Error inesperado: {ex}'
    # endregion
    # endregion
# endregion


