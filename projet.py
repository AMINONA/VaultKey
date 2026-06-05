import json

def read_account():
    try:
        with open("accounts.json", "r") as file:
            accounts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        accounts = {}
        return("error",accounts)
    return("succes",accounts)

def add_account():
    site = input("Entrez le nom du site: ")
    identifiant = input("Entrez votre identifiant: ")
    password = input("Entrez votre mot de passe: ")

    accounts=read_account()[1]

    accounts[site] = {
        "id": identifiant,
        "password": password
    }

    with open("accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)
add_account()