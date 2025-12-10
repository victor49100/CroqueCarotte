import random, time
import sys
from colorama import Fore, Style

P1 = [0, 4, True]
P2 = [0, 4]
numTour = 0
Speed = 0.05
Score = {'P1': 0, 'P2': 0}
Trap = False
CarteJouer = []
P1_Name = ""
P2_Name = ""
ModeInteractif = False

Cartes = ["av1_1","av1_2","av1_3","av1_4","av1_5","av1_6","av2_1","av2_2","av2_3","av2_4","av2_5","av2_6","av3_1","av3_2","av3_3","av3_4","av3_5","av3_6","Carotte_1","Carotte_2","Carotte_3","Carotte_4","Carotte_5","Carotte_6"]

def start():
    print("Debut du jeu")
    global P1_Name, P2_Name, Cartes
    
    setupMode()

    print("Nom du joueur 1 ? :")
    P1_Name = input()
    print("Nom du joueur 2 ? :")
    P2_Name = input()
    
    random.shuffle(Cartes)
    AffichePlateau(P1, P2, Trap)
    time.sleep(Speed)
    TourSuivant(Cartes)

def setupMode():
    global ModeInteractif
    print("Choisissez le mode de jeu :")
    print("1 - Automatique (Appuyez sur Entrée pour avancer)") 
    print("2 - Interactif (Vous choisissez les cartes)")
    ans = input("Votre choix (1 ou 2) ? : ").strip()
    while ans != '1' and ans != '2':
        ans = input("Choix invalide. Tapez 1 ou 2 : ").strip()
    
    if ans == '2':
        ModeInteractif = True
        print(f"{Fore.CYAN}Mode Interactif activé !{Style.RESET_ALL}")
    else:
        ModeInteractif = False
        print(f"{Fore.CYAN}Mode Auto activé.{Style.RESET_ALL}")
    time.sleep(0.5)

def restart(n1, n2, score):
    global P1_Name, P2_Name, P1, P2, numTour, Trap, CarteJouer, Cartes
    print("Debut du jeu")
    print(score)
    P1 = [0, 4, True]
    P2 = [0, 4]
    numTour = 0
    Trap = False
    CarteJouer = []
    Cartes = ["av1_1","av1_2","av1_3","av1_4","av1_5","av1_6","av2_1","av2_2","av2_3","av2_4","av2_5","av2_6","av3_1","av3_2","av3_3","av3_4","av3_5","av3_6","Carotte_1","Carotte_2","Carotte_3","Carotte_4","Carotte_5","Carotte_6"]
    random.shuffle(Cartes)
    P1_Name = n1
    P2_Name = n2
    AffichePlateau(P1, P2, Trap)
    time.sleep(Speed)
    TourSuivant(Cartes)

def retry():
    print("Relancer une partie | R | Quittez | Q | ?")
    answer = input().strip().upper()
    while answer != 'R' and answer != 'Q':
        answer = input().strip().upper()
    if answer == 'Q':
        print("Au revoir !")
        sys.exit(0)
    elif answer == 'R':
        restart(P1_Name, P2_Name, Score)

def TourSuivant(Cartes):
    global numTour
    numTour += 1
    if (P1[1] < 1): mort("p1")
    if (P2[1] < 1): mort("p2")
    
    if not ModeInteractif:
        input(f"{Style.DIM}Appuyez sur Entrée pour jouer le tour suivant...{Style.RESET_ALL}")
    else:
        time.sleep(Speed)

    TestPiege(P1, P2, Trap)
    
    if((P1[0] >= 25) or (P2[0] >= 25)):
        print("Fin")
        if (P1[0] >= 25):
            Score["P1"] += 1
            fin(str(P1_Name))
        else:
            Score["P2"] += 1
            fin(str(P2_Name))
    
    if (len(Cartes) == 0):
        Cartes = ["av1_1","av1_2","av1_3","av1_4","av1_5","av1_6","av2_1","av2_2","av2_3","av2_4","av2_5","av2_6","av3_1","av3_2","av3_3","av3_4","av3_5","av3_6","Carotte_1","Carotte_2","Carotte_3","Carotte_4","Carotte_5","Carotte_6"]
        random.shuffle(Cartes)

    joueur_actuel = P1_Name if P1[2] else P2_Name
    
    if P1[2] == True:
        # P1 joue
        c = tirerCarte(Cartes, joueur_actuel)
        activeEffect(P1, c, joueur_actuel)
        P1[2] = False
    else:
        # P2 joue
        c = tirerCarte(Cartes, joueur_actuel)
        activeEffect(P1, c, joueur_actuel)
        P1[2] = True

    AffichePlateau(P1, P2, Trap)
    TourSuivant(Cartes)

