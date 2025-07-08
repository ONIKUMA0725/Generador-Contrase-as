from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QFont, QColor, QPalette, QPainter, QBrush, QPen, QIcon
from PIL import Image, ImageQt
from PySide6.QtGui import QPixmap
import secrets
import string
import sys

# Lógica para generar contraseñas seguras (igual que tu función original)
def generar_contraseñas(cantidad, longitud):
    if longitud < 8:
        return None, "Lo siento, para que tu contraseña sea segura tiene que tener más de 8 caracteres."
    contraseñas = []
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    for _ in range(cantidad):
        while True:
            # Garantiza al menos un carácter de cada tipo
            password = [
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.digits),
                secrets.choice(string.punctuation)
            ]
            # Completa el resto de la contraseña
            password += [secrets.choice(alfabeto) for _ in range(longitud - 4)]
            # Baraja para evitar patrones
            secrets.SystemRandom().shuffle(password)
            contraseña = ''.join(password)
            # Validación extra (opcional, pero ya está garantizado)
            if (any(c.islower() for c in contraseña) and
                any(c.isupper() for c in contraseña) and
                any(c.isdigit() for c in contraseña) and
                any(c in string.punctuation for c in contraseña)):
                contraseñas.append(contraseña)
                break
    return contraseñas, None

