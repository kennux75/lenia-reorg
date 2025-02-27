#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programme principal de la simulation Lenia
-----------------------------------------
Ce script lance la simulation Lenia avec quatre fenêtres séparées:
1. Fenêtre de simulation - Affiche la simulation Lenia en temps réel
2. Fenêtre de menu - Permet de contrôler les kernels actifs et les fonctions de croissance
3. Fenêtre de matrice d'interaction - Permet de modifier les interactions entre canaux
4. Fenêtre d'oscilloscope - Affiche en temps réel les courbes des fonctions de croissance

Les fenêtres de simulation et d'oscilloscope sont mises à jour en temps réel.
Toutes les fenêtres communiquent entre elles pour partager des informations.

Commandes:
- Espace : mettre en pause ou reprendre la simulation
- A : injecter un "aquarium" (motifs prédéfinis)
- R : réinitialiser la simulation
"""

import numpy as np
import pygame
import sys
from data.creatures import init_grid
from functions.display.visualization import produce_movie_multi
from functions.evolution.evolution import evolve_multi_channels_interactions

def main():
    """
    Fonction principale qui lance la simulation avec les quatre fenêtres séparées.
    """
    # Initialisation de pygame (nécessaire pour l'affichage)
    if not pygame.get_init():
        pygame.init()
    
    # Initialisation des grilles pour chaque canal (rouge, vert, bleu)
    Xs = init_grid()
    
    # Lancement de la simulation avec interactions entre canaux
    # Cette fonction va créer les 4 fenêtres séparées
    produce_movie_multi(Xs, evolve_multi_channels_interactions)
    
    # À la fin de la simulation, quitter proprement
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main() 