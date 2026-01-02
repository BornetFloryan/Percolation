# Architecture technique

## Organisation générale

Le projet est structuré selon une séparation claire des responsabilités :

```

model/       # modèle mathématique
controller/  # logique de simulation et analyses
analysis/    # études statistiques (Monte-Carlo)
view/        # interface graphique
doc/         # documentation

```

## Modèle

Le module `Forest` encapsule :
- la grille,
- les règles de propagation,
- l’état de la simulation.

Il est indépendant de toute interface graphique.

## Contrôleur

Le contrôleur assure :
- l’évolution temporelle de la simulation,
- les mesures statistiques,
- les expériences Monte-Carlo.

Cela permet de réutiliser le modèle sans interface graphique.

## Interface graphique

L’interface (Tkinter) permet :
- l’interaction utilisateur,
- la visualisation du feu,
- le lancement des études statistiques.

## Choix techniques

- Python : lisibilité, rapidité de prototypage.
- Numpy : efficacité sur les grilles 2D.
- Tkinter : interface simple et portable.
- Monte-Carlo : méthode adaptée aux phénomènes aléatoires.

## Extensibilité

Cette architecture permet facilement :
- l’ajout de nouvelles mesures (temps de propagation, taille d’amas),
- l’export des résultats,
- l’extension à d’autres modèles de percolation.