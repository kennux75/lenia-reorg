#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programme principal de la simulation Lenia
-----------------------------------------
Ce script lance la simulation Lenia avec un menu latéral pour contrôler les fonctions de croissance.
"""

import numpy as np
from data.creatures import init_grid
from functions.display.visualization import produce_movie_multi
from functions.evolution.evolution import evolve_multi_channels_interactions

def main():
    """
    Fonction principale qui lance la simulation.
    """
    # Initialisation des grilles pour chaque canal (rouge, vert, bleu)
    Xs = init_grid()
    
    # Lancement de la simulation avec interactions entre canaux
    produce_movie_multi(Xs, evolve_multi_channels_interactions)

if __name__ == "__main__":
    main() 