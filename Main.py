import random , time ,sys
from colorama import Fore, Style

P1=[0,4,True]
P2=[0,4]
numTour = 0
Speed = 0.5
Score = {'P1':0,'P2':0}
Trap = False
CarteJouer=[]
P1_Name = ""
P2_Name = ""
Cartes = ["av1_1","av1_2","av1_3","av1_4","av1_5","av1_6","av2_1","av2_2","av2_3","av2_4","av2_5","av2_6","av3_1","av3_2","av3_3","av3_4","av3_5","av3_6","Carotte_1","Carotte_2","Carotte_3","Carotte_4","Carotte_5","Carotte_6"]


def start():
    print("Debut du jeu")
    
    global P1_Name
    global P2_Name
    print("Nom du joueur 1 ? :")
    P1_Name = input()
    print("Nom du joueur 2 ? :")
    P2_Name = input()
    AffichePlateau(P1,P2,Trap)
    time.sleep(Speed)
    TourSuivant(Cartes)

def mode():
  pass  

def restart(n1, n2, score):
    global P1_Name, P2_Name, P1, P2, numTour, Trap, CarteJouer
    print("Debut du jeu")
    print(score)
    
    # Réinitialisation de la partie
    P1 = [0, 4, True]    
    P2 = [0, 4]        
    numTour = 0
    Trap = False
    CarteJouer = []
    Cartes = ["av1_1","av1_2","av1_3","av1_4","av1_5","av1_6","av2_1","av2_2","av2_3","av2_4","av2_5","av2_6","av3_1","av3_2","av3_3","av3_4","av3_5","av3_6","Carotte_1","Carotte_2","Carotte_3","Carotte_4","Carotte_5","Carotte_6"]
    P1_Name = n1
    P2_Name = n2
    AffichePlateau(P1, P2, Trap)
    time.sleep(Speed)
    TourSuivant(Cartes)

def retry():
    print("Relancer une partie | R | Quittez | Q | ?")
    answer = input().strip().upper()
    
    while answer != 'R' and answer != 'Q':  # ← Bonne logique
        print("Entrée invalide ! Relancer une partie | R | Quittez | Q | ?")
        answer = input().strip().upper()
    
    if answer == 'Q':
        print("Au revoir !")
        sys.exit(0)
    elif answer == 'R':
        restart(P1_Name, P2_Name, Score)

def TourSuivant(Cartes):
    global numTour
    numTour +=1
    #clear()
    if (P1[1]<1):
        mort("p1")
    if (P2[1]<1):
        mort("p2")
    time.sleep(Speed)
    TestPiege(P1,P2,Trap)
    if((P1[0]>=25)or(P2[0]>=25)):
        print ("Fin")
        if (P1[0]>=25):
            s = Score["P1"]
            #print(f"score : {s}")
            s = Score["P1"]
            Score["P1"] = s+1
            fin(str(P1_Name))
        else:
            s = Score["P2"]
            #print(f"score : {s}")
            Score["P2"] = s+1
            fin(str(P2_Name))

    # carte vide
    if (len(Cartes) == 0):
        Cartes = ["av1_1","av1_2","av1_3","av1_4","av1_5","av1_6","av2_1","av2_2","av2_3","av2_4","av2_5","av2_6","av3_1","av3_2","av3_3","av3_4","av3_5","av3_6","Carotte_1","Carotte_2","Carotte_3","Carotte_4","Carotte_5","Carotte_6"]

    if P1[2]==True:
        print(f"{P1_Name} Tire une carte")
        c = tirerCarte(Cartes)
        activeEffect(P1,c)
        P1[2] = False
        AffichePlateau(P1,P2,Trap)
        TourSuivant(Cartes)
    else :
        print("P2 Tire une carte")
        c = tirerCarte(Cartes)
        activeEffect(P1,c)
        P1[2] = True
        AffichePlateau(P1,P2,Trap)
        TourSuivant(Cartes)

def SwitchTrap():
    #piege 6 13 20
    global Trap
    if Trap == False:
        Trap = True
        if P1[0] in (6, 13, 20):
            P1[0]=0
            P1[1]-=1
        if P2[0] in (6, 13, 20):
            P2[0]=0
            P2[1]-=1
    else:
        Trap = False

