import numpy as np


class Forest:
    """
    Modèle de percolation (feu de forêt) sur une grille n×n.

    États :
      0 : vide
      1 : arbre (intact)
      2 : feu
      3 : brûlé
    """

    EMPTY = 0
    TREE = 1
    FIRE = 2
    BURNED = 3

    def __init__(self, n, density, neighbors=4, p_fire=1.0, rng=None):
        self.n = int(n)
        self.density = float(density)
        self.neighbors = int(neighbors)  # 4 ou 8
        self.p_fire = float(p_fire)

        self.rng = rng if rng is not None else np.random.default_rng()

        # Terrain figé (reproductible si seed fixe)
        self.initial_grid = (self.rng.random((self.n, self.n)) < self.density).astype(np.int8) * self.TREE
        self.grid = self.initial_grid.copy()

        self.iteration = 0

    def reset(self):
        """Remet la grille au terrain initial sans feu."""
        self.grid = self.initial_grid.copy()
        self.iteration = 0

    def ignite_at(self, i, j):
        """Allume le feu en (i,j) si c'est un arbre."""
        if 0 <= i < self.n and 0 <= j < self.n and self.grid[i, j] == self.TREE:
            self.grid[i, j] = self.FIRE
            return True
        return False

    def step(self):
        """
        Un pas d'évolution :
        - les cellules en feu deviennent brûlées
        - elles enflamment leurs voisins (4 ou 8) avec probabilité p_fire
        """
        burning = np.argwhere(self.grid == self.FIRE)
        if burning.size == 0:
            return False

        new_grid = self.grid.copy()

        if self.neighbors == 4:
            neigh = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        else:
            neigh = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for i, j in burning:
            new_grid[i, j] = self.BURNED
            for di, dj in neigh:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.n and 0 <= nj < self.n:
                    if self.grid[ni, nj] == self.TREE:
                        # propagation probabiliste
                        if self.rng.random() < self.p_fire:
                            new_grid[ni, nj] = self.FIRE

        self.grid = new_grid
        self.iteration += 1
        return True

    # ---------- métriques scientifiques ----------
    def percolates(self):
        """Coin bas-droit atteint (feu ou brûlé)."""
        return self.grid[self.n - 1, self.n - 1] in (self.FIRE, self.BURNED)

    def burned_count(self):
        return int(np.sum(self.grid == self.BURNED))

    def burned_fraction(self):
        return float(np.mean(self.grid == self.BURNED))

    def time_to_extinction(self):
        """
        Si la simulation est terminée : iteration.
        Sinon : valeur courante (utile pendant la simulation).
        """
        return int(self.iteration)

    def burned_frontier_count(self):
        """
        Frontière de l’amas brûlé :
        nombre de cellules brûlées qui sont adjacentes à au moins un arbre intact.
        (Version 4-voisins pour la frontière, lisible et stable.)
        """
        g = self.grid
        n = self.n
        burned = (g == self.BURNED)

        if not burned.any():
            return 0

        frontier = 0
        for i in range(n):
            for j in range(n):
                if not burned[i, j]:
                    continue
                # regarde si au moins un voisin (4) est un arbre intact
                for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < n and 0 <= nj < n and g[ni, nj] == self.TREE:
                        frontier += 1
                        break
        return frontier

    def snapshot_for_restart(self):
        """Renvoie une copie du terrain initial (pour restart propre)."""
        return self.initial_grid.copy()
