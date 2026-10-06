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
        self.setWindowTitle("Confirmar registro R4")
        self.setFixedSize(400, 340)

        diseño = QVBoxLayout(self)

        aviso = QLabel("Confirma los datos de tu registro:")
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
        self.setWindowTitle("Registro R4 completado")
        self.setFixedSize(320, 180)

        diseño = QVBoxLayout(self)

        ok = QLabel("Registro AlanG completado")
        ok.setAlignment(Qt.AlignCenter)
        ok.setFont(QFont("Arial", 16, QFont.Bold))
        ok.setStyleSheet(f"color: {VERDE}; background: transparent;")
        diseño.addWidget(ok)

        detalle = QLabel(f"Bienvenido, {usuario}")
        detalle.setAlignment(Qt.AlignCenter)
        detalle.setStyleSheet("background: transparent;")
        diseño.addWidget(detalle)

        caja_texto = QTextEdit()
        caja_texto.setReadOnly(True)
        caja_texto.setFixedHeight(40)
        caja_texto.append("Tus datos fueron guardados correctamente.")
        diseño.addWidget(caja_texto)

        boton = QDialogButtonBox(QDialogButtonBox.Ok)
        boton.accepted.connect(self.accept)
        diseño.addWidget(boton)


class FormularioR4(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        diseño = QVBoxLayout(self)
        diseño.setContentsMargins(0, 0, 0, 0)

        encabezado = QLabel("Datos personales")
        encabezado.setFont(QFont("Arial", 11, QFont.Bold))
        encabezado.setStyleSheet(f"color: {VERDE}; background: transparent;")
        diseño.addWidget(encabezado)

        rejilla = QGridLayout()

        self.txt_nombre = QLineEdit()
        self.txt_apellido = QLineEdit()

        rejilla.addWidget(QLabel("Nombre:"), 0, 0)
        rejilla.addWidget(self.txt_nombre, 0, 1)
        rejilla.addWidget(QLabel("Apellido:"), 0, 2)
        rejilla.addWidget(self.txt_apellido, 0, 3)
        rejilla.setColumnStretch(1, 1)
        rejilla.setColumnStretch(3, 1)

        diseño.addLayout(rejilla)

        formulario = QFormLayout()
        self.txt_email = QLineEdit()
        self.txt_usuario = QLineEdit()
        self.txt_clave = QLineEdit()
        self.txt_clave.setEchoMode(QLineEdit.Password)
        self.txt_clave2 = QLineEdit()
        self.txt_clave2.setEchoMode(QLineEdit.Password)

        formulario.addRow("Correo:", self.txt_email)
        formulario.addRow("Usuario:", self.txt_usuario)
        formulario.addRow("Clave:", self.txt_clave)
        formulario.addRow("Repetir clave:", self.txt_clave2)
        diseño.addLayout(formulario)

        extras = QHBoxLayout()

        grupo_izquierdo = QFormLayout()
        self.combo_pais = QComboBox()
        self.combo_pais.addItems(
            ["Argentina", "Brasil", "Chile", "Paraguay", "Uruguay"]
        )
        grupo_izquierdo.addRow("Pais:", self.combo_pais)

        self.radio_femenino = QRadioButton("Femenino")
        self.radio_masculino = QRadioButton("Masculino")
        self.radio_masculino.setChecked(True)
        grupo_izquierdo.addRow("Genero:", self.radio_femenino)
        grupo_izquierdo.addRow("", self.radio_masculino)
        extras.addLayout(grupo_izquierdo)

        grupo_derecho = QVBoxLayout()
        self.chk_terminos = QCheckBox("Acepto los terminos y condiciones")
        self.chk_noticias = QCheckBox("Quiero recibir novedades")
        grupo_derecho.addWidget(self.chk_terminos)
        grupo_derecho.addWidget(self.chk_noticias)
        extras.addLayout(grupo_derecho)

        diseño.addLayout(extras)
        diseño.addStretch(1)

        diseño.addWidget(QLabel("Comentarios:"))
        self.txt_comentarios = QTextEdit()
        self.txt_comentarios.setPlaceholderText("Escribe aqui tus comentarios...")
        self.txt_comentarios.setFixedHeight(65)
        diseño.addWidget(self.txt_comentarios)

        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet(
            "color: #e74c3c; background: transparent; font-weight: bold;"
        )
        self.lbl_error.setWordWrap(True)
        diseño.addWidget(self.lbl_error)

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
            ("Terminos", "Aceptados" if self.chk_terminos.isChecked() else "No"),
            ("Novedades", "Si" if self.chk_noticias.isChecked() else "No"),
            ("Comentarios", self.txt_comentarios.toPlainText() or "(vacio)"),
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
        self.txt_comentarios.clear()
        self.chk_terminos.setChecked(False)
        self.chk_noticias.setChecked(False)
        self.lbl_error.clear()


class VentanaRegistroR4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALAN - Registro R4")
        self.setMinimumSize(540, 600)

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

        subtitulo = QLabel("Cuarto formulario de registro")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("color: #7f8c8d; background: transparent;")
        principal.addWidget(subtitulo)

        self.formulario = FormularioR4()
        principal.addWidget(self.formulario)

        self.marca_agua = QLabel("AlanG", self.contenido)
        self.marca_agua.setFont(QFont("Arial", 105, QFont.Bold))
        self.marca_agua.setAlignment(Qt.AlignCenter)
        self.marca_agua.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.marca_agua.setStyleSheet(
            "color: rgba(39, 174, 96, 28); background: transparent;"
        )
        self.marca_agua.lower()

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
        self.statusBar().showMessage("Completa el formulario R4")

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

        self.statusBar().showMessage("Registro guardado correctamente")
        DialogoExito(self.formulario.txt_usuario.text(), self).exec_()

    def acerca_de(self):
        QMessageBox.information(
            self,
            "Acerca de",
            "ALAN - Registro R4\nMarca de agua AlanG\nIncluye QCheckBox, QRadioButton y QComboBox",
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
            QCheckBox, QRadioButton {{ color: #2c3e50; background: transparent; }}
            """
        )

    def resizeEvent(self, evento):
        self.marca_agua.setGeometry(self.contenido.rect())
        super().resizeEvent(evento)

    def closeEvent(self, evento):
        respuesta = QMessageBox.question(
            self,
            "Salir",
            "Deseas salir del registro AlanG?",
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
    ventana = VentanaRegistroR4()
    ventana.show()
    sys.exit(app.exec_())