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
import sys

from config.display_config import DPI, width, height, screen, FPS, DEFAULT_INTERPOLATION, MENU_WIDTH, WHITE, BLACK, RED, DARK_GRAY
from data.creatures import inject_aquarium, init_grid
from functions.display.menu_manager import MenuManager
from functions.display.ui_widgets import Oscilloscope, InteractionMatrix, Button
from config.simulation_config import kernels, ms, ss, hs, sources, destinations, interaction_matrix
from functions.growth import growth_functions

def produce_movie_multi(Xs, evolve, interpolation=DEFAULT_INTERPOLATION):
    """
    Produit une animation de la simulation Lenia avec plusieurs canaux dans une grande fenêtre
    divisée en 4 zones distinctes.
    
    Args:
        Xs (list): Liste des grilles pour chaque canal
        evolve (function): Fonction d'évolution à utiliser
        interpolation (str, optional): Méthode d'interpolation pour l'affichage. Par défaut DEFAULT_INTERPOLATION.
    """
    # Initialisation de pygame
    if not pygame.get_init():
        pygame.init()
    
    # Dimensions de la fenêtre principale
    window_width = 1500
    window_height = 950
    
    # Dimensions et positions des 4 zones pour simuler des fenêtres séparées
    sim_width, sim_height = 750, 600
    menu_width, menu_height = 350, 600
    matrix_width, matrix_height = 400, 600
    oscillo_width, oscillo_height = 1500, 350
    
    # Positions des zones
    sim_x, sim_y = 0, 0
    menu_x, menu_y = sim_width, 0
    matrix_x, matrix_y = sim_width + menu_width, 0
    oscillo_x, oscillo_y = 0, sim_height
    
    # Création d'une seule grande fenêtre
    pygame.display.set_caption("Simulation Lenia - Environnement Multi-Vues")
    screen = pygame.display.set_mode((window_width, window_height))
    
    # Variables partagées
    paused = False
    running = True
    clock = pygame.time.Clock()
    
    # Initialisation du gestionnaire de menu
    # Créer un menu directement positionné à la bonne position
    menu_manager = MenuManager(kernels, ms, ss, hs, sources, destinations, menu_width=menu_width, 
                               offset_x=menu_x, offset_y=menu_y)
    
    # Créer des noms abrégés pour les canaux dans la matrice d'interaction
    channel_names_short = ["R", "V", "B"]  # Noms très courts pour économiser de l'espace
    
    # Initialisation de la matrice d'interaction
    interaction_widget = InteractionMatrix(
        matrix_x + 10, matrix_y + 10, 
        matrix_width - 20, matrix_height - 20, 
        interaction_matrix,
        title="Matrice d'interaction",
        channel_names=channel_names_short
    )
    
    # Création de l'oscilloscope
    oscilloscope = Oscilloscope(
        oscillo_x + 10, oscillo_y + 10, 
        oscillo_width - 20, oscillo_height - 60,  # Laisser de l'espace pour les boutons
        "Fonctions de croissance",
        history_size=50
    )
    
    # Boutons pour contrôler l'historique de l'oscilloscope
    button_font = pygame.font.SysFont('Arial', 12)
    toggle_history_button = Button(
        oscillo_x + 20, oscillo_y + oscillo_height - 40, 
        120, 20, 
        "Activer/Désactiver historique", button_font, 
        lambda: oscilloscope.toggle_history()
    )
    
    clear_history_button = Button(
        oscillo_x + 150, oscillo_y + oscillo_height - 40, 
        100, 20, 
        "Effacer historique", button_font, 
        lambda: oscilloscope.clear_history()
    )
    
    # Variables pour l'oscilloscope dynamique
    active_growth_funcs = ["gauss"]  # Par défaut
    last_update_time = time.time()
    update_interval = 0.1  # Intervalle de mise à jour en secondes
    growth_params = {}  # Dictionnaire pour stocker les paramètres actuels des fonctions
    time_counter = 0  # Compteur pour suivre l'évolution du temps
    animation_speed = 0.01  # Vitesse d'animation des courbes
    x_range = (0, 1)
    active_indices = []
    growth_func = None
    
    # Calcul du ratio original et des dimensions pour maintenir ce ratio
    original_width = Xs[0].shape[1]
    original_height = Xs[0].shape[0]
    original_ratio = original_width / original_height
    
    # Calcul des dimensions pour conserver le ratio
    if original_ratio > 1:  # Plus large que haut
        display_width = sim_width - 20  # Marge de 10px de chaque côté
        display_height = int(display_width / original_ratio)
        if display_height > sim_height - 20:
            display_height = sim_height - 20
            display_width = int(display_height * original_ratio)
    else:  # Plus haut que large ou carré
        display_height = sim_height - 20
        display_width = int(display_height * original_ratio)
        if display_width > sim_width - 20:
            display_width = sim_width - 20
            display_height = int(display_width / original_ratio)
    
    # Calcul des positions pour centrer la simulation
    display_x = sim_x + (sim_width - display_width) // 2
    display_y = sim_y + (sim_height - display_height) // 2
    
    # Rectangle de bordure (liseré rouge)
    border_rect = pygame.Rect(
        display_x - 2,  # -2 pour la bordure
        display_y - 2,
        display_width + 4,  # +4 pour la bordure (2 pixels de chaque côté)
        display_height + 4
    )
    
    # Informations pour l'affichage
    font = pygame.font.SysFont('Arial', 18)
    title_font = pygame.font.SysFont('Arial', 20, bold=True)
    
    # Création des rectangles pour délimiter les zones
    sim_rect = pygame.Rect(sim_x, sim_y, sim_width, sim_height)
    menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    matrix_rect = pygame.Rect(matrix_x, matrix_y, matrix_width, matrix_height)
    oscillo_rect = pygame.Rect(oscillo_x, oscillo_y, oscillo_width, oscillo_height)
    
    # Boucle principale
    while running:
        # Collecter tous les événements une seule fois
        events = pygame.event.get()
        
        # Construire une liste d'événements originale pour les widgets
        event_list = []
        
        # Traitement des événements
        for event in events:
            # Créer une copie de l'événement pour la liste
            event_copy = pygame.event.Event(event.type, event.__dict__)
            event_list.append(event_copy)
            
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_a:  # Si la touche 'a' est pressée
                    Xs = inject_aquarium(Xs)
                if event.key == pygame.K_r:  # Si la touche 'r' est pressée
                    Xs = init_grid()
                    oscilloscope.clear_history()
                    menu_manager.reset_all()
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Effacer l'écran avec un fond gris neutre
        screen.fill((240, 240, 240))
        
        # Dessiner les séparateurs entre les zones
        pygame.draw.line(screen, BLACK, (sim_width, 0), (sim_width, sim_height), 2)
        pygame.draw.line(screen, BLACK, (sim_width + menu_width, 0), (sim_width + menu_width, sim_height), 2)
        pygame.draw.line(screen, BLACK, (0, sim_height), (window_width, sim_height), 2)
        
        # Dessiner les titres de chaque zone
        sim_title = title_font.render("Simulation", True, BLACK)
        menu_title = title_font.render("Menu", True, BLACK)
        matrix_title = title_font.render("Matrice d'interaction", True, BLACK)
        oscillo_title = title_font.render("Oscilloscope", True, BLACK)
        
        screen.blit(sim_title, (sim_x + 10, sim_y + 10))
        screen.blit(menu_title, (menu_x + 10, menu_y + 10))
        screen.blit(matrix_title, (matrix_x + 10, matrix_y + 10))
        screen.blit(oscillo_title, (oscillo_x + 10, oscillo_y + 10))
        
        # ========= RENDU DE LA ZONE DE SIMULATION =========
        # Zone de fond pour la simulation (blanc)
        pygame.draw.rect(screen, WHITE, sim_rect)
        
        # Dessiner un rectangle de bordure rouge autour de la zone de simulation
        pygame.draw.rect(screen, RED, border_rect, 2)
        
        # Conversion de la simulation en image
        data = np.dstack(Xs)
        data_uint8 = (255 * np.clip(data, 0, 1)).astype(np.uint8)
        
        # Création d'une surface pygame pour la simulation
        surface = pygame.surfarray.make_surface(data_uint8.swapaxes(0, 1))
        scaled_surface = pygame.transform.smoothscale(surface, (display_width, display_height))
        
        # Affichage de la simulation centrée
        screen.blit(scaled_surface, (display_x, display_y))
        
        # Affichage du statut de pause
        status_text = "PAUSE" if paused else "EN COURS"
        status_surface = font.render(status_text, True, BLACK)
        screen.blit(status_surface, (sim_x + 10, sim_y + 40))
        
        # ========= RENDU DE LA ZONE DE MENU =========
        # Zone de fond pour le menu (blanc)
        pygame.draw.rect(screen, WHITE, menu_rect)
        
        # ========= MISE À JOUR DU MENU =========
        # Mise à jour du menu avec les événements originaux
        menu_manager.update(event_list)
        
        # Dessiner le menu directement sur l'écran
        menu_manager.draw(screen)
        
        # Récupération des indices de kernels actifs
        active_indices = menu_manager.get_active_kernel_indices()
        
        # Récupération de la fonction de croissance active
        growth_func = menu_manager.get_active_growth_function()
        
        # Récupération des noms des fonctions de croissance actives
        active_growth_funcs = menu_manager.get_active_growth_function_names()
        
        # ========= MISE À JOUR DE LA MATRICE D'INTERACTION =========
        # Mise à jour du widget de matrice d'interaction
        interaction_widget.update(event_list)
        
        # ========= RENDU DE LA ZONE DE MATRICE =========
        # Zone de fond pour la matrice (blanc)
        pygame.draw.rect(screen, WHITE, matrix_rect)
        
        # Vérifier si la matrice d'interaction a été modifiée
        current_interaction_matrix = interaction_widget.get_matrix()
        
        # Affichage du widget de matrice d'interaction
        interaction_widget.draw(screen)
        
        # ========= MISE À JOUR DE LA SIMULATION =========
        if not paused and growth_func is not None and active_indices:
            # Évolution du système avec les kernels actifs, la fonction de croissance et la matrice d'interaction
            Xs = evolve(Xs, active_indices, growth_func, current_interaction_matrix)
            
            # Mettre à jour le compteur de temps pour l'animation des courbes
            time_counter += animation_speed
        
        # ========= MISE À JOUR DE L'OSCILLOSCOPE =========
        # Zone de fond pour l'oscilloscope (blanc)
        pygame.draw.rect(screen, WHITE, oscillo_rect)
        
        # Mise à jour des boutons de contrôle de l'historique
        toggle_history_button.update(event_list)
        clear_history_button.update(event_list)
        
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
        
        # Dessiner l'oscilloscope avec l'historique
        oscilloscope.draw(screen, active_growth_functions, active_growth_labels, x_range)
        
        # Dessiner les boutons de contrôle de l'historique
        toggle_history_button.draw(screen)
        clear_history_button.draw(screen)
        
        # Mise à jour de l'affichage
        pygame.display.flip()
        
        # Contrôle de la fréquence d'images
        clock.tick(FPS)
    
    # Fermeture de pygame
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