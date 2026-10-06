import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

VERDE = "#27ae60"
VERDE_CLARO = "#2ecc71"
GRIS_CLARO = "#ecf0f1"
GRIS = "#bdc3c7"


class DialogoConfirmacion(QDialog):
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmar registro")
        self.setFixedSize(360, 300)

        diseño = QVBoxLayout(self)

        aviso = QLabel("Verifica tus datos:")
        aviso.setFont(QFont("Arial", 12, QFont.Bold))
        aviso.setStyleSheet(f"color: {VERDE}; background: transparent;")
        diseño.addWidget(aviso)

        resumen = QTextEdit()
        resumen.setReadOnly(True)
        resumen.setFont(QFont("Consolas", 10))
        for etiqueta, valor in datos:
            resumen.append(f"{etiqueta}: {valor}")
        diseño.addWidget(resumen)

        cajas = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        cajas.button(QDialogButtonBox.Ok).setText("Confirmar")
        cajas.button(QDialogButtonBox.Cancel).setText("Cancelar")
        cajas.accepted.connect(self.accept)
        cajas.rejected.connect(self.reject)
        diseño.addWidget(cajas)


class DialogoExito(QDialog):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registro exitoso")
        self.setFixedSize(300, 160)

        diseño = QVBoxLayout(self)

        ok = QLabel("Registro completado")
        ok.setAlignment(Qt.AlignCenter)
        ok.setFont(QFont("Arial", 16, QFont.Bold))
        ok.setStyleSheet(f"color: {VERDE}; background: transparent;")
        diseño.addWidget(ok)

        detalle = QLabel(f"Bienvenido, {usuario}")
        detalle.setAlignment(Qt.AlignCenter)
        detalle.setStyleSheet("background: transparent;")
        diseño.addWidget(detalle)

        boton = QDialogButtonBox(QDialogButtonBox.Ok)
        boton.accepted.connect(self.accept)
        diseño.addWidget(boton)


