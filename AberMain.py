import random
import tkinter as tk

P1=[0,4,True]
P2=[0,4]

Cartes = ["av1_1","av1_2","av1_3","av1_4","av1_5","av1_6","av2_1","av2_2","av2_3","av2_4","av2_5","av2_6","av3_1","av3_2","av3_3","av3_4","av3_5","av3_6","Carotte_1","Carotte_2","Carotte_3","Carotte_4","Carotte_5","Carotte_6"]
CarteJouer=[]
traps = False






#troue position 6 13 20
def tirerCarte():
    global CarteJouer
    global Cartes
    if not Cartes:
        Cartes = ["av1_1","av1_2","av1_3","av1_4","av1_5","av1_6","av2_1","av2_2","av2_3","av2_4","av2_5","av2_6","av3_1","av3_2","av3_3","av3_4","av3_5","av3_6","Carotte_1","Carotte_2","Carotte_3","Carotte_4","Carotte_5","Carotte_6"]
        CarteJouer.clear()
    carte = random.choice(Cartes)
    Cartes.remove(carte)
    CarteJouer.append(carte)
    print(carte)
    return carte


def activeEffect(P1,Carte):
    global traps
    if (P1[2]==True):
        if ("av1_" in Carte):
            P1[0]=P1[0]+1
        if ("av2_" in Carte):
            P1[0]=P1[0]+2
        if ("av3_" in Carte):
            P1[0]=P1[0]+3
        if (P1[0]==P2[0]):
            P1[0]=P1[0]+1
    if (P1[2]==False):
        if ("av1_" in Carte):
            P2[0]=P2[0]+1
        if ("av2_" in Carte):
            P2[0]=P2[0]+2
        if ("av3_" in Carte):
            P2[0]=P2[0]+3
        if (P2[0]==P1[0]):
            P2[0]=P2[0]+1
    if ("Carotte" in Carte):
            traps = not  traps
    if (P1[0]==6 or P1[0]==13 or P1[0]==20 )and traps==True:
        P1[0]=0
        P1[1]=P1[1]-1
    if (P2[0]==6 or P2[0]==13 or P2[0]==20 )and traps==True:
        P2[0]=0
        P2[1]=P2[1]-1
    P1[2]=not P1[2]
    
while(1):
    input("Press Enter to draw and move")
    activeEffect(P1,tirerCarte())
    print(CarteJouer)
    print("Player1 HP:",P1[1]," Position ",P1[0])
    print("Player2 HP:",P2[1]," Position ",P2[0])
    if P1[2]==True :
        print("player1 turn")
    else:
        print("player2 turn")
    
    if P1[1]==0 or P2[0]==25:
        print("P2 Wins")
        break

    if P2[1]==0 or P1[0]==25:
        print("P1 Wins")
        break



