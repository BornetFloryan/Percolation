class SimulationController:
    """
    Fait le lien entre le modèle (Forest) et l'interface graphique
    """

    def __init__(self, forest):
        self.forest = forest
        self.running = False

    def step(self):
        return self.forest.step()

    def stats(self):
        return {
            "iteration": self.forest.iteration,
            "burned": self.forest.burned_percentage(),
            "reached": self.forest.reached_bottom_right(),
        }
