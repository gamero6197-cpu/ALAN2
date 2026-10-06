import sys
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog,
    QLabel, QPushButton, QLineEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QCheckBox, QRadioButton, QComboBox, QMessageBox
)

# ---------------------------------------------------------
# DIÁLOGO MODAL (QDialog)
# ---------------------------------------------------------
class DialogoConfirmacion(QDialog):
    def __init__(self, parent=None, resumen=""):
        super().__init__(parent)
        self.setWindowTitle("Confirmación de Datos")
        self.setFixedSize(360, 260)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e293b;
                color: #ffffff;
            }
            QLabel {
                color: #f8fafc;
                font-size: 13px;
            }
            QPushButton {
                background-color: #22c55e;
                color: #ffffff;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
        """)

        layout = QVBoxLayout()
        lbl_info = QLabel("<b>Detalle de la cuenta registrada:</b>")
        
        self.txt_detalle = QTextEdit()
        self.txt_detalle.setReadOnly(True)
        self.txt_detalle.setPlainText(resumen)
        self.txt_detalle.setStyleSheet("background-color: #0f172a; color: #4ade80; border: 1px solid #334155; border-radius: 6px;")

        btn_ok = QPushButton("Aceptar y Finalizar")
        btn_ok.clicked.connect(self.accept)

        layout.addWidget(lbl_info)
        layout.addWidget(self.txt_detalle)
        layout.addWidget(btn_ok)
        self.setLayout(layout)


# ---------------------------------------------------------
# WIDGET CON MARCA DE AGUA PERSONALIZADA (paintEvent)
# ---------------------------------------------------------
class WatermarkWidget(QWidget):
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Configuración de fuente estilizada para la marca de agua
        font = QFont("Arial Black", 85)
        font.setBold(True)
        painter.setFont(font)

        # Posicionamiento centrado e inclinado
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(-25)

        # 1. Sombra posterior (verde sombra oscura)
        painter.setPen(QColor(5, 46, 22, 90))
        painter.drawText(-295, 35, "ALANG")

        # 2. Texto frontal translúcido (verde esmeralda suave)
        painter.setPen(QColor(34, 197, 94, 50))
        painter.drawText(-300, 30, "ALANG")

        painter.restore()


# ---------------------------------------------------------
# VENTANA PRINCIPAL (QMainWindow)
# ---------------------------------------------------------
class FormularioRegistro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Registro - PyQt5")
        self.resize(750, 780)

        # Widget central con marca de agua incorporada
        self.central_widget = WatermarkWidget(self)
        self.setCentralWidget(self.central_widget)

        # Hoja de estilos moderna y llamativa
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0b1315;
            }
            QLabel {
                color: #e2e8f0;
                font-weight: 600;
                font-size: 13px;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: rgba(15, 23, 42, 0.85);
                color: #f8fafc;
                border: 1.5px solid #1e3a2f;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1.5px solid #22c55e;
                background-color: rgba(2, 44, 34, 0.85);
            }
            QCheckBox, QRadioButton {
                color: #cbd5e1;
                font-weight: 500;
                spacing: 8px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QPushButton#btn_enviar {
                background-color: #16a34a;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 10px 18px;
                border: 1px solid #22c55e;
            }
            QPushButton#btn_enviar:hover {
                background-color: #22c55e;
            }
            QPushButton#btn_limpiar {
                background-color: #334155;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 18px;
            }
            QPushButton#btn_limpiar:hover {
                background-color: #475569;
            }
        """)

        self.inicializar_ui()
        self.configurar_reloj()

    def inicializar_ui(self):
        # Layout raíz (QVBoxLayout)
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(35, 25, 35, 25)
        layout_principal.setSpacing(14)

        # Encabezado (QHBoxLayout)
        layout_header = QHBoxLayout()
        lbl_titulo = QLabel("FORMULARIO DE REGISTRO")
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: 900; color: #4ade80;")
        
        self.lbl_reloj = QLabel("00:00:00")
        self.lbl_reloj.setStyleSheet("font-size: 13px; color: #86efac; font-family: Consolas;")
        
        layout_header.addWidget(lbl_titulo)
        layout_header.addStretch()
        layout_header.addWidget(self.lbl_reloj)
        layout_principal.addLayout(layout_header)

        # Formulario de datos personales (QFormLayout)
        layout_form = QFormLayout()
        layout_form.setSpacing(10)

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ej. joaquin_dev")

        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("correo@ejemplo.com")

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setPlaceholderText("••••••••")

        self.combo_pais = QComboBox()
        self.combo_pais.addItems(["Selecciona tu país", "Bolivia", "Argentina", "Chile", "Perú", "México", "España"])

        layout_form.addRow("Usuario:", self.input_usuario)
        layout_form.addRow("Correo electrónico:", self.input_correo)
        layout_form.addRow("Contraseña:", self.input_password)
        layout_form.addRow("País:", self.combo_pais)
        layout_principal.addLayout(layout_form)

        # Distribución en cuadrícula para Género y Preferencias (QGridLayout)
        grid_opciones = QGridLayout()

        # Género (QRadioButton)
        lbl_genero = QLabel("Género:")
        self.rb_masculino = QRadioButton("Masculino")
        self.rb_femenino = QRadioButton("Femenino")
        self.rb_otro = QRadioButton("Otro")
        self.rb_masculino.setChecked(True)

        layout_radio = QHBoxLayout()
        layout_radio.addWidget(self.rb_masculino)
        layout_radio.addWidget(self.rb_femenino)
        layout_radio.addWidget(self.rb_otro)
        layout_radio.addStretch()

        grid_opciones.addWidget(lbl_genero, 0, 0)
        grid_opciones.addLayout(layout_radio, 0, 1)

        # Intereses (QCheckBox)
        lbl_preferencias = QLabel("Intereses:")
        self.chk_noticias = QCheckBox("Novedades y Noticias")
        self.chk_terminos = QCheckBox("Acepto los términos y condiciones")

        grid_opciones.addWidget(lbl_preferencias, 1, 0)
        grid_opciones.addWidget(self.chk_noticias, 1, 1)
        grid_opciones.addWidget(self.chk_terminos, 2, 1)

        layout_principal.addLayout(grid_opciones)

        # Biografía adicional (QTextEdit)
        lbl_bio = QLabel("Descripción / Comentarios:")
        self.txt_biografia = QTextEdit()
        self.txt_biografia.setPlaceholderText("Escribe una breve descripción personal o notas adicionales...")
        self.txt_biografia.setMaximumHeight(80)

        layout_principal.addWidget(lbl_bio)
        layout_principal.addWidget(self.txt_biografia)

        # Botones de Acción (QHBoxLayout + QPushButton)
        layout_botones = QHBoxLayout()
        self.btn_limpiar = QPushButton("Restablecer")
        self.btn_limpiar.setObjectName("btn_limpiar")
        self.btn_limpiar.setCursor(Qt.PointingHandCursor)

        self.btn_enviar = QPushButton("Completar Registro")
        self.btn_enviar.setObjectName("btn_enviar")
        self.btn_enviar.setCursor(Qt.PointingHandCursor)

        layout_botones.addWidget(self.btn_limpiar)
        layout_botones.addWidget(self.btn_enviar)
        layout_principal.addLayout(layout_botones)

        self.central_widget.setLayout(layout_principal)

        # Conectar Señales y Slots
        self.btn_enviar.clicked.connect(self.procesar_registro)
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)

    # -----------------------------------------------------
    # TEMPORIZADOR (QTimer)
    # -----------------------------------------------------
    def configurar_reloj(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_reloj)
        self.timer.start(1000)
        self.actualizar_reloj()

    def actualizar_reloj(self):
        hora_actual = QTime.currentTime().toString("hh:mm:ss")
        self.lbl_reloj.setText(f"Hora del servidor: {hora_actual}")

    # -----------------------------------------------------
    # SLOTS / CONTROLADORES DE EVENTOS
    # -----------------------------------------------------
    def procesar_registro(self):
        usuario = self.input_usuario.text().strip()
        correo = self.input_correo.text().strip()
        pais = self.combo_pais.currentText()

        # Validaciones
        if not usuario or not correo:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor ingresa usuario y correo electrónico.")
            return

        if not self.chk_terminos.isChecked():
            QMessageBox.warning(self, "Términos Obligatorios", "Debes aceptar los términos y condiciones para continuar.")
            return

        # Determinación de género seleccionado
        genero = "Masculino" if self.rb_masculino.isChecked() else ("Femenino" if self.rb_femenino.isChecked() else "Otro")
        suscripcion = "Sí" if self.chk_noticias.isChecked() else "No"
        notas = self.txt_biografia.toPlainText() or "Sin notas"

        resumen = (
            f"Usuario: {usuario}\n"
            f"Correo: {correo}\n"
            f"País: {pais}\n"
            f"Género: {genero}\n"
            f"Recibir novedades: {suscripcion}\n"
            f"Descripción: {notas}"
        )

        # Apertura de la ventana modal QDialog
        dialogo = DialogoConfirmacion(self, resumen)
        if dialogo.exec_() == QDialog.Accepted:
            self.limpiar_formulario()
            QMessageBox.information(self, "Éxito", "¡El usuario ha sido registrado correctamente!")

    def limpiar_formulario(self):
        self.input_usuario.clear()
        self.input_correo.clear()
        self.input_password.clear()
        self.combo_pais.setCurrentIndex(0)
        self.rb_masculino.setChecked(True)
        self.chk_noticias.setChecked(False)
        self.chk_terminos.setChecked(False)
        self.txt_biografia.clear()


# ---------------------------------------------------------
# PUNTO DE ENTRADA (QApplication)
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FormularioRegistro()
    ventana.show()
    sys.exit(app.exec_())