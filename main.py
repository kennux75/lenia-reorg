#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lenia Simulation - Main Entry Point
-----------------------------------
Ce fichier est le point d'entrée principal de la simulation Lenia.
Il importe les différents modules et lance la simulation.
"""

import numpy as np
import pygame

# Import des configurations
from config.display_config import DPI, width, height
from config.simulation_config import N, M, dt

# Import des fonctions
from functions.growth.growth_functions import gauss
from functions.evolution.evolution import evolve_multi_channels_interactions
from functions.display.visualization import produce_movie_multi

# Import des données
from data.creatures import init_grid

def main():
    """
    Fonction principale qui initialise et lance la simulation Lenia.
    """
    # Initialisation de la grille
    Xs = init_grid()
    
    # Lancement de la simulation
    produce_movie_multi(Xs, evolve_multi_channels_interactions)

if __name__ == "__main__":
    main() 