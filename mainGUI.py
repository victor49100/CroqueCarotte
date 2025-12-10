import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class CroqueCarotte(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Croque Carotte")
        self.geometry("600x700")
        self.resizable(False, False)

        # Variables globales
        self.P1 = [0, 4, True]
        self.P2 = [0, 4]
        self.numTour = 0
        self.Score = {'P1': 0, 'P2': 0}
        self.Trap = False
        self.CarteJouer = []
        self.P1_Name = ""
        self.P2_Name = ""
        self.ModeInteractif = False
        self.Cartes = [
            "av1_1", "av1_2", "av1_3", "av1_4", "av1_5", "av1_6",
            "av2_1", "av2_2", "av2_3", "av2_4", "av2_5", "av2_6",
            "av3_1", "av3_2", "av3_3", "av3_4", "av3_5", "av3_6",
            "Carotte_1", "Carotte_2", "Carotte_3", "Carotte_4", "Carotte_5", "Carotte_6"
        ]

        # Éléments UI
        self.board_labels = [[None] * 5 for _ in range(5)]
        self.status_labels = {}
        self.action_frame = None
        self.grille_pos = [
            [1, 2, 3, 4, 5],
            [16, 17, 18, 19, 6],
            [15, 24, 25, 20, 7],
            [14, 23, 22, 21, 8],
            [13, 12, 11, 10, 9]
        ]

        self.setup_ui()
        self.ask_setup()

    def setup_ui(self):
        # Frame scores en haut
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)
        tk.Label(top_frame, text="Scores", font=('Arial', 12, 'bold')).pack()
        self.status_labels['score'] = tk.Label(top_frame, text="", font=('Arial', 10))
        self.status_labels['score'].pack()

        # Frame plateau
        board_frame = tk.Frame(self)
        board_frame.pack(pady=20)
        for r in range(5):
            for c in range(5):
                lab = tk.Label(board_frame, text="", width=6, height=2, borderwidth=1, relief="solid", font=('Arial', 10, 'bold'))
                lab.grid(row=r, column=c, padx=1, pady=1)
                self.board_labels[r][c] = lab

        # Frame status
        status_frame = tk.Frame(self)
        status_frame.pack(pady=10)
        self.status_labels['tour'] = tk.Label(status_frame, text="", font=('Arial', 10, 'bold'))
        self.status_labels['tour'].pack()
        self.status_labels['tour_player'] = tk.Label(status_frame, text="", font=('Arial', 10))
        self.status_labels['tour_player'].pack()
        self.status_labels['pions'] = tk.Label(status_frame, text="", font=('Arial', 10))
        self.status_labels['pions'].pack()
        self.status_labels['piege'] = tk.Label(status_frame, text="", font=('Arial', 10))
        self.status_labels['piege'].pack()
        self.status_labels['start'] = tk.Label(status_frame, text="", fg='green', font=('Arial', 10))
        self.status_labels['start'].pack()

        # Frame actions
        self.action_frame = tk.Frame(self)
        self.action_frame.pack(pady=20, fill=tk.X)

    def ask_setup(self):
        # Choix mode
        mode = simpledialog.askinteger("Mode de jeu", "Choisissez le mode :\n1 - Automatique (bouton pour avancer)\n2 - Interactif (choix de carte)", minvalue=1, maxvalue=2)
        if mode is None:
            self.quit()
        self.ModeInteractif = (mode == 2)
        messagebox.showinfo("Mode", f"Mode {'Interactif activé !' if self.ModeInteractif else 'Automatique activé.'}")

        # Noms
        self.P1_Name = simpledialog.askstring("Nom Joueur 1", "Nom du joueur 1 ?") or "Joueur 1"
        self.P2_Name = simpledialog.askstring("Nom Joueur 2", "Nom du joueur 2 ?") or "Joueur 2"

        self.init_game()

    def init_game(self):
        random.shuffle(self.Cartes)
        self.P1 = [0, 4, True]
        self.P2 = [0, 4]
        self.numTour = 0
        self.Trap = False
        self.CarteJouer = []
        self.update_display()
        self.next_turn_setup()

    def next_turn_setup(self):
        self.numTour += 1
        if self.P1[1] < 1:
            self.mort("p1")
            return
        if self.P2[1] < 1:
            self.mort("p2")
            return

        self.TestPiege()

        if self.P1[0] >= 25 or self.P2[0] >= 25:
            self.fin_game()
            return

        if len(self.Cartes) == 0:
            self.Cartes = [
                "av1_1", "av1_2", "av1_3", "av1_4", "av1_5", "av1_6",
                "av2_1", "av2_2", "av2_3", "av2_4", "av2_5", "av2_6",
                "av3_1", "av3_2", "av3_3", "av3_4", "av3_5", "av3_6",
                "Carotte_1", "Carotte_2", "Carotte_3", "Carotte_4", "Carotte_5", "Carotte_6"
            ]
            random.shuffle(self.Cartes)

        # Nettoyer frame actions
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        joueur_actuel = self.P1_Name if self.P1[2] else self.P2_Name

        if self.ModeInteractif:
            # Boutons pour cartes
            tk.Label(self.action_frame, text=f"--- C'est à {joueur_actuel} de jouer --- Choisissez une carte (1 - {len(self.Cartes)}):", font=('Arial', 10, 'bold')).pack()
            for i in range(len(self.Cartes)):
                btn = tk.Button(self.action_frame, text=str(i + 1), width=4, height=1,
                                command=lambda idx=i: self.play_card(idx, joueur_actuel))
                btn.pack(side=tk.LEFT, padx=2)
        else:
            btn = tk.Button(self.action_frame, text="Tour Suivant", font=('Arial', 12, 'bold'),
                            command=lambda: self.play_random_card(joueur_actuel))
            btn.pack(pady=10)

        self.update_display()

    def play_card(self, index, nom):
        if 0 <= index < len(self.Cartes):
            carte = self.Cartes.pop(index)
            self.CarteJouer.append(carte)
            self.activeEffect(carte, nom)
            # Changer tour
            self.P1[2] = not self.P1[2]
            self.update_display()
            # Délai puis prochain tour
            self.after(1500, self.next_turn_setup)

    def play_random_card(self, nom):
        if self.Cartes:
            index = random.randint(0, len(self.Cartes) - 1)
            self.play_card(index, nom)

    def activeEffect(self, carte, nom):
        joueur_actif = self.P1 if self.P1[2] else self.P2
        texte_action = ""
        icone = ""

        if "av1_" in carte:
            texte_action = "AVANCE DE 1 CASE"
            icone = "1️⃣"
            joueur_actif[0] += 1
        elif "av2_" in carte:
            texte_action = "AVANCE DE 2 CASES"
            icone = "2️⃣"
            joueur_actif[0] += 2
        elif "av3_" in carte:
            texte_action = "AVANCE DE 3 CASES"
            icone = "3️⃣"
            joueur_actif[0] += 3
        elif "Carotte_" in carte:
            texte_action = "CLIC ! CAROTTE !"
            icone = "🥕"
            self.SwitchTrap()

        self.show_card_event(nom, texte_action, icone)

    def show_card_event(self, nom, action, icone):
        msg = f"{nom} a pioché :\n{action}\n{icone}"
        messagebox.showinfo("Carte Jouée", msg)

    def SwitchTrap(self):
        if not self.Trap:
            # Activation
            self.Trap = True
            messagebox.showwarning("Piège Activé", "🚧 CRIC CRAC ! Les trous s'ouvrent ! 🚧")
            cases_piegees = {6, 13, 20}
            if self.P1[0] in cases_piegees:
                self.P1[0] = 0
                self.P1[1] -= 1
                messagebox.showerror("Chute", f"😱 {self.P1_Name} tombe dans un trou !")
            if self.P2[0] in cases_piegees:
                self.P2[0] = 0
                self.P2[1] -= 1
                messagebox.showerror("Chute", f"😱 {self.P2_Name} tombe dans un trou !")
        else:
            # Désactivation
            self.Trap = False
            messagebox.showinfo("Piège Désactivé", "🛡️ OUF ! Les trous se referment.")

    def TestPiege(self):
        if self.Trap:
            cases_piegees = {6, 13, 20}
            if self.P1[0] in cases_piegees:
                self.P1[0] = 0
                self.P1[1] -= 1
            if self.P2[0] in cases_piegees:
                self.P2[0] = 0
                self.P2[1] -= 1

    def update_display(self):
        # Status
        self.status_labels['score'].config(text=f"Scores : {self.P1_Name}: {self.Score['P1']} | {self.P2_Name}: {self.Score['P2']}")
        self.status_labels['tour'].config(text=f"Tour n°: {self.numTour}")

        if self.P1[2]:
            color = 'red'
            tour_nom = self.P1_Name
        else:
            color = 'blue'
            tour_nom = self.P2_Name
        self.status_labels['tour_player'].config(text=f"C'est au tour de : {tour_nom}", fg=color)

        self.status_labels['pions'].config(text=f"Pions restants -> {self.P1_Name}: {self.P1[1]} | {self.P2_Name}: {self.P2[1]}")
        self.status_labels['piege'].config(text=f"Mode Piège : {'Actif 💀' if self.Trap else 'Inactif'}")

        # Départ
        start_text = ""
        if self.P1[0] == 0 and self.P2[0] == 0:
            start_text = f"● {self.P1_Name} et {self.P2_Name} (Départ)"
        elif self.P1[0] == 0:
            start_text = f"● {self.P1_Name} (Départ)"
        elif self.P2[0] == 0:
            start_text = f"● {self.P2_Name} (Départ)"
        self.status_labels['start'].config(text=start_text)

        # Plateau
        cases_piegees = {6, 13, 20}
        for r in range(5):
            for c in range(5):
                case = self.grille_pos[r][c]
                label = self.board_labels[r][c]
                p1_ici = (self.P1[0] == case)
                p2_ici = (self.P2[0] == case)

                if case == 25:
                    contenu = "🥕"
                    fg = 'orange'
                elif p1_ici and p2_ici:
                    contenu = "P1&P2"
                    fg = 'purple'
                elif p1_ici:
                    contenu = "P1"
                    fg = 'red'
                elif p2_ici:
                    contenu = "P2"
                    fg = 'blue'
                else:
                    if self.Trap and case in cases_piegees:
                        contenu = "💀"
                        fg = 'orange'
                    else:
                        contenu = f"{case:2d}"
                        fg = 'gray'

                label.config(text=contenu, fg=fg)

    def fin_game(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()
        winner = self.P1_Name if self.P1[0] >= 25 else self.P2_Name
        if winner == self.P1_Name:
            self.Score['P1'] += 1
        else:
            self.Score['P2'] += 1
        messagebox.showinfo("Fin de Partie", f"Partie terminée en {self.numTour} Tours\n{winner} a gagné")
        self.update_display()  # Met à jour le score

        # Boutons fin
        btn_restart = tk.Button(self.action_frame, text="Relancer (R)", font=('Arial', 12, 'bold'),
                                command=self.restart_game)
        btn_restart.pack(side=tk.LEFT, padx=20, pady=10)
        btn_quit = tk.Button(self.action_frame, text="Quitter (Q)", font=('Arial', 12, 'bold'),
                             command=self.quit)
        btn_quit.pack(side=tk.LEFT, pady=10)

    def mort(self, p):
        if p == "p1":
            messagebox.showinfo("Mort", f"{self.P1_Name} est mort 💀, fin de partie {self.P2_Name} gagne")
            self.Score['P2'] += 1
            winner = self.P2_Name
        else:
            messagebox.showinfo("Mort", f"{self.P2_Name} est mort 💀, fin de partie {self.P1_Name} gagne")
            self.Score['P1'] += 1
            winner = self.P1_Name
        self.show_end(winner)

    def show_end(self, winner):
        messagebox.showinfo("Fin de Partie", f"Partie terminée en {self.numTour} Tours\n{winner} a gagné")
        self.update_display()
        self.fin_game()  # Affiche les boutons

    def restart_game(self):
        self.init_game()

if __name__ == "__main__":
    app = CroqueCarotte()
    app.mainloop()