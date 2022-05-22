import random
import secrets
import os

#/*
# *
# *
# * programme sans POO obligeant a utiliser des variables globales
# *
# *
# */

"""modeles de cartes"""
NUMERO_CARTES = {"0": "Zero", "1": "Un", "2": "Deux", "3": "Trois", "4": "Quatre", "5": "Cinq",\
                    "6": "Six", "7": "Sept", "8": "Huit", "9": "Neuf",\
                    "D": "Plus Deux", "I": "Changement de sens"}
COULEUR_CARTES = {"R": "Rouge", "B": "Bleu", "V": "Vert", "J": "Jaune"}
CARTE_BONUS = {"Q": "Plus Quatre", "JK": "Changement de couleur"}
"""liste contenant les cartes du jeu"""
JOUEURS = []
CARTE_JOUEES = []
TAS = []
"""changement de couleur"""
CHANGEMENT_COULEUR = [False, ""]
"""sens du jeu"""
SENS_HORRAIRE = True
"""joue"""
IS_PLAYING = False


def clear_console():
    """efface le contenu de la console"""

    #commandes differentes selon l'OS
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def creation_paquet():
    """créer le paquet de carte"""

    paquet = []
    for i in COULEUR_CARTES:
        for j, num in enumerate(NUMERO_CARTES):
            paquet.append(i + num)
            if j > 0:
                paquet.append(i + num)
        paquet.append("Q")
        paquet.append("JK")

    #melange la liste pour simplifier la suite
    random.shuffle(paquet)
    return paquet


def tirage_cartes_jeu_par_main():
    """tire aléatoirement 7 cartes pour chaque personne"""

    global TAS

    la_main = []
    for i in range(7):
        la_main.append(TAS[i])
        TAS.pop(i)

    return la_main


def tirage_cartes_tas(nombre):
    """tire aléatoirement un nombre carte du tas"""

    global TAS

    if len(TAS) <= 0:
        remplir_tas_vider_jeu()
    intr = []
    for i in range(nombre):
        intr.append(TAS[i])
        TAS.pop(i)
        
    return intr


def remplir_tas_vider_jeu():
    """supprimer les cartes deja jouées et les remet dans la pioche"""

    global TAS, CARTE_JOUEES

    #cree une nouvelle liste contenant
    # le contenu (*) des dexu autre
    TAS = [*TAS, *CARTE_JOUEES]
    CARTE_JOUEES = CARTE_JOUEES.pop()


def tirage_cartes_tas_debut():
    """tire aléatoirement la premiere carte du jeu"""

    global TAS

    carte = secrets.choice(TAS)
    if carte == "Q" or carte == "JK" or carte[1] == "I" or carte[1] == "D":
        carte = tirage_cartes_tas_debut()
    else:
        idx = TAS.index(carte)
        TAS.pop(idx)
        
    return carte


def list_to_string(lis):
    """converti une liste en chaine de caracteres"""

    result = ""
    for i, char in enumerate(lis):
        result += colore_carte(char) + (", " if i < len(lis)-1 else "")
        #ajout de retour a la ligne pour eviter les lignes trop longues
        if (i+1) % 7 == 0:
            result += "\n"
    return result


def generation_joueurs(nmb):
    """genere le paquet d'un joueur"""

    jeu = []
    for i in range(nmb):
        jeu.append(tirage_cartes_jeu_par_main())

    return jeu


def montrer_paquets(joueurs):
    """affiche le paquet des joueur en debut de partie"""
    input("\n\033[1;31m!!!\033[0;0m Montrer les paquets des joueurs \033[1;31m!!!\033[0;0m")
    for i in range(len(joueurs)):
        clear_console()
        print(f"\nJoueur {i+1} : {list_to_string(joueurs[i])}")
        input("\nVoir le joueur suivant (appuyer sur entrer) ")


def retirer_carte(carte):
    """retire une carte du tas"""

    global TAS

    idx = TAS.index(carte)
    TAS.pop(idx)


def choisir_carte(arg, derniere):
    """permet de choisir une carte dans le jeu d'un joueur et de la jouer"""

    print("Pour tirer un carte de la pioche tappez", "'\033[0;34mN\033[0;0m'")
    res = input("Choisi une carte à jouer : ").upper()

    if res == "N":
        arg.append(*tirage_cartes_tas(1))
        return arg, None
    #tant que la rep n'entre pas dans les criteres
    while not len(res) > 0 or res not in arg or not peut_jouer_carte(res, derniere):
        res = input("Tu ne peux pas jouer carte choisi bien : ").upper()
        if res == "N":
            arg.append(*tirage_cartes_tas(1))
            return arg, None

    idx = arg.index(res)
    arg.pop(idx)
    return arg, res


def peut_jouer_carte(arg, carte):
    """retourne si une carte peut etre jouee sur la precedente"""

    global CHANGEMENT_COULEUR

    auth = False
    #pylint n'autorise pas de mettre directement des return
    #donc ajout d'une variable intermediaire
    if arg == "":
        auth = False
    if CHANGEMENT_COULEUR[0] and arg[0] == CHANGEMENT_COULEUR[1]:
        CHANGEMENT_COULEUR[0] = False
        auth = True
    elif CHANGEMENT_COULEUR[0] and arg[0] != CHANGEMENT_COULEUR[1] and arg != "Q" and arg != "JK":
        auth = False
    elif arg == "Q" or arg == "JK" or arg[0] == carte[0] or arg[1] == carte[1]:
        auth = True

    return auth

