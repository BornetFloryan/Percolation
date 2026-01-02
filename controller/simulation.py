class SimulationController:
    """
    Contrôleur temps réel : Start / Pause / Restart
    Le modèle Forest contient l'état.
    """

    def __init__(self, forest):
        self.forest = forest

    def step(self):
        return self.forest.step()

    def metrics(self):
        return {
            "iteration": self.forest.iteration,
            "burned_count": self.forest.burned_count(),
            "burned_fraction": self.forest.burned_fraction(),
            "frontier": self.forest.burned_frontier_count(),
            "percolates": self.forest.percolates(),
        }
