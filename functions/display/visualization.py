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
import time

from config.display_config import DPI, width, height, screen, FPS, DEFAULT_INTERPOLATION, MENU_WIDTH, WHITE, BLACK, RED, DARK_GRAY
from data.creatures import inject_aquarium, init_grid
from functions.display.menu_manager import MenuManager
from functions.display.ui_widgets import Oscilloscope, InteractionMatrix
from config.simulation_config import kernels, ms, ss, hs, sources, destinations, interaction_matrix
from functions.growth import growth_functions

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
    
    # Dimensions optimisées pour une résolution d'écran de 1800x1169
    menu_width = 300         # Augmenté de 250 à 300 pour plus d'explications
    sim_width = 750          # Maintenu pour l'affichage de la simulation
    matrix_width = 450       # Maintenu pour la matrice d'interaction
    
    # Calcul de la largeur totale
    total_width = min(1800, menu_width + sim_width + matrix_width)
    
    if total_width > 1800:
        available_width = 1800
        menu_width = int(available_width * 0.20)  # Augmenté de 0.17 à 0.20
        matrix_width = int(available_width * 0.30)  # Maintenu à 30%
        sim_width = available_width - menu_width - matrix_width
    
    total_height = 950
    sim_height = int(total_height * 2/3)
    oscillo_height = total_height - sim_height
    
    # Définir le titre de la fenêtre
    pygame.display.set_caption("Simulation Lenia - Interactions multi-canaux")
    
    # Création de la fenêtre avec des dimensions optimisées
    screen = pygame.display.set_mode((total_width, total_height))
    
    # Initialisation du gestionnaire de menu avec une largeur personnalisée
    menu_manager = MenuManager(kernels, ms, ss, hs, sources, destinations, menu_width=menu_width)
    
    # Calcul du ratio original et des dimensions pour maintenir ce ratio
    original_width = Xs[0].shape[1]
    original_height = Xs[0].shape[0]
    original_ratio = original_width / original_height
    
    # Calcul des dimensions pour conserver le ratio
    if original_ratio > 1:  # Plus large que haut
        display_width = sim_width
        display_height = int(display_width / original_ratio)
        if display_height > sim_height:
            display_height = sim_height
            display_width = int(display_height * original_ratio)
    else:  # Plus haut que large ou carré
        display_height = sim_height
        display_width = int(display_height * original_ratio)
        if display_width > sim_width:
            display_width = sim_width
            display_height = int(display_width / original_ratio)
    
    # Calcul des positions pour centrer la simulation
    display_x = menu_width + (sim_width - display_width) // 2
    display_y = (sim_height - display_height) // 2
    
    # Rectangle de bordure (liseré rouge)
    border_rect = pygame.Rect(
        display_x - 2,  # -2 pour la bordure
        display_y - 2,
        display_width + 4,  # +4 pour la bordure (2 pixels de chaque côté)
        display_height + 4
    )
    
    # Position de la matrice d'interaction (collée directement à droite de la zone de simulation)
    matrix_x = menu_width + sim_width
    matrix_y = 10
    matrix_height = sim_height - 20  # Laisser un peu d'espace en haut et en bas
    
    # Créer des noms abrégés pour les canaux dans la matrice d'interaction
    channel_names_short = ["R", "V", "B"]  # Noms très courts pour économiser de l'espace
    
    interaction_widget = InteractionMatrix(
        matrix_x, matrix_y, 
        matrix_width, matrix_height, 
        interaction_matrix,
        title="Matrice d'interaction",
        channel_names=channel_names_short  # Utiliser des noms abrégés
    )
    
    # Création de l'oscilloscope pour afficher les fonctions de croissance
    oscillo_x = menu_width
    oscillo_y = sim_height + 10  # 10 pixels de séparation avec la simulation
    oscillo_width = total_width - menu_width  # Occupe toute la largeur disponible
    
    oscilloscope = Oscilloscope(
        oscillo_x, oscillo_y, 
        oscillo_width, oscillo_height - 20,  # Laisser un peu d'espace en bas
        "Fonctions de croissance"
    )
    
    # Création de la figure matplotlib pour les statistiques si nécessaire
    figsize = (sim_width / DPI, sim_height / DPI)
    fig, ax = plt.subplots(figsize=figsize, dpi=DPI)
    
    canvas = FigureCanvas(fig)
    im = ax.imshow(np.dstack(Xs), interpolation=interpolation)
    
    # Variables pour l'affichage des informations
    font = pygame.font.SysFont('Arial', 18)
    info_font = pygame.font.SysFont('Arial', 14)
    active_growth_funcs = ["gauss"]  # Par défaut
    info_surface = None
    info_time = 0
    
    # Variables pour l'oscilloscope dynamique
    last_update_time = time.time()
    update_interval = 0.1  # Intervalle de mise à jour en secondes
    growth_params = {}  # Dictionnaire pour stocker les paramètres actuels des fonctions
    time_counter = 0  # Compteur pour suivre l'évolution du temps
    animation_speed = 0.01  # Vitesse d'animation des courbes
    
    # Plage pour afficher les fonctions
    x_range = (0, 1)
    
    # Copie locale de la matrice d'interaction pour suivre les changements
    current_interaction_matrix = interaction_matrix.copy()

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
        
        # Mise à jour du widget de matrice d'interaction
        interaction_widget.update(event_list)
        
        # Récupération des indices de kernels actifs
        active_indices = menu_manager.get_active_kernel_indices()
        
        # Récupération de la fonction de croissance active
        growth_func = menu_manager.get_active_growth_function()
        
        # Récupération des noms des fonctions de croissance actives pour l'affichage
        new_active_growth_funcs = menu_manager.get_active_growth_function_names()
        
        # Si les fonctions actives ont changé, mettre à jour l'affichage des infos
        if new_active_growth_funcs != active_growth_funcs:
            active_growth_funcs = new_active_growth_funcs
            
            # Créer une surface pour afficher les infos
            info_text = "Fonctions actives: " + ", ".join(active_growth_funcs)
            info_surface = info_font.render(info_text, True, BLACK, WHITE)
            
            # Durée d'affichage (en millisecondes)
            info_time = pygame.time.get_ticks() + 3000
        
        # Mettre à jour le compteur de temps pour l'animation des courbes
        if not paused:
            time_counter += animation_speed
        
        # Vérifier s'il est temps de mettre à jour les paramètres de l'oscilloscope
        current_time = time.time()
        if current_time - last_update_time > update_interval:
            last_update_time = current_time
            
            # Mettre à jour les paramètres des fonctions de croissance
            for name in active_growth_funcs:
                if name not in growth_params:
                    # Initialiser les paramètres pour cette fonction
                    growth_params[name] = {
                        "m": 0.15,  # Valeur moyenne initiale
                        "s": 0.015,  # Écart-type initial
                        "phase": np.random.random() * 2 * np.pi  # Phase aléatoire pour l'animation
                    }
                
                # Si des kernels sont actifs, utiliser leurs paramètres pour cette fonction
                if active_indices:
                    # Calculer la moyenne des paramètres des kernels actifs
                    avg_m = np.mean([ms[idx] for idx in active_indices])
                    avg_s = np.mean([ss[idx] for idx in active_indices])
                    
                    # Ajouter une petite variation en fonction du temps pour l'animation
                    variation_m = 0.01 * np.sin(time_counter + growth_params[name]["phase"])
                    variation_s = 0.002 * np.cos(time_counter * 1.5 + growth_params[name]["phase"])
                    
                    growth_params[name]["m"] = avg_m + variation_m
                    growth_params[name]["s"] = avg_s + variation_s
        
        # Vérifier si la matrice d'interaction a été modifiée
        new_matrix = interaction_widget.get_matrix()
        if not np.array_equal(current_interaction_matrix, new_matrix):
            # Mettre à jour la matrice d'interaction utilisée par la simulation
            current_interaction_matrix = new_matrix.copy()
        
        if not paused:
            # Évolution du système avec les kernels actifs, la fonction de croissance et la matrice d'interaction courante
            Xs = evolve(Xs, active_indices, growth_func, current_interaction_matrix)
            
            # Conversion de la simulation en image
            data = np.dstack(Xs)
            data_uint8 = (255 * np.clip(data, 0, 1)).astype(np.uint8)
            
            # Création d'une surface pygame pour la simulation
            surface = pygame.surfarray.make_surface(data_uint8.swapaxes(0, 1))
            scaled_surface = pygame.transform.smoothscale(surface, (display_width, display_height))

            # Effacer l'écran avec un fond gris neutre pour harmoniser l'interface
            screen.fill((240, 240, 240))
            
            # Dessiner un rectangle de bordure rouge autour de la zone de simulation
            pygame.draw.rect(screen, RED, border_rect, 2)
            
            # Affichage de la simulation centrée avec le ratio préservé
            screen.blit(scaled_surface, (display_x, display_y))
            
            # Affichage du widget de matrice d'interaction
            interaction_widget.draw(screen)
            
            # Affichage de l'oscilloscope
            # Récupérer les fonctions de croissance actives
            active_growth_functions = []
            active_growth_labels = []
            
            for name in active_growth_funcs:
                # Obtenir la fonction à partir du module growth_functions
                func = getattr(growth_functions, name, None)
                if func and name in growth_params:
                    # Créer une fonction qui appelle la fonction de croissance avec les paramètres dynamiques
                    def create_func_wrapper(func, params):
                        return lambda x: 2 * func(x, params["m"], params["s"]) - 1
                    
                    func_wrapper = create_func_wrapper(func, growth_params[name])
                    active_growth_functions.append(func_wrapper)
                    # Abréger les noms des fonctions si nécessaire pour l'affichage
                    label = f"{name} (m={growth_params[name]['m']:.2f}, s={growth_params[name]['s']:.3f})"
                    active_growth_labels.append(label)
            
            # Dessiner l'oscilloscope
            oscilloscope.draw(screen, active_growth_functions, active_growth_labels, x_range)
            
            # Dessiner le menu (sur fond blanc pour contraster avec le fond gris)
            # Créer une surface pour le menu
            menu_surface = pygame.Surface((menu_width, total_height))
            menu_surface.fill(WHITE)
            screen.blit(menu_surface, (0, 0))
            menu_manager.draw(screen)
            
            # Afficher les infos sur les fonctions actives si nécessaire
            if info_surface and pygame.time.get_ticks() < info_time:
                info_x = menu_width + 10
                info_y = 5
                screen.blit(info_surface, (info_x, info_y))
            
            # Ajouter un séparateur visuel entre la simulation et l'oscilloscope
            pygame.draw.line(screen, DARK_GRAY, 
                            (menu_width, sim_height), 
                            (total_width, sim_height), 1)
            
            # Ajouter un séparateur visuel entre la simulation et la matrice
            pygame.draw.line(screen, DARK_GRAY, 
                            (menu_width + sim_width, 0), 
                            (menu_width + sim_width, sim_height), 1)
            
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