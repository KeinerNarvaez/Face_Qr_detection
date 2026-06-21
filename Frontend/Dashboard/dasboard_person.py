from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QScrollArea
from Services.dashboard.dashboard_person import DashboardPerson


class DashboardPersonUi(QWidget):
    def __init__(self):
        super().__init__()

        # =========================
        # Estilos
        # =========================
        self.style = ""

        with open("Frontend/Resources/Qss/Comon.qss", "r") as file:
            self.style += file.read()

        with open("Frontend/Resources/Qss/dashboard.qss", "r") as file:
            self.style += file.read()

        self.setStyleSheet(self.style)

        # =========================
        # Configuración ventana
        # =========================

        self.setMaximumSize(550, 400)
        self.setMinimumSize(550, 400)

        self.setWindowTitle(
            "Dashboard de usuarios y entrenamiento de modelo"
        )
        self.setWindowIcon(
            QIcon("Frontend/Resources/img/icon.ico")
        )

        # =========================
        # Servicios
        # =========================
        self.objectDashboard = DashboardPerson()

        # =========================
        # Widgets
        # =========================
        self.person_label = QLabel("Personas registradas")
        table_container = QWidget()
        table_container.setObjectName("Table")
        header_widget = QWidget()
        header_widget.setObjectName("Header")

        # =========================
        # Estructuras de datos
        # =========================
        self.btn_delete = {}
        self.btn_modify = {}
        self.person = {}

        # =========================
        # Layouts
        # =========================
        self.TableLayout = QVBoxLayout()
        main_body = QVBoxLayout()
        main_header = QHBoxLayout()
        layout_main = QVBoxLayout()
        header_layout = QVBoxLayout()
        # =========================
        # Construcción interfaz
        # =========================
        header_layout.addWidget(self.person_label,alignment=Qt.AlignmentFlag.AlignCenter)
        header_widget.setLayout(header_layout)
        main_header.addWidget(header_widget)
        table_container.setLayout(self.TableLayout)
        main_body.addWidget(table_container)
        layout_main.addLayout(main_header)
        layout_main.addLayout(main_body)

        # =========================
        # Cargar datos
        # =========================
        self.list_persons()

        # =========================
        # Layout principal
        # =========================
        self.setLayout(layout_main)

    def persons(self):
        return DashboardPerson().folders()

    def delete(self, person):
        self.objectDashboard.delete_person(person)


    def modify(self, current_name,new_name):
        self.objectDashboard.modify_name(current_name,new_name)

    def list_persons(self):
        try:
            names = self.persons()
            scroll_item_people = QScrollArea()
            container = QWidget()
            container.setObjectName("ScrollItems")
            container_layout = QVBoxLayout()
            for person in names:
                row_widget = QWidget()
                row_widget.setObjectName("ItemsTable")
                row = QHBoxLayout()
                label = QLabel(person)
                btn_delete = QPushButton("Eliminar")
                btn_modify = QPushButton("Modificar")
                btn_delete.clicked.connect(lambda _, p=person: self.delete(p))
                btn_modify.clicked.connect(lambda _, p=person: self.modify(p))
                row.addWidget(label,alignment=Qt.AlignmentFlag.AlignCenter)
                row.addWidget(btn_modify)
                row.addWidget(btn_delete)
                row_widget.setLayout(row)
                container_layout.addWidget(row_widget)
                container.setLayout(container_layout)

            scroll_item_people.setWidget(container)
            scroll_item_people.setWidgetResizable(True)
            self.TableLayout.addWidget(scroll_item_people)
        except Exception as ex:
            return ex