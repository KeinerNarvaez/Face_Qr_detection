from PyQt6.QtWidgets import (QDialog,QVBoxLayout,QLabel,QLineEdit,QPushButton,QHBoxLayout)
class ModifyUserDialog(QDialog):
    def __init__(self, current_name):
        super().__init__()
        with open("Frontend/Resources/Qss/Comon.qss", "r") as file:
            self.setStyleSheet(file.read())
        self.setWindowTitle("Modificar usuario")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        title = QLabel(f"Modificar usuario: {current_name}")

        self.input_name = QLineEdit()
        self.input_name.setText(current_name)
        self.input_name.setPlaceholderText("Escribe el nuevo nombre al usuario")


        buttons = QHBoxLayout()

        btn_save = QPushButton("Guardar")
        btn_cancel = QPushButton("Cancelar")

        btn_save.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        buttons.addWidget(btn_save)
        buttons.addWidget(btn_cancel)

        layout.addWidget(title)
        layout.addWidget(self.input_name)
        layout.addLayout(buttons)

        self.setLayout(layout)

    def get_name(self):
        return self.input_name.text().title()