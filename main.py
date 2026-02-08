import sys
import qrcode
import io
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QGroupBox, QCheckBox, QMessageBox,
    QFileDialog, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont, QImage, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer

class PerfectQRGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perfect Wi-Fi QR Generator")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        self.setup_ui()
        
        # Setup timer for real-time updates
        self.update_timer = QTimer()
        self.update_timer.setInterval(500)  # Update every 500ms
        self.update_timer.timeout.connect(self.generate_qr)
        self.update_timer.start()
        
        # Initialize with demo values
        self.ssid_input.setText("")
        self.security_combo.setCurrentIndex(0)
        
    def setup_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header = QLabel("Perfect Wi-Fi QR Generator")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2c3e50; padding: 15px 0;")
        main_layout.addWidget(header)
        
        # Description
        desc = QLabel("Create flawless QR codes for your Wi-Fi network")
        desc.setFont(QFont("Arial", 12))
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #7f8c8d; padding: 0 20px;")
        main_layout.addWidget(desc)
        
        # Main content layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Input section
        input_group = QGroupBox("Wi-Fi Configuration")
        input_group.setMinimumWidth(300)
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)
        
        # SSID
        ssid_layout = QVBoxLayout()
        ssid_label = QLabel("Network Name (SSID):")
        ssid_label.setFont(QFont("Arial", 10))
        self.ssid_input = QLineEdit()
        self.ssid_input.setFont(QFont("Arial", 10))
        self.ssid_input.setPlaceholderText("Enter your Wi-Fi network name")
        self.ssid_input.textChanged.connect(self.on_input_change)
        ssid_layout.addWidget(ssid_label)
        ssid_layout.addWidget(self.ssid_input)
        input_layout.addLayout(ssid_layout)
        
        # Password
        password_layout = QVBoxLayout()
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 10))
        self.password_input = QLineEdit()
        self.password_input.setFont(QFont("Arial", 10))
        self.password_input.setPlaceholderText("Enter your Wi-Fi password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.on_input_change)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        input_layout.addLayout(password_layout)
        
        # Security type
        security_layout = QVBoxLayout()
        security_label = QLabel("Security Type:")
        security_label.setFont(QFont("Arial", 10))
        self.security_combo = QComboBox()
        self.security_combo.setFont(QFont("Arial", 10))
        self.security_combo.addItems([
            "WPA/WPA2 (Recommended)",
            "WPA3",
            "WEP",
            "None (Open Network)"
        ])
        self.security_combo.currentIndexChanged.connect(self.on_input_change)
        security_layout.addWidget(security_label)
        security_layout.addWidget(self.security_combo)
        input_layout.addLayout(security_layout)
        
        # Hidden network
        self.hidden_checkbox = QCheckBox("This is a hidden network (not broadcasting SSID)")
        self.hidden_checkbox.setFont(QFont("Arial", 10))
        self.hidden_checkbox.stateChanged.connect(self.on_input_change)
        input_layout.addWidget(self.hidden_checkbox)
        
        input_group.setLayout(input_layout)
        content_layout.addWidget(input_group)
        
        # QR Preview section
        qr_group = QGroupBox("Perfect QR Preview")
        qr_group.setMinimumWidth(400)
        qr_layout = QVBoxLayout()
        qr_layout.setAlignment(Qt.AlignCenter)
        
        # QR Code display area
        self.qr_display = QLabel()
        self.qr_display.setAlignment(Qt.AlignCenter)
        self.qr_display.setMinimumSize(400, 400)
        self.qr_display.setStyleSheet("""
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
        """)
        self.qr_display.setText("QR code will appear here")
        self.qr_display.setFont(QFont("Arial", 12))
        self.qr_display.setStyleSheet("""
            color: #bdc3c7; 
            font-style: italic;
            font-size: 14px;
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
        """)
        
        qr_layout.addWidget(self.qr_display)
        qr_group.setLayout(qr_layout)
        content_layout.addWidget(qr_group)
        
        main_layout.addLayout(content_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(20)
        
        self.save_btn = QPushButton("Save QR Code")
        self.save_btn.setFont(QFont("Arial", 12))
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px 30px;
                font-weight: bold;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1d6fa5;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_qr)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        
    def on_input_change(self):
        # Visual feedback that input has changed
        self.qr_display.setStyleSheet("""
            background-color: white;
            border: 2px solid #3498db;
            border-radius: 10px;
        """)
        QTimer.singleShot(300, lambda: self.qr_display.setStyleSheet("""
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
        """))
        
    def generate_qr(self):
        # Get inputs
        ssid = self.ssid_input.text().strip()
        password = self.password_input.text().strip()
        security = self.security_combo.currentText()
        hidden = self.hidden_checkbox.isChecked()
        
        # Don't generate if SSID is empty
        if not ssid:
            self.qr_display.setText("Enter your Wi-Fi details to generate a QR code")
            self.qr_display.setStyleSheet("""
                color: #bdc3c7; 
                font-style: italic;
                font-size: 14px;
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            """)
            self.save_btn.setEnabled(False)
            return
        
        # Map security types
        security_map = {
            "WPA/WPA2 (Recommended)": "WPA",
            "WPA3": "WPA3",
            "WEP": "WEP",
            "None (Open Network)": "nopass"
        }
        security_value = security_map.get(security, "WPA")
        
        # Create Wi-Fi config string
        wifi_config = f"WIFI:T:{security_value};S:{ssid};"
        if security_value != "nopass":
            wifi_config += f"P:{password};"
        if hidden:
            wifi_config += "H:true;"
        wifi_config += ";"
        
        try:
            # Generate QR code with qrcode
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(wifi_config)
            qr.make(fit=True)
            
            # Create image in memory
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            
            # Create QPixmap from bytes
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes.read())
            
            # Scale to fit the display area
            scaled_pixmap = pixmap.scaled(
                380, 380, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            # Update display
            self.qr_display.setPixmap(scaled_pixmap)
            self.qr_display.setStyleSheet("""
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            """)
            self.save_btn.setEnabled(True)
            
            # Save image for later saving
            self.qr_image = img
            
        except Exception as e:
            # Handle errors gracefully
            error_msg = "Error generating QR code\n\n"
            error_msg += "Make sure you have Pillow installed:\n"
            error_msg += "pip install pillow\n\n"
            error_msg += f"Error details: {str(e)}"
            
            self.qr_display.setText(error_msg)
            self.qr_display.setStyleSheet("""
                color: #e74c3c; 
                font-weight: bold;
                font-size: 12px;
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            """)
            self.save_btn.setEnabled(False)
    
    def save_qr(self):
        if not hasattr(self, 'qr_image'):
            return
            
        # Get save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save QR Code",
            f"{self.ssid_input.text().strip()}_wifi_qr.png",
            "PNG Image (*.png)"
        )
        
        if file_path:
            try:
                # Create a high-resolution version for saving
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=20,
                    border=8,
                )
                qr.add_data(self.get_wifi_config())
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Save image
                img.save(file_path)
                
                # Show success message
                QMessageBox.information(
                    self,
                    "Success",
                    f"QR code saved successfully!\n\nFile saved to:\n{file_path}",
                    QMessageBox.Ok
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save QR code:\n{str(e)}",
                    QMessageBox.Ok
                )
    
    def get_wifi_config(self):
        """Generate the Wi-Fi configuration string"""
        ssid = self.ssid_input.text().strip()
        password = self.password_input.text().strip()
        security = self.security_combo.currentText()
        hidden = self.hidden_checkbox.isChecked()
        
        security_map = {
            "WPA/WPA2 (Recommended)": "WPA",
            "WPA3": "WPA3",
            "WEP": "WEP",
            "None (Open Network)": "nopass"
        }
        security_value = security_map.get(security, "WPA")
        
        wifi_config = f"WIFI:T:{security_value};S:{ssid};"
        if security_value != "nopass":
            wifi_config += f"P:{password};"
        if hidden:
            wifi_config += "H:true;"
        wifi_config += ";"
        
        return wifi_config

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create a clean palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(230, 230, 230))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = PerfectQRGenerator()
    window.show()
    sys.exit(app.exec_())
