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

from config.display_config import DPI, width, height, screen, FPS, DEFAULT_INTERPOLATION, MENU_WIDTH, WHITE, BLACK
from data.creatures import inject_aquarium, init_grid
from functions.display.menu_manager import MenuManager
from config.simulation_config import kernels, ms, ss, hs, sources, destinations

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
    
    # Création de la fenêtre
    screen = pygame.display.set_mode((width, height))
    
    # Initialisation du gestionnaire de menu
    menu_manager = MenuManager(kernels, ms, ss, hs, sources, destinations)
    
    # Taille de la surface pour la simulation (sans le menu)
    sim_width = width - MENU_WIDTH
    sim_height = height
    
    # Création de la figure matplotlib pour les statistiques si nécessaire
    figsize = (sim_width / DPI, sim_height / DPI)
    fig, ax = plt.subplots(figsize=figsize, dpi=DPI)
    
    canvas = FigureCanvas(fig)
    im = ax.imshow(np.dstack(Xs), interpolation=interpolation)

    while running:
        # Liste pour collecter les événements de cette frame
        event_list = []
        
        for event in pygame.event.get():
            event_list.append(event)
            
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_a:  # Si la touche 'a' est pressée
                    Xs = inject_aquarium(Xs)
                if event.key == pygame.K_r:  # Si la touche 'r' est pressée
                    Xs = init_grid()
        
        # Mise à jour du menu
        menu_manager.update(event_list)
        
        # Récupération des indices de kernels actifs
        active_indices = menu_manager.get_active_kernel_indices()
        
        if not paused:
            # Évolution du système avec les kernels actifs
            Xs = evolve(Xs, active_indices)
            
            # Conversion de la simulation en image
            data = np.dstack(Xs)
            data_uint8 = (255 * np.clip(data, 0, 1)).astype(np.uint8)
            
            # Création d'une surface pygame pour la simulation
            surface = pygame.surfarray.make_surface(data_uint8.swapaxes(0, 1))
            scaled_surface = pygame.transform.smoothscale(surface, (sim_width, sim_height))

            # Effacer l'écran
            screen.fill(WHITE)
            
            # Affichage de la simulation à droite du menu
            screen.blit(scaled_surface, (MENU_WIDTH, 0))
            
            # Dessiner le menu
            menu_manager.draw(screen)
            
            # Mise à jour de l'affichage
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