class FormularioRegistro(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        diseño = QVBoxLayout(self)
        diseño.setContentsMargins(0, 0, 0, 0)

        seccion = QGridLayout()
        seccion.addWidget(QLabel("Datos personales"), 0, 0, 1, 2)

        formulario = QFormLayout()
        self.txt_nombre = QLineEdit()
        self.txt_apellido = QLineEdit()
        self.txt_email = QLineEdit()
        self.txt_usuario = QLineEdit()
        self.txt_clave = QLineEdit()
        self.txt_clave.setEchoMode(QLineEdit.Password)
        self.txt_clave2 = QLineEdit()
        self.txt_clave2.setEchoMode(QLineEdit.Password)

        formulario.addRow("Nombre:", self.txt_nombre)
        formulario.addRow("Apellido:", self.txt_apellido)
        formulario.addRow("Correo:", self.txt_email)
        formulario.addRow("Usuario:", self.txt_usuario)
        formulario.addRow("Clave:", self.txt_clave)
        formulario.addRow("Repetir clave:", self.txt_clave2)
        seccion.addLayout(formulario, 1, 0)

        extras = QVBoxLayout()
        extras.addWidget(QLabel("Pais:"))
        self.combo_pais = QComboBox()
        self.combo_pais.addItems(["Argentina", "Chile", "Paraguay", "Uruguay", "Peru"])
        extras.addWidget(self.combo_pais)

        self.radio_femenino = QRadioButton("Femenino")
        self.radio_masculino = QRadioButton("Masculino")
        self.radio_masculino.setChecked(True)
        extras.addWidget(QLabel("Genero:"))
        extras.addWidget(self.radio_femenino)
        extras.addWidget(self.radio_masculino)

        self.chk_terminos = QCheckBox("Acepto los terminos y condiciones")
        extras.addWidget(self.chk_terminos)

        self.chk_noticias = QCheckBox("Recibir novedades por correo")
        extras.addWidget(self.chk_noticias)

        seccion.addLayout(extras, 1, 1)
        diseño.addLayout(seccion)

        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet(
            "color: #e74c3c; background: transparent; font-weight: bold;"
        )
        self.lbl_error.setWordWrap(True)
        diseño.addWidget(self.lbl_error)

        self.resumen = QTextEdit()
        self.resumen.setReadOnly(True)
        self.resumen.setPlaceholderText("Aqui se mostrara tu ficha de registro...")
        self.resumen.setFixedHeight(80)
        diseño.addWidget(self.resumen)

        acciones = QHBoxLayout()
        self.btn_registrar = QPushButton("Registrar")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_salir = QPushButton("Salir")
        self.btn_registrar.setObjectName("confirmar")
        self.btn_limpiar.setObjectName("borrar")
        acciones.addWidget(self.btn_registrar)
        acciones.addWidget(self.btn_limpiar)
        acciones.addWidget(self.btn_salir)
        diseño.addLayout(acciones)

    def obtener_datos(self):
        return [
            ("Nombre", self.txt_nombre.text()),
            ("Apellido", self.txt_apellido.text()),
            ("Correo", self.txt_email.text()),
            ("Usuario", self.txt_usuario.text()),
            ("Clave", "*" * len(self.txt_clave.text())),
            ("Pais", self.combo_pais.currentText()),
            (
                "Genero",
                "Femenino" if self.radio_femenino.isChecked() else "Masculino",
            ),
            ("Novedades", "Si" if self.chk_noticias.isChecked() else "No"),
        ]

    def validar(self):
        if not self.txt_nombre.text().strip():
            return "El nombre es obligatorio."
        if not self.txt_apellido.text().strip():
            return "El apellido es obligatorio."
        if "@" not in self.txt_email.text():
            return "El correo no es valido."
        if len(self.txt_usuario.text()) < 4:
            return "El usuario debe tener al menos 4 caracteres."
        if len(self.txt_clave.text()) < 6:
            return "La clave debe tener al menos 6 caracteres."
        if self.txt_clave.text() != self.txt_clave2.text():
            return "Las claves no coinciden."
        if not self.chk_terminos.isChecked():
            return "Debes aceptar los terminos y condiciones."
        return ""

    def limpiar(self):
        for campo in (
            self.txt_nombre,
            self.txt_apellido,
            self.txt_email,
            self.txt_usuario,
            self.txt_clave,
            self.txt_clave2,
        ):
            campo.clear()
        self.chk_terminos.setChecked(False)
        self.chk_noticias.setChecked(False)
        self.resumen.clear()
        self.lbl_error.clear()


class VentanaRegistro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALAN - Registro")
        self.setMinimumSize(520, 520)

        self.contenido = QWidget()
        self.contenido.setObjectName("contenido")
        self.contenido.setAttribute(Qt.WA_StyledBackground, True)
        self.setCentralWidget(self.contenido)

        principal = QVBoxLayout(self.contenido)
        principal.setContentsMargins(14, 14, 14, 14)

        titulo = QLabel("ALAN")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        principal.addWidget(titulo)

        subtitulo = QLabel("Formulario de registro - R1")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("color: #7f8c8d; background: transparent;")
        principal.addWidget(subtitulo)

        self.formulario = FormularioRegistro()
        principal.addWidget(self.formulario)

        self._crear_menus()
        self._crear_barra_estado()
        self._aplicar_tema()

        self.formulario.btn_registrar.clicked.connect(self.registrar)
        self.formulario.btn_limpiar.clicked.connect(self.formulario.limpiar)
        self.formulario.btn_salir.clicked.connect(self.close)

    def _crear_menus(self):
        menu_archivo = self.menuBar().addMenu("&Archivo")
        accion_nuevo = QAction("Nuevo registro", self)
        accion_nuevo.setShortcut(QKeySequence("Ctrl+N"))
        accion_nuevo.triggered.connect(self.formulario.limpiar)
        accion_salir = QAction("Salir", self)
        accion_salir.setShortcut(QKeySequence("Ctrl+Q"))
        accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(accion_nuevo)
        menu_archivo.addSeparator()
        menu_archivo.addAction(accion_salir)

        menu_ayuda = self.menuBar().addMenu("&Ayuda")
        accion_acerca = QAction("Acerca de", self)
        accion_acerca.triggered.connect(self.acerca_de)
        menu_ayuda.addAction(accion_acerca)

    def _crear_barra_estado(self):
        self.statusBar().showMessage("Completa el formulario para registrarte")

    def registrar(self):
        error = self.formulario.validar()
        if error:
            self.formulario.lbl_error.setText(error)
            self.statusBar().showMessage("Registro con errores")
            return

        self.formulario.lbl_error.clear()
        datos = self.formulario.obtener_datos()

        confirmacion = DialogoConfirmacion(datos, self)
        if confirmacion.exec_() != QDialog.Accepted:
            self.statusBar().showMessage("Registro cancelado")
            return

        self.formulario.resumen.clear()
        for etiqueta, valor in datos:
            self.formulario.resumen.append(f"{etiqueta}: {valor}")

        self.statusBar().showMessage("Registro guardado correctamente")
        DialogoExito(self.formulario.txt_usuario.text(), self).exec_()

    def acerca_de(self):
        QMessageBox.information(
            self,
            "Acerca de",
            "ALAN - Registro R1\nInterfaz creada con PyQt5",
        )

    def _aplicar_tema(self):
        self.setStyleSheet(
            f"""
            QWidget#contenido {{ background-color: {GRIS_CLARO}; }}
            QLabel#titulo {{
                background-color: {VERDE};
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }}
            QLineEdit {{
                background-color: white;
                border: 1px solid {GRIS};
                border-radius: 6px;
                padding: 5px;
                color: #2c3e50;
            }}
            QLineEdit:focus {{ border: 2px solid {VERDE}; }}
            QTextEdit {{
                background-color: white;
                border: 1px solid {GRIS};
                border-radius: 6px;
                color: #2c3e50;
            }}
            QPushButton {{
                background-color: {VERDE_CLARO};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {VERDE}; }}
            QPushButton#borrar {{ background-color: #e74c3c; }}
            QPushButton#confirmar {{ background-color: {VERDE}; }}
            QComboBox {{
                background-color: white;
                border: 1px solid {GRIS};
                border-radius: 6px;
                padding: 4px;
                color: #2c3e50;
            }}
            QMenuBar {{ background-color: #d5dbdb; color: #2c3e50; }}
            QMenuBar::item:selected {{
                background-color: {VERDE};
                color: white;
            }}
            QMenu {{
                background-color: white;
                color: #2c3e50;
                border: 1px solid {GRIS};
            }}
            QMenu::item:selected {{
                background-color: {VERDE_CLARO};
                color: white;
            }}
            QStatusBar {{
                background-color: #d5dbdb;
                color: #2c3e50;
            }}
            QLabel {{ color: #2c3e50; background: transparent; }}
            QCheckBox {{ color: #2c3e50; background: transparent; }}
            QRadioButton {{ color: #2c3e50; background: transparent; }}
            """
        )

    def closeEvent(self, evento):
        respuesta = QMessageBox.question(
            self,
            "Salir",
            "Deseas salir del formulario de registro?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if respuesta == QMessageBox.Yes:
            evento.accept()
        else:
            evento.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    ventana = VentanaRegistro()
    ventana.show()
    sys.exit(app.exec_())
