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
        return [k for i, k in enumerate(self.kernel_list) if self.active_kernels[i]]
    
    def get_active_indices(self):
        """
        Retourne les indices des kernels actifs.
        
        Returns:
            list: Liste des indices des kernels actifs
        """
        return [i for i, active in enumerate(self.active_kernels) if active]

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
    
    def __init__(self, kernels, ms, ss, hs, sources, destinations, menu_width=None):
        """
        Initialise le gestionnaire de menu.
        
        Args:
            kernels (list): Liste des kernels de la simulation
            ms (list): Liste des moyennes des fonctions de croissance
            ss (list): Liste des écarts-types des fonctions de croissance
            hs (list): Liste des hauteurs des fonctions de croissance
            sources (list): Liste des canaux sources
            destinations (list): Liste des canaux destinations
            menu_width (int, optional): Largeur du menu en pixels. Si None, utilise MENU_WIDTH de config.
        """
        self.kernel_manager = KernelManager(kernels)
        self.growth_manager = GrowthFunctionManager()
        self.ms = ms
        self.ss = ss
        self.hs = hs
        self.sources = sources
        self.destinations = destinations
        
        # Utiliser la largeur spécifiée ou la valeur par défaut
        from config.display_config import MENU_WIDTH
        self.menu_width = menu_width if menu_width is not None else MENU_WIDTH
        
        # Initialisation des polices
        self.title_font = pygame.font.SysFont('Arial', 18, bold=True)
        self.font = pygame.font.SysFont('Arial', 14)
        self.small_font = pygame.font.SysFont('Arial', 12)
        self.info_font = pygame.font.SysFont('Arial', 11)  # Police pour les popups d'information
        
        # Descriptions des paramètres des kernels
        self.kernel_descriptions = [
            f"Kernel {i}:\n"
            f"- Canal source: {self.sources[i]}\n"
            f"- Canal destination: {self.destinations[i]}\n"
            f"- Fonction: Convolution 2D\n"
            f"- Rôle: Définit comment le canal {self.sources[i]} influence le canal {self.destinations[i]}\n"
            f"- Paramètres: Taille, forme et intensité du noyau"
            for i in range(len(kernels))
        ]
        
        # Création des éléments d'interface
        self._create_ui_elements()
    
    def _create_ui_elements(self):
        """Crée les éléments d'interface du menu."""
        # Titre du menu
        self.title = Label(10, 10, "Menu Lenia", self.title_font)
        
        # Titre de la section des kernels
        self.kernels_title = Label(10, 40, "Kernels actifs", self.title_font)
        
        # Calcul des hauteurs de contenu
        kernel_count = len(self.kernel_manager.get_active_indices())
        kernel_item_height = 40  # Augmenté de 30 à 40 pour plus d'espace
        kernels_content_height = kernel_count * kernel_item_height
        
        all_growth_functions = list(self.growth_manager.growth_functions.keys())
        growth_item_height = 30
        growth_content_height = len(all_growth_functions) * growth_item_height
        
        # Calcul de l'espace disponible
        total_available_height = 950 - (40 + 30 + 30 + 50) - 60
        min_panel_height = 200
        
        # Répartition équilibrée de l'espace
        if total_available_height >= 2 * min_panel_height:
            total_content = kernels_content_height + growth_content_height
            if total_content > 0:
                kernel_ratio = kernels_content_height / total_content
                growth_ratio = growth_content_height / total_content
                
                kernel_panel_height = max(min_panel_height, int(total_available_height * kernel_ratio))
                growth_panel_height = max(min_panel_height, int(total_available_height * growth_ratio))
                
                if kernel_panel_height + growth_panel_height > total_available_height:
                    excess = (kernel_panel_height + growth_panel_height) - total_available_height
                    kernel_panel_height -= int(excess * kernel_ratio)
                    growth_panel_height -= int(excess * growth_ratio)
            else:
                kernel_panel_height = total_available_height // 2
                growth_panel_height = total_available_height // 2
        else:
            kernel_panel_height = min(min_panel_height, total_available_height // 2)
            growth_panel_height = min(min_panel_height, total_available_height // 2)
        
        # Panneau défilant pour les kernels
        self.kernels_panel = ScrollablePanel(
            10, 70, 
            self.menu_width - 20, kernel_panel_height, 
            kernels_content_height
        )
        
        # Checkboxes et boutons d'information pour chaque kernel
        self.kernel_checkboxes = []
        self.kernel_info_buttons = []
        
        for i in range(kernel_count):
            # Créer une fonction d'action pour ce kernel
            def create_action(idx):
                def action(state):
                    self.toggle_kernel(idx, state)
                return action
            
            # Créer la checkbox avec un texte plus descriptif
            checkbox = Checkbox(
                20, 10 + i * kernel_item_height, 
                20, f"Kernel {i} ({self.sources[i]} → {self.destinations[i]})", 
                self.small_font, True, create_action(i)
            )
            
            # Créer le bouton d'information
            info_button = InfoButton(
                self.menu_width - 50, 10 + i * kernel_item_height, 
                20, self.small_font, 
                self.kernel_descriptions[i], self.info_font
            )
            
            self.kernel_checkboxes.append(checkbox)
            self.kernel_info_buttons.append(info_button)
        
        # Titre de la section des fonctions de croissance
        self.growth_title = Label(10, self.kernels_panel.rect.bottom + 20, "Fonctions de croissance", self.title_font)
        
        # Panneau défilant pour les fonctions de croissance
        self.growth_panel = ScrollablePanel(
            10, self.growth_title.pos[1] + 30, 
            self.menu_width - 20, growth_panel_height, 
            growth_content_height
        )
        
        # Checkboxes pour chaque fonction de croissance
        self.growth_checkboxes = []
        
        for i, name in enumerate(all_growth_functions):
            # Créer une fonction d'action pour cette fonction de croissance
            def create_action(name):
                def action(state):
                    self.toggle_growth_function(name, state)
                return action
            
            # Vérifier si la fonction est active
            is_active = self.growth_manager.active_functions.get(name, False)
            
            # Créer la checkbox
            checkbox = Checkbox(
                20, 10 + i * growth_item_height, 
                20, name, 
                self.small_font, is_active, create_action(name)
            )
            
            self.growth_checkboxes.append(checkbox)
        
        # Bouton de réinitialisation
        self.reset_button = Button(
            10, self.growth_panel.rect.bottom + 20, 
            self.menu_width - 20, 30, 
            "Réinitialiser", self.font, self.reset_all
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
        self.title.draw(surface)
        
        # Titre de la section des kernels
        self.kernels_title.draw(surface)
        
        # Panneau des kernels
        self.kernels_panel.draw(surface)
        content_rect = self.kernels_panel.get_content_rect()
        
        # Dessiner les checkboxes et boutons d'information des kernels
        for i, (checkbox, info_button) in enumerate(zip(self.kernel_checkboxes, self.kernel_info_buttons)):
            y_pos = content_rect.top + i * 40 + 10  # Ajusté pour l'espacement de 40
            
            # Vérifier si l'élément est visible dans le panneau défilant
            if self.kernels_panel.is_visible(y_pos):
                # Ajuster la position pour le défilement
                adjusted_y = y_pos - self.kernels_panel.scroll_y
                
                # Créer une copie temporaire de la checkbox à la position ajustée
                temp_checkbox = Checkbox(
                    checkbox.rect.x, adjusted_y,
                    checkbox.size, checkbox.text,
                    checkbox.font, checkbox.checked, checkbox.action
                )
                temp_checkbox.draw(surface)
                
                # Créer une copie temporaire du bouton d'information à la position ajustée
                temp_info_button = InfoButton(
                    info_button.rect.x, adjusted_y,
                    info_button.rect.width, info_button.font,
                    info_button.popup_content, info_button.popup_font
                )
                temp_info_button.popup_visible = info_button.popup_visible
                temp_info_button.draw(surface)
        
        # Titre de la section des fonctions de croissance
        self.growth_title.draw(surface)
        
        # Panneau des fonctions de croissance
        self.growth_panel.draw(surface)
        growth_content_rect = self.growth_panel.get_content_rect()
        
        # Dessiner les checkboxes des fonctions de croissance
        for i, checkbox in enumerate(self.growth_checkboxes):
            y_pos = growth_content_rect.top + i * 30 + 10
            
            # Vérifier si l'élément est visible dans le panneau défilant
            if self.growth_panel.is_visible(y_pos):
                # Ajuster la position pour le défilement
                adjusted_y = y_pos - self.growth_panel.scroll_y
                
                # Créer une copie temporaire de la checkbox à la position ajustée
                temp_checkbox = Checkbox(
                    checkbox.rect.x, adjusted_y,
                    checkbox.size, checkbox.text,
                    checkbox.font, checkbox.checked, checkbox.action
                )
                temp_checkbox.draw(surface)
        
        # Bouton de réinitialisation
        self.reset_button.draw(surface)
        
    def update(self, event_list):
        """
        Met à jour l'état du menu en fonction des événements.
        
        Args:
            event_list (list): Liste des événements pygame
        """
        # Mettre à jour le panneau défilant des kernels
        self.kernels_panel.update(event_list)
        
        # Mettre à jour le panneau défilant des fonctions de croissance
        self.growth_panel.update(event_list)
        
        # Mettre à jour les checkboxes et boutons d'information des kernels
        content_rect = self.kernels_panel.get_content_rect()
        for i, (checkbox, info_button) in enumerate(zip(self.kernel_checkboxes, self.kernel_info_buttons)):
            y_pos = content_rect.top + i * 40 + 10  # Ajusté pour l'espacement de 40
            
            # Vérifier si l'élément est visible et ajuster sa position
            if self.kernels_panel.is_visible(y_pos):
                adjusted_y = y_pos - self.kernels_panel.scroll_y
                
                # Déplacer temporairement la checkbox pour l'interaction
                temp_checkbox = Checkbox(
                    checkbox.rect.x, adjusted_y,
                    checkbox.size, checkbox.text,
                    checkbox.font, checkbox.checked, checkbox.action
                )
                
                # Mettre à jour la checkbox temporaire et reporter l'état sur l'originale
                if temp_checkbox.update(event_list):
                    checkbox.checked = temp_checkbox.checked
                
                # Déplacer temporairement le bouton d'information pour l'interaction
                temp_info_button = InfoButton(
                    info_button.rect.x, adjusted_y,
                    info_button.rect.width, info_button.font,
                    info_button.popup_content, info_button.popup_font
                )
                temp_info_button.popup_visible = info_button.popup_visible
                
                # Mettre à jour le bouton d'information temporaire et reporter l'état sur l'original
                temp_info_button.update(event_list)
                info_button.popup_visible = temp_info_button.popup_visible
        
        # Mettre à jour les checkboxes des fonctions de croissance
        growth_content_rect = self.growth_panel.get_content_rect()
        for i, checkbox in enumerate(self.growth_checkboxes):
            y_pos = growth_content_rect.top + i * 30 + 10
            
            # Vérifier si l'élément est visible et ajuster sa position
            if self.growth_panel.is_visible(y_pos):
                adjusted_y = y_pos - self.growth_panel.scroll_y
                
                # Déplacer temporairement la checkbox pour l'interaction
                temp_checkbox = Checkbox(
                    checkbox.rect.x, adjusted_y,
                    checkbox.size, checkbox.text,
                    checkbox.font, checkbox.checked, checkbox.action
                )
                
                # Mettre à jour la checkbox temporaire et reporter l'état sur l'originale
                if temp_checkbox.update(event_list):
                    checkbox.checked = temp_checkbox.checked
        
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