# Lenia Simulation

Une implémentation modulaire de Lenia, un système d'automates cellulaires continus.

## Description

Lenia est un système d'automates cellulaires continus qui peut générer des motifs complexes et des comportements émergents. Cette implémentation utilise plusieurs canaux (RGB) pour créer des interactions complexes entre différentes "espèces" de cellules.

## Structure du projet

Le projet est organisé en plusieurs répertoires:

```
lenia-reorg/
├── config/                 # Configuration de la simulation
│   ├── display_config.py   # Paramètres d'affichage
│   └── simulation_config.py # Paramètres de simulation
├── functions/              # Fonctions de la simulation
│   ├── growth/             # Fonctions de croissance
│   │   └── growth_functions.py
│   ├── evolution/          # Fonctions d'évolution
│   │   ├── evolution.py
│   │   └── kernel_generator.py
│   └── display/            # Fonctions d'affichage
│       └── visualization.py
├── data/                   # Définitions des créatures
│   └── creatures.py
└── main.py                 # Point d'entrée principal
```

## Installation

### Prérequis

- Python 3.6+
- NumPy
- SciPy
- Matplotlib
- Pygame

### Installation des dépendances

```bash
pip install numpy scipy matplotlib pygame
```

## Utilisation

Pour lancer la simulation:

```bash
python main.py
```

### Contrôles

- **Espace**: Pause/Reprise de la simulation
- **A**: Ajouter un "aquarium" à une position aléatoire
- **R**: Réinitialiser la grille

## Personnalisation

### Ajouter de nouvelles créatures

Pour ajouter de nouvelles créatures, modifiez le fichier `data/creatures.py` en définissant de nouveaux patterns pour les trois canaux (RGB).

### Modifier les paramètres de simulation

Les paramètres de simulation peuvent être modifiés dans `config/simulation_config.py`:

- Dimensions de la grille
- Paramètres des kernels
- Matrice d'interaction entre canaux
- Pas de temps

### Ajouter de nouvelles fonctions de croissance

Pour ajouter de nouvelles fonctions de croissance, modifiez le fichier `functions/growth/growth_functions.py`.

## Fonctionnement

Lenia fonctionne en appliquant des convolutions (via FFT) avec des kernels spécifiques sur une grille 2D, puis en appliquant une fonction de croissance sur le résultat. Cette implémentation utilise plusieurs canaux qui peuvent interagir entre eux, créant des comportements complexes.

## Licence

Ce projet est sous licence MIT.

## Références

- [Lenia - Biology of Artificial Life](https://arxiv.org/abs/1812.05433) par Bert Chan
- [Lenia and Expanded Universe](https://arxiv.org/abs/2005.03742) par Bert Chan 