# Fonctions de Croissance

Ce répertoire contient les fonctions de croissance utilisées dans la simulation Lenia. Ces fonctions déterminent comment les cellules évoluent en fonction de leur environnement.

## Fonctions disponibles

### `gauss(x, mu, sigma)`

Fonction gaussienne classique.

- **Paramètres**:
  - `x`: Valeur d'entrée
  - `mu`: Moyenne de la gaussienne
  - `sigma`: Écart-type de la gaussienne
  
- **Formule**: $f(x) = e^{-\frac{(x-\mu)^2}{2\sigma^2}}$

- **Comportement**: Produit une courbe en forme de cloche centrée sur `mu` avec une largeur déterminée par `sigma`.

### `sigmoid(x, mu, sigma)`

Fonction sigmoïde, utile pour les transitions douces entre états.

- **Paramètres**:
  - `x`: Valeur d'entrée
  - `mu`: Point central de la transition
  - `sigma`: Pente de la transition
  
- **Formule**: $f(x) = \frac{1}{1 + e^{-\frac{x-\mu}{\sigma}}}$

- **Comportement**: Produit une transition douce de 0 à 1, centrée sur `mu` avec une pente déterminée par `sigma`.

### `multi_peak_growth(x, mu, sigma, h)`

Fonction de croissance à pics multiples, permettant des comportements plus complexes.

- **Paramètres**:
  - `x`: Valeur d'entrée
  - `mu`: Liste des moyennes pour chaque pic
  - `sigma`: Liste des écarts-types pour chaque pic
  - `h`: Liste des hauteurs pour chaque pic
  
- **Comportement**: Combine plusieurs gaussiennes avec différentes hauteurs, moyennes et écarts-types.

### `growth_function_3(x, mu, sigma)`

Fonction de croissance spécifique à Lenia, basée sur une gaussienne avec un plateau.

- **Paramètres**:
  - `x`: Valeur d'entrée
  - `mu`: Moyenne de la fonction
  - `sigma`: Écart-type de la fonction
  
- **Comportement**: Produit une courbe en forme de cloche avec un plateau, adaptée aux simulations Lenia.

### `growth_function_4(x, mu, sigma)`

Variante de la fonction de croissance pour Lenia.

- **Paramètres**:
  - `x`: Valeur d'entrée
  - `mu`: Moyenne de la fonction
  - `sigma`: Écart-type de la fonction
  
- **Comportement**: Similaire à `growth_function_3` mais avec des caractéristiques légèrement différentes.

## Utilisation

Ces fonctions sont utilisées dans le processus d'évolution de la simulation pour déterminer comment les cellules réagissent à leur environnement. Elles sont appelées par les fonctions d'évolution dans le module `functions/evolution`.

Exemple d'utilisation:

```python
from functions.growth.growth_functions import gauss

# Calculer la croissance pour une valeur donnée
growth_value = gauss(0.7, 0.5, 0.15)
```

## Visualisation

Pour visualiser ces fonctions et comprendre leur comportement, vous pouvez utiliser le module de visualisation inclus dans le projet:

```python
from functions.display.visualization import plot_growth_function
from functions.growth.growth_functions import gauss

# Visualiser la fonction gaussienne
plot_growth_function(gauss, mu=0.5, sigma=0.15)
``` 