def changer_de_couleur():
    """fait un changement de couleur"""

    global CARTE_JOUEES, CHANGEMENT_COULEUR

    res = input("Choisi une couleur (R, B, V, J) : ").upper()
    while res not in COULEUR_CARTES:
        res = input("Ce n'est pas un couleur disponible réessaye : ").upper()
    CHANGEMENT_COULEUR = [True, res]


def carte_a_effet(carte, idx):
    """applique les effects des cartes"""

    global SENS_HORRAIRE, JOUEURS

    # donne l'indice du joueur suivant selon le sens du jeu
    app_j = idx + 1 if SENS_HORRAIRE else -1
    if app_j >= len(JOUEURS)-1:
        app_j = 0
    elif app_j < 0:
        app_j = len(JOUEURS)

    if carte == "Q":
        JOUEURS[app_j] = [*JOUEURS[app_j], *tirage_cartes_tas(4)]
        changer_de_couleur()
    elif carte == "JK":
        changer_de_couleur()
    elif carte[1] == "I":
        SENS_HORRAIRE = not SENS_HORRAIRE
    elif carte[1] == "D":
        JOUEURS[app_j] = [*JOUEURS[app_j], *tirage_cartes_tas(2)]


def colore_carte(carte):
    """colore les caracteres selon la couleur qu'ils representent"""

    col_c = ""
    #pylint n'autorise pas de mettre directement des return
    #donc ajout d'une variable intermediaire
    if carte in ("Q", "JK"):
        col_c = "\033[0;35m" + nom_carte(carte) + f" ({carte})" + "\033[0;0m"
    elif carte[0] == "R":
        col_c = "\033[0;31m" + nom_carte(carte) + f" ({carte})" + "\033[0;0m"
    elif carte[0] == "B":
        col_c = "\033[0;34m" + nom_carte(carte) + f" ({carte})" + "\033[0;0m"
    elif carte[0] == "V":
        col_c = "\033[0;32m" + nom_carte(carte) + f" ({carte})" + "\033[0;0m"
    elif carte[0] == "J":
        col_c = "\033[0;33m" + nom_carte(carte) + f" ({carte})" + "\033[0;0m"

    return col_c


def nom_carte(carte):
    """retourne le nom d'une carte"""

    global CARTE_BONUS, NUMERO_CARTES, CHANGEMENT_COULEUR

    if carte in CARTE_BONUS:
        return CARTE_BONUS[carte]
    else:
        if len(carte) > 1:
            return NUMERO_CARTES[carte[1]] + " " + COULEUR_CARTES[carte[0]]
        # si seule la couleur est demandé
        return COULEUR_CARTES[carte[0]]


def jouer_carte(joueur):
    """demande quelle carte jouer"""

    global JOUEURS, CHANGEMENT_COULEUR, CARTE_JOUEES

    clear_console()
    #pylint n'autorise pas de tout metre sur une ligne
    # et oblige a complexifié
    if CHANGEMENT_COULEUR[0]:
        #si changement de couleur afficher la couleur a jouer
        chan_c = f"\033[0;0mCouleur à jouer : \033[0;0m{colore_carte(CHANGEMENT_COULEUR[1])}"
    else:
        chan_c = ""
    print("\033[0;36mDerniere carte jouée :", colore_carte(CARTE_JOUEES[-1]), chan_c)

    list_j = list_to_string(JOUEURS[joueur])
    paqt = (f"\nVoici ton paquet choisi quelle carte tu veux jouer : {list_j}")
    print(f"\n\033[0;33mJoueur {joueur+1}\033[0;0m à toi de jouer !\n", paqt, '\n')

    res = choisir_carte(JOUEURS[joueur], CARTE_JOUEES[-1])

    JOUEURS[joueur], n_carte_jouee = res
    #si le joueur a joué une carte l'ajouter aux cartes jouees
    # et la retirer de son paquet
    if n_carte_jouee is not None:
        CARTE_JOUEES.append(n_carte_jouee)
        carte_a_effet(n_carte_jouee, joueur)


def est_la_fin_jeu(arg):
    """regarde si le jeu est fini si oui arrete le jeu"""

    for i, j in enumerate(arg):
        if len(j) == 0:
            #un joueur a son paquet vide
            print(f"\n\n\033[0;31mJoueur {i} gagne la partie\n")
            return True
    return False


def main():
    """fonction principale initialize le jeu et lance la boucle de jeu"""

    global TAS, JOUEURS, SENS_HORRAIRE, CHANGEMENT_COULEUR, CARTE_JOUEES, IS_PLAYING

    TAS = creation_paquet()

    clear_console()
    lign1 = "\033[4;36mConsigne : Pour jouer une carte tappez son code (entre parentheses)"
    lign2 = "ou sur 'N' pour tirer une carte de la pioche"
    lign3 = "\n\033[0;0m"
    print(lign1, lign2, lign3)

    nb_joueurs = input("\033[0;32mCombien y a t il de joueur ? \033[0;0m")
    JOUEURS = generation_joueurs(int(nb_joueurs))
    montrer_paquets(JOUEURS)
    
    #variable de jeu
    IS_PLAYING = True
    tour_index = 0
    CARTE_JOUEES = [tirage_cartes_tas_debut()]

    #boucle de jeu
    while IS_PLAYING:
        if tour_index >= len(JOUEURS):
            tour_index = 0
        elif tour_index < 0:
            tour_index = len(JOUEURS)-1

        jouer_carte(tour_index)
        tour_index += 1 if SENS_HORRAIRE else -1

        if est_la_fin_jeu(JOUEURS):
            #verification de fin de jeu
            IS_PLAYING = False


"""lancement du jeu"""
main()