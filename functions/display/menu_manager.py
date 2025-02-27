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
    
    def __init__(self, kernels, ms, ss, hs, sources, destinations, menu_width=None, offset_x=0, offset_y=0):
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
            offset_x (int, optional): Décalage horizontal du menu. Par défaut 0.
            offset_y (int, optional): Décalage vertical du menu. Par défaut 0.
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
        
        # Décalages pour le positionnement
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        # Initialisation des polices
        self.title_font = pygame.font.SysFont('Arial', 18, bold=True)
        self.font = pygame.font.SysFont('Arial', 14)
        self.small_font = pygame.font.SysFont('Arial', 12)
        self.info_font = pygame.font.SysFont('Arial', 11)  # Police pour les popups d'information
        
        # Descriptions détaillées des paramètres des kernels
        self.kernel_descriptions = [
            f"Kernel {i} - Détails:\n"
            f"- Canal source: {self.sources[i]}\n"
            f"- Canal destination: {self.destinations[i]}\n"
            f"- Fonction: Convolution 2D\n"
            f"- Rôle: Définit comment le canal {self.sources[i]} influence le canal {self.destinations[i]}\n"
            f"- Moyenne (m): {self.ms[i]:.3f} - Détermine le centre de la fonction de réponse\n"
            f"- Écart-type (s): {self.ss[i]:.3f} - Contrôle la largeur de la fonction de réponse\n"
            f"- Hauteur (h): {self.hs[i]:.3f} - Amplitude de l'effet\n"
            f"- Effet: {self._get_kernel_effect_description(i)}"
            for i in range(len(kernels))
        ]
        
        # Création des éléments d'interface
        self._create_ui_elements()
    
    def _create_ui_elements(self):
        """Crée les éléments d'interface du menu."""
        # Titre du menu
        self.title = Label(self.offset_x + 10, self.offset_y + 10, "Menu Lenia", self.title_font)
        
        # Titre de la section des kernels
        self.kernels_title = Label(self.offset_x + 10, self.offset_y + 40, "Kernels actifs", self.title_font)
        
        # Calcul des hauteurs de contenu
        kernel_count = len(self.kernel_manager.kernel_list)
        kernel_item_height = 50  # Augmenté de 40 à 50 pour plus d'espace
        kernels_content_height = kernel_count * kernel_item_height
        
        all_growth_functions = list(self.growth_manager.growth_functions.keys())
        growth_item_height = 30
        growth_content_height = len(all_growth_functions) * growth_item_height
        
        # Calcul de l'espace disponible
        total_available_height = 600 - (40 + 30 + 30 + 50) - 60
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
            self.offset_x + 10, self.offset_y + 70, 
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
                    self.kernel_manager.toggle_kernel(idx, state)
                return action
            
            # Créer une checkbox à la position relative par rapport au panneau
            checkbox = Checkbox(
                10, i * kernel_item_height + 5, 
                f"Kernel {i} - {self.sources[i]} → {self.destinations[i]}", 
                self.font, create_action(i),
                True  # Tous les kernels sont actifs par défaut
            )
            
            # Créer un bouton d'information à la position relative par rapport au panneau
            info_button = InfoButton(
                self.kernels_panel.width - 30, i * kernel_item_height + 5, 
                "i", self.font, self.kernel_descriptions[i]
            )
            
            self.kernel_checkboxes.append(checkbox)
            self.kernel_info_buttons.append(info_button)
            
            # Ajouter les éléments au panneau des kernels
            self.kernels_panel.add_element(checkbox)
            self.kernels_panel.add_element(info_button)
            
            # Définir explicitement les positions originales pour aider le défilement
            checkbox._original_pos = (10, i * kernel_item_height + 5)
            info_button._original_pos = (self.kernels_panel.width - 30, i * kernel_item_height + 5)
        
        # Titre de la section des fonctions de croissance
        self.growth_func_title = Label(
            self.offset_x + 10, 
            self.offset_y + 70 + kernel_panel_height + 20, 
            "Fonctions de croissance", 
            self.title_font
        )
        
        # Panneau défilant pour les fonctions de croissance
        self.growth_panel = ScrollablePanel(
            self.offset_x + 10, 
            self.offset_y + 70 + kernel_panel_height + 50, 
            self.menu_width - 20, growth_panel_height, 
            growth_content_height
        )
        
        # Checkboxes pour chaque fonction de croissance
        self.growth_func_checkboxes = []
        
        for i, func_name in enumerate(all_growth_functions):
            # Créer une fonction d'action pour cette fonction de croissance
            def create_action(name):
                def action(state):
                    self.growth_manager.toggle_function(name, state)
                return action
            
            # Par défaut, seule la fonction gaussienne est active
            is_checked = func_name == "gauss"
            
            # Créer la checkbox à la position relative par rapport au panneau
            checkbox = Checkbox(
                10, i * growth_item_height + 5, 
                func_name, 
                self.font, create_action(func_name),
                is_checked
            )
            
            self.growth_func_checkboxes.append(checkbox)
            
            # Ajouter la checkbox au panneau des fonctions de croissance
            self.growth_panel.add_element(checkbox)
            
            # Définir explicitement la position originale
            checkbox._original_pos = (10, i * growth_item_height + 5)
        
        # Zone d'information au bas du menu (instructions, états, etc.)
        self.info_text = Label(
            self.offset_x + 10, 
            self.offset_y + 70 + kernel_panel_height + 50 + growth_panel_height + 10, 
            "Contrôles: Espace=Pause, A=Aquarium, R=Reset", 
            self.small_font, 
            color=pygame.Color(100, 100, 100)
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
        for checkbox in self.growth_func_checkboxes:
            checkbox.checked = checkbox.text == "gauss"
        
    def draw(self, surface):
        """
        Dessine le menu sur la surface fournie.
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner le menu
        """
        # Dessiner le fond du menu
        menu_rect = pygame.Rect(
            self.offset_x, self.offset_y, 
            self.menu_width, 600
        )
        pygame.draw.rect(surface, WHITE, menu_rect)
        
        # Dessiner les titres
        self.title.draw(surface)
        self.kernels_title.draw(surface)
        self.growth_func_title.draw(surface)
        self.info_text.draw(surface)
        
        # Dessiner les panneaux défilants
        self.kernels_panel.draw(surface)
        self.growth_panel.draw(surface)
        
        # Dessiner la bordure du menu
        pygame.draw.rect(surface, BLACK, menu_rect, 1)
    
    def update(self, events):
        """
        Met à jour les éléments du menu en fonction des événements.
        
        Args:
            events (list): Liste des événements pygame à traiter
        """
        # Ajuster les events pour le décalage du menu
        adjusted_events = []
        for event in events:
            if hasattr(event, 'pos'):
                original_pos = event.pos
                # Ajuster les coordonnées pour rendre l'événement relatif au menu
                # si l'événement est dans la zone du menu
                x, y = original_pos
                menu_rect = pygame.Rect(
                    self.offset_x, self.offset_y, 
                    self.menu_width, 600
                )
                
                if menu_rect.collidepoint(original_pos):
                    # L'événement est dans la zone du menu, on l'utilise
                    # Les positions sont relatives à l'élément d'interface
                    # qui va tester si l'événement le concerne
                    adjusted_event = pygame.event.Event(event.type, {**event.__dict__, 'pos': (x, y)})
                    adjusted_events.append(adjusted_event)
                else:
                    # L'événement est hors de la zone du menu, on l'ignore
                    continue
            else:
                # L'événement n'a pas de position, on le garde tel quel
                adjusted_events.append(event)
        
        # Mettre à jour les panneaux défilants avec les événements ajustés
        self.kernels_panel.update(adjusted_events)
        self.growth_panel.update(adjusted_events)
        
        # Mettre à jour les tooltips des boutons d'information
        for info_button in self.kernel_info_buttons:
            info_button.update(adjusted_events)
    
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
    
    def _get_kernel_effect_description(self, index):
        """
        Génère une description de l'effet du kernel basée sur ses paramètres.
        
        Args:
            index (int): Indice du kernel
            
        Returns:
            str: Description de l'effet du kernel
        """
        m, s, h = self.ms[index], self.ss[index], self.hs[index]
        source, dest = self.sources[index], self.destinations[index]
        
        # Déterminer le type d'effet basé sur les paramètres
        if h > 0:
            if source == dest:
                return f"Auto-activation du canal {source} (croissance)"
            else:
                return f"Activation du canal {dest} par le canal {source}"
        else:
            if source == dest:
                return f"Auto-inhibition du canal {source} (décroissance)"
            else:
                return f"Inhibition du canal {dest} par le canal {source}" 