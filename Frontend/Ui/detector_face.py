from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QScrollArea

from Frontend.Dashboard.dasboard_person import DashboardPersonUi
from Services.face.scanner import ScannerPerson
from Services.face.coach import Coach
from Services.face.recognition import Recognition

class DetectPersonUi(QWidget):
    def __init__(self,camera):
        super().__init__()
        self.setMaximumSize(550,260)
        self.setMinimumSize(550,260)
        self.style = ""
        with open("Frontend/Resources/Qss/Comon.qss","r") as file:
            self.style +=file.read()
        with open("Frontend/Resources/Qss/detector_face.qss", "r") as file:
            self.style +=file.read()
        self.setStyleSheet(self.style)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("Reconocimiento Facial")

        self.camera = camera
        self.btn_train = QPushButton("Entrenar Modelo")
        self.btn_scanner_face = QPushButton("Detectar cara")
        self.btn_face = QPushButton("Reconocimiento Facial")
        self.btn_manage_user = QPushButton("Gestionar usuarios")
        self.btn_manage_user.setFixedWidth(300)
        self.setWindowIcon(QIcon("Frontend/Resources/img/icon.ico"))
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nombre de la persona")

        self.scanner_face_label=QLabel("Registrar usuarios:")
        self.status_label=QLabel("Estado de los procedimientos:")
        self.status_label.setObjectName('StatusLabel')
        self.status = QLabel()
        self.status.setObjectName("Status")
        self.status.setWordWrap(True)
        self.scroll_status = QScrollArea()
        self.scroll_status.setWidget(self.status)
        self.scroll_status.setWidgetResizable(True)

        main_layout = QHBoxLayout()
        self.main_face_layout = QVBoxLayout()
        scanner_face = QVBoxLayout()
        scanner_face.addWidget(self.scanner_face_label)
        scanner_face.addWidget(self.input_name)
        scanner_face.addWidget(self.btn_scanner_face)


        scanner_btn_layout = QHBoxLayout()
        scanner_btn_layout.addWidget(self.btn_train)
        scanner_btn_layout.addWidget(self.btn_face)

        manage_btn_layout = QVBoxLayout()
        manage_btn_layout.addWidget(self.btn_manage_user)

        status_layout = QVBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.scroll_status)

        self.face_container = QWidget()
        self.face_container.setObjectName("LayoutFace")
        self.face_container3 = QWidget()
        self.face_container3.setObjectName("LayoutFace")
        self.face_container2 = QWidget()
        self.face_container2.setObjectName("LayoutFace")

        self.face_container.setLayout(scanner_face)
        self.face_container2.setLayout(scanner_btn_layout)
        self.face_container3.setLayout(manage_btn_layout)

        self.main_face_layout.addWidget(self.face_container)
        self.main_face_layout.addWidget(self.face_container2)
        self.main_face_layout.addWidget(self.face_container3)

        main_layout.addLayout(self.main_face_layout)
        main_layout.addLayout(status_layout)
        self.setLayout(main_layout)

        self.btn_scanner_face.clicked.connect(self.detect_person)
        self.btn_train.clicked.connect(self.train_model)
        self.btn_face.clicked.connect(self.face_detection)
        self.btn_manage_user.clicked.connect(self.open_dashboard)


    def face_detection(self):
        try:
            recognition = Recognition(
                self.camera
            )
            recognition.detect()
        except Exception as ex:
            self.status.setText("Error inesperado abriendo pestaña de detección")

    def detect_person(self):
        try:
            if self.input_name.text() != "":
                person = ScannerPerson(self.input_name.text(), self.camera)
                self.status.setText(person.detect_person())
            else:
                self.status.setText("Ingrese un nombre")
        except Exception as ex:
            self.status.setText("Error inesperado abriendo pestaña de escaner")

    def train_model(self):
        try:
            self.status.setText("Entrenando...")
            coach = Coach()
            self.status.setText(coach.load_training_data())
        except Exception as ex:
            self.status.setText("Error inesperado abriendo pestaña de entrenamiento")

    def open_dashboard(self):
        try:
            self.dashboard = DashboardPersonUi()
            self.dashboard.show()
        except Exception as ex:
            self.status.setText("Error inesperado abriendo pestaña de lista de personas")
