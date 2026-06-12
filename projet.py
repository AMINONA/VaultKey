import json
from cryptography.fernet import Fernet
import sys
import os
import webview
import secrets
import string
import time
import shutil
import requests
import subprocess
from urllib.request import urlopen
import tkinter as tk
from tkinter import simpledialog
import hashlib

APP_DIR = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
VERSION = "1.3.0"

# ----- Definition des fonctions -----
def get_path(filename):
    data_dir = os.path.join(os.environ["APPDATA"], "VaultKey")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, filename)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_key():
    if not os.path.exists(get_path("key.key")):
        key = Fernet.generate_key()

        with open(get_path("key.key"), "wb") as file:
            file.write(key)

        return key

    with open(get_path("key.key"), "rb") as file:
        return file.read()

key=load_key()

def get_accounts():
    try:
        with open(get_path("accounts.json"), "r", encoding="utf-8") as file:
            accounts = json.load(file)
        return accounts
    except (FileNotFoundError, json.JSONDecodeError):
        accounts = {}
        return accounts

def add_account(site,identifiant,password):

    accounts=get_accounts()
    password_strength, password_len = password_stats(password)

    accounts[site] = {
        "id": identifiant,
        "password": encrypt_password(password,key),
        "password_strength": password_strength,
        "password_len": password_len,
        "date": time.strftime("%d/%m/%Y") + " à " + time.strftime("%H") + "h" + time.strftime("%M")
    }

    with open(get_path("accounts.json"), "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4, ensure_ascii=False)
    
    return "account added"

def password_stats(password):
    if len(password) < 8:
        return ("weak",len(password))

    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    for char in password:
        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        else:
            has_special = True

    if has_lower and has_upper and has_digit and has_special:
        return ("strong",len(password))
    elif has_lower and has_upper:
        return ("medium",len(password))
    else:
        return ("weak",len(password))

def encrypt_password(password, key):
    return (Fernet(key).encrypt(password.encode()).decode())

def decrypt_password(encrypted_password, key):
    return Fernet(key).decrypt(encrypted_password.encode()).decode()

def get_password (site):
    accounts = get_accounts()
    
    if site not in accounts:
        return None

    password = decrypt_password(accounts[site]["password"],key)
    return password

def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password="0"
    while password_stats(password)[0] != "strong":
        password = ''.join(secrets.choice(chars) for _ in range(20))
    return password

def delete_account(site):
    accounts = get_accounts()

    if site not in accounts:
        return "error: Account not found"
    
    del accounts[site]

    with open(get_path("accounts.json"),"w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4, ensure_ascii=False)
    
    return "Account deleted"

def update_account(site,identifiant,password):
    accounts=get_accounts()
    password_strength, password_len = password_stats(password)

    if site not in accounts:
        return "error: Account not found"

    accounts[site] = {
        "id": identifiant,
        "password": encrypt_password(password,key),
        "password_strength": password_strength,
        "password_len": password_len,
        "date": time.strftime("%d/%m/%Y") + " à " + time.strftime("%H") + "h" + time.strftime("%M")
    }

    with open(get_path("accounts.json"), "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4, ensure_ascii=False)
    
    return "account updated"

def delete_data():
    try:
        shutil.rmtree(
            os.path.join(os.environ["APPDATA"], "VaultKey"),
            ignore_errors=True
        )

        return "All data deleted"

    except Exception as e:
        return f"error: {e}"

def check_update():
    try:
        with urlopen(
            "https://api.github.com/repos/AMINONA/VaultKey/releases/latest"
        ) as response:
            data = json.load(response)

        latest_version = data["tag_name"].replace("v", "")

        if latest_version == VERSION:
            print("à jour")
            return False

        download_url = data["assets"][0]["browser_download_url"]

        r = requests.get(download_url)
        r.raise_for_status()

        with open(os.path.join(APP_DIR, "VaultKey_new.exe"), "wb") as file:
            file.write(r.content)

        return True

    except Exception as e:
        print("Erreur MAJ :", e)
        return False

def update_app():
    print("APP_DIR =", APP_DIR)

    bat_path = os.path.join(APP_DIR, "update.bat")

    print("BAT PATH =", bat_path)
    bat_path = os.path.join(APP_DIR, "update.bat")

    bat = f"""@echo off

        taskkill /f /im VaultKey.exe >nul 2>&1

        timeout /t 1 /nobreak >nul

        del /f /q "{APP_DIR}\\VaultKey.exe"

        ren "{APP_DIR}\\VaultKey_new.exe" VaultKey.exe

        cd /d "{APP_DIR}"

        explorer.exe "{APP_DIR}\\VaultKey.exe"
        del "%~f0"
    """
    
    with open(bat_path, "w", encoding="utf-8") as file:
        print("BAT créé :", os.path.exists(bat_path))
        file.write(bat)

    subprocess.Popen(
        ["cmd", "/k", bat_path],
        cwd=APP_DIR
    )

    os._exit(0)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def master_password_exists():
    return os.path.exists(get_path("master_password.txt"))

def set_master_password(password):
    with open(get_path("master_password.txt"), "w") as file:
        file.write(hash_password(password))

def verify_master_password(password):
    try:
        with open(get_path("master_password.txt"), "r") as file:
            saved_hash = file.read()

        return saved_hash == hash_password(password)

    except FileNotFoundError:
        return False

def ask_master_password():
    root = tk.Tk()
    root.withdraw()  # cache la fenêtre principale

    password = simpledialog.askstring(
        "VaultKey",
        "Entrez le mot de passe maître :",
        show="*"
    )

    root.destroy()
    return password

# ----- Fonctions exposés au JS -----
class Api:
    def get_accounts(self):
        return get_accounts()
    def get_password(self, site):
        return get_password(site)
    def generate_password(self):
        return generate_password()
    def add_account(self, site, identifiant, password):
        return add_account(site, identifiant, password)
    def password_stats(self,password):
        return password_stats(password)
    def delete_account(self,site):
        return delete_account(site)
    def update_account(self,site,identifiant,password):
        return update_account(site,identifiant,password)
    def delete_data(self):
        return delete_data()
    def update_app(self):
        return update_app()
    def check_update(self):
        return check_update()
    def get_version(self):
        return VERSION

# ----- Création et lancement de la fenêtre interface -----
window = webview.create_window(
    "Password Manager",
    resource_path("index.html"),
    js_api=Api()
)

check_update()

if not master_password_exists():
    password = ask_master_password()

    if password:
        set_master_password(password)
    else:
        sys.exit()

else:
    password = ask_master_password()

    if not verify_master_password(password):
        print("Mot de passe incorrect")
        sys.exit()

webview.start()