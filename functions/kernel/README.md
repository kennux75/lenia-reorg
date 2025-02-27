# Génération de Kernels

Ce répertoire contient les fonctions nécessaires à la génération des kernels utilisés dans la simulation Lenia. Les kernels sont des matrices qui définissent comment les cellules interagissent avec leur voisinage.

## Fonctions principales

### `generate_kernels(shape, active_indices, bs, rs, R)`

Génère les kernels pour la simulation Lenia.

- **Paramètres**:
  - `shape`: Tuple (hauteur, largeur) définissant la taille de la grille
  - `active_indices`: Liste des indices des kernels actifs
  - `bs`: Liste des poids pour chaque anneau dans les kernels
  - `rs`: Liste des rayons relatifs pour chaque kernel
  - `R`: Rayon de base pour tous les kernels
  
- **Retour**: Liste des transformées de Fourier des kernels actifs

### `generate_kernel_shell(r, R, shape)`

Génère un anneau (shell) pour un kernel.

- **Paramètres**:
  - `r`: Rayon relatif de l'anneau
  - `R`: Rayon de base
  - `shape`: Tuple (hauteur, largeur) définissant la taille de la grille
  
- **Retour**: Matrice représentant l'anneau

### `generate_kernel(bs, rs, R, shape)`

Génère un kernel complet à partir de plusieurs anneaux.

- **Paramètres**:
  - `bs`: Liste des poids pour chaque anneau
  - `rs`: Liste des rayons relatifs pour chaque anneau
  - `R`: Rayon de base
  - `shape`: Tuple (hauteur, largeur) définissant la taille de la grille
  
- **Retour**: Matrice représentant le kernel complet

## Concepts clés

### Kernels dans Lenia

Dans Lenia, les kernels définissent comment les cellules interagissent avec leur voisinage. Ils sont généralement composés d'anneaux concentriques avec différents poids, créant des motifs d'interaction complexes.

### Transformée de Fourier

Les kernels sont convertis en transformées de Fourier pour accélérer les calculs de convolution lors de la simulation. Cela permet d'effectuer des convolutions rapides dans le domaine fréquentiel plutôt que des convolutions directes dans le domaine spatial.

### Paramètres des kernels

- **Rayon (R)**: Définit la taille globale du kernel. Un rayon plus grand signifie que les cellules interagissent avec un voisinage plus large.
- **Rayons relatifs (rs)**: Définissent les positions des anneaux par rapport au rayon de base.
- **Poids (bs)**: Définissent l'importance de chaque anneau dans le kernel.

## Visualisation

Pour visualiser les kernels générés, vous pouvez utiliser le module de visualisation inclus dans le projet:

```python
from functions.display.visualization import plot_kernel
from functions.kernel.kernel_generation import generate_kernel

# Générer un kernel simple
kernel = generate_kernel([1.0], [0.5], 12, (256, 256))

# Visualiser le kernel
plot_kernel(kernel)
```

## Exemples de kernels

Différentes combinaisons de paramètres produisent différents types de kernels:

1. **Kernel uniforme**: `bs=[1.0], rs=[1.0]`
   - Toutes les cellules dans le rayon ont la même influence

2. **Kernel à anneaux multiples**: `bs=[1.0, -0.5, 0.2], rs=[0.5, 0.7, 0.9]`
   - Crée des zones d'influence positive et négative à différentes distances

3. **Kernel gaussien**: Approximé avec plusieurs anneaux avec des poids suivant une distribution gaussienne
   - Influence qui diminue progressivement avec la distance 