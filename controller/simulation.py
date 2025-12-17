class SimulationController:
    """
    Lien entre le modèle et l'interface
    """

    def __init__(self, forest):
        self.forest = forest

    def step(self):
        return self.forest.step()

    def stats(self):
        return {
            "iteration": self.forest.iteration,
            "burned": self.forest.burned_percentage(),
            "reached": self.forest.reached_bottom_right(),
        }
