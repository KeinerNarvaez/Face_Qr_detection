from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QLineEdit)
from Services.face.coach import Coach
from Frontend.Ui.qr_scanner import QrScannerUi
from Services.face.scanner import ScannerPerson
from Frontend.Ui.detector_face import DetectPersonUi


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detección de persona y Qr")
        with open("Frontend/Resources/Qss/Comon.qss","r") as file:
            self.setStyleSheet(file.read())
        self.setMaximumSize(300,190)
        self.setMinimumSize(300,190)
        self.setWindowIcon(QIcon("Frontend/Resources/img/icon.ico"))

        self.labelCamara = QLabel("Tipo de Cámara:")
        self.input_name= QLineEdit()
        self.input_name.setPlaceholderText("Nombre de la persona")
        self.status = QLabel()
        self.camera = QComboBox()
        self.camera.addItems(["Interna", "Externa","Telefono"])
        self.btn_face = QPushButton("Reconocimiento facial")
        self.btn_qr = QPushButton("Escanear QR")

        layout = QVBoxLayout()
        layout.addWidget(self.labelCamara)
        layout.addWidget(self.camera)
        layout.addWidget(self.btn_face)
        layout.addWidget(self.btn_qr)
        layout.addWidget(self.status)
        self.setLayout(layout)

        self.btn_face.clicked.connect(self.face_detector)
        self.btn_qr.clicked.connect(self.qr_detection)
        self.camera.currentTextChanged.connect(
            self.update_camera_tooltip
        )
        self.update_camera_tooltip(
            self.camera.currentText()
        )

    def update_camera_tooltip(self, camera):
        if camera == "Interna":
            self.camera.setToolTip(
                "Utiliza la webcam integrada del portátil."
            )
        elif camera == "Externa":
            self.camera.setToolTip(
                "Utiliza una cámara USB externa conectada al equipo."
            )
        elif camera == "Telefono":
            self.camera.setToolTip(
                "Utiliza DroidCam o aplicaciones similares para usar el teléfono como cámara.(en caso de algun fallo comprueba con tipo de cámara Externa)"
            )

    def face_detector(self):
        self.face_window = DetectPersonUi(self.camera.currentText())
        self.face_window.show()

    def qr_detection(self):
        self.qr_window = QrScannerUi(self.camera.currentText())
        self.qr_window.show()