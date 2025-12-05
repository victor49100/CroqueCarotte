import random
import tkinter as tk

P1=[0,4,True]
P2=[0,4]

Cartes = ["av1_1","av1_2","av1_3","av1_4","av1_5","av1_6","av2_1","av2_2","av2_3","av2_4","av2_5","av2_6","av3_1","av3_2","av3_3","av3_4","av3_5","av3_6","Carotte_1","Carotte_2","Carotte_3","Carotte_4","Carotte_5","Carotte_6"]
CarteJouer=[]
traps = False



import tkinter as tk

def start_game():
    # Hide title and buttons
    title.pack_forget()
    start_btn.pack_forget()
    quit_btn.pack_forget()

    # Display the image
    global img  # keep a reference
    img = tk.PhotoImage(file="carotte.png")
    img_label = tk.Label(root, image=img, bg="#FFA500")
    img_label.pack(expand=True)

root = tk.Tk()
root.title("CROQUE CAROTTE")
root.geometry("1280x720")
root.config(bg="#FFA500")

# Title
title = tk.Label(root, text="My Game Menu", fg="white", bg="#FFA500", font=("Arial", 24))
title.pack(pady=30)

# Buttons
start_btn = tk.Button(root, text="Start Game", width=15, command=start_game)
start_btn.pack(pady=10)

quit_btn = tk.Button(root, text="Quit", width=15, command=root.quit)
quit_btn.pack(pady=10)

root.mainloop()


#troue position 6 13 20
def tirerCarte(Cartes):
    carte = random.choice(Cartes)
    Cartes.remove(carte)
    CarteJouer.append(carte)
    return carte


def activeEffect(P1,Carte):
    if (P1[2]==True):
        if ("av1_" in Carte):
            P1[0]=P1[0]+1
        if ("av2_" in Carte):
            P1[0]=P1[0]+2
        if ("av3_" in Carte):
            P1[0]=P1[0]+3
    if (P1[2]==false):
        if ("av1_" in Carte):
            P2[0]=P1[0]+1
        if ("av2_" in Carte):
            P2[0]=P1[0]+2
        if ("av3_" in Carte):
            P2[0]=P1[0]+3
    if ("Carotte_" in Carte):
            traps = not traps
    if (P1[0]==6 or P1[0]==13 or P1[0]==20 ):
        P1[0]=0
        P1[1]=P1[1]-1
    if (P2[0]==6 or P2[0]==13 or P2[0]==20 ):
        P2[0]=0
        P2[1]=P2[1]-1







