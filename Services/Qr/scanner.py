# region Importaciones
import cv2
#endregion
# region Clase
class QrScanner():
    #region Constructor
    def __init__(self,camera):
        self.camera = camera
        self.qrDetect = cv2.QRCodeDetector()
        self.cap = None
        self.data = None
        self.rectifiedImage= None
    # endregion
    #region Metodos
    def open_camera(self):
        try:
            if self.camera == 'Interna':
                self.cap = cv2.VideoCapture(0)
            elif self.camera == 'Externa':
                self.cap = cv2.VideoCapture(1)
            elif self.camera == 'Telefono':
                self.cap = cv2.VideoCapture(2)
            else:
                return "Tipo de cámara no válido."
            if not self.cap.isOpened():
                return "No se puedo abrir la cámara seleccionada"
        except Exception as ex:
            print(f'Error al indentificar la camara o al crear el archivos necesarios. {ex}')
            return f'Error inesperado en la camara'

    def decode(self,frame):
        if self.data:
            print(f'Dato: {self.data}')

            self.rectifiedImage = cv2.resize(self.rectifiedImage, (300,300), interpolation = cv2.INTER_AREA)
            cv2.imshow("Detectar Qr",self.rectifiedImage)
            cv2.waitKey(3000)
        else:
            cv2.imshow("Detectar Qr",frame)

    def get_image(self):
        return self.rectifiedImage

    def detect_qr(self):
        try:
            error = self.open_camera()
            if error:
                return error
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                if (cv2.waitKey(1) == 27):  # Esc
                    break
                if self.data and self.rectifiedImage is not None:
                    break
                self.data, bbox, self.rectifiedImage = self.qrDetect.detectAndDecode(frame)
                self.decode(frame)
        except Exception as ex:
            print(f'Error inesperado: {ex}')
            return f'Error inesperado.'
        finally:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
    # endregion
#endregion