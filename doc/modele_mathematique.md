# Modèle mathématique

## Contexte : percolation

La percolation est un modèle mathématique introduit par John Hammersley (1957) pour étudier la connectivité dans des milieux aléatoires.

Dans le cadre de ce projet, nous nous intéressons à une **percolation de site en dimension 2**, modélisée sur une grille carrée finie.

## Modélisation de la forêt

La forêt est assimilée à une grille carrée de taille n × n, analogue à un sous-ensemble fini de ℤ².

Chaque case peut être dans l’un des états suivants :
- 0 : vide
- 1 : arbre intact
- 2 : arbre en feu
- 3 : arbre brûlé

La distribution initiale des arbres suit une loi de Bernoulli de paramètre d (densité).

## Règle de propagation

À chaque itération :
- une case en feu devient brûlée,
- elle enflamme ses voisins intacts selon :
  - un voisinage à 4 ou 8 voisins,
  - une probabilité de propagation p_fire.

Ce mécanisme définit un **automate cellulaire** discret.

## Problème étudié

On s’intéresse à la question suivante :

> Pour une densité donnée, quelle est la probabilité que le feu atteigne le coin opposé de la grille ?

Cette probabilité est une approximation numérique de la probabilité de percolation θ(d).

## Lien avec la théorie

En percolation de site sur ℤ² infini, il existe un seuil critique théorique pc ≈ 0.5.

Dans notre cas :
- la grille est finie,
- les conditions aux bords influencent les résultats,
- la percolation est définie de manière opérationnelle (atteinte du coin bas-droit).

Les simulations permettent d’observer expérimentalement une transition de phase analogue au cas théorique.
