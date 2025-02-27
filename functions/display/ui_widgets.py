#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Widgets pour l'interface utilisateur
------------------------------------
Ce module contient les classes et fonctions pour créer l'interface utilisateur du menu.
"""

import pygame
from config.display_config import BLACK, WHITE, GRAY, LIGHT_GRAY, DARK_GRAY, BLUE, GREEN

class Button:
    """Un bouton cliquable pour l'interface utilisateur."""
    
    def __init__(self, x, y, width, height, text, font, action=None):
        """
        Initialise un bouton.
        
        Args:
            x (int): Position X du bouton
            y (int): Position Y du bouton
            width (int): Largeur du bouton
            height (int): Hauteur du bouton
            text (str): Texte à afficher sur le bouton
            font (pygame.font.Font): Police à utiliser pour le texte
            action (function, optional): Fonction à appeler lorsque le bouton est cliqué
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        """Dessine le bouton sur la surface."""
        color = LIGHT_GRAY if self.hovered else GRAY
        border_color = BLUE if self.hovered else DARK_GRAY
        
        # Dessiner le fond du bouton
        pygame.draw.rect(surface, color, self.rect)
        # Dessiner le bord du bouton
        pygame.draw.rect(surface, border_color, self.rect, 2)
        
        # Dessiner le texte
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, event_list):
        """Met à jour l'état du bouton en fonction des événements."""
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
                if self.action:
                    self.action()
                return True
        return False

class Checkbox:
    """Une case à cocher pour activer/désactiver une option."""
    
    def __init__(self, x, y, size, text, font, checked=True, action=None):
        """
        Initialise une case à cocher.
        
        Args:
            x (int): Position X de la case
            y (int): Position Y de la case
            size (int): Taille de la case
            text (str): Texte à afficher à côté de la case
            font (pygame.font.Font): Police à utiliser pour le texte
            checked (bool, optional): État initial (cochée ou non)
            action (function, optional): Fonction à appeler lorsque l'état change
        """
        self.rect = pygame.Rect(x, y, size, size)
        self.text = text
        self.font = font
        self.checked = checked
        self.action = action
        self.hovered = False
        self.size = size
        
    def draw(self, surface):
        """Dessine la case à cocher sur la surface."""
        border_color = BLUE if self.hovered else DARK_GRAY
        
        # Dessiner la case
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 2)
        
        # Dessiner la coche si cochée
        if self.checked:
            inner_rect = pygame.Rect(
                self.rect.x + self.size * 0.2,
                self.rect.y + self.size * 0.2,
                self.size * 0.6,
                self.size * 0.6
            )
            pygame.draw.rect(surface, GREEN, inner_rect)
        
        # Dessiner le texte
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(
            midleft=(self.rect.right + 10, self.rect.centery)
        )
        surface.blit(text_surf, text_rect)
        
    def update(self, event_list):
        """Met à jour l'état de la case à cocher en fonction des événements."""
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
                self.checked = not self.checked
                if self.action:
                    self.action(self.checked)
                return True
        return False

class Label:
    """Un simple texte à afficher dans l'interface."""
    
    def __init__(self, x, y, text, font, color=BLACK):
        """
        Initialise un label.
        
        Args:
            x (int): Position X du label
            y (int): Position Y du label
            text (str): Texte à afficher
            font (pygame.font.Font): Police à utiliser pour le texte
            color (tuple, optional): Couleur du texte
        """
        self.pos = (x, y)
        self.text = text
        self.font = font
        self.color = color
        
    def draw(self, surface):
        """Dessine le label sur la surface."""
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, self.pos)
        
class Panel:
    """Un panneau rectangulaire pour regrouper des éléments d'interface."""
    
    def __init__(self, x, y, width, height, color=LIGHT_GRAY):
        """
        Initialise un panneau.
        
        Args:
            x (int): Position X du panneau
            y (int): Position Y du panneau
            width (int): Largeur du panneau
            height (int): Hauteur du panneau
            color (tuple, optional): Couleur de fond du panneau
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
    def draw(self, surface):
        """Dessine le panneau sur la surface."""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 2) 