import numpy as np


class Forest:
    """
    Modèle mathématique de la forêt (automate cellulaire)
    États :
      0 : vide
      1 : arbre intact
      2 : arbre en feu
      3 : arbre brûlé
    """

    def __init__(self, n, density):
        self.n = n
        self.density = density
        self.grid = (np.random.random((n, n)) < density).astype(np.int8)
        self.iteration = 0

    def ignite(self, mode="coin"):
        if mode == "coin":
            if self.grid[0, 0] == 1:
                self.grid[0, 0] = 2

        elif mode == "centre":
            c = self.n // 2
            if self.grid[c, c] == 1:
                self.grid[c, c] = 2

        elif mode == "ligne":
            self.grid[0, self.grid[0, :] == 1] = 2

    def step(self):
        """
        Règle d'évolution :
        - un arbre en feu brûle
        - il enflamme ses voisins (haut, bas, gauche, droite)
        """
        n = self.n
        f = self.grid

        burning = (f == 2)
        if not burning.any():
            return False  # feu éteint

        intact = (f == 1)
        new_fire = np.zeros((n, n), dtype=bool)

        new_fire[:-1, :] |= burning[1:, :] & intact[:-1, :]
        new_fire[1:, :] |= burning[:-1, :] & intact[1:, :]
        new_fire[:, :-1] |= burning[:, 1:] & intact[:, :-1]
        new_fire[:, 1:] |= burning[:, :-1] & intact[:, 1:]

        f[burning] = 3
        f[new_fire] = 2

        self.iteration += 1
        return True

    def burned_percentage(self):
        return np.mean(self.grid == 3) * 100.0

    def reached_bottom_right(self):
        return self.grid[self.n - 1, self.n - 1] in (2, 3)
