import os
from termcolor import cprint
import pyqrcode

# Logging colorat
def log(msg: str, color: str = 'white'):
    cprint(msg, color)

# Afișează QR code în terminal
def show_qr(data: str):
    cprint('[*] Scanează QR-ul cu WhatsApp Web:', 'cyan')
    qr = pyqrcode.create(data)
    print(qr.terminal(quiet_zone=1))

# Salvare/încărcare date binare
def save_bin(path: str, data: bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)

def load_bin(path: str) -> bytes:
    return open(path, 'rb').read(import os
from termcolor import cprint

# Logging colorat
def log(msg: str, color: str = 'white'):
    cprint(msg, color)

# Afișează cod de asociere textual
def show_pairing_code(code: str):
    cprint('[*] Cod de asociere:', 'cyan')
    print(code)

# Salvare/încărcare date binare
def save_bin(path: str, data: bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)

def load_bin(path: str) -> bytes:
    return open(path, 'rb').read()
