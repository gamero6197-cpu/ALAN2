import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Calculadora(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALAN")
        self.setFixedSize(420, 560)

        self.expresion = ""
        self.memoria = 0.0

        self._crear_interfaz()

    def _crear_interfaz(self):
        principal = QVBoxLayout(self)

        titulo = QLabel("ALAN")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Arial", 24, QFont.Bold))
        titulo.setStyleSheet(
            "background-color: #2c3e50; color: white; padding: 12px;"
        )
        principal.addWidget(titulo)

        self.pantalla = QLineEdit()
        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignRight)
        self.pantalla.setFont(QFont("Arial", 20))
        self.pantalla.setStyleSheet(
            "border: 2px solid #7f8c8d; padding: 8px; background-color: #ecf0f1;"
        )
        principal.addWidget(self.pantalla)

        opciones = QHBoxLayout()

        grupo_base = QFormLayout()
        self.combo_operaciones = QComboBox()
        self.combo_operaciones.addItems(
            ["Suma (+)", "Resta (-)", "Multiplicacion (*)", "Division (/)"]
        )
        grupo_base.addRow(QLabel("Operacion:"), self.combo_operaciones)

        self.chk_historial = QCheckBox("Guardar en historial")
        self.chk_historial.setChecked(True)
        grupo_base.addRow(self.chk_historial)

        opciones.addLayout(grupo_base)

        grupo_unidad = QFormLayout()
        self.radio_grados = QRadioButton("Grados")
        self.radio_radianes = QRadioButton("Radianes")
        self.radio_grados.setChecked(True)
        grupo_unidad.addRow(QLabel("Angulos:"), self.radio_grados)
        grupo_unidad.addRow("", self.radio_radianes)

        self.chk_memoria = QCheckBox("Usar memoria")
        grupo_unidad.addRow(self.chk_memoria)

        opciones.addLayout(grupo_unidad)

        principal.addLayout(opciones)

        filas = [
            ["C", "←", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]

        grid = QGridLayout()
        for fila, textos in enumerate(filas):
            columna = 0
            for texto in textos:
                boton = QPushButton(texto)
                boton.setFont(QFont("Arial", 14, QFont.Bold))
                boton.setFixedHeight(45)
                boton.clicked.connect(lambda _, t=texto: self.presionar(t))

                if texto in ("C", "←"):
                    boton.setStyleSheet(
                        "background-color: #e74c3c; color: white; border: none;"
                    )
                elif texto == "=":
                    boton.setStyleSheet(
                        "background-color: #3498db; color: white; border: none;"
                    )
                else:
                    boton.setStyleSheet(
                        "background-color: #ecf0f1; border: none;"
                    )

                if texto == "0":
                    grid.addWidget(boton, fila, columna, 1, 2)
                    columna += 2
                else:
                    grid.addWidget(boton, fila, columna)
                    columna += 1

        principal.addLayout(grid)

        historial_layout = QHBoxLayout()
        historial_layout.addWidget(QLabel("Historial:"))
        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        self.historial.setFixedHeight(90)
        self.historial.setFont(QFont("Consolas", 10))
        self.historial.setStyleSheet(
            "border: 1px solid #7f8c8d; background-color: #fdfefe;"
        )
        historial_layout.addWidget(self.historial)
        principal.addLayout(historial_layout)

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

    def calcular(self):
        if not self.expresion:
            return

        try:
            resultado = eval(self.expresion, {"__builtins__": {}}, {})
        except Exception:
            self.pantalla.setText("Error")
            self.expresion = ""
            return

        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)

        if self.chk_memoria.isChecked():
            self.memoria += float(resultado)

        if self.chk_historial.isChecked():
            self.historial.append(f"{self.expresion} = {resultado}")

        self.pantalla.setText(str(resultado))
        self.expresion = str(resultado)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Calculadora()
    ventana.show()
    sys.exit(app.exec_())
