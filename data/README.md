# Données et Créatures

Ce répertoire contient les données utilisées par la simulation Lenia, notamment les définitions des créatures et les configurations prédéfinies.

## Créatures (`creatures.py`)

Le fichier `creatures.py` contient les définitions des créatures qui peuvent être utilisées dans la simulation. Chaque créature est définie comme un tableau NumPy avec des valeurs entre 0 et 1.

### Créatures disponibles

#### Aquarium

L'aquarium est une créature à 3 canaux (RGB) qui contient plusieurs organismes interagissant entre eux. C'est un écosystème complet qui évolue au fil du temps.

#### Autres créatures

D'autres créatures sont disponibles, chacune avec ses propres caractéristiques et comportements:

- Orbium
- Geminium
- Pentaorbium
- Hydrogeminium
- Etc.

### Fonctions utilitaires

Le module `creatures.py` contient également plusieurs fonctions utilitaires:

- **`get_random_position(grid_shape, creature_shape)`**: Génère une position aléatoire valide pour placer une créature.
- **`inject_aquarium(grid, position=None)`**: Place l'aquarium dans la grille à la position spécifiée.
- **`init_grid(shape, creature=None, position=None)`**: Initialise une grille avec une créature optionnelle.

## Configurations prédéfinies

Le répertoire contient également des configurations prédéfinies pour différents types de simulations:

- Paramètres de kernels optimisés pour différentes créatures
- Matrices d'interaction pour des comportements spécifiques
- Configurations de fonctions de croissance

## Utilisation

### Charger une créature

```python
import numpy as np
from data.creatures import init_grid, inject_aquarium

# Initialiser une grille vide
grid_shape = (3, 256, 256)  # 3 canaux RGB, 256x256 pixels
grid = np.zeros(grid_shape)

# Injecter l'aquarium à une position aléatoire
grid = inject_aquarium(grid)
```

### Utiliser une configuration prédéfinie

```python
from config.simulation_config import kernels, interaction_matrix
from functions.kernel.kernel_generation import generate_kernels

# Générer les kernels à partir de la configuration prédéfinie
shape = (256, 256)
active_indices = range(len(kernels))
bs = [k['b'] for k in kernels]
rs = [k['r'] for k in kernels]
R = 12  # Rayon de base

kernels_fft = generate_kernels(shape, active_indices, bs, rs, R)
```

## Création de nouvelles créatures

Pour créer une nouvelle créature, vous pouvez:

1. Définir un tableau NumPy avec les valeurs initiales
2. Ajouter la définition à `creatures.py`
3. Créer une fonction d'injection similaire à `inject_aquarium`

Exemple:

```python
def create_my_creature():
    # Créer une créature simple à 1 canal
    creature = np.zeros((1, 20, 20))
    
    # Définir un motif (par exemple, un carré au centre)
    creature[0, 5:15, 5:15] = 0.8
    
    return creature

def inject_my_creature(grid, position=None):
    # Similaire à inject_aquarium
    creature = create_my_creature()
    # ... code pour injecter la créature dans la grille ...
    return grid
``` 