#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gestionnaire de menu
-------------------
Ce module contient les classes et fonctions pour gérer le menu latéral.
"""

import pygame
import numpy as np
import inspect
from config.display_config import MENU_WIDTH, BLACK, WHITE, LIGHT_GRAY, RED, BLUE, GREEN, YELLOW, PURPLE
from functions.display.ui_widgets import Button, Checkbox, Label, Panel, InfoButton, ScrollablePanel
from functions.growth import growth_functions

class KernelManager:
    """
    Gestionnaire des kernels.
    Gère l'état d'activation des différents kernels.
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

class GrowthFunctionManager:
    """
    Gestionnaire des fonctions de croissance.
    Gère l'état d'activation des différentes fonctions de croissance.
    """
    
    def __init__(self):
        """Initialise le gestionnaire des fonctions de croissance."""
        # Récupérer toutes les fonctions du module growth_functions
        self.growth_functions = self._get_growth_functions()
        
        # Par défaut, seule la fonction gaussienne est active (celle utilisée actuellement)
        self.active_functions = {"gauss": True}
        for func_name in self.growth_functions:
            if func_name != "gauss":
                self.active_functions[func_name] = False
                
    def _get_growth_functions(self):
        """
        Récupère toutes les fonctions du module growth_functions.
        
        Returns:
            dict: Dictionnaire des fonctions de croissance
        """
        functions = {}
        for name, obj in inspect.getmembers(growth_functions):
            if inspect.isfunction(obj) and not name.startswith('_'):
                functions[name] = obj
        return functions
        
    def toggle_function(self, name, state):
        """
        Active ou désactive une fonction de croissance.
        
        Args:
            name (str): Nom de la fonction à modifier
            state (bool): Nouvel état de la fonction (True=actif, False=inactif)
        """
        if name in self.active_functions:
            self.active_functions[name] = state
            
    def get_active_functions(self):
        """
        Retourne les fonctions de croissance actives.
        
        Returns:
            dict: Dictionnaire des fonctions actives (nom: fonction)
        """
        return {name: func for name, func in self.growth_functions.items() 
                if self.active_functions.get(name, False)}
    
    def get_active_function_names(self):
        """
        Retourne les noms des fonctions de croissance actives.
        
        Returns:
            list: Liste des noms des fonctions actives
        """
        return [name for name, is_active in self.active_functions.items() if is_active]
    
    def get_current_growth_function(self):
        """
        Retourne la fonction de croissance à utiliser pour la simulation.
        Par défaut, on utilise gauss, mais on peut choisir une autre fonction active.
        
        Returns:
            function: Fonction de croissance à utiliser
        """
        active_funcs = self.get_active_functions()
        # Si gauss est active, on la privilégie pour la compatibilité
        if "gauss" in active_funcs:
            return active_funcs["gauss"]
        # Sinon on prend la première fonction active
        elif active_funcs:
            return next(iter(active_funcs.values()))
        # Si aucune fonction n'est active, on utilise gauss par défaut
        return self.growth_functions["gauss"]
        
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
        self.kernel_manager = KernelManager(kernels)
        self.growth_manager = GrowthFunctionManager()
        self.ms = ms
        self.ss = ss
        self.hs = hs
        self.sources = sources
        self.destinations = destinations
        
        # Police pour le texte
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 18, bold=True)
        self.font = pygame.font.SysFont('Arial', 16)
        self.small_font = pygame.font.SysFont('Arial', 14)
        
        # Hauteur totale estimée pour les kernels
        kernel_section_height = 50 + len(kernels) * 30  # Titre + checkboxes
        
        # Dimensions de la fenêtre
        screen_height = pygame.display.get_surface().get_height()
        
        # Widgets pour les kernels
        self.kernel_panel = ScrollablePanel(
            10, 60, 
            MENU_WIDTH - 20, min(400, screen_height // 2),
            kernel_section_height,
            LIGHT_GRAY
        )
        
        self.kernels_title = Label(20, 20, "Kernels", self.title_font)
        
        # Calculer la hauteur disponible pour les fonctions de croissance
        growth_section_y = self.kernel_panel.rect.bottom + 20
        growth_section_height = screen_height - growth_section_y - 70  # Espace pour le bouton en bas
        
        # Widgets pour les fonctions de croissance
        self.growth_panel = Panel(
            10, growth_section_y, 
            MENU_WIDTH - 20, growth_section_height,
            LIGHT_GRAY
        )
        
        self.growth_title = Label(20, growth_section_y + 10, "Fonctions de croissance", self.title_font)
        
        # Créer les checkboxes pour chaque kernel
        self.kernel_checkboxes = []
        self.kernel_info_buttons = []
        
        for i, (m, s, h, src, dst) in enumerate(zip(ms, ss, hs, sources, destinations)):
            name = f"K{i}: {src}->{dst} (m={m:.2f}, h={h:.2f})"
            y_pos = 70 + i * 30
            
            # Créer une fonction d'action spécifique pour chaque indice
            def create_action(idx):
                def action(state):
                    self.toggle_kernel(idx, state)
                return action
                
            checkbox = Checkbox(
                30, y_pos, 20, name, self.font, 
                checked=True,
                action=create_action(i)
            )
            self.kernel_checkboxes.append(checkbox)
            
            # Créer un bouton d'information pour chaque kernel
            info_text = (
                f"Kernel {i}\n"
                f"Canal source: {src}\n"
                f"Canal destination: {dst}\n"
                f"Moyenne (m): {m:.4f}\n"
                f"Écart-type (s): {s:.4f}\n"
                f"Hauteur (h): {h:.4f}\n"
                f"Contribution: {h:.2f} * (2*gauss(U, {m:.2f}, {s:.2f}) - 1)"
            )
            
            info_button = InfoButton(
                MENU_WIDTH - 40, y_pos, 20, 
                self.font, info_text, self.small_font
            )
            self.kernel_info_buttons.append(info_button)
            
        # Créer les checkboxes pour chaque fonction de croissance
        self.growth_checkboxes = []
        y_offset = growth_section_y + 50
        
        for i, func_name in enumerate(self.growth_manager.growth_functions.keys()):
            # La fonction gauss est cochée par défaut
            is_default = (func_name == "gauss")
            
            def create_action(name):
                def action(state):
                    self.toggle_growth_function(name, state)
                return action
                
            checkbox = Checkbox(
                30, y_offset + i * 30, 20, 
                func_name, self.font, 
                checked=is_default,
                action=create_action(func_name)
            )
            self.growth_checkboxes.append(checkbox)
            
        # Bouton pour réinitialiser
        self.reset_button = Button(
            20, screen_height - 60,
            MENU_WIDTH - 40, 40, "Réinitialiser", self.font,
            action=self.reset_all
        )
        
    def toggle_kernel(self, index, state):
        """
        Active ou désactive un kernel et met à jour l'interface.
        
        Args:
            index (int): Indice du kernel à modifier
            state (bool): Nouvel état du kernel
        """
        self.kernel_manager.toggle_kernel(index, state)
        
    def toggle_growth_function(self, name, state):
        """
        Active ou désactive une fonction de croissance.
        
        Args:
            name (str): Nom de la fonction à modifier
            state (bool): Nouvel état de la fonction
        """
        self.growth_manager.toggle_function(name, state)
        
    def reset_all(self):
        """Réinitialise tous les kernels et les fonctions de croissance."""
        # Réinitialiser les kernels
        for i in range(len(self.kernel_manager.active_kernels)):
            self.kernel_manager.toggle_kernel(i, True)
            
        # Mettre à jour l'état des checkboxes
        for checkbox in self.kernel_checkboxes:
            checkbox.checked = True
            
        # Réinitialiser les fonctions de croissance (seule gauss active)
        for name in self.growth_manager.active_functions:
            self.growth_manager.toggle_function(name, name == "gauss")
            
        # Mettre à jour l'état des checkboxes
        for checkbox in self.growth_checkboxes:
            checkbox.checked = checkbox.text == "gauss"
        
    def draw(self, surface):
        """
        Dessine le menu sur la surface.
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner le menu
        """
        # Titre principal
        self.kernels_title.draw(surface)
        
        # Panneau des kernels
        self.kernel_panel.draw(surface)
        content_rect = self.kernel_panel.get_content_rect()
        
        # Dessiner les checkboxes et boutons d'info des kernels
        for i, (checkbox, info_button) in enumerate(zip(self.kernel_checkboxes, self.kernel_info_buttons)):
            y_pos = 70 + i * 30
            
            # Vérifier si l'élément est visible dans le panneau défilant
            if self.kernel_panel.is_visible(y_pos):
                # Ajuster la position pour le défilement
                adjusted_y = y_pos - self.kernel_panel.scroll_y
                
                # Créer des copies temporaires des widgets à la position ajustée
                temp_checkbox = Checkbox(
                    checkbox.rect.x, adjusted_y, 
                    checkbox.size, checkbox.text, 
                    checkbox.font, checkbox.checked
                )
                temp_checkbox.draw(surface)
                
                temp_info_button = InfoButton(
                    info_button.rect.x, adjusted_y, 
                    info_button.rect.width, 
                    info_button.font, 
                    info_button.popup_content, 
                    info_button.popup_font
                )
                temp_info_button.popup_visible = info_button.popup_visible
                temp_info_button.draw(surface)
        
        # Titre des fonctions de croissance
        self.growth_title.draw(surface)
        
        # Panneau des fonctions de croissance
        self.growth_panel.draw(surface)
        
        # Dessiner les checkboxes des fonctions de croissance
        for checkbox in self.growth_checkboxes:
            checkbox.draw(surface)
            
        # Dessiner le bouton de réinitialisation
        self.reset_button.draw(surface)
        
    def update(self, event_list):
        """
        Met à jour l'état du menu en fonction des événements.
        
        Args:
            event_list (list): Liste des événements pygame
        """
        # Mettre à jour le panneau défilant
        self.kernel_panel.update(event_list)
        
        # Mettre à jour les checkboxes et boutons d'info des kernels
        for i, (checkbox, info_button) in enumerate(zip(self.kernel_checkboxes, self.kernel_info_buttons)):
            y_pos = 70 + i * 30
            
            # Vérifier si l'élément est visible et ajuster sa position
            if self.kernel_panel.is_visible(y_pos):
                adjusted_y = y_pos - self.kernel_panel.scroll_y
                
                # Déplacer temporairement les widgets pour l'interaction
                original_rect = checkbox.rect.copy()
                checkbox.rect.y = adjusted_y
                checkbox.update(event_list)
                checkbox.rect = original_rect
                
                original_rect = info_button.rect.copy()
                info_button.rect.y = adjusted_y
                info_button.update(event_list)
                info_button.rect = original_rect
            
        # Mettre à jour les checkboxes des fonctions de croissance
        for checkbox in self.growth_checkboxes:
            checkbox.update(event_list)
            
        # Mettre à jour le bouton de réinitialisation
        self.reset_button.update(event_list)
        
    def get_active_kernel_indices(self):
        """
        Retourne les indices des kernels actifs.
        
        Returns:
            list: Liste des indices des kernels actifs
        """
        return self.kernel_manager.get_active_indices()
    
    def get_active_growth_function(self):
        """
        Retourne la fonction de croissance active.
        
        Returns:
            function: Fonction de croissance à utiliser
        """
        return self.growth_manager.get_current_growth_function()
    
    def get_active_growth_function_names(self):
        """
        Retourne les noms des fonctions de croissance actives.
        
        Returns:
            list: Liste des noms des fonctions actives
        """
        return self.growth_manager.get_active_function_names() 