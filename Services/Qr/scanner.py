# region Importaciones
import cv2
#endregion
# region Clase
class QrScanner:
    #region Constructor
    def __init__(self,camera):
        self.camera = camera
        self.qrDetect = cv2.QRCodeDetector()
        self.cap = None
        self.data = None
    # endregion
    #region Metodos
    def open_camera(self):
        try:
            if self.camera == 'Interna':
                self.cap = cv2.VideoCapture(0)
            elif self.cap == 'Externa':
                self.camera = cv2.VideoCapture(1)
            else:
                return "Tipo de cámara no válido"
            if not self.cap.isOpened():
                return "No se puedo abrir la cámara seleccionada, verifica la cámara"
        except Exception as ex:
            return f'Error al indentificar la camara o al crear el archivos necesarios. {ex}'

    def decode(self,rectifiedImage,frame):
        if self.data:
            print(f'Dato: {self.data}')
            rectifiedImage = cv2.resize(rectifiedImage, (300,300), interpolation = cv2.INTER_AREA)
            cv2.imshow("Detectar Qr",rectifiedImage)
            cv2.waitKey(3000)
        else:
            cv2.imshow("Detectar Qr",frame)

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
                self.data, bbox, rectifiedImage = self.qrDetect.detectAndDecode(frame)
                self.decode(rectifiedImage,frame)
        except Exception as ex:
            return f'Error inesperado: {ex}'
        finally:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
    # endregion
#endregion