# Botón personalizado con borde RGB animado
class RGBButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFont(QFont("Pixelify Sans Regular", 14))
        self.setStyleSheet("""
            QPushButton {
                background-color: #181818;
                color: #00FFD0;
                border-radius: 12px;
                border: 3px solid #FF00CC;
                padding: 10px 20px;
            }
        """)
        self._hue = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_border)
        self._timer.start(30)

    def _update_border(self):
        self._hue = (self._hue + 2) % 360
        color = QColor.fromHsv(self._hue, 255, 255)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #181818;
                color: #00FFD0;
                border-radius: 12px;
                border: 3px solid {color.name()};
                padding: 10px 20px;
            }}
        """)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Contraseñas == Onikuma0725 ❤")
        self.setFixedSize(500, 590)
        self.setStyleSheet("background-color: #181818;")
        self.setWindowIcon(QIcon("restablecer-la-contrasena.png"))

        # --- Fondo de pantalla adaptativo ---
        fondo = Image.open("wp4676582-4k-pc-wallpapers.jpg")  # Cambia por el nombre de tu imagen
        fondo = fondo.resize((self.width(), self.height()), Image.LANCZOS) # Redimensiona la imagen al tamaño de la ventana
        fondo_qt = ImageQt.ImageQt(fondo)
        self.fondo_pixmap = QPixmap.fromImage(fondo_qt)
        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(self.fondo_pixmap)
        self.fondo_label.setGeometry(0, 0, self.width(), self.height())
        self.fondo_label.lower()  # Manda el fondo detrás de los widgets
        # -----------------------------------

        # Título animado tipo pixel art
        self.titulo_texto = "  Echo x Onikuma0725 ❤      "
        self.titulo_label = QLabel(self.titulo_texto)
        self.titulo_label.setFont(QFont("Pixelify Sans Regular", 20, QFont.Weight.Bold))
        self.titulo_label.setStyleSheet("color: #FFF; background: transparent;")
        self.titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo_timer = QTimer(self)
        self.titulo_timer.timeout.connect(self.animar_titulo)
        self.titulo_timer.start(300)

        # Entradas y etiquetas
        self.cantidad_label = QLabel("Cantidad de contraseñas:")
        self.cantidad_label.setFont(QFont("Pixelify Sans Regular", 14))
        self.cantidad_label.setStyleSheet("color: #FFF; background: transparent;")
        self.cantidad_entry = QLineEdit()
        self.cantidad_entry.setFont(QFont("Pixelify Sans Regular", 13))
        self.cantidad_entry.setStyleSheet("""
            QLineEdit {
                background: rgba(34, 34, 34, 0.35);
                color: #FFF;
                border-radius: 14px;
                border: 2px solid #00FFD0;
                padding: 10px;
                font-size: 15px;
            }
            QLineEdit::placeholder {
                color: #Ff0000;  /* Cambia este color al que prefieras */
            }
        """)
        self.cantidad_entry.setPlaceholderText("Ejemplo: 5:")
        self.cantidad_entry.setFixedWidth(280)  # Personaliza el ancho aquí

        self.longitud_label = QLabel("Longitud de las contraseñas:")
        self.longitud_label.setFont(QFont("Pixelify Sans Regular", 14))
        self.longitud_label.setStyleSheet("color: #FFF; background: transparent;")
        self.longitud_entry = QLineEdit()
        self.longitud_entry.setFont(QFont("Pixelify Sans Regular", 13))
        self.longitud_entry.setStyleSheet("""
            QLineEdit {
                background: rgba(34, 34, 34, 0.35);
                color: #Ffffff; /* Cambia este color al que prefieras */
                border-radius: 14px;
                border: 2px solid #00FFD0;
                padding: 10px;
                font-size: 15px;
            }
            QLineEdit::placeholder {
                color: #FFF;  /* Cambia este color al que prefieras */
            }
        """)
        self.longitud_entry.setPlaceholderText("Ejemplo: +8")
        self.longitud_entry.setFixedWidth(280)  # Personaliza el ancho aquí

        # Botón generar con borde RGB animado
        self.generar_btn = RGBButton("Generar Contraseña(s)")
        self.generar_btn.clicked.connect(self.on_generar)
        self.generar_btn.setFixedWidth(240)  # Ajusta el ancho a tu gusto
        self.generar_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(34, 34, 34, 0.35);
                color: #00FFD0;
                border-radius: 18px;
                border: 3px solid #FF00CC;
                padding: 10px 20px;
                font-size: 15px;
            }
        """)

        # Centrar el botón usando un QHBoxLayout
        generar_layout = QHBoxLayout()
        generar_layout.addStretch()
        generar_layout.addWidget(self.generar_btn)
        generar_layout.addStretch()

        # Cuadro de texto para mostrar contraseñas
        self.output_text = QTextEdit()
        self.output_text.setFont(QFont("Pixelify Sans Regular", 13))
        self.output_text.setStyleSheet("""
            QTextEdit {
                background: rgba(34, 34, 34, 0.35);
                color: #00FFD0;
                border-radius: 18px;
                border: 2px solid #00FFD0;
                font-size: 15px;
                box-shadow: 0 4px 30px rgba(0,0,0,0.1);
            }
        """)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(140)

        # Botones copiar y guardar con borde RGB animado e iconos
        # Botón copiar solo con icono y forma circular
        self.copiar_btn = RGBButton("")
        self.copiar_btn.setIcon(QIcon("copia-de-escritura.png"))
        self.copiar_btn.setIconSize(QSize(40, 40))  # Tamaño más grande
        self.copiar_btn.setFixedSize(50, 50)  # Botón cuadrado para que el círculo sea perfecto
        self.copiar_btn.setStyleSheet("""
            QPushButton {
                background-color: #181818;
                border-radius: 25px;  /* La mitad de 50 */
                border: 3px solid #00FFD0;
                padding: 0px;
            }
        """)
        self.copiar_btn.clicked.connect(self.copiar_contraseña)
        self.copiar_btn.setToolTip("Copiar contraseña(s)")

        # Botón guardar solo con icono y forma circular
        self.guardar_btn = RGBButton("")
        self.guardar_btn.setIcon(QIcon("guardar-datos.png"))
        self.guardar_btn.setIconSize(QSize(40, 40))
        self.guardar_btn.setFixedSize(50, 50)
        self.guardar_btn.setStyleSheet("""
            QPushButton {
                background-color: #181818;
                border-radius: 25px;
                border: 3px solid #00FFD0;
                padding: 0px;
            }
        """)
        self.guardar_btn.clicked.connect(self.guardar_contraseña)
        self.guardar_btn.setToolTip("Guardar contraseña(s)")

        # Indicador de fortaleza
        self.fortaleza_label = QLabel("Fortaleza: ")
        self.fortaleza_label.setFont(QFont("Pixelify Sans Regular", 12))
        self.fortaleza_label.setStyleSheet("color: #FFF; background: transparent;")
        self.fortaleza_barra = QProgressBar()
        self.fortaleza_barra.setFixedHeight(18)
        self.fortaleza_barra.setRange(0, 100)
        self.fortaleza_barra.setValue(0)
        self.fortaleza_barra.setTextVisible(False)
        self.fortaleza_barra.setStyleSheet("""
            QProgressBar {
                border-radius: 8px;
                background: rgba(34,34,34,0.35);
                border: 2px solid #00FFD0;
            }
            QProgressBar::chunk {
                border-radius: 8px;
                background-color: #FF4B4B;
            }
        """)

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.titulo_label)
        layout.addSpacing(20)  # Más espacio debajo del título

        # Cantidad (título arriba y campo centrado)
        cantidad_vbox = QVBoxLayout()
        cantidad_vbox.addWidget(self.cantidad_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        cantidad_vbox.addWidget(self.cantidad_entry, alignment=Qt.AlignmentFlag.AlignHCenter)

        cantidad_layout = QHBoxLayout()
        cantidad_layout.addStretch()
        cantidad_layout.addLayout(cantidad_vbox)
        cantidad_layout.addStretch()
        layout.addLayout(cantidad_layout)
        layout.addSpacing(15)

        # Longitud (título arriba y campo centrado)
        longitud_vbox = QVBoxLayout()
        longitud_vbox.addWidget(self.longitud_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        longitud_vbox.addWidget(self.longitud_entry, alignment=Qt.AlignmentFlag.AlignHCenter)

        longitud_layout = QHBoxLayout()
        longitud_layout.addStretch()
        longitud_layout.addLayout(longitud_vbox)
        longitud_layout.addStretch()
        layout.addLayout(longitud_layout)
        layout.addSpacing(20)

        # Botón generar centrado
        generar_layout = QHBoxLayout()
        generar_layout.addStretch()
        generar_layout.addWidget(self.generar_btn)
        generar_layout.addStretch()
        layout.addLayout(generar_layout)
        layout.addSpacing(20)

        # Cuadro de texto
        layout.addWidget(self.output_text)
        layout.addSpacing(20)

        # Botones copiar y guardar centrados
        botones_layout = QHBoxLayout()
        botones_layout.addStretch()
        botones_layout.addWidget(self.copiar_btn)
        botones_layout.addSpacing(20)
        botones_layout.addWidget(self.guardar_btn)
        botones_layout.addStretch()
        layout.addLayout(botones_layout)
        layout.addStretch()

        # Indicador de fortaleza
        fortaleza_layout = QHBoxLayout()
        fortaleza_layout.addStretch()
        fortaleza_layout.addWidget(self.fortaleza_label)
        fortaleza_layout.addWidget(self.fortaleza_barra)
        fortaleza_layout.addStretch()
        layout.addLayout(fortaleza_layout)
        layout.addSpacing(10)

        self.setLayout(layout)

    def animar_titulo(self):
        self.titulo_texto = self.titulo_texto[1:] + self.titulo_texto[0]
        self.titulo_label.setText(self.titulo_texto)

    def on_generar(self):
        try:
            cantidad = int(self.cantidad_entry.text())
            longitud = int(self.longitud_entry.text())
        except ValueError:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Por favor, ingresa valores numéricos válidos.")
            msg.setStyleSheet("QLabel{color: white;} QMessageBox{background-color: #181818;}")
            msg.exec()
            return
        contraseñas, error = generar_contraseñas(cantidad, longitud)
        if error:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(error)
            msg.setStyleSheet("QLabel{color: white;} QMessageBox{background-color: #181818;}")
            msg.exec()
            return
        if contraseñas:
            self.output_text.setPlainText("\n".join(contraseñas))
            # Evalúa la fortaleza de la primera contraseña generada
            self.evaluar_fortaleza(contraseñas[0])

    def actualizar_fortaleza(self, longitud):
        # Ejemplo simple: la fortaleza es directamente proporcional a la longitud
        fortaleza = min(longitud * 10, 100)  # Máximo 100
        self.fortaleza_barra.setValue(fortaleza)

        # Cambiar color según la fortaleza
        if fortaleza < 40:
            color = "#FF4B4B"  # Rojo
        elif fortaleza < 70:
            color = "#FFCC00"  # Amarillo
        else:
            color = "#4BFF4B"  # Verde
        self.fortaleza_barra.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 8px;
                background: rgba(34,34,34,0.35);
                border: 2px solid #00FFD0;
            }}
            QProgressBar::chunk {{
                border-radius: 8px;
                background-color: {color};
            }}
        """)

    def evaluar_fortaleza(self, contraseña):
        longitud = len(contraseña)
        tiene_mayus = any(c.isupper() for c in contraseña)
        tiene_minus = any(c.islower() for c in contraseña)
        tiene_num = any(c.isdigit() for c in contraseña)
        tiene_simbolo = any(c in string.punctuation for c in contraseña)
        score = sum([tiene_mayus, tiene_minus, tiene_num, tiene_simbolo]) + (longitud >= 12) + (longitud >= 16)
        # Score máximo: 6
        if score <= 2:
            texto, valor, color = "Débil", 30, "#FF4B4B"
        elif score <= 4:
            texto, valor, color = "Media", 65, "#FFD700"
        else:
            texto, valor, color = "Fuerte", 100, "#00FF7F"
        self.fortaleza_label.setText(f"Fortaleza: {texto}")
        self.fortaleza_barra.setValue(valor)
        self.fortaleza_barra.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 8px;
                background: rgba(34,34,34,0.35);
                border: 2px solid #00FFD0;
            }}
            QProgressBar::chunk {{
                border-radius: 8px;
                background-color: {color};
            }}
        """)

    def copiar_contraseña(self):
        contraseñas = self.output_text.toPlainText().strip()
        if contraseñas:
            clipboard = QApplication.clipboard()
            clipboard.setText(contraseñas)
            QMessageBox.information(self, "Copiado", "Contraseña(s) copiada(s) al portapapeles.")

    def guardar_contraseña(self):
        contraseñas = self.output_text.toPlainText().strip()
        if contraseñas:
            from PySide6.QtWidgets import QFileDialog
            archivo, _ = QFileDialog.getSaveFileName(self, "Guardar contraseña", "mi_contraseña.txt", "Archivo de texto (*.txt);;PDF (*.pdf)")
            if archivo:
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write(contraseñas)
                QMessageBox.information(self, "Guardado", f"Contraseña(s) guardada(s) en {archivo}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())