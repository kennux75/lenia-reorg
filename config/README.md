# Configuration de Lenia

Ce répertoire contient les fichiers de configuration pour la simulation Lenia.

## Fichiers

### `display_config.py`

Configuration de l'interface graphique et de l'affichage.

#### Paramètres principaux

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|------------------|
| `DPI` | Résolution en points par pouce | 100 |
| `MENU_WIDTH` | Largeur du menu latéral en pixels | 350 |
| `MAX_WINDOW_WIDTH` | Largeur maximale de la fenêtre | 2000 |
| `width`, `height` | Dimensions de la fenêtre | 1600×950 |
| `FPS` | Images par seconde pour l'animation | 25 |

#### Couleurs

Le fichier définit également plusieurs constantes de couleurs utilisées dans l'interface :
- `BLACK`, `WHITE`, `GRAY`, `LIGHT_GRAY`, `DARK_GRAY`
- `BLUE`, `GREEN`, `RED`, `YELLOW`, `PURPLE`

#### Paramètres des popups

| Paramètre | Description |
|-----------|-------------|
| `POPUP_PADDING` | Espacement interne des popups |
| `POPUP_BORDER_WIDTH` | Épaisseur de la bordure des popups |
| `POPUP_BACKGROUND` | Couleur de fond des popups |
| `POPUP_BORDER` | Couleur de la bordure des popups |

#### Paramètres d'affichage

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|------------------|
| `DEFAULT_INTERPOLATION` | Méthode d'interpolation pour l'affichage | 'bicubic' |

### `simulation_config.py`

Configuration des paramètres de la simulation Lenia.

#### Dimensions de la grille

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|------------------|
| `N` | Hauteur de la grille | 256 |
| `M` | Largeur de la grille (calculée pour un ratio 16:9) | ~455 |

#### Paramètres temporels

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|------------------|
| `dt` | Pas de temps pour l'évolution | 0.5 |

#### Paramètres des kernels

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|------------------|
| `R` | Rayon de base pour les kernels | 12 |
| `kernel_mu` | Moyenne pour la fonction gaussienne dans les kernels | 0.5 |
| `kernel_sigma` | Écart-type pour la fonction gaussienne dans les kernels | 0.15 |

#### Matrice d'interaction

La matrice `interaction_matrix` définit l'influence de chaque canal sur les autres. Une valeur positive indique une influence positive (activation), tandis qu'une valeur négative indique une influence négative (inhibition).

#### Définition des kernels

Le fichier contient une liste de dictionnaires `kernels` qui définissent les différents kernels utilisés dans la simulation. Chaque kernel est défini par les paramètres suivants :

| Paramètre | Description |
|-----------|-------------|
| `b` | Poids des anneaux |
| `m` | Moyenne de la fonction de croissance |
| `s` | Écart-type de la fonction de croissance |
| `h` | Hauteur (amplitude) de l'effet |
| `r` | Rayon relatif par rapport au rayon de base |
| `c0` | Canal source (0=rouge, 1=vert, 2=bleu) |
| `c1` | Canal destination (0=rouge, 1=vert, 2=bleu) |

Les paramètres extraits `bs`, `rs`, `ms`, `ss`, `hs`, `sources` et `destinations` sont des listes qui regroupent les valeurs correspondantes de tous les kernels pour faciliter l'accès. 