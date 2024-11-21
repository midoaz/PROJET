import os
import pandas as pd
import numpy as np
import openpyxl
from tabulate import tabulate
import colorama
from colorama import Fore, Style
import sys

colorama.init(autoreset=True)

# Définition des informations de connexion
username_valid = "admin"
password_valid = "password"

# Fonction pour demander les informations de connexion
def ask_credentials():
    username = input("Entrez votre nom d'utilisateur : ")
    print("--------------------------------------")
    password = input("Entrez votre mot de passe : ")
    return username, password

# Fonction pour vérifier les informations de connexion
def check_credentials(username, password):
    return username == username_valid and password == password_valid

def Ajout():
    L = []
    while True:
        rep = input('Voulez-vous ajouter (O/N)?: ')
        if rep.lower() == 'o':
            id = input('ID       : ')
            df2 = pd.read_excel('stock1.xlsx')
            if id in df2['ID'].values:
                print(f"L'ID {id} existe déjà dans la base de données.")
            else:
                desig = input('DESIG    : ')
                pu = input('PU       : ')
                if pu == '':
                    pu = 0
                qtstq = input('QTSTQ    : ')
                if qtstq == '':
                    qtstq = 0
                d = {"ID": int(id),
                     "DESIG": desig,
                     "PU": float(pu),
                     "QTSTQ": int(qtstq),
                     }
                L.append(d)
        else:
            break
    df1 = pd.DataFrame(L, columns=['ID', 'DESIG', 'PU', 'QTSTQ'])
    df2 = pd.read_excel('stock1.xlsx')
    data = pd.concat([df2, df1])

    with pd.ExcelWriter("stock1.xlsx", mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        data.to_excel(writer, sheet_name="liste-stock", index=False)

    # Ajout de l'alerte de stock
    qt_min = 5  # quantité minimale pour déclencher l'alerte
    for index, row in data.iterrows():
        if row['QTSTQ'] <= qt_min:
            print(f"Alerte de stock : {row['DESIG']} - Quantité en stock : {row['QTSTQ']}")

    print(tabulate(data, headers='keys', tablefmt='pretty', showindex=False))
    input()

def Affichage():
    df0 = pd.read_excel('stock1.xlsx')
    print("Tableau des produits...........................")
    print(tabulate(df0, headers='keys', tablefmt='pretty', showindex=False))
    input()

def Recherche():
    df = pd.read_excel('stock1.xlsx')
    id = int(input("Entrer l'id   :  "))
    condition = df['ID'] == id
    if df[condition].any().any():
        df = df.query("ID == @id")
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
    else:
        print("Cet id n'existe pas......")
    input()

def Modification():
    df = pd.read_excel('stock1.xlsx')
    id = int(input("Entrer l'id  : "))
    df2 = df.query("ID == @id")
    print(tabulate(df2, headers='keys', tablefmt='pretty', showindex=False))
    if id != '':
        desigNv = input("Entrer nouvelle designation    :")
        puNv = input("Entrer nouveau prix unitaire      :")
        qtNv = input("Entrer nouvelle quantité          :")

        cond = df['ID'] == int(id)
        if desigNv != '':
            df['DESIG'] = np.where(cond, desigNv, df['DESIG'])
        if puNv != '':
            df['PU'] = np.where(cond, puNv, df['PU'])
        if qtNv != '':
            df['QTSTQ'] = np.where(cond, qtNv, df['QTSTQ'])
        with pd.ExcelWriter("stock1.xlsx", mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name="liste-stock", index=False)
        print("Modification effectuée...!")
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
        input()
    else:
        input("Entrer un id : ")

def Suppression():
    df = pd.read_excel('stock1.xlsx')
    id = int(input("Entrer l'id  : "))
    dfs = df.query("ID == @id")
    print(tabulate(dfs, headers='keys', tablefmt='pretty', showindex=False))

    rep = input('Voulez-vous supprimer (O/N)?: ')
    if rep.lower() == 'o':
        df = df.drop(df[df['ID'] == id].index)
        print("Suppression effectuée...!")
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
        with pd.ExcelWriter("stock1.xlsx", mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name="liste-stock", index=False)
    input()

def Menustock():
    choix = ''
    while choix != '0':
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f" {Style.NORMAL}{Fore.WHITE}*[1] Entrer 1 -> Ajout              | ")
        print(f" {Style.NORMAL}{Fore.WHITE}*[2] Entrer 2 -> Affichage          | ")
        print(f" {Style.NORMAL}{Fore.WHITE}*[3] Entrer 3 -> Recherche          | ")
        print(f" {Style.NORMAL}{Fore.WHITE}*[4] Entrer 4 -> Modification       | ")
        print(f" {Style.NORMAL}{Fore.WHITE}*[5] Entrer 5 -> Suppression        | ")
        print(f" {Style.NORMAL}{Fore.WHITE}*[0] Entrer 0 -> menu principal     | ")

        choix = input(f"{Style.NORMAL}{Fore.WHITE}      Entrer votre choix  :")

        if choix == '1':
            Ajout()
        elif choix == '2':
            Affichage()
        elif choix == '3':
            Recherche()
        elif choix == '4':
            Modification()
        elif choix == '5':
            Suppression()
        elif choix == '0':
            break
        else:
            print("choix invalide !")
            input()

