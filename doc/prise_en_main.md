# Prise en main de l’application

## Prérequis

- Python ≥ 3.9
- Bibliothèques :
  - numpy
  - tkinter (inclus par défaut avec Python)

Installation des dépendances :
```bash
pip install -r requirements.txt
```

## Lancement

À la racine du projet :

```bash
python main.py
```

## Interface graphique

L’application se compose de deux parties :

### 1. Simulation interactive

* La forêt est représentée par une grille 2D.
* Vert : arbre intact
* Rouge : arbre en feu
* Noir : arbre brûlé
* Blanc : absence d’arbre

Fonctionnement :

1. Choisir les paramètres (densité, voisinage, probabilité de propagation).
2. Cliquer sur une case verte pour choisir le point de départ du feu.
3. Cliquer sur **Start** pour lancer la propagation.
4. **Pause / Play** permet d’arrêter ou reprendre la simulation.
5. **Restart** réinitialise la forêt sans feu (même terrain).

### 2. Mode étude

Le bouton **Étudier** lance une étude statistique basée sur des simulations Monte-Carlo afin d’estimer la probabilité de percolation.

Les résultats sont affichés sous forme de tableau et de jauges visuelles.

## Objectif pédagogique

L’interface permet de :

* visualiser un phénomène de percolation,
* comprendre l’influence des paramètres,
* observer une transition de phase.