def SwitchTrap():
    global Trap

    if Trap == False:
        Trap = True
        print(f"{Fore.YELLOW}🚧 CRIC CRAC ! Les trous s'ouvrent ! 🚧{Style.RESET_ALL}")
        
        if P1[0] in (6, 13, 20):
            P1[0] = 0
            P1[1] -= 1
            print(f"{Fore.RED}😱 {P1_Name} tombe dans un trou !{Style.RESET_ALL}")
            
        if P2[0] in (6, 13, 20):
            P2[0] = 0
            P2[1] -= 1
            print(f"{Fore.BLUE}😱 {P2_Name} tombe dans un trou !{Style.RESET_ALL}")
    else:
        # Désactivation du piège
        Trap = False
        print(f"{Fore.GREEN}🛡️ OUF ! Les trous se referment.{Style.RESET_ALL}")

def tirerCarte(Cartes, nom_joueur):
    nb_cartes = len(Cartes)
    
    if ModeInteractif:
        print(f"\n{Fore.CYAN}--- C'est à {nom_joueur} de jouer ---{Style.RESET_ALL}")
        print(f"Choisissez une carte cachée (1 - {nb_cartes}) :")
        visuel = " ".join(["[?]" for _ in range(min(nb_cartes, 10))])
        if nb_cartes > 10: visuel += " ..."
        print(visuel)

        choix_valide = False
        index_choisi = 0
        while not choix_valide:
            try:
                user_input = input("Votre choix > ")
                index_choisi = int(user_input) - 1
                if 0 <= index_choisi < nb_cartes:
                    choix_valide = True
                else:
                    print(f"Erreur : Choisissez entre 1 et {nb_cartes}")
            except ValueError:
                print("Erreur : Nombre entier requis.")
        carte = Cartes.pop(index_choisi)
    else:
        carte = random.choice(Cartes)
        Cartes.remove(carte)
    
    CarteJouer.append(carte)
    return carte

def activeEffect(P1, Carte, nom_joueur):
    joueur_actif = P1 if P1[2] else P2
    
    texte_action = ""
    couleur_carte = ""
    icone = ""

    if "av1_" in Carte:
        couleur_carte = Fore.GREEN
        texte_action = "AVANCE DE 1 CASE"
        icone = "1️⃣"
        joueur_actif[0] += 1
    elif "av2_" in Carte:
        couleur_carte = Fore.BLUE
        texte_action = "AVANCE DE 2 CASES"
        icone = "2️⃣"
        joueur_actif[0] += 2
    elif "av3_" in Carte:
        couleur_carte = Fore.YELLOW
        texte_action = "AVANCE DE 3 CASES"
        icone = "3️⃣"
        joueur_actif[0] += 3
    elif "Carotte_" in Carte:
        couleur_carte = Fore.RED
        texte_action = "CLIC ! CAROTTE !"
        icone = "🥕"
        SwitchTrap()

    AfficherCarteEvent(nom_joueur, texte_action, couleur_carte, icone)

