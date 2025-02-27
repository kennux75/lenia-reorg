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
│   ├── simulation_config.py # Paramètres de simulation
│   └── README.md           # Documentation des paramètres de configuration
├── functions/              # Fonctions de la simulation
│   ├── growth/             # Fonctions de croissance
│   │   ├── growth_functions.py
│   │   └── README.md       # Documentation des fonctions de croissance
│   ├── kernel/             # Fonctions de génération de kernels
│   │   ├── kernel_generation.py
│   │   └── README.md       # Documentation des kernels
│   ├── evolution/          # Fonctions d'évolution
│   │   ├── evolution.py
│   │   ├── kernel_generator.py
│   │   └── README.md       # Documentation des fonctions d'évolution
│   └── display/            # Fonctions d'affichage
│       ├── visualization.py
│       ├── ui_widgets.py
│       ├── menu_manager.py
│       └── README.md       # Documentation des fonctions d'affichage
├── data/                   # Définitions des créatures
│   ├── creatures.py
│   └── README.md           # Documentation des créatures disponibles
└── main.py                 # Point d'entrée principal
```

## Documentation

Chaque répertoire principal contient un fichier README.md qui explique en détail les fonctionnalités et paramètres disponibles:

- [Configuration](config/README.md) - Paramètres de configuration de la simulation et de l'affichage
- [Fonctions de croissance](functions/growth/README.md) - Fonctions qui déterminent l'évolution des cellules
- [Kernels](functions/kernel/README.md) - Génération des kernels pour les convolutions
- [Évolution](functions/evolution/README.md) - Fonctions d'évolution temporelle de la simulation
- [Affichage](functions/display/README.md) - Interface utilisateur et visualisation
- [Données et créatures](data/README.md) - Créatures prédéfinies et leur utilisation

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
- **S**: Sauvegarder l'état actuel
- **L**: Charger un état sauvegardé
- **M**: Générer une vidéo de la simulation

## Personnalisation

### Ajouter de nouvelles créatures

Pour ajouter de nouvelles créatures, modifiez le fichier `data/creatures.py` en définissant de nouveaux patterns pour les trois canaux (RGB). Consultez [la documentation des créatures](data/README.md) pour plus de détails.

### Modifier les paramètres de simulation

Les paramètres de simulation peuvent être modifiés dans `config/simulation_config.py`:

- Dimensions de la grille
- Paramètres des kernels
- Matrice d'interaction entre canaux
- Pas de temps

Consultez [la documentation de configuration](config/README.md) pour une description détaillée de tous les paramètres.

### Ajouter de nouvelles fonctions de croissance

Pour ajouter de nouvelles fonctions de croissance, modifiez le fichier `functions/growth/growth_functions.py`. Consultez [la documentation des fonctions de croissance](functions/growth/README.md) pour comprendre les fonctions existantes.

## Fonctionnement

Lenia fonctionne en appliquant des convolutions (via FFT) avec des kernels spécifiques sur une grille 2D, puis en appliquant une fonction de croissance sur le résultat. Cette implémentation utilise plusieurs canaux qui peuvent interagir entre eux, créant des comportements complexes.

Pour une compréhension approfondie:
- Consultez [la documentation des kernels](functions/kernel/README.md) pour comprendre la génération des kernels
- Consultez [la documentation d'évolution](functions/evolution/README.md) pour comprendre le processus d'évolution

## Licence

Ce projet est sous licence MIT.

## Références

- [Lenia - Biology of Artificial Life](https://arxiv.org/abs/1812.05433) par Bert Chan
- [Lenia and Expanded Universe](https://arxiv.org/abs/2005.03742) par Bert Chan 