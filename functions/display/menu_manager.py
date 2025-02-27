#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gestionnaire de menu
-------------------
Ce module contient les classes et fonctions pour gérer le menu latéral.
"""

import pygame
import numpy as np
from config.display_config import MENU_WIDTH, BLACK, WHITE, LIGHT_GRAY
from functions.display.ui_widgets import Button, Checkbox, Label, Panel

class GrowthFunctionManager:
    """
    Gestionnaire des fonctions de croissance.
    Gère l'état d'activation des différentes fonctions de croissance.
    """
    
    def __init__(self, kernel_list):
        """
        Initialise le gestionnaire.
        
        Args:
            kernel_list (list): Liste des kernels utilisés dans la simulation
        """
        self.kernel_list = kernel_list
        self.active_kernels = [True] * len(kernel_list)  # Par défaut, tous les kernels sont actifs
        
    def toggle_kernel(self, index, state):
        """
        Active ou désactive un kernel.
        
        Args:
            index (int): Indice du kernel à modifier
            state (bool): Nouvel état du kernel (True=actif, False=inactif)
        """
        if 0 <= index < len(self.active_kernels):
            self.active_kernels[index] = state
            
    def get_active_kernels(self):
        """
        Retourne la liste des kernels actifs.
        
        Returns:
            list: Liste des kernels actifs
        """
        return [k for k, a in zip(self.kernel_list, self.active_kernels) if a]
    
    def get_active_indices(self):
        """
        Retourne les indices des kernels actifs.
        
        Returns:
            list: Liste des indices des kernels actifs
        """
        return [i for i, a in enumerate(self.active_kernels) if a]
        
class MenuManager:
    """
    Gestionnaire du menu latéral.
    Gère l'affichage et les interactions avec le menu.
    """
    
    def __init__(self, kernels, ms, ss, hs, sources, destinations):
        """
        Initialise le gestionnaire de menu.
        
        Args:
            kernels (list): Liste des kernels de la simulation
            ms (list): Liste des moyennes des fonctions de croissance
            ss (list): Liste des écarts-types des fonctions de croissance
            hs (list): Liste des hauteurs des fonctions de croissance
            sources (list): Liste des canaux sources
            destinations (list): Liste des canaux destinations
        """
        self.growth_manager = GrowthFunctionManager(kernels)
        self.ms = ms
        self.ss = ss
        self.hs = hs
        self.sources = sources
        self.destinations = destinations
        
        # Police pour le texte
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.font = pygame.font.SysFont('Arial', 16)
        
        # Widgets
        self.panel = Panel(0, 0, MENU_WIDTH, pygame.display.get_surface().get_height(), LIGHT_GRAY)
        self.title = Label(20, 20, "Fonctions de croissance", self.title_font)
        
        # Créer les checkboxes pour chaque kernel
        self.checkboxes = []
        for i, (m, s, h, src, dst) in enumerate(zip(ms, ss, hs, sources, destinations)):
            name = f"K{i}: {src}->{dst} (m={m:.2f}, h={h:.2f})"
            y_pos = 70 + i * 30
            
            # Ne pas dépasser la hauteur de l'écran
            if y_pos > pygame.display.get_surface().get_height() - 50:
                break
                
            # Créer une fonction d'action spécifique pour chaque indice
            def create_action(idx):
                def action(state):
                    self.toggle_kernel(idx, state)
                return action
                
            checkbox = Checkbox(
                20, y_pos, 20, name, self.font, 
                checked=True,
                action=create_action(i)
            )
            self.checkboxes.append(checkbox)
            
        # Bouton pour réinitialiser
        self.reset_button = Button(
            20, pygame.display.get_surface().get_height() - 60,
            MENU_WIDTH - 40, 40, "Réinitialiser", self.font,
            action=self.reset_kernels
        )
        
    def toggle_kernel(self, index, state):
        """
        Active ou désactive un kernel et met à jour l'interface.
        
        Args:
            index (int): Indice du kernel à modifier
            state (bool): Nouvel état du kernel
        """
        self.growth_manager.toggle_kernel(index, state)
        
    def reset_kernels(self):
        """Réinitialise tous les kernels à l'état actif."""
        for i in range(len(self.growth_manager.active_kernels)):
            self.growth_manager.toggle_kernel(i, True)
            
        # Mettre à jour l'état des checkboxes
        for checkbox in self.checkboxes:
            checkbox.checked = True
        
    def draw(self, surface):
        """
        Dessine le menu sur la surface.
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner le menu
        """
        # Dessiner le panneau de fond
        self.panel.draw(surface)
        
        # Dessiner le titre
        self.title.draw(surface)
        
        # Dessiner les checkboxes
        for checkbox in self.checkboxes:
            checkbox.draw(surface)
            
        # Dessiner le bouton de réinitialisation
        self.reset_button.draw(surface)
        
    def update(self, event_list):
        """
        Met à jour l'état du menu en fonction des événements.
        
        Args:
            event_list (list): Liste des événements pygame
        """
        # Mettre à jour les checkboxes
        for checkbox in self.checkboxes:
            checkbox.update(event_list)
            
        # Mettre à jour le bouton de réinitialisation
        self.reset_button.update(event_list)
        
    def get_active_kernel_indices(self):
        """
        Retourne les indices des kernels actifs.
        
        Returns:
            list: Liste des indices des kernels actifs
        """
        return self.growth_manager.get_active_indices() 