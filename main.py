# -*- coding: utf-8 -*-
import numpy as np
from random import randint
from tkinter import *

class FeuForet(Frame):
    """ Code des couleurs :
         - 0 : sans arbre,
         - 1 : arbre,
         - 2 : arbre en feu,
         - 3 : arbre brûlé.
    """

    _couleur = {0: 'white', 1: 'green', 2: 'red', 3: 'black'}

    def __init__(self, taille=64, densite=0.6, temps=300):
        Frame.__init__(self)
        self.pack()

        self._n = taille
        self._foret = np.zeros((self._n, self._n), dtype=int)

        self._can = Canvas(self, bg='white', height=512, width=512)
        self._can.pack()

        nb_sites = int(densite * taille * taille)
        for _ in range(nb_sites):
            i = randint(0, self._n - 1)
            j = randint(0, self._n - 1)
            self._foret[i, j] = 1

        self.miseAFeu()

        for _ in range(temps):
            self.representeForet()
            self.miseAJour()

    def miseAFeu(self):
        if self._foret[0, 0] == 1:
            self._foret[0, 0] = 2

    def miseAJour(self):
        """Règle d'évolution de l'automate cellulaire.

        Si une cellule est en feu (2), alors :
            - elle communique le feu aux voisins (haut, bas, droite, gauche) qui sont des arbres (1),
            - elle devient brûlée (3).
        """
        matrice = np.zeros((self._n, self._n), dtype=int)

        for k in range(self._n):
            for l in range(self._n):
                if self._foret[k, l] == 2:
                    matrice[k, l] = 3
                    for (m, p) in ((k - 1, l), (k + 1, l), (k, l + 1), (k, l - 1)):
                        if m < 0 or m >= self._n or p < 0 or p >= self._n:
                            continue
                        if self._foret[m, p] == 1:
                            matrice[m, p] = 2
                else:
                    if matrice[k, l] == 0:
                        matrice[k, l] = self._foret[k, l]

        self._foret = matrice

    def representeForet(self):
        self._can.delete("all")
        pas = 512 / self._n

        for k in range(self._n):
            for l in range(self._n):
                etat = int(self._foret[k, l])
                couleur = self._couleur[etat]
                x0 = k * pas
                y0 = l * pas
                x1 = (k + 1) * pas
                y1 = (l + 1) * pas
                self._can.create_rectangle(x0, y0, x1, y1, fill=couleur, outline="")

        self.update()


if __name__ == "__main__":
    FeuForet(taille=64, densite=0.8, temps=300).mainloop()