def fournisseur():
    print("----------menu pour produit entré--------")
    print("-----------------------------------------------------")
    nom_fournisseur = input("Entrez le nom du Fournisseur : ")
    print(f"Bienvenue, {nom_fournisseur}!")

    df = pd.read_excel('stock1.xlsx')
    print("Tableau des produits disponibles...........................")
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

    id_livraison = int(input("Entrer l'ID du produit que vous souhaitez acheter : "))
    qt_livraison = int(input("Entrer la quantité que vous souhaitez acheter : "))

    condition = df['ID'] == id_livraison
    if df[condition].any().any():
        produit = df.loc[condition].iloc[0]
        qt_stock = produit['QTSTQ']
        df.loc[condition, 'QTSTQ'] += qt_livraison
        with pd.ExcelWriter("stock1.xlsx", mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name="liste-stock", index=False)
        print(f"Vous avez acheté {qt_livraison} unités de {produit['DESIG']}")
        print("Achat effectuée avec succès!")

        # Generate and display the invoice
        total_cost = qt_livraison * produit['PU']
        print("\n------------ Facture ------------")
        print(f"Nom du fournisseur  : {nom_fournisseur}")
        print(f"Produit Acheté      : {produit['DESIG']}")
        print(f"Quantité            : {qt_livraison}")
        print(f"Prix unitaire (PU)  : {produit['PU']}")
        print(f"Coût total          : {total_cost}")
        print("---------------------------------")
    else:
        print("Erreur : le produit n'existe pas dans le stock.")
    input()


def Achat():
    print("----------menu pour client d'achat de produit--------")
    print("-------------------- ---------------------------------")
    nom_client = input("Entrez nom CLIENT: ")
    print(f"Bienvenue, {nom_client}!")

    df = pd.read_excel('stock1.xlsx')
    print("Tableau des produits disponibles...........................")
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

    id_achat = int(input("Entrer l'ID du produit que vous souhaitez Livré : "))
    qt_achat = int(input("Entrer la quantité que vous souhaitez livré au client : "))

    condition = df['ID'] == id_achat
    if df[condition].any().any():
        produit = df.loc[condition].iloc[0]
        qt_stock = produit['QTSTQ']
        if qt_stock < 0:
            print("Erreur : stock invalide. La quantité en stock ne peut pas être négative.")
        elif qt_stock >= qt_achat:
            print(f"Vous avez livré {qt_achat} unités de {produit['DESIG']}")
            df.loc[condition, 'QTSTQ'] -= qt_achat
            with pd.ExcelWriter("stock1.xlsx", mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name="liste-stock", index=False)
            qt_stock -= qt_achat
            if qt_stock <= 20:
                print("Alerte de stock : la quantité en stock est inférieure à 20 unités.")
            print("Achat effectué avec succès!")

            # Generate and display the invoice
            total_cost = qt_achat * produit['PU']
            print("\n------------ Facture ------------")
            print(f"Nom du client       : {nom_client}")
            print(f"Produit vendue      : {produit['DESIG']}")
            print(f"Quantité            : {qt_achat}")
            print(f"Prix unitaire (PU)  : {produit['PU']}")
            print(f"Coût total          : {total_cost}")
            print("---------------------------------")
        else:
            print("Erreur : la quantité en stock est insuffisante.")
    else:
        print("Erreur : le produit n'existe pas dans le stock.")
    input()



def MenuPrincipal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n-----------------Menu principal-------------------------------")
        print("1-Gestion de stock :")
        print("2-Gestion des fournisseurs :")
        print("3-Gestion des clients :")
        print("4-Quitter :")
        try:
            choix = int(input(f"{Fore.WHITE}{Fore.CYAN}Entrer votre choix :{Fore.RESET} "))
            if choix in [1, 2, 3]:
                match choix:
                    case 1:
                        Menustock()
                    case 2:
                        fournisseur()
                    case 3:
                        Achat()
                    case 4:
                        exit()
            else:
                print("Votre choix doit être 1, 2 ou 3, veuillez réessayer.")
        except ValueError:
            print("Votre choix doit être un nombre entier, veuillez réessayer.")
            input("Appuyez sur Entrée pour continuer...")

# Programme principal
def main():
    print("\nBienvenue dans l'application My Stock!")
    print("--------------------------------------")

    while True:
        username, password = ask_credentials()
        if check_credentials(username, password):
            print("Connexion réussie!")
            MenuPrincipal()
            break
        else:
            print("Erreur de connexion. Veuillez réessayer.")

if __name__ == "__main__":
    main()
