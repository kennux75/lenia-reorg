#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programme principal de la simulation Lenia
-----------------------------------------
Ce script lance la simulation Lenia avec un menu latéral permettant de contrôler:
- Les kernels actifs avec un menu popup pour voir leurs détails
- Les fonctions de croissance à utiliser
"""

import numpy as np
import pygame
import sys
from data.creatures import init_grid
from functions.display.visualization import produce_movie_multi
from functions.evolution.evolution import evolve_multi_channels_interactions

def main():
    """
    Fonction principale qui lance la simulation.
    """
    # Initialisation de pygame (nécessaire pour l'affichage)
    if not pygame.get_init():
        pygame.init()
    
    # Initialisation des grilles pour chaque canal (rouge, vert, bleu)
    Xs = init_grid()
    
    # Lancement de la simulation avec interactions entre canaux
    produce_movie_multi(Xs, evolve_multi_channels_interactions)

if __name__ == "__main__":
    main() 