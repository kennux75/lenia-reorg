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
MENU_WIDTH = 300  # Largeur du menu latéral en pixels
width, height = 1280 + MENU_WIDTH, 720  # Résolution en pixels de la fenêtre avec menu

# Calculer la taille de la figure en pouces pour matplotlib
figsize = (width / DPI, height / DPI)

# Initialisation de pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lenia Simulation")

# Couleurs pour l'interface
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 120, 215)
GREEN = (0, 180, 0)

# Paramètres d'interpolation pour l'affichage
DEFAULT_INTERPOLATION = 'bicubic'  # Méthode d'interpolation pour l'affichage

# Paramètres de rafraîchissement
FPS = 25  # Images par seconde pour l'animation 