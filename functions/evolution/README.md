# Évolution dans Lenia

Ce répertoire contient les fonctions qui gèrent l'évolution temporelle de la simulation Lenia. Ces fonctions déterminent comment l'état de la grille change à chaque pas de temps.

## Fonctions principales

### `evolve_single_channel(grid, kernel_fft, growth_func, mu, sigma, dt)`

Fait évoluer un seul canal de la grille.

- **Paramètres**:
  - `grid`: Matrice 2D représentant l'état actuel du canal
  - `kernel_fft`: Transformée de Fourier du kernel d'évolution
  - `growth_func`: Fonction de croissance à appliquer
  - `mu`: Moyenne pour la fonction de croissance
  - `sigma`: Écart-type pour la fonction de croissance
  - `dt`: Pas de temps pour l'évolution
  
- **Retour**: Nouvelle matrice 2D représentant l'état mis à jour du canal

### `evolve_multi_channels(grid, kernels_fft, growth_func, ms, ss, dt, sources, destinations, hs)`

Fait évoluer plusieurs canaux de la grille avec des interactions entre eux.

- **Paramètres**:
  - `grid`: Matrice 3D représentant l'état actuel de tous les canaux
  - `kernels_fft`: Liste des transformées de Fourier des kernels
  - `growth_func`: Fonction de croissance à appliquer
  - `ms`: Liste des moyennes pour chaque fonction de croissance
  - `ss`: Liste des écarts-types pour chaque fonction de croissance
  - `dt`: Pas de temps pour l'évolution
  - `sources`: Liste des canaux sources pour chaque kernel
  - `destinations`: Liste des canaux destinations pour chaque kernel
  - `hs`: Liste des hauteurs (amplitudes) pour chaque interaction
  
- **Retour**: Nouvelle matrice 3D représentant l'état mis à jour de tous les canaux

### `kernel_generator(shape, active_indices, bs, rs, R)`

Génère les kernels nécessaires pour l'évolution.

- **Paramètres**:
  - `shape`: Tuple (hauteur, largeur) définissant la taille de la grille
  - `active_indices`: Liste des indices des kernels actifs
  - `bs`: Liste des poids pour chaque anneau dans les kernels
  - `rs`: Liste des rayons relatifs pour chaque kernel
  - `R`: Rayon de base pour tous les kernels
  
- **Retour**: Liste des transformées de Fourier des kernels actifs

## Processus d'évolution

L'évolution dans Lenia suit ces étapes principales:

1. **Convolution**: Chaque cellule calcule une moyenne pondérée de son voisinage en utilisant le kernel.
2. **Fonction de croissance**: Le résultat de la convolution est passé à une fonction de croissance qui détermine comment la cellule doit changer.
3. **Mise à jour**: L'état de la cellule est mis à jour en fonction du résultat de la fonction de croissance et du pas de temps.

## Évolution multi-canaux

Dans le cas de l'évolution multi-canaux:

1. Chaque canal peut influencer les autres canaux.
2. L'influence est déterminée par les kernels et la matrice d'interaction.
3. Les paramètres `sources` et `destinations` définissent quels canaux influencent quels autres canaux.
4. Le paramètre `hs` définit l'amplitude de chaque influence.

## Optimisation

Les fonctions d'évolution utilisent la transformée de Fourier rapide (FFT) pour accélérer les calculs de convolution. Cela permet de simuler des grilles de grande taille avec une performance raisonnable.

## Exemple d'utilisation

```python
import numpy as np
from functions.evolution.evolution import evolve_multi_channels
from functions.kernel.kernel_generation import generate_kernels
from functions.growth.growth_functions import growth_function_3

# Initialiser la grille
grid = np.random.rand(3, 256, 256)  # 3 canaux RGB

# Générer les kernels
kernels_fft = generate_kernels((256, 256), [0, 1, 2], 
                              [[1.0], [1.0], [1.0]], 
                              [[0.5], [0.5], [0.5]], 
                              12)

# Paramètres d'évolution
ms = [0.5, 0.5, 0.5]  # Moyennes
ss = [0.15, 0.15, 0.15]  # Écarts-types
dt = 0.1  # Pas de temps
sources = [0, 1, 2]  # Canaux sources
destinations = [0, 1, 2]  # Canaux destinations
hs = [1.0, 1.0, 1.0]  # Hauteurs

# Faire évoluer la grille
new_grid = evolve_multi_channels(grid, kernels_fft, growth_function_3, 
                                ms, ss, dt, sources, destinations, hs)
``` 