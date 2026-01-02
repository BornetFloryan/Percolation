# Étude statistique du phénomène de percolation

## Objectif

L’objectif de l’étude est d’estimer numériquement la probabilité de percolation
en fonction de la densité de la forêt.

Cette estimation est réalisée par des simulations Monte-Carlo.

## Méthode Monte-Carlo

Pour une densité donnée d :
1. Générer plusieurs forêts aléatoires indépendantes.
2. Allumer le feu au même point initial.
3. Laisser la propagation se faire jusqu’à extinction.
4. Vérifier si le feu atteint le coin opposé.

La probabilité est estimée par :
```

P ≈ (nombre de succès) / (nombre de simulations)

```

## Résultats

Les résultats sont affichés sous forme :
- de pourcentages,
- de barres visuelles,
- d’une courbe de transition implicite.

On observe :
- une faible probabilité pour d < 0.4,
- une augmentation rapide autour de d ≈ 0.5,
- une forte probabilité pour d > 0.6.

## Interprétation

Cette transition brutale est caractéristique d’un phénomène de percolation.

Les écarts avec la valeur théorique s’expliquent par :
- la taille finie de la grille,
- les effets de bord,
- la définition opérationnelle de la percolation.

## Intérêt scientifique

Cette étude montre comment un phénomène mathématique abstrait peut être exploré expérimentalement grâce à des outils informatiques.
