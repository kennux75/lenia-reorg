# Affichage et Visualisation

Ce répertoire contient les modules responsables de l'interface utilisateur et de la visualisation des simulations Lenia.

## Modules principaux

### `ui_widgets.py`

Contient les widgets de l'interface utilisateur.

#### Classes principales:

- **`Button`**: Bouton cliquable avec texte et action associée.
- **`Slider`**: Curseur permettant de sélectionner une valeur dans une plage.
- **`Checkbox`**: Case à cocher pour les options booléennes.
- **`Dropdown`**: Menu déroulant pour sélectionner parmi plusieurs options.
- **`TextInput`**: Champ de texte pour saisir des valeurs.
- **`Panel`**: Conteneur pour regrouper plusieurs widgets.
- **`InteractionMatrix`**: Matrice interactive pour ajuster les interactions entre canaux.
- **`Oscilloscope`**: Affiche l'évolution des valeurs au fil du temps avec historique.

### `visualization.py`

Fonctions pour visualiser les données de la simulation.

#### Fonctions principales:

- **`plot_grid`**: Affiche la grille de simulation.
- **`plot_kernel`**: Visualise un kernel.
- **`plot_growth_function`**: Trace une fonction de croissance.
- **`produce_movie`**: Génère une animation à partir d'une séquence d'états de grille.
- **`produce_movie_multi`**: Génère une animation multi-canaux.

### `menu_manager.py`

Gère les menus et l'organisation de l'interface utilisateur.

#### Classes principales:

- **`MenuManager`**: Gère l'ensemble des menus et panneaux de l'interface.
- **`SimulationPanel`**: Panneau de contrôle pour la simulation.
- **`KernelPanel`**: Panneau pour visualiser et modifier les kernels.
- **`CreaturePanel`**: Panneau pour sélectionner et placer des créatures.

## Fonctionnalités clés

### Interface adaptative

L'interface s'adapte automatiquement à la résolution de l'écran, avec une largeur maximale de 1800 pixels pour garantir une bonne lisibilité.

### Visualisation en temps réel

- Affichage en temps réel de la grille de simulation.
- Oscilloscope pour suivre l'évolution des valeurs au cours du temps.
- Visualisation des kernels et des fonctions de croissance.

### Contrôles interactifs

- Matrice d'interaction avec sliders et boutons +/- pour ajuster les influences entre canaux.
- Contrôles pour ajuster les paramètres de simulation (dt, fonctions de croissance, etc.).
- Options pour sauvegarder/charger des configurations.

### Génération de médias

- Capture d'images de la simulation.
- Génération de vidéos à partir des simulations.

## Personnalisation

Les paramètres d'affichage peuvent être modifiés dans le fichier `config/display_config.py`, notamment:

- Dimensions de la fenêtre
- Couleurs de l'interface
- Taille des polices
- Paramètres des popups

## Exemple d'utilisation

```python
import pygame
from functions.display.menu_manager import MenuManager
from functions.display.visualization import plot_grid
import numpy as np

# Initialiser pygame
pygame.init()

# Créer une grille exemple
grid = np.random.rand(3, 256, 256)

# Initialiser le gestionnaire de menu
menu_manager = MenuManager()

# Afficher la grille
plot_grid(grid, menu_manager.screen)

# Mettre à jour l'affichage
pygame.display.flip()
``` 