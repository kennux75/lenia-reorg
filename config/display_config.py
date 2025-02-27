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
width, height = 1280, 720  # Résolution en pixels de la fenêtre

# Calculer la taille de la figure en pouces pour matplotlib
figsize = (width / DPI, height / DPI)

# Initialisation de pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lenia Simulation")

# Paramètres d'interpolation pour l'affichage
DEFAULT_INTERPOLATION = 'bicubic'  # Méthode d'interpolation pour l'affichage

# Paramètres de rafraîchissement
FPS = 25  # Images par seconde pour l'animation 