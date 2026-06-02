import json

def add_account():
    accounts = {}
    site = input("Entrez le nom du site: ")
    id = input("Entrez votre identifiant: ")
    password = input("Entrez votre mot de passe: ")

    accounts[site] = {
        "id": id,
        "password": password
    }

    with open("accounts.json", "w") as file:
        json.dump(accounts, file)

def list_accounts():
    
def read_account():
    return()
add_account()