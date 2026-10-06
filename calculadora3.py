import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
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
VERDE_OSCURO = "#1e8449"
VERDE_CLARO = "#2ecc71"
GRIS_CLARO = "#ecf0f1"
GRIS = "#bdc3c7"


class DialogoPreferencias(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferencias")
        self.setFixedSize(320, 220)

        diseño = QVBoxLayout(self)

        formulario = QFormLayout()
        self.combo_tema = QComboBox()
        self.combo_tema.addItems(["Verde", "Verde oscuro", "Gris claro"])
        formulario.addRow("Tema:", self.combo_tema)

        self.chk_marca = QCheckBox("Mostrar marca de agua ALAN")
        self.chk_marca.setChecked(True)
        formulario.addRow(self.chk_marca)

        self.radio_grande = QRadioButton("Texto grande")
        self.radio_normal = QRadioButton("Texto normal")
        self.radio_normal.setChecked(True)
        formulario.addRow("Teclado:", self.radio_grande)
        formulario.addRow("", self.radio_normal)

        diseño.addLayout(formulario)

        cajas = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        cajas.accepted.connect(self.accept)
        cajas.rejected.connect(self.reject)
        diseño.addWidget(cajas)


class DialogoAcercaDe(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de")
        self.setFixedSize(300, 180)

        diseño = QVBoxLayout(self)

        titulo = QLabel("ALAN")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Arial", 28, QFont.Bold))
        titulo.setStyleSheet(f"color: {VERDE}; background: transparent;")
        diseño.addWidget(titulo)

        datos = QLabel("Calculadora creada con PyQt5\nVersion 1.0")
        datos.setAlignment(Qt.AlignCenter)
        datos.setStyleSheet("background: transparent;")
        diseño.addWidget(datos)

        boton = QDialogButtonBox(QDialogButtonBox.Ok)
        boton.accepted.connect(self.accept)
        diseño.addWidget(boton)


class Calculadora(QMainWindow):
    resultado_calculado = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALAN - Calculadora")
        self.setMinimumSize(460, 600)

        self.expresion = ""
        self.botones = []

        self._crear_interfaz()
        self._crear_acciones()
        self._crear_menus()
        self._crear_barra_estado()

        self.resultado_calculado.connect(self._agregar_al_historial)

        self._aplicar_tema()

    def _crear_interfaz(self):
        self.contenido = QWidget()
        self.contenido.setObjectName("contenido")
        self.contenido.setAttribute(Qt.WA_StyledBackground, True)
        self.setCentralWidget(self.contenido)

        principal = QVBoxLayout(self.contenido)
        principal.setContentsMargins(12, 12, 12, 12)
        principal.setSpacing(10)

        titulo = QLabel("ALAN")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        principal.addWidget(titulo)

        self.pantalla = QLineEdit()
        self.pantalla.setObjectName("pantalla")
        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignRight)
        self.pantalla.setPlaceholderText("0")
        principal.addWidget(self.pantalla)

        opciones = QHBoxLayout()

        grupo_izquierdo = QFormLayout()
        self.combo_operacion = QComboBox()
        self.combo_operacion.addItems(
            ["Suma (+)", "Resta (-)", "Multiplicacion (*)", "Division (/)"]
        )
        grupo_izquierdo.addRow("Operacion:", self.combo_operacion)
        self.chk_historial = QCheckBox("Guardar en historial")
        self.chk_historial.setChecked(True)
        grupo_izquierdo.addRow(self.chk_historial)
        opciones.addLayout(grupo_izquierdo)

        grupo_derecho = QFormLayout()
        self.radio_grados = QRadioButton("Grados")
        self.radio_radianes = QRadioButton("Radianes")
        self.radio_grados.setChecked(True)
        grupo_derecho.addRow("Angulos:", self.radio_grados)
        grupo_derecho.addRow("", self.radio_radianes)
        self.chk_memoria = QCheckBox("Acumular memoria")
        grupo_derecho.addRow(self.chk_memoria)
        opciones.addLayout(grupo_derecho)

        principal.addLayout(opciones)

        filas = [
            ["C", "←", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]

        teclado = QGridLayout()
        for fila, textos in enumerate(filas):
            columna = 0
            for texto in textos:
                boton = QPushButton(texto)
                boton.setFixedHeight(46)
                boton.clicked.connect(lambda _, t=texto: self.presionar(t))

                if texto in ("C", "←"):
                    boton.setObjectName("borrar")
                elif texto == "=":
                    boton.setObjectName("igual")

                self.botones.append(boton)
                if texto == "0":
                    teclado.addWidget(boton, fila, columna, 1, 2)
                    columna += 2
                else:
                    teclado.addWidget(boton, fila, columna)
                    columna += 1

        principal.addLayout(teclado)

        historial_layout = QHBoxLayout()
        historial_layout.addWidget(QLabel("Historial:"))
        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        self.historial.setFixedHeight(95)
        historial_layout.addWidget(self.historial)
        principal.addLayout(historial_layout)

        self.marca_agua = QLabel("ALAN", self.contenido)
        self.marca_agua.setFont(QFont("Arial", 110, QFont.Bold))
        self.marca_agua.setAlignment(Qt.AlignCenter)
        self.marca_agua.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.marca_agua.lower()

    def _crear_acciones(self):
        self.accion_nuevo = QAction("Nuevo", self)
        self.accion_nuevo.setShortcut(QKeySequence("Ctrl+N"))
        self.accion_nuevo.triggered.connect(self.limpiar_todo)

        self.accion_salir = QAction("Salir", self)
        self.accion_salir.setShortcut(QKeySequence("Ctrl+Q"))
        self.accion_salir.triggered.connect(self.close)

        self.accion_borrar = QAction("Borrar ultimo", self)
        self.accion_borrar.setShortcut(QKeySequence("Backspace"))
        self.accion_borrar.triggered.connect(lambda: self.presionar("←"))

        self.accion_copiar = QAction("Copiar resultado", self)
        self.accion_copiar.setShortcut(QKeySequence("Ctrl+C"))
        self.accion_copiar.triggered.connect(self.copiar_resultado)

        self.accion_preferencias = QAction("Preferencias...", self)
        self.accion_preferencias.triggered.connect(self.abrir_preferencias)

        self.accion_historial = QAction(
            "Mostrar historial", self, checkable=True, checked=True
        )
        self.accion_historial.toggled.connect(self.historial.setVisible)

        self.accion_marca = QAction(
            "Marca de agua", self, checkable=True, checked=True
        )
        self.accion_marca.toggled.connect(self.marca_agua.setVisible)

        self.accion_acerca = QAction("Acerca de ALAN", self)
        self.accion_acerca.triggered.connect(self.abrir_acerca_de)

    def _crear_menus(self):
        menu_archivo = self.menuBar().addMenu("&Archivo")
        menu_archivo.addAction(self.accion_nuevo)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accion_salir)

        menu_editar = self.menuBar().addMenu("&Editar")
        menu_editar.addAction(self.accion_borrar)
        menu_editar.addAction(self.accion_copiar)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accion_preferencias)

        menu_ver = self.menuBar().addMenu("&Ver")
        menu_ver.addAction(self.accion_historial)
        menu_ver.addAction(self.accion_marca)

        menu_ayuda = self.menuBar().addMenu("&Ayuda")
        menu_ayuda.addAction(self.accion_acerca)

    def _crear_barra_estado(self):
        self.statusBar().showMessage("Listo")

        self.reloj = QTimer(self)
        self.reloj.timeout.connect(self._actualizar_reloj)
        self.reloj.start(1000)
        self._actualizar_reloj()

        self.tiempo_mensaje = QTimer(self)
        self.tiempo_mensaje.setSingleShot(True)
        self.tiempo_mensaje.timeout.connect(self.statusBar().clearMessage)

    def _actualizar_reloj(self):
        from datetime import datetime

        self.statusBar().showMessage(
            datetime.now().strftime("%H:%M:%S")
        )

    def mostrar_mensaje(self, texto):
        self.statusBar().showMessage(texto)
        self.tiempo_mensaje.start(3000)

    def presionar(self, texto):
        if texto == "C":
            self.expresion = ""
        elif texto == "←":
            self.expresion = self.expresion[:-1]
        elif texto == "=":
            self.calcular()
            return
        elif texto == "%":
            self.expresion += "/100"
        else:
            self.expresion += texto

        self.pantalla.setText(self.expresion)
        self.mostrar_mensaje(f"Tecla {texto}")

    def calcular(self):
        if not self.expresion:
            return

        try:
            resultado = eval(self.expresion, {"__builtins__": {}}, {})
        except Exception:
            self.pantalla.setText("Error")
            self.expresion = ""
            self.mostrar_mensaje("Error en la expresion")
            return

        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)

        self.pantalla.setText(str(resultado))
        self.expresion = str(resultado)

        if self.chk_historial.isChecked():
            self.resultado_calculado.emit(
                f"{resultado}  [{self.combo_operacion.currentText()}]"
            )

        self.mostrar_mensaje("Resultado calculado")

    def _agregar_al_historial(self, texto):
        self.historial.append(texto)

    def limpiar_todo(self):
        self.expresion = ""
        self.pantalla.clear()
        self.historial.clear()
        self.mostrar_mensaje("Nueva calculadora")

    def copiar_resultado(self):
        QApplication.clipboard().setText(self.pantalla.text())
        self.mostrar_mensaje("Resultado copiado")

    def abrir_preferencias(self):
        dialogo = DialogoPreferencias(self)
        if dialogo.exec_() == QDialog.Accepted:
            self._aplicar_tema(dialogo.combo_tema.currentText())
            self.accion_marca.setChecked(dialogo.chk_marca.isChecked())
            tamaño = 16 if dialogo.radio_grande.isChecked() else 14
            for boton in self.botones:
                boton.setFont(QFont("Arial", tamaño, QFont.Bold))
            self.mostrar_mensaje("Preferencias aplicadas")

    def abrir_acerca_de(self):
        DialogoAcercaDe(self).exec_()

    def _aplicar_tema(self, tema="Verde"):
        if tema == "Verde oscuro":
            principal, claro = VERDE_OSCURO, VERDE
        elif tema == "Gris claro":
            principal, claro = GRIS, "#95a5a6"
        else:
            principal, claro = VERDE, VERDE_CLARO

        self.setStyleSheet(
            f"""
            QWidget#contenido {{ background-color: {GRIS_CLARO}; }}
            QLabel#titulo {{
                background-color: {principal};
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }}
            QLineEdit#pantalla {{
                background-color: white;
                color: #2c3e50;
                border: 2px solid {principal};
                border-radius: 8px;
                padding: 8px;
                font-size: 20px;
            }}
            QPushButton {{
                background-color: {claro};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {principal}; }}
            QPushButton#borrar {{ background-color: #e74c3c; }}
            QPushButton#igual {{ background-color: #16a085; }}
            QTextEdit {{
                background-color: white;
                border: 1px solid {GRIS};
                border-radius: 6px;
                color: #2c3e50;
            }}
            QMenuBar {{ background-color: #d5dbdb; color: #2c3e50; }}
            QMenuBar::item:selected {{
                background-color: {principal};
                color: white;
            }}
            QMenu {{
                background-color: white;
                color: #2c3e50;
                border: 1px solid {GRIS};
            }}
            QMenu::item:selected {{
                background-color: {claro};
                color: white;
            }}
            QStatusBar {{
                background-color: #d5dbdb;
                color: #2c3e50;
            }}
            QLabel {{ color: #2c3e50; background: transparent; }}
            QCheckBox {{ color: #2c3e50; background: transparent; }}
            QRadioButton {{ color: #2c3e50; background: transparent; }}
            QComboBox {{
                background-color: white;
                border: 1px solid {GRIS};
                border-radius: 6px;
                padding: 4px;
                color: #2c3e50;
            }}
            """
        )
        self.marca_agua.setStyleSheet(
            f"color: rgba(39, 174, 96, 30); background: transparent;"
        )

    def keyPressEvent(self, evento):
        teclas = {
            Qt.Key_0: "0", Qt.Key_1: "1", Qt.Key_2: "2",
            Qt.Key_3: "3", Qt.Key_4: "4", Qt.Key_5: "5",
            Qt.Key_6: "6", Qt.Key_7: "7", Qt.Key_8: "8",
            Qt.Key_9: "9", Qt.Key_Period: ".", Qt.Key_Comma: ".",
            Qt.Key_Plus: "+", Qt.Key_Minus: "-",
            Qt.Key_Asterisk: "*", Qt.Key_Slash: "/",
            Qt.Key_Percent: "%",
            Qt.Key_Return: "=", Qt.Key_Enter: "=",
            Qt.Key_Backspace: "←", Qt.Key_Escape: "C",
        }

        if evento.key() in teclas:
            self.presionar(teclas[evento.key()])
        else:
            super().keyPressEvent(evento)

    def resizeEvent(self, evento):
        self.marca_agua.setGeometry(self.contenido.rect())
        super().resizeEvent(evento)

    def closeEvent(self, evento):
        respuesta = QMessageBox.question(
            self,
            "Salir",
            "Deseas cerrar la calculadora ALAN?",
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
    ventana = Calculadora()
    ventana.show()
    sys.exit(app.exec_())
