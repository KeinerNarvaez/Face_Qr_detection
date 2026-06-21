from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from Services.Qr.scanner import QrScanner


class QrScannerUi(QWidget):
    def __init__(self,camera):
        super().__init__()
        self.style = ""
        with open("Frontend/Resources/Qss/Comon.qss","r") as file:
            self.style +=file.read()
        with open("Frontend/Resources/Qss/Qr_scannerUi.qss", "r") as file:
            self.style +=file.read()
        self.setStyleSheet(self.style)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMaximumSize(260,250)
        self.setMinimumSize(260,310)
        self.camera = camera
        self.setWindowTitle("Detector de Qr")
        self.setWindowIcon(QIcon("Frontend/Resources/img/icon.ico"))
        self.url= QLabel()
        self.url.setOpenExternalLinks(True)
        self.status = QLabel()
        self.qr_image = QLabel()
        self.qr_image.setFixedSize(210, 200)
        self.qr_image.setObjectName("qrImage")
        self.btn_qr = QPushButton("Escanear Qr")
        layout = QVBoxLayout()
        layout.addWidget(self.qr_image, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.url)
        layout.addWidget(self.status)
        layout.addWidget(self.btn_qr)
        self.setLayout(layout)
        self.btn_qr.clicked.connect(self.qr_detection)


    def qr_detection(self):
        scanner = QrScanner(
            self.camera
        )
        error = scanner.detect_qr()
        if error:
            self.status.setText(error)
            return
        self.url.setText(
            f'<a href="{scanner.data}">Link</a>'
            if scanner.data
            else "QR no detectado"
        )
        try:
            if scanner.rectifiedImage is not None:
                image = scanner.rectifiedImage

                height, width = image.shape
                bytes_per_line = width

                q_image = QImage(
                    image.data,
                    width,
                    height,
                    bytes_per_line,
                    QImage.Format.Format_Grayscale8
                )

                pixmap = QPixmap.fromImage(q_image)

                self.qr_image.setPixmap(
                    pixmap.scaled(
                        190,190
                    )
                )
                self.status.setText("Exito al leer el Qr")
        except Exception as ex:
            print(f'Error al insertar imagen Qr: {ex}')
            return 'Error al insertar imagen Qr'