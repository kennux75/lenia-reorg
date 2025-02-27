#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration de l'affichage
----------------------------
Ce fichier contient les paramètres de configuration pour l'affichage de la simulation.
"""

import pygame

# Paramètres d'affichage
DPI = 100  # DPI de la fenêtre (dots per inch)
MENU_WIDTH = 350  # Largeur du menu latéral en pixels (augmenté de 300 à 350)
MAX_WINDOW_WIDTH = 2000  # Largeur maximale de la fenêtre (augmentée de 1800 à 2000)
width, height = min(1600, MAX_WINDOW_WIDTH), 950  # Résolution en pixels de la fenêtre avec menu (augmenté de 1500 à 1600)
width = min(width, MAX_WINDOW_WIDTH - MENU_WIDTH)  # Ajuster la largeur dans les limites

# Calculer la taille de la figure en pouces pour matplotlib
figsize = (width / DPI, height / DPI)

# Initialisation de pygame
pygame.init()
screen = pygame.display.set_mode((width + MENU_WIDTH, height))
pygame.display.set_caption("Lenia Simulation - Interactions multi-canaux")

# Couleurs pour l'interface
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 120, 215)
GREEN = (0, 180, 0)
RED = (200, 50, 50)
YELLOW = (230, 200, 40)
PURPLE = (150, 50, 150)

# Paramètres pour les popups
POPUP_PADDING = 10
POPUP_BORDER_WIDTH = 2
POPUP_BACKGROUND = (250, 250, 250)
POPUP_BORDER = DARK_GRAY

# Paramètres d'interpolation pour l'affichage
DEFAULT_INTERPOLATION = 'bicubic'  # Méthode d'interpolation pour l'affichage

# Paramètres de rafraîchissement
FPS = 25  # Images par seconde pour l'animation 