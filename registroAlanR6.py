import sys
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog,
    QLabel, QPushButton, QLineEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QCheckBox, QRadioButton, QComboBox, QMessageBox,
    QAction
)

# ---------------------------------------------------------
# QDialog - Diálogo de Confirmación
# ---------------------------------------------------------
class DialogoConfirmacion(QDialog):
    def __init__(self, parent=None, resumen=""):
        super().__init__(parent)
        self.setWindowTitle("Confirmación de Datos")
        self.setFixedSize(380, 270)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #ffffff;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 13px;
            }
            QPushButton {
                background-color: #00ff66;
                color: #000000;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #22c55e;
                color: #ffffff;
            }
        """)

        layout = QVBoxLayout()
        lbl_info = QLabel("<b>Detalle del registro recibido:</b>")
        
        self.txt_detalle = QTextEdit()
        self.txt_detalle.setReadOnly(True)
        self.txt_detalle.setPlainText(resumen)
        self.txt_detalle.setStyleSheet("""
            background-color: rgba(2, 6, 23, 0.9);
            color: #00ff88;
            border: 1px solid #10b981;
            border-radius: 6px;
        """)

        btn_ok = QPushButton("Aceptar")
        btn_ok.clicked.connect(self.accept)

        layout.addWidget(lbl_info)
        layout.addWidget(self.txt_detalle)
        layout.addWidget(btn_ok)
        self.setLayout(layout)


# ---------------------------------------------------------
# QWidget Marca de Agua - Círculo y Texto Fosforescente Translúcido
# ---------------------------------------------------------
class WatermarkWidget(QWidget):
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() / 2
        cy = self.height() / 2

        # 1. Sombra suave posterior con transparencia
        pen_sombra = QPen(QColor(5, 46, 22, 45), 8)
        painter.setPen(pen_sombra)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(int(cx - 158), int(cy - 158), 320, 320)

        # 2. Círculo principal verde fosforescente translúcido
        pen_muyurina = QPen(QColor(0, 255, 128, 55), 5)
        painter.setPen(pen_muyurina)
        painter.drawEllipse(int(cx - 160), int(cy - 160), 320, 320)

        # 3. Círculo interno punteado tenue
        pen_ukhu = QPen(QColor(52, 211, 153, 40), 2, Qt.DashLine)
        painter.setPen(pen_ukhu)
        painter.drawEllipse(int(cx - 145), int(cy - 145), 290, 290)

        # 4. Texto ALANG fosforescente con transparencia balanceada
        font = QFont("Impact", 68)
        font.setBold(True)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 6)
        painter.setFont(font)

        # Sombra del texto semitransparente
        painter.setPen(QColor(2, 44, 34, 60))
        painter.drawText(int(cx - 160) + 3, int(cy - 160) + 3, 320, 320, Qt.AlignCenter, "ALANG")

        # Texto frontal verde neón brillante y translúcido
        painter.setPen(QColor(0, 255, 102, 65))
        painter.drawText(int(cx - 160), int(cy - 160), 320, 320, Qt.AlignCenter, "ALANG")


# ---------------------------------------------------------
# QMainWindow - Ventana Principal
# ---------------------------------------------------------
class FormularioRegistroCompleto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Registro - PyQt5 (ALANG)")
        self.resize(780, 840)

        # Widget central con marca de agua
        self.central_widget = WatermarkWidget(self)
        self.setCentralWidget(self.central_widget)

        # Estilo visual moderno y llamativo
        self.setStyleSheet("""
            QMainWindow {
                background-color: #050b0a;
            }
            QMenuBar {
                background-color: #0b1715;
                color: #e2e8f0;
                font-size: 13px;
                border-bottom: 2px solid #00ff88;
            }
            QMenuBar::item:selected {
                background-color: #00ff88;
                color: #000000;
                font-weight: bold;
            }
            QMenu {
                background-color: #0f201d;
                color: #ffffff;
                border: 1px solid #00ff88;
            }
            QMenu::item:selected {
                background-color: #10b981;
                color: #000000;
            }
            QLabel {
                color: #e2e8f0;
                font-weight: 600;
                font-size: 13px;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: rgba(10, 25, 22, 0.85);
                color: #ffffff;
                border: 1.5px solid #059669;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1.5px solid #00ff88;
                background-color: rgba(6, 38, 30, 0.95);
            }
            QCheckBox, QRadioButton {
                color: #e2e8f0;
                font-weight: 500;
                spacing: 8px;
            }
            QPushButton#btn_enviar {
                background-color: #00cc55;
                color: #000000;
                font-weight: 900;
                font-size: 14px;
                border-radius: 8px;
                padding: 11px 18px;
                border: 1px solid #00ff88;
            }
            QPushButton#btn_enviar:hover {
                background-color: #00ff66;
            }
            QPushButton#btn_limpiar {
                background-color: #1e293b;
                color: #ffffff;
                font-weight: bold;
                border-radius: 8px;
                padding: 11px 18px;
                border: 1px solid #475569;
            }
            QPushButton#btn_limpiar:hover {
                background-color: #334155;
            }
        """)

        self.crear_menus()
        self.inicializar_ui()
        self.iniciar_reloj()

    # -----------------------------------------------------
    # MENÚS (QMenuBar & QAction)
    # -----------------------------------------------------
    def crear_menus(self):
        barra_menu = self.menuBar()

        # 1. Menú Archivo
        menu_archivo = barra_menu.addMenu("&Archivo")

        accion_limpiar = QAction("Limpiar Formulario", self)
        accion_limpiar.setShortcut("Ctrl+L")
        accion_limpiar.triggered.connect(self.limpiar_formulario)
        menu_archivo.addAction(accion_limpiar)

        accion_salir = QAction("Salir", self)
        accion_salir.setShortcut("Ctrl+Q")
        accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(accion_salir)

        # 2. Menú Herramientas
        menu_herramientas = barra_menu.addMenu("&Herramientas")

        accion_validar = QAction("Verificar Datos Rápidos", self)
        accion_validar.setShortcut("Ctrl+V")
        accion_validar.triggered.connect(self.verificar_rapido)
        menu_herramientas.addAction(accion_validar)

        accion_reiniciar_reloj = QAction("Sincronizar Reloj", self)
        accion_reiniciar_reloj.triggered.connect(self.actualizar_reloj)
        menu_herramientas.addAction(accion_reiniciar_reloj)

        # 3. Menú Ayuda
        menu_ayuda = barra_menu.addMenu("&Ayuda")
        accion_acerca = QAction("Acerca de ALANG", self)
        accion_acerca.triggered.connect(self.mostrar_acerca_de)
        menu_ayuda.addAction(accion_acerca)

    # -----------------------------------------------------
    # FORMULARIO Y CONTROLES VISUALES
    # -----------------------------------------------------
    def inicializar_ui(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 20, 40, 25)
        layout_principal.setSpacing(14)

        # Encabezado y Reloj
        layout_header = QHBoxLayout()
        lbl_titulo = QLabel("SISTEMA DE REGISTRO")
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: 900; color: #00ff88;")

        self.lbl_reloj = QLabel("00:00:00")
        self.lbl_reloj.setStyleSheet("font-size: 13px; color: #6ee7b7; font-family: monospace; font-weight: bold;")

        layout_header.addWidget(lbl_titulo)
        layout_header.addStretch()
        layout_header.addWidget(self.lbl_reloj)
        layout_principal.addLayout(layout_header)

        # Campos de texto
        layout_form = QFormLayout()
        layout_form.setSpacing(10)

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingresa tu nombre de usuario...")

        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("correo@ejemplo.com")

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setPlaceholderText("••••••••")

        self.combo_pais = QComboBox()
        self.combo_pais.addItems(["Selecciona tu país...", "Bolivia", "Perú", "Argentina", "Chile", "México", "España"])

        layout_form.addRow("Usuario:", self.input_usuario)
        layout_form.addRow("Correo electrónico:", self.input_correo)
        layout_form.addRow("Contraseña:", self.input_password)
        layout_form.addRow("País:", self.combo_pais)
        layout_principal.addLayout(layout_form)

        # Opciones (Género y Términos)
        grid_opciones = QGridLayout()

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

        lbl_preferencias = QLabel("Preferencias:")
        self.chk_noticias = QCheckBox("Recibir noticias y novedades")
        self.chk_terminos = QCheckBox("Acepto los términos y condiciones")

        grid_opciones.addWidget(lbl_preferencias, 1, 0)
        grid_opciones.addWidget(self.chk_noticias, 1, 1)
        grid_opciones.addWidget(self.chk_terminos, 2, 1)

        layout_principal.addLayout(grid_opciones)

        # Biografía
        lbl_bio = QLabel("Descripción / Comentarios:")
        self.txt_biografia = QTextEdit()
        self.txt_biografia.setPlaceholderText("Escribe aquí información adicional o notas...")
        self.txt_biografia.setMaximumHeight(85)

        layout_principal.addWidget(lbl_bio)
        layout_principal.addWidget(self.txt_biografia)

        # Botones de acción
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
    # QTimer - Reloj en tiempo real
    # -----------------------------------------------------
    def iniciar_reloj(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_reloj)
        self.timer.start(1000)
        self.actualizar_reloj()

    def actualizar_reloj(self):
        hora = QTime.currentTime().toString("hh:mm:ss")
        self.lbl_reloj.setText(f"Hora: {hora}")

    # -----------------------------------------------------
    # Slots y Eventos
    # -----------------------------------------------------
    def verificar_rapido(self):
        usuario = self.input_usuario.text().strip()
        correo = self.input_correo.text().strip()
        if usuario and correo:
            QMessageBox.information(self, "Verificación", "Los campos principales están completos.")
        else:
            QMessageBox.warning(self, "Verificación", "Falta completar Usuario o Correo electrónico.")

    def procesar_registro(self):
        usuario = self.input_usuario.text().strip()
        correo = self.input_correo.text().strip()
        pais = self.combo_pais.currentText()

        if not usuario or not correo:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, ingresa tu usuario y correo electrónico.")
            return

        if not self.chk_terminos.isChecked():
            QMessageBox.warning(self, "Términos Obligatorios", "Debes aceptar los términos y condiciones para continuar.")
            return

        genero = "Masculino" if self.rb_masculino.isChecked() else ("Femenino" if self.rb_femenino.isChecked() else "Otro")
        suscripcion = "Sí" if self.chk_noticias.isChecked() else "No"
        notas = self.txt_biografia.toPlainText() or "Sin notas adicionales"

        resumen = (
            f"Usuario: {usuario}\n"
            f"Correo: {correo}\n"
            f"País: {pais}\n"
            f"Género: {genero}\n"
            f"Recibir novedades: {suscripcion}\n"
            f"Descripción: {notas}"
        )

        dialogo = DialogoConfirmacion(self, resumen)
        if dialogo.exec_() == QDialog.Accepted:
            self.limpiar_formulario()
            QMessageBox.information(self, "Éxito", "¡El registro se ha completado correctamente!")

    def limpiar_formulario(self):
        self.input_usuario.clear()
        self.input_correo.clear()
        self.input_password.clear()
        self.combo_pais.setCurrentIndex(0)
        self.rb_masculino.setChecked(True)
        self.chk_noticias.setChecked(False)
        self.chk_terminos.setChecked(False)
        self.txt_biografia.clear()

    def mostrar_acerca_de(self):
        QMessageBox.about(self, "ALANG Software", "Aplicación de Registro creada con PyQt5.\nMarca de agua con círculo fosforescente ALANG.")


# ---------------------------------------------------------
# QApplication - Punto de entrada
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FormularioRegistroCompleto()
    ventana.show()
    sys.exit(app.exec_())