import tkinter as tk
from tkinter import ttk

from model.forest import Forest
from controller.simulation import SimulationController


class FeuForetApp(tk.Tk):
    COULEUR = {0: "white", 1: "green", 2: "red", 3: "black"}

    def __init__(self):
        super().__init__()
        self.title("Percolation – Feu de forêt")
        self.resizable(False, False)

        self.size = 64
        self.canvas_px = 640
        self.cell_px = self.canvas_px // self.size

        self.forest = None
        self.controller = None
        self.after_id = None

        self._build_ui()
        self.reset()

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.grid(row=0, column=0)

        self.canvas = tk.Canvas(main, width=self.canvas_px, height=self.canvas_px, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10)

        panel = ttk.Frame(main)
        panel.grid(row=0, column=1, sticky="n")

        self.density = tk.DoubleVar(value=0.8)
        ttk.Label(panel, text="Densité").pack(anchor="w")
        ttk.Scale(panel, from_=0, to=1, variable=self.density).pack(fill="x")

        self.mode = tk.StringVar(value="coin")
        ttk.Radiobutton(panel, text="Coin", variable=self.mode, value="coin").pack(anchor="w")
        ttk.Radiobutton(panel, text="Centre", variable=self.mode, value="centre").pack(anchor="w")
        ttk.Radiobutton(panel, text="Ligne", variable=self.mode, value="ligne").pack(anchor="w")

        ttk.Button(panel, text="Start", command=self.start).pack(fill="x", pady=2)
        ttk.Button(panel, text="Pause", command=self.pause).pack(fill="x", pady=2)
        ttk.Button(panel, text="Reset", command=self.reset).pack(fill="x", pady=2)

        self.info = ttk.Label(panel, text="")
        self.info.pack(pady=10)

    def reset(self):
        self.pause()
        self.forest = Forest(self.size, self.density.get())
        self.forest.ignite(self.mode.get())
        self.controller = SimulationController(self.forest)
        self.draw()
        self.update_info()

    def start(self):
        self._loop()

    def pause(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def _loop(self):
        alive = self.controller.step()
        self.draw()
        self.update_info()
        if alive:
            self.after_id = self.after(80, self._loop)

    def draw(self):
        self.canvas.delete("all")
        g = self.forest.grid
        p = self.cell_px

        for i in range(self.size):
            for j in range(self.size):
                self.canvas.create_rectangle(
                    i * p, j * p, (i + 1) * p, (j + 1) * p,
                    fill=self.COULEUR[int(g[i, j])],
                    outline=""
                )

    def update_info(self):
        s = self.controller.stats()
        self.info.config(
            text=f"Itérations : {s['iteration']}\n"
                 f"% brûlé : {s['burned']:.1f}\n"
                 f"Bas-droite atteint : {'Oui' if s['reached'] else 'Non'}"
        )
