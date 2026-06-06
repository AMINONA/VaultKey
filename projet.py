import json
from cryptography.fernet import Fernet
import os

def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()

        with open("key.key", "wb") as file:
            file.write(key)

        return key

    with open("key.key", "rb") as file:
        return file.read()

key=load_key()

def read_account():
    try:
        with open("accounts.json", "r") as file:
            accounts = json.load(file)
        return("succes",accounts)
    except (FileNotFoundError, json.JSONDecodeError):
        accounts = {}
        return ("error",accounts)

def add_account():
    site = input("Entrez le nom du site: ")
    identifiant = input("Entrez votre identifiant: ")
    password = input("Entrez votre mot de passe: ")

    accounts=read_account()[1]
    password_strength, password_len = password_stats(password)

    accounts[site] = {
        "id": identifiant,
        "password": encrypt_password(password,key),
        "password_strength": password_strength,
        "password_len": password_len
        # AJOUTER DATE
    }

    with open("accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)

def password_stats(password):
    if len(password) < 8:
        return ("bad",len(password))

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
        return ("very strong",len(password))
    elif has_lower and has_upper:
        return ("strong",len(password))
    else:
        return ("bad",len(password))

def encrypt_password(password, key):
    return(Fernet(key).encrypt(password.encode()).decode())

def decrypt_password(encrypted_password, key):
    return Fernet(key).decrypt(encrypted_password.encode()).decode()

# ------ A FAIRE ------
def generate_password():
    return

add_account()