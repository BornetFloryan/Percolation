import numpy as np
from model.forest import Forest


def run_one_trial(n, density, neighbors, p_fire, start_cell, rng):
    forest = Forest(n, density, neighbors=neighbors, p_fire=p_fire, rng=rng)

    i0, j0 = start_cell
    if not forest.ignite_at(i0, j0):
        # départ sur une case vide → on considère l’essai invalide
        return None

    while forest.step():
        pass

    return {
        "percolates": forest.percolates(),
        "burned_count": forest.burned_count(),
        "burned_fraction": forest.burned_fraction(),
        "time": forest.time_to_extinction(),
        "frontier": forest.burned_frontier_count(),
    }


def monte_carlo(n, density, neighbors, p_fire, start_cell, trials=200, seed=None):
    """
    Lance trials simulations indépendantes et renvoie :
    - probabilité de percolation
    - moyennes / variances des métriques
    Reproductible si seed est fixé.
    """
    rng = np.random.default_rng(seed)

    results = []
    for _ in range(trials):
        r = run_one_trial(n, density, neighbors, p_fire, start_cell, rng)
        if r is not None:
            results.append(r)

    if len(results) == 0:
        return None

    percs = np.array([r["percolates"] for r in results], dtype=float)
    burned_frac = np.array([r["burned_fraction"] for r in results], dtype=float)
    times = np.array([r["time"] for r in results], dtype=float)
    frontiers = np.array([r["frontier"] for r in results], dtype=float)

    return {
        "trials_used": len(results),
        "theta": float(percs.mean()),
        "theta_var": float(percs.var()),
        "burned_mean": float(burned_frac.mean()),
        "burned_var": float(burned_frac.var()),
        "time_mean": float(times.mean()),
        "time_var": float(times.var()),
        "frontier_mean": float(frontiers.mean()),
        "frontier_var": float(frontiers.var()),
    }


def theta_curve(n, densities, neighbors, p_fire, start_cell, trials=200, seed=None):
    """
    Calcule θ(d) pour une liste de densités.
    """
    curve = []
    for d in densities:
        stats = monte_carlo(
            n=n, density=d, neighbors=neighbors, p_fire=p_fire,
            start_cell=start_cell, trials=trials, seed=seed
        )
        if stats is None:
            curve.append((d, 0.0))
        else:
            curve.append((d, stats["theta"]))
    return curve
