#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Widgets pour l'interface utilisateur
------------------------------------
Ce module contient les classes et fonctions pour créer l'interface utilisateur du menu.
"""

import pygame
from config.display_config import (
    BLACK, WHITE, GRAY, LIGHT_GRAY, DARK_GRAY, BLUE, GREEN, 
    POPUP_PADDING, POPUP_BACKGROUND, POPUP_BORDER, POPUP_BORDER_WIDTH
)

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

class InfoButton(Button):
    """Un bouton d'information qui affiche un popup."""
    
    def __init__(self, x, y, size, font, popup_content, popup_font):
        """
        Initialise un bouton d'information.
        
        Args:
            x (int): Position X du bouton
            y (int): Position Y du bouton
            size (int): Taille du bouton (carré)
            font (pygame.font.Font): Police à utiliser pour le texte
            popup_content (str): Contenu à afficher dans le popup
            popup_font (pygame.font.Font): Police à utiliser pour le popup
        """
        super().__init__(x, y, size, size, "i", font, None)
        self.popup_content = popup_content
        self.popup_font = popup_font
        self.popup_visible = False
        
    def toggle_popup(self):
        """Affiche ou masque le popup."""
        self.popup_visible = not self.popup_visible
        
    def draw(self, surface):
        """Dessine le bouton et éventuellement le popup."""
        # Dessiner le bouton
        super().draw(surface)
        
        # Dessiner le popup si visible
        if self.popup_visible:
            # Calculer les dimensions du popup
            lines = self.popup_content.split('\n')
            width = max(self.popup_font.size(line)[0] for line in lines) + 2 * POPUP_PADDING
            height = sum(self.popup_font.size(line)[1] for line in lines) + 2 * POPUP_PADDING
            
            # Assurer qu'il reste dans les limites de l'écran
            screen_width, screen_height = surface.get_size()
            x = min(self.rect.right + 5, screen_width - width - 5)
            y = min(self.rect.top, screen_height - height - 5)
            
            # Créer le rectangle du popup
            popup_rect = pygame.Rect(x, y, width, height)
            
            # Dessiner le fond
            pygame.draw.rect(surface, POPUP_BACKGROUND, popup_rect)
            pygame.draw.rect(surface, POPUP_BORDER, popup_rect, POPUP_BORDER_WIDTH)
            
            # Dessiner le texte
            y_offset = y + POPUP_PADDING
            for line in lines:
                text_surf = self.popup_font.render(line, True, BLACK)
                surface.blit(text_surf, (x + POPUP_PADDING, y_offset))
                y_offset += self.popup_font.size(line)[1]
    
    def update(self, event_list):
        """Met à jour l'état du bouton et du popup."""
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered:
                    self.toggle_popup()
                    return True
                elif self.popup_visible and not self.rect.collidepoint(mouse_pos):
                    # Fermer le popup si on clique ailleurs
                    self.popup_visible = False
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
        
class ScrollablePanel(Panel):
    """Un panneau avec défilement pour afficher beaucoup d'éléments."""
    
    def __init__(self, x, y, width, height, content_height, color=LIGHT_GRAY):
        """
        Initialise un panneau défilant.
        
        Args:
            x (int): Position X du panneau
            y (int): Position Y du panneau
            width (int): Largeur du panneau
            height (int): Hauteur visible du panneau
            content_height (int): Hauteur totale du contenu
            color (tuple, optional): Couleur de fond du panneau
        """
        super().__init__(x, y, width, height, color)
        self.content_height = content_height
        self.scroll_y = 0
        self.max_scroll = max(0, content_height - height)
        self.scrollbar_width = 15 if self.max_scroll > 0 else 0
        self.dragging_scrollbar = False
        
    def update(self, event_list):
        """Met à jour l'état du panneau défilant."""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in event_list:
            # Défilement avec la molette
            if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(mouse_pos):
                self.scroll_y = max(0, min(self.max_scroll, self.scroll_y - event.y * 20))
                
            # Drag and drop de la scrollbar
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                scrollbar_rect = self._get_scrollbar_rect()
                if scrollbar_rect.collidepoint(mouse_pos):
                    self.dragging_scrollbar = True
                    
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging_scrollbar = False
                
            if event.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
                # Calcul de la nouvelle position de défilement
                if self.max_scroll > 0:
                    ratio = (mouse_pos[1] - self.rect.top) / self.rect.height
                    self.scroll_y = max(0, min(self.max_scroll, int(ratio * self.content_height)))
                    
        return False
        
    def _get_scrollbar_rect(self):
        """Retourne le rectangle de la scrollbar."""
        if self.max_scroll <= 0:
            return pygame.Rect(0, 0, 0, 0)
        
        bar_height = max(30, int(self.rect.height * (self.rect.height / self.content_height)))
        bar_y = self.rect.top + int((self.rect.height - bar_height) * (self.scroll_y / self.max_scroll))
        
        return pygame.Rect(
            self.rect.right - self.scrollbar_width, 
            bar_y, 
            self.scrollbar_width, 
            bar_height
        )
        
    def draw(self, surface):
        """Dessine le panneau et sa scrollbar."""
        # Dessiner le fond
        super().draw(surface)
        
        # Dessiner la scrollbar si nécessaire
        if self.max_scroll > 0:
            scrollbar_rect = self._get_scrollbar_rect()
            pygame.draw.rect(surface, GRAY, scrollbar_rect)
            pygame.draw.rect(surface, DARK_GRAY, scrollbar_rect, 1)
            
    def get_content_rect(self):
        """Retourne le rectangle pour dessiner le contenu."""
        return pygame.Rect(
            self.rect.left,
            self.rect.top - self.scroll_y,
            self.rect.width - self.scrollbar_width,
            self.content_height
        )
            
    def is_visible(self, y_pos):
        """Vérifie si une position Y est visible dans le panneau."""
        return (self.rect.top <= y_pos - self.scroll_y <= self.rect.bottom)
        
