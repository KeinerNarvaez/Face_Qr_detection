# region Importaciones
import os
import cv2
#endregion
# region Clase
class FaceBase:
    #region Constructor
    def __init__(self,camera):
        self.data_path = "../../Data/recognition/"
        self.model_path = "../../Data/models/Model.xml"
        self.people_list = []
        self.face_model_path = '../../Data/models/res10_300x300_ssd_iter_140000.caffemodel'
        self.prototxt_path ='../../Data/models/deploy.prototxt.txt'
        self.camera = camera
        self.cap=None
    #endregion
    #region Metodos
    def detect_name_person(self):
        try:
            #Hago un recorrido para identificar las carpetas ignorando los documentos
            for path in os.listdir(self.data_path):
                #Uno de forma segura para evitar errores entre dispositivos
                data = os.path.join(self.data_path, path)
                if os.path.isdir(data):
                    #Se agrega los nombres al arreglo evitando agregar el de documentos, ejemplo .gitkeep
                    self.people_list.append(path)
            print('Lista de personas',self.people_list)
        except Exception as ex:
            return f'Error al detectar nombres de personas: {ex}'

    def load_detector(self):
        return cv2.dnn.readNetFromCaffe(self.prototxt_path,self.face_model_path)

    def open_camera(self):
        try:
            if self.camera == 'Interna':
                self.cap = cv2.VideoCapture(0)
            elif self.camera == 'Externa':
                self.cap = cv2.VideoCapture(1)
            else:
                return "Tipo de cámara no válido"
            if not self.cap.isOpened():
                return "No se puedo abrir la cámara seleccionada, verifica la cámara"
        except Exception as ex:
            return f'Error al indentificar la camara o al crear el archivos necesarios. {ex}'
    #endregion
#endregion