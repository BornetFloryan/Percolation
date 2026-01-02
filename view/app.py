import tkinter as tk
from tkinter import ttk

import numpy as np

from model.forest import Forest
from controller.simulation import SimulationController
from analysis.monte_carlo import monte_carlo, theta_curve


class FeuForetApp(tk.Tk):
    COLOR = {0: "white", 1: "green", 2: "red", 3: "black"}

    def __init__(self):
        super().__init__()
        self.title("Percolation – Feu de forêt (simulation + étude)")
        self.resizable(False, False)

        # simulation
        self.n = 32
        self.canvas_px = 384
        self.cell_px = self.canvas_px // self.n

        self.after_id = None
        self.running = False

        self.start_cell = None
        self.forest = None
        self.controller = None

        # terrain figé pour restart
        self._fixed_initial_grid = None

        self._build_ui()
        self._new_world()

    # ---------------- UI ----------------
    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.grid(row=0, column=0)

        # Left: simulation canvas
        left = ttk.Frame(main)
        left.grid(row=0, column=0, padx=(0, 10))

        self.canvas = tk.Canvas(left, width=self.canvas_px, height=self.canvas_px, bg="white")
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.sim_info = ttk.Label(left, text="", width=48, justify="left")
        self.sim_info.grid(row=1, column=0, pady=(8, 0), sticky="w")

        # Right: notebook (Study)
        right = ttk.Frame(main)
        right.grid(row=0, column=1)

        self.tabs = ttk.Notebook(right)
        self.tabs.grid(row=0, column=0, sticky="n")

        self.tab_params = ttk.Frame(self.tabs, padding=10)
        self.tab_study = ttk.Frame(self.tabs, padding=10)
        self.tabs.add(self.tab_params, text="Paramètres / Simulation")
        self.tabs.add(self.tab_study, text="Étude statistique")

        # ----- Params tab -----
        self.density = tk.DoubleVar(value=0.60)
        self.p_fire = tk.DoubleVar(value=1.00)
        self.neighbors = tk.IntVar(value=4)

        ttk.Label(self.tab_params, text="Densité d (arbres)").grid(row=0, column=0, sticky="w")
        ttk.Scale(self.tab_params, from_=0.1, to=0.95, variable=self.density,
                  command=lambda _=None: self._new_world()).grid(row=1, column=0, sticky="we")

        ttk.Label(self.tab_params, text="Probabilité de propagation p_fire").grid(row=2, column=0, sticky="w", pady=(10, 0))
        ttk.Scale(self.tab_params, from_=0.1, to=1.0, variable=self.p_fire,
                  command=lambda _=None: self._new_world()).grid(row=3, column=0, sticky="we")

        ttk.Label(self.tab_params, text="Voisinage").grid(row=4, column=0, sticky="w", pady=(10, 0))
        r = ttk.Frame(self.tab_params)
        r.grid(row=5, column=0, sticky="w")
        ttk.Radiobutton(r, text="4 voisins", variable=self.neighbors, value=4, command=self._new_world).grid(row=0, column=0, padx=(0, 10))
        ttk.Radiobutton(r, text="8 voisins", variable=self.neighbors, value=8, command=self._new_world).grid(row=0, column=1)

        # Seed controls
        ttk.Label(self.tab_params, text="Reproductibilité").grid(row=6, column=0, sticky="w", pady=(10, 0))
        seed_box = ttk.Frame(self.tab_params)
        seed_box.grid(row=7, column=0, sticky="w")

        self.seed_fixed = tk.BooleanVar(value=False)
        ttk.Checkbutton(seed_box, text="Seed fixe", variable=self.seed_fixed, command=self._new_world).grid(row=0, column=0, padx=(0, 10))

        self.seed_value = tk.StringVar(value="1234")
        ttk.Label(seed_box, text="Seed :").grid(row=0, column=1)
        e = ttk.Entry(seed_box, textvariable=self.seed_value, width=8)
        e.grid(row=0, column=2, padx=(5, 0))
        e.bind("<Return>", lambda _=None: self._new_world())

        # Controls
        ctrl = ttk.Frame(self.tab_params)
        ctrl.grid(row=8, column=0, sticky="w", pady=(12, 0))
        self.btn_start = ttk.Button(ctrl, text="Start", command=self.start)
        self.btn_pause = ttk.Button(ctrl, text="Pause", command=self.pause)
        self.btn_play = ttk.Button(ctrl, text="Play", command=self.play)
        self.btn_restart = ttk.Button(ctrl, text="Restart", command=self.restart)

        self.btn_start.grid(row=0, column=0, padx=(0, 8))
        self.btn_pause.grid(row=0, column=1, padx=(0, 8))
        self.btn_play.grid(row=0, column=2, padx=(0, 8))
        self.btn_restart.grid(row=0, column=3)

        ttk.Label(self.tab_params, text="(clic gauche) choisir départ | (clic droit) enlever départ").grid(
            row=9, column=0, sticky="w", pady=(10, 0)
        )

        # ----- Study tab -----
        self.trials = tk.IntVar(value=200)
        ttk.Label(self.tab_study, text="Nombre de simulations (Monte-Carlo)").grid(row=0, column=0, sticky="w")
        ttk.Scale(self.tab_study, from_=50, to=500, variable=self.trials, command=lambda _=None: self._update_trials_label()).grid(row=1, column=0, sticky="we")
        self.trials_label = ttk.Label(self.tab_study, text="")
        self.trials_label.grid(row=2, column=0, sticky="w")
        self._update_trials_label()

        self.btn_study = ttk.Button(self.tab_study, text="Lancer étude (θ(d) + stats)", command=self.run_study)
        self.btn_study.grid(row=3, column=0, sticky="we", pady=(10, 0))

        self.study_canvas = tk.Canvas(self.tab_study, width=420, height=260, bg="white")
        self.study_canvas.grid(row=4, column=0, pady=(10, 0))

        self.study_text = tk.Text(self.tab_study, width=58, height=10)
        self.study_text.grid(row=5, column=0, pady=(10, 0))

    def _update_trials_label(self):
        self.trials_label.config(text=f"{int(self.trials.get())} simulations")

    # ---------------- World / RNG ----------------
    def _rng_for_world(self):
        if not self.seed_fixed.get():
            return np.random.default_rng()
        try:
            s = int(self.seed_value.get())
        except Exception:
            s = 1234
        return np.random.default_rng(s)

    def _new_world(self):
        # stop simulation
        self.pause()

        rng = self._rng_for_world()

        self.forest = Forest(
            n=self.n,
            density=self.density.get(),
            neighbors=self.neighbors.get(),
            p_fire=self.p_fire.get(),
            rng=rng,
        )
        self._fixed_initial_grid = self.forest.snapshot_for_restart()
        self.controller = SimulationController(self.forest)

        # reset start selection
        self.start_cell = None
        self.running = False

        self.draw()
        self._update_sim_info()

    def restart(self):
        """
        Restart = même terrain (même initial_grid) remis à zéro,
        et on peut re-choisir le départ.
        """
        self.pause()
        self.running = False

        # remet terrain initial figé
        self.forest.initial_grid = self._fixed_initial_grid.copy()
        self.forest.reset()
        self.controller = SimulationController(self.forest)

        self.start_cell = None
        self.draw()
        self._update_sim_info()

    # ---------------- Interaction départ ----------------
    def on_left_click(self, event):
        if self.running:
            return
        i = event.x // self.cell_px
        j = event.y // self.cell_px
        if 0 <= i < self.n and 0 <= j < self.n:
            # départ seulement si arbre
            if self.forest.grid[i, j] == self.forest.TREE:
                self.start_cell = (i, j)
                self.draw()
                self._update_sim_info()

    def on_right_click(self, event):
        if self.running:
            return
        i = event.x // self.cell_px
        j = event.y // self.cell_px
        if self.start_cell == (i, j):
            self.start_cell = None
            self.draw()
            self._update_sim_info()

    # ---------------- Simulation controls ----------------
    def start(self):
        if self.running:
            return
        if self.start_cell is None:
            return

        # toujours repartir d'une forêt "propre" au start :
        self.forest.reset()
        i0, j0 = self.start_cell
        ok = self.forest.ignite_at(i0, j0)
        if not ok:
            return

        self.running = True
        self._loop()

    def play(self):
        if self.running:
            return
        # reprend seulement si déjà allumé (il y a du feu)
        if np.any(self.forest.grid == self.forest.FIRE):
            self.running = True
            self._loop()

    def pause(self):
        self.running = False
        if self.after_id is not None:
            try:
                self.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

    def _loop(self):
        if not self.running:
            return

        alive = self.controller.step()
        self.draw()
        self._update_sim_info()

        if alive:
            self.after_id = self.after(60, self._loop)
        else:
            self.running = False
            self._update_sim_info()

    # ---------------- Drawing & Info ----------------
    def draw(self):
        self.canvas.delete("all")
        g = self.forest.grid
        p = self.cell_px

        for i in range(self.n):
            x0 = i * p
            x1 = x0 + p
            for j in range(self.n):
                y0 = j * p
                y1 = y0 + p
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.COLOR[int(g[i, j])], outline="")

        # highlight start
        if self.start_cell is not None:
            i, j = self.start_cell
            self.canvas.create_rectangle(i*p, j*p, (i+1)*p, (j+1)*p, outline="blue", width=2)

    def _update_sim_info(self):
        m = self.controller.metrics()
        txt = (
            f"Départ : {self.start_cell}\n"
            f"Itérations : {m['iteration']}\n"
            f"Brûlé : {m['burned_count']} cases ({m['burned_fraction']*100:.1f} %)\n"
            f"Frontière (rugosité) : {m['frontier']}\n"
            f"Percolation (coin bas-droit atteint) : {'Oui' if m['percolates'] else 'Non'}\n"
            f"État : {'en cours' if self.running else 'arrêt'}"
        )
        self.sim_info.config(text=txt)

    # ---------------- Study mode ----------------
    def run_study(self):
        if self.start_cell is None:
            return

        trials = int(self.trials.get())

        # densités fines pour courbe lisse
        densities = [round(x, 3) for x in np.linspace(0.1, 0.95, 18)]

        # seed : si fixe → reproductible
        seed = None
        if self.seed_fixed.get():
            try:
                seed = int(self.seed_value.get())
            except Exception:
                seed = 1234

        # courbe theta(d)
        curve = theta_curve(
            n=self.n,
            densities=densities,
            neighbors=self.neighbors.get(),
            p_fire=self.p_fire.get(),
            start_cell=self.start_cell,
            trials=trials,
            seed=seed
        )

        # stats détaillées pour la densité courante (celle du slider)
        stats = monte_carlo(
            n=self.n,
            density=float(self.density.get()),
            neighbors=self.neighbors.get(),
            p_fire=self.p_fire.get(),
            start_cell=self.start_cell,
            trials=trials,
            seed=seed
        )

        self._draw_curve(curve)
        self._write_stats(stats)

    def _draw_curve(self, curve):
        c = self.study_canvas
        c.delete("all")

        w, h = 420, 260
        margin = 40

        # axes
        c.create_line(margin, h - margin, w - margin, h - margin)
        c.create_line(margin, h - margin, margin, margin)

        c.create_text(w//2, 14, text="Courbe θ(d) = P(percolation)", font=("Arial", 10, "bold"))

        # legend / labels
        c.create_text(w//2, h - 12, text="d (densité)")
        c.create_text(14, h//2, text="θ(d)", angle=90)

        xs = [d for d, _ in curve]
        ys = [p for _, p in curve]

        dmin, dmax = min(xs), max(xs)

        def X(d):
            return margin + int((d - dmin) / (dmax - dmin) * (w - 2*margin))

        def Y(p):
            return (h - margin) - int(p * (h - 2*margin))

        # points + lines
        prev = None
        for d, p in curve:
            x, y = X(d), Y(p)
            c.create_oval(x-3, y-3, x+3, y+3, fill="red", outline="")
            if prev is not None:
                c.create_line(prev[0], prev[1], x, y)
            prev = (x, y)

        # graduation simple
        for k in range(0, 6):
            p = k / 5
            y = Y(p)
            c.create_line(margin-4, y, margin+4, y)
            c.create_text(margin-18, y, text=f"{p:.1f}")

    def _write_stats(self, stats):
        t = self.study_text
        t.delete("1.0", "end")

        if stats is None:
            t.insert("end", "Étude impossible : départ sur case non arbre.\n")
            return

        # affichage clair, math-friendly
        t.insert("end", f"Paramètres (étude)\n")
        t.insert("end", f"- n = {self.n}\n")
        t.insert("end", f"- d = {self.density.get():.3f}\n")
        t.insert("end", f"- voisinage = {self.neighbors.get()}\n")
        t.insert("end", f"- p_fire = {self.p_fire.get():.3f}\n")
        t.insert("end", f"- départ = {self.start_cell}\n")
        t.insert("end", f"- essais = {stats['trials_used']}\n\n")

        t.insert("end", f"Résultats (Monte-Carlo)\n")
        t.insert("end", f"θ(d) = P(percolation) ≈ {stats['theta']:.3f}  (~ {stats['theta']*100:.1f} %)\n")
        t.insert("end", f"moyenne brûlé ≈ {stats['burned_mean']*100:.1f} %   | variance ≈ {stats['burned_var']:.4f}\n")
        t.insert("end", f"temps moyen ≈ {stats['time_mean']:.1f} itérations | variance ≈ {stats['time_var']:.2f}\n")
        t.insert("end", f"frontière moyenne ≈ {stats['frontier_mean']:.1f}   | variance ≈ {stats['frontier_var']:.2f}\n")