class DropdownMenu:
    """Un menu déroulant pour choisir parmi plusieurs options."""
    
    def __init__(self, x, y, width, height, options, font, selected_index=0, action=None):
        """
        Initialise un menu déroulant.
        
        Args:
            x (int): Position X du menu
            y (int): Position Y du menu
            width (int): Largeur du menu
            height (int): Hauteur du menu fermé
            options (list): Liste des options à afficher
            font (pygame.font.Font): Police à utiliser pour le texte
            selected_index (int, optional): Indice de l'option sélectionnée par défaut
            action (function, optional): Fonction à appeler quand une option est sélectionnée
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.font = font
        self.selected_index = selected_index
        self.action = action
        self.is_open = False
        self.hovered_index = -1
        
        # Calculer la hauteur d'une option
        self.option_height = height
        
        # Calculer le rectangle du menu déployé
        self.dropdown_rect = pygame.Rect(
            x, y + height, 
            width, len(options) * self.option_height
        )
        
    def draw(self, surface):
        """Dessine le menu déroulant."""
        # Dessiner le menu principal
        color = LIGHT_GRAY
        border_color = BLUE if self.is_open else DARK_GRAY
        
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 2)
        
        # Dessiner le texte de l'option sélectionnée
        if 0 <= self.selected_index < len(self.options):
            text = self.options[self.selected_index]
            text_surf = self.font.render(text, True, BLACK)
            text_rect = text_surf.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
            surface.blit(text_surf, text_rect)
        
        # Dessiner la flèche
        arrow_points = [
            (self.rect.right - 20, self.rect.centery - 5),
            (self.rect.right - 10, self.rect.centery + 5),
            (self.rect.right - 30, self.rect.centery + 5)
        ]
        pygame.draw.polygon(surface, BLACK, arrow_points)
        
        # Si le menu est ouvert, dessiner les options
        if self.is_open:
            pygame.draw.rect(surface, WHITE, self.dropdown_rect)
            pygame.draw.rect(surface, DARK_GRAY, self.dropdown_rect, 2)
            
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.dropdown_rect.left,
                    self.dropdown_rect.top + i * self.option_height,
                    self.dropdown_rect.width,
                    self.option_height
                )
                
                # Surligner l'option survolée
                if i == self.hovered_index:
                    pygame.draw.rect(surface, LIGHT_GRAY, option_rect)
                
                text_surf = self.font.render(option, True, BLACK)
                text_rect = text_surf.get_rect(midleft=(option_rect.left + 10, option_rect.centery))
                surface.blit(text_surf, text_rect)
    
    def update(self, event_list):
        """Met à jour l'état du menu déroulant."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Vérifier si la souris survole une option
        if self.is_open and self.dropdown_rect.collidepoint(mouse_pos):
            self.hovered_index = (mouse_pos[1] - self.dropdown_rect.top) // self.option_height
            self.hovered_index = max(0, min(self.hovered_index, len(self.options) - 1))
        else:
            self.hovered_index = -1
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Si on clique sur le menu principal, l'ouvrir ou le fermer
                if self.rect.collidepoint(mouse_pos):
                    self.is_open = not self.is_open
                    return True
                
                # Si on clique sur une option, la sélectionner
                elif self.is_open and self.dropdown_rect.collidepoint(mouse_pos):
                    self.selected_index = self.hovered_index
                    self.is_open = False
                    if self.action:
                        self.action(self.selected_index)
                    return True
                
                # Si on clique ailleurs, fermer le menu
                elif self.is_open:
                    self.is_open = False
        
        return False 