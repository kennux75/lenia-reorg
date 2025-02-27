#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions de visualisation
-------------------------
Ce module contient les fonctions pour visualiser la simulation Lenia.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pygame

from config.display_config import DPI, width, height, screen, FPS, DEFAULT_INTERPOLATION
from data.creatures import inject_aquarium, init_grid

def produce_movie_multi(Xs, evolve, interpolation=DEFAULT_INTERPOLATION):
    """
    Produit une animation de la simulation Lenia avec plusieurs canaux.
    
    Args:
        Xs (list): Liste des grilles pour chaque canal
        evolve (function): Fonction d'évolution à utiliser
        interpolation (str, optional): Méthode d'interpolation pour l'affichage. Par défaut DEFAULT_INTERPOLATION.
    """
    running = True
    paused = False
    clock = pygame.time.Clock()

    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    figsize = (width / DPI, height / DPI)
    fig, ax = plt.subplots(figsize=figsize, dpi=DPI)
    
    canvas = FigureCanvas(fig)
    im = ax.imshow(np.dstack(Xs), interpolation=interpolation)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_a:  # Si la touche 'a' est pressée
                    Xs = inject_aquarium(Xs)
                if event.key == pygame.K_r:  # Si la touche 'r' est pressée
                    Xs = init_grid()
        
        if not paused:
            # Évolution du système
            Xs = evolve(Xs)
            
            # Conversion de la simulation en image
            data = np.dstack(Xs)
            data_uint8 = (255 * np.clip(data, 0, 1)).astype(np.uint8)
            
            # Création d'une surface pygame
            surface = pygame.surfarray.make_surface(data_uint8.swapaxes(0, 1))
            scaled_surface = pygame.transform.smoothscale(surface, (width, height))

            # Affichage
            screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            
            # Contrôle de la fréquence d'images
            clock.tick(FPS)
    
    pygame.quit()

def plot_growth_functions(ms, ss, hs):
    """
    Trace les fonctions de croissance utilisées dans la simulation.
    
    Args:
        ms (list): Liste des moyennes
        ss (list): Liste des écarts-types
        hs (list): Liste des hauteurs
    """
    from functions.growth.growth_functions import gauss
    
    plt.figure(figsize=(10, 10))
    x = np.linspace(0, 1, 100)
    
    for m, s, h in zip(ms, ss, hs):
        plt.plot(x, h * (2 * gauss(x, m, s) - 1))
    
    plt.title("Fonctions de croissance")
    plt.xlabel("Valeur d'entrée")
    plt.ylabel("Taux de croissance")
    plt.grid(True)
    plt.savefig("growth_functions.png")
    plt.close() 