def tirerCarte(Cartes):
    print(f"Carte Jouer : {len(CarteJouer)} \nCarte Restante {len(Cartes)}")
    carte = random.choice(Cartes)
    #print(f"carte tirer {carte}")
    Cartes.remove(carte)
    CarteJouer.append(carte)
    return carte

def AffichePlateau(P1, P2, Trap):
    grille = [
        [1, 2,  3,  4,  5],
        [16, 17, 18, 19, 6],
        [15, 24, 25, 20, 7],
        [14, 23, 22, 21, 8],
        [13, 12, 11, 10, 9]
    ]

    cases_piegees = {6, 13, 20}

    for ligne in grille:
        ligne_str = ""
        for case in ligne:
             
            if case == 25:
                contenu = "🥕"   
            else:
                contenu = f"{case:02d}"   

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

    print("")   
    print("-" * 35)

     
    if P1[0] == 0:
        print(f"{Fore.RED}● {P1_Name} (Rouge){Style.RESET_ALL} n'a pas encore commencé (Pos 0).")
    if P2[0] == 0:
        print(f"{Fore.BLUE}● {P2_Name} (Bleu){Style.RESET_ALL} n'a pas encore commencé (Pos 0).")

     
    tour = f"{Fore.RED}P1{Style.RESET_ALL}" if P1[2] else f"{Fore.BLUE}P2{Style.RESET_ALL}"
    print(f"\nTour numero: {numTour+1}")
    print(f"\nC'est au tour de : {tour}")
    print(f"Pions restants -> {Fore.RED}P1: {P1[1]}{Style.RESET_ALL} | {Fore.BLUE}P2: {P2[1]}{Style.RESET_ALL}")
    print(f"Mode Piège (Trap): {'Actif 💀' if Trap else 'Inactif'}")
    print("-" * 35)
 
def activeEffect(P1,Carte):
    if (P1[2]==True):
        if ("av1_" in Carte):
            print(Fore.GREEN+"Avance de 1"+Style.RESET_ALL)
            P1[0]=P1[0]+1
        if (("av2_" in Carte)):
            print(Fore.BLUE+"Avance de 2"+Style.RESET_ALL)
            P1[0]=P1[0]+2
        if (("av3_" in Carte)):
            print(Fore.YELLOW+"Avance de 3"+Style.RESET_ALL)
            P1[0]=P1[0]+3
        if ("Carotte_" in Carte):
            print(Fore.RED+"Tire Carotte"+Style.RESET_ALL)
            SwitchTrap()
            
    else:
        if ("av1_" in Carte):
            print(Fore.GREEN+"Avance de 1"+Style.RESET_ALL)
            P2[0]=P2[0]+1
        if (("av2_" in Carte)):
            print(Fore.BLUE+"Avance de 2"+Style.RESET_ALL)
            P2[0]=P2[0]+2
        if (("av3_" in Carte)):
            print(Fore.YELLOW+"Avance de 3"+Style.RESET_ALL)
            P2[0]=P2[0]+3
        if ("Carotte_" in Carte):
            print(Fore.RED+"Tire Carotte"+Style.RESET_ALL)
            SwitchTrap()

def fin(WIN):
    global numTour
    print (f"Partie terminer en {numTour} Tours")
    print(f"{WIN} à Gagne")
    PrintScore(Score)
    retry()

def mort(p):
    if p=="p1":
        print(f"{P1_Name} est mort 💀, fin de partie p2 gagne")
        s = Score["P2"]
        Score["P2"] = s+1
        fin(str(P2_Name))
        
    else:
        print(f"{P2_Name} est mort 💀, fin de partie p1 gagne")
        s = Score["P1"]
        Score["P1"] = s+1
        fin(str(P1_Name))

def PrintScore(Score):
    sp1 = Score["P1"]
    sp2 = Score["P2"]
    print (f"Voici les scores : {P1_Name} : {sp1} pts | {P2_Name} : {sp2} pts")


def TestPiege(P1,P2,Trap):
    if Trap == True:
        if P1[0] in (6, 13, 20):
            P1[0]=0
            P1[1]-=1
        if P2[0] in (6, 13, 20):
            P2[0]=0
            P2[1]-=1

#Debut du programme
start()

