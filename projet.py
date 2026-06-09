import json
from cryptography.fernet import Fernet
import os
import webview
import secrets
import string

def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()

        with open("key.key", "wb") as file:
            file.write(key)

        return key

    with open("key.key", "rb") as file:
        return file.read()

key=load_key()

def get_accounts():
    try:
        with open("accounts.json", "r") as file:
            accounts = json.load(file)
        return(accounts)
    except (FileNotFoundError, json.JSONDecodeError):
        accounts = {}
        return(accounts)
    return(accounts)

def add_account(site,identifiant,password,date): # !!!! Attention ! Le password ne doit pas contenir de " !!!!!!!

    accounts=get_accounts()
    password_strength, password_len = password_stats(password)

    accounts[site] = {
        "id": identifiant,
        "password": encrypt_password(password,key),
        "password_strength": password_strength,
        "password_len": password_len,
        "date": date
    }

    with open("accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)
    
    return ("account added")

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
    return(Fernet(key).encrypt(password.encode()).decode())

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
    return ''.join(secrets.choice(chars) for _ in range(20))

# ------ A FAIRE ------
def delete_account():
    return

def update_account():
    return

class Api:
    def get_accounts(self):
        return get_accounts()
    def get_password(self, site):
        return get_password(site)
    def generate_password(self):
        return generate_password()
    def add_account(self, site, identifiant, password,date):
        return add_account(site, identifiant, password,date)
    def password_stats(self,password):
        return password_stats(password)
window = webview.create_window(
    "Password Manager",
    "page.html",
    js_api=Api()
)

webview.start()