def AfficherCarteEvent(nom, action, couleur, icone):
    print("\n")
    bordure = couleur + "╔" + "═"*30 + "╗" + Style.RESET_ALL
    vide    = couleur + "║" + " "*30 + "║" + Style.RESET_ALL
    
    txt_nom = f"{nom} a pioché :"
    padding_nom = max(0, (30 - len(txt_nom)) // 2)
    ligne_nom = couleur + "║" + " "*padding_nom + txt_nom + " "*(30-len(txt_nom)-padding_nom) + "║" + Style.RESET_ALL
    
    # Simple centrage
    ligne_action = couleur + "║" + f"{action:^30}" + "║" + Style.RESET_ALL

    print(bordure)
    print(vide)
    print(ligne_nom)
    print(ligne_action)
    print(vide)
    print(couleur + "╚" + "═"*30 + "╝" + Style.RESET_ALL)
    print("\n")

def AffichePlateau(P1, P2, Trap):
    grille = [
        [1, 2, 3, 4, 5],
        [16, 17, 18, 19, 6],
        [15, 24, 25, 20, 7],
        [14, 23, 22, 21, 8],
        [13, 12, 11, 10, 9]
    ]
    cases_piegees = {6, 13, 20}
    
    print("-" * 35)
    for ligne in grille:
        ligne_str = ""
        for case in ligne:
            if case == 25: contenu = "🥕"
            else: contenu = f"{case:02d}"
            
            p1_ici = (P1[0] == case)
            p2_ici = (P2[0] == case)
            
            if p1_ici and p2_ici:
                contenu = Fore.RED + "P1" + Fore.BLUE + "P2" + Style.RESET_ALL
            elif p1_ici:
                contenu = Fore.RED + "P1" + Style.RESET_ALL
            elif p2_ici:
                contenu = Fore.BLUE + "P2" + Style.RESET_ALL
            else:
                if Trap and case in cases_piegees:
                    contenu = Fore.YELLOW + "💀" + Style.RESET_ALL
                elif case == 25:
                    contenu = "🥕"
                else:
                    contenu = Style.DIM + contenu + Style.RESET_ALL
            ligne_str += f" [{contenu}] "
        print(ligne_str)
    
    print("-" * 35)
    
    if P1[0] == 0:
        print(f"{Fore.RED}● {P1_Name}{Style.RESET_ALL} (Départ)")
    if P2[0] == 0:
        print(f"{Fore.BLUE}● {P2_Name}{Style.RESET_ALL} (Départ)")
        
    tour_nom = f"{Fore.RED}{P1_Name}{Style.RESET_ALL}" if P1[2] else f"{Fore.BLUE}{P2_Name}{Style.RESET_ALL}"
    
    print(f"\nTour n°: {numTour+1}")
    print(f"C'est au tour de : {tour_nom}")
    print(f"Pions restants -> {Fore.RED}{P1_Name}: {P1[1]}{Style.RESET_ALL} | {Fore.BLUE}{P2_Name}: {P2[1]}{Style.RESET_ALL}")
    print(f"Mode Piège : {'Actif 💀' if Trap else 'Inactif'}")
    print("-" * 35)

def fin(WIN):
    global numTour
    print(f"Partie terminée en {numTour} Tours")
    print(f"{WIN} a gagné")
    PrintScore(Score)
    retry()
    
def mort(p):
    if p == "p1":
        print(f"{P1_Name} est mort 💀, fin de partie {P2_Name} gagne")
        Score["P2"] += 1
        fin(str(P2_Name))
    else:
        print(f"{P2_Name} est mort 💀, fin de partie {P1_Name} gagne")
        Score["P1"] += 1
        fin(str(P1_Name))

def PrintScore(Score):
    print(f"Scores : {P1_Name}: {Score['P1']} | {P2_Name}: {Score['P2']}")

def TestPiege(P1, P2, Trap):
    if Trap == True:
        if P1[0] in (6, 13, 20): P1[0] = 0; P1[1] -= 1
        if P2[0] in (6, 13, 20): P2[0] = 0; P2[1] -= 1

start()