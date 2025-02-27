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

class InfoButton:
    """Un bouton d'information qui affiche un popup."""
    
    def __init__(self, x, y, text, font, popup_content):
        """
        Initialise un bouton d'information.
        
        Args:
            x (int): Position X du bouton
            y (int): Position Y du bouton
            text (str): Texte à afficher sur le bouton (généralement "i" pour info)
            font (pygame.font.Font): Police à utiliser pour le texte
            popup_content (str): Contenu à afficher dans le popup
        """
        self.rect = pygame.Rect(x, y, 20, 20)  # Taille fixe pour le bouton d'info
        self.text = text
        self.font = font
        self.popup_content = popup_content
        self.popup_visible = False
        self.hovered = False
        self._original_pos = (x, y)  # Pour le défilement
        
    def toggle_popup(self):
        """Affiche ou masque le popup."""
        self.popup_visible = not self.popup_visible
        
    def draw(self, surface):
        """Dessine le bouton et éventuellement le popup."""
        # Couleurs du bouton en fonction de l'état
        bg_color = LIGHT_GRAY if self.hovered else GRAY
        text_color = WHITE
        border_color = BLUE if self.hovered or self.popup_visible else DARK_GRAY
        
        # Dessiner le fond du bouton
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=10)
        # Dessiner la bordure
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=10)
        
        # Dessiner le texte
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
        # Dessiner le popup si visible
        if self.popup_visible:
            self._draw_popup(surface)
            
    def _draw_popup(self, surface):
        """Dessine le popup d'information."""
        # Paramètres du popup
        padding = 10
        line_height = self.font.get_height() + 2
        
        # Découper le contenu en lignes
        lines = self.popup_content.split('\n')
        
        # Calculer les dimensions du popup
        max_line_width = max(self.font.size(line)[0] for line in lines)
        popup_width = max_line_width + 2 * padding
        popup_height = len(lines) * line_height + 2 * padding
        
        # Position du popup (à droite du bouton par défaut, ou au-dessus si pas assez d'espace)
        screen_width, screen_height = surface.get_size()
        
        # Vérifier si le popup dépasse à droite
        if self.rect.right + popup_width > screen_width:
            popup_x = max(0, self.rect.left - popup_width)
        else:
            popup_x = self.rect.right + 5
            
        # Vérifier si le popup dépasse en bas
        if self.rect.centery + popup_height/2 > screen_height:
            popup_y = max(0, screen_height - popup_height)
        else:
            popup_y = max(0, self.rect.centery - popup_height/2)
            
        # Créer le rectangle du popup
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        
        # Dessiner le fond du popup
        pygame.draw.rect(surface, POPUP_BACKGROUND, popup_rect, border_radius=5)
        # Dessiner la bordure du popup
        pygame.draw.rect(surface, POPUP_BORDER, popup_rect, POPUP_BORDER_WIDTH, border_radius=5)
        
        # Dessiner le texte du popup
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, BLACK)
            surface.blit(text_surf, (popup_x + padding, popup_y + padding + i * line_height))
        
    def update(self, event_list):
        """Met à jour l'état du bouton en fonction des événements."""
        mouse_pos = pygame.mouse.get_pos()
        old_hovered = self.hovered
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Vérifier s'il y a eu un changement d'état de survol
        if old_hovered != self.hovered and not self.hovered:
            # La souris vient de quitter le bouton, fermer le popup
            self.popup_visible = False
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.toggle_popup()
                    return True
                elif self.popup_visible and not self._popup_contains_point(event.pos, surface=pygame.display.get_surface()):
                    # Clic en dehors du popup, le fermer
                    self.popup_visible = False
                    return True
        return False
        
    def _popup_contains_point(self, point, surface):
        """Vérifie si un point est dans le popup."""
        if not self.popup_visible:
            return False
            
        # Recalculer les dimensions du popup (similaire à _draw_popup)
        padding = 10
        line_height = self.font.get_height() + 2
        lines = self.popup_content.split('\n')
        max_line_width = max(self.font.size(line)[0] for line in lines)
        popup_width = max_line_width + 2 * padding
        popup_height = len(lines) * line_height + 2 * padding
        
        screen_width, screen_height = surface.get_size()
        
        if self.rect.right + popup_width > screen_width:
            popup_x = max(0, self.rect.left - popup_width)
        else:
            popup_x = self.rect.right + 5
            
        if self.rect.centery + popup_height/2 > screen_height:
            popup_y = max(0, screen_height - popup_height)
        else:
            popup_y = max(0, self.rect.centery - popup_height/2)
            
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        return popup_rect.collidepoint(point)

class Checkbox:
    """Une case à cocher interactive."""
    
    def __init__(self, x, y, text, font, action=None, checked=False, text_color=BLACK):
        """
        Initialise une case à cocher.
        
        Args:
            x (int): Position X de la case
            y (int): Position Y de la case
            text (str): Texte à afficher à côté de la case
            font (pygame.font.Font): Police à utiliser pour le texte
            action (function, optional): Fonction à appeler lorsque l'état change
            checked (bool, optional): État initial de la case
            text_color (tuple): Couleur du texte (R,G,B)
        """
        self.rect = pygame.Rect(x, y, 20, 20)  # Taille de la case à cocher
        self.text = text
        self.font = font
        self.action = action
        self.checked = checked
        self.text_color = text_color
        self.hovered = False
        self._original_pos = (x, y)  # Stocker la position originale pour le défilement
        
        # Calculer la largeur totale nécessaire (case + texte)
        text_width = font.size(text)[0]
        self.width = 20 + 10 + text_width  # Case + espacement + texte
        
    def draw(self, surface):
        """Dessine la case à cocher et son texte."""
        # Dessiner le fond de la case
        bg_color = LIGHT_GRAY if self.hovered else WHITE
        pygame.draw.rect(surface, bg_color, self.rect)
        
        # Dessiner la bordure de la case
        border_color = BLUE if self.hovered else BLACK
        pygame.draw.rect(surface, border_color, self.rect, 2)
        
        # Dessiner la coche si la case est cochée
        if self.checked:
            inner_rect = pygame.Rect(
                self.rect.x + 4, 
                self.rect.y + 4, 
                self.rect.width - 8, 
                self.rect.height - 8
            )
            pygame.draw.rect(surface, BLUE, inner_rect)
        
        # Dessiner le texte à droite de la case avec un fond coloré pour le rendre plus visible
        text_surf = self.font.render(self.text, True, BLACK)  # Toujours utiliser du noir pour le texte
        text_width = text_surf.get_width()
        text_height = text_surf.get_height()
        
        # Position du texte
        text_x = self.rect.right + 10
        text_y = self.rect.centery - text_height // 2
        
        # Dessiner un fond légèrement coloré derrière le texte
        text_bg_rect = pygame.Rect(text_x - 2, text_y - 2, text_width + 4, text_height + 4)
        pygame.draw.rect(surface, (240, 240, 255), text_bg_rect)  # Fond très légèrement bleuté
        pygame.draw.rect(surface, (200, 200, 220), text_bg_rect, 1)  # Bordure plus foncée
        
        # Dessiner le texte
        surface.blit(text_surf, (text_x, text_y))
        
    def update(self, event_list):
        """Met à jour l'état de la case en fonction des événements."""
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
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
        
class ScrollablePanel:
    """Panneau défilant pour afficher du contenu plus grand que l'espace disponible."""
    
    def __init__(self, x, y, width, height, content_height):
        """
        Initialise un panneau défilant.
        
        Args:
            x (int): Position X du panneau
            y (int): Position Y du panneau
            width (int): Largeur du panneau
            height (int): Hauteur du panneau
            content_height (int): Hauteur totale du contenu à afficher
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.content_height = max(content_height, height)
        self.scroll_y = 0
        self.max_scroll = max(0, self.content_height - self.height)
        self.elements = []
        self.dragging = False
        self.drag_start = 0
        self.scroll_speed = 15  # Vitesse de défilement augmentée
        self.scroll_bar_width = 10
        self.debug = False  # Mode debug pour voir les positions
        
    def add_element(self, element):
        """Ajoute un élément au panneau."""
        # Stocker la position originale de l'élément lors de l'ajout
        if hasattr(element, 'rect'):
            # Utiliser _original_pos s'il existe déjà
            if not hasattr(element, '_original_pos'):
                element._original_pos = (element.rect.x, element.rect.y)
        self.elements.append(element)
        
    def is_visible(self, y_pos):
        """Vérifie si une position Y est visible dans le panneau."""
        return self.rect.top <= y_pos <= self.rect.bottom
        
    def get_content_rect(self):
        """Retourne le rectangle du contenu (incluant le défilement)."""
        return pygame.Rect(self.rect.x, self.rect.y - self.scroll_y, self.rect.width, self.content_height)
        
    def update(self, event_list):
        """Met à jour l'état du panneau en fonction des événements."""
        for event in event_list:
            # Gestion du défilement avec la molette de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if event.button == 4:  # Roulette vers le haut
                        self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
                    elif event.button == 5:  # Roulette vers le bas
                        self.scroll_y = min(self.max_scroll, self.scroll_y + self.scroll_speed)
                    elif event.button == 1:  # Clic gauche sur la barre de défilement
                        # Vérifier si le clic est sur la barre de défilement
                        scrollbar_rect = self._get_scrollbar_rect()
                        if scrollbar_rect.collidepoint(event.pos):
                            self.dragging = True
                            self.drag_start = event.pos[1]
                
            # Gestion du glissement de la barre de défilement
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    # Calcul du déplacement relatif
                    delta_y = event.pos[1] - self.drag_start
                    # Conversion du déplacement en pixels en déplacement de défilement
                    scrollbar_height = self._get_scrollbar_height()
                    content_ratio = self.content_height / self.height
                    self.scroll_y += delta_y * content_ratio
                    # Limiter le défilement
                    self.scroll_y = max(0, min(self.max_scroll, self.scroll_y))
                    # Mettre à jour le point de référence
                    self.drag_start = event.pos[1]
        
        # Mettre à jour tous les éléments du panneau
        for element in self.elements:
            # Ajuster la position en fonction du défilement
            if hasattr(element, 'rect') and hasattr(element, '_original_pos'):
                # Calculer la nouvelle position y en tenant compte du défilement
                new_y = self.rect.top + element._original_pos[1] - self.scroll_y
                
                # Mettre à jour la position de l'élément
                element.rect.x = self.rect.left + element._original_pos[0]
                element.rect.y = new_y
            
            # Mettre à jour l'élément s'il est visible
            if hasattr(element, 'update'):
                if hasattr(element, 'rect') and self._is_element_visible(element):
                    element.update(event_list)
                
    def draw(self, surface):
        """Dessine le panneau et son contenu sur la surface."""
        # Dessiner le fond du panneau avec une couleur légèrement différente pour le rendre visible
        pygame.draw.rect(surface, (245, 245, 250), self.rect)  # Couleur légèrement bleutée
        
        # Définir un rectangle de clipping pour ne dessiner que ce qui est visible
        old_clip = surface.get_clip()
        surface.set_clip(self.rect)
        
        # Dessiner tous les éléments visibles
        visible_count = 0
        for element in self.elements:
            if hasattr(element, 'rect') and self._is_element_visible(element):
                element.draw(surface)
                visible_count += 1
                
                # Dessiner un rectangle de débogage autour de l'élément si le mode debug est actif
                if self.debug:
                    pygame.draw.rect(surface, (255, 0, 0), element.rect, 1)
        
        # Dessiner la barre de défilement si nécessaire
        if self.content_height > self.height:
            scrollbar_rect = self._get_scrollbar_rect()
            # Dessiner la piste de la barre de défilement (fond)
            track_rect = pygame.Rect(scrollbar_rect.x, self.rect.top, 
                                    self.scroll_bar_width, self.height)
            pygame.draw.rect(surface, (220, 220, 220), track_rect)
            
            # Dessiner la poignée de la barre de défilement
            pygame.draw.rect(surface, (120, 120, 150), scrollbar_rect)
            pygame.draw.rect(surface, (80, 80, 100), scrollbar_rect, 1)  # Bordure
            
        # Dessiner une bordure plus marquée autour du panneau
        pygame.draw.rect(surface, (100, 100, 140), self.rect, 2)
        
        # Afficher des informations de débogage si le mode debug est actif
        if self.debug:
            debug_font = pygame.font.SysFont('Arial', 10)
            debug_text = debug_font.render(
                f"Visible: {visible_count}/{len(self.elements)}, Scroll: {self.scroll_y}/{self.max_scroll}", 
                True, (50, 50, 50)
            )
            surface.blit(debug_text, (self.rect.x + 5, self.rect.y + 5))
        
        # Restaurer le rectangle de clipping
        surface.set_clip(old_clip)
    
    def _is_element_visible(self, element):
        """Vérifie si un élément est visible dans le panneau."""
        if not hasattr(element, 'rect'):
            return False
        # Un élément est visible si une partie de son rectangle est dans le panneau
        return (element.rect.bottom > self.rect.top and 
                element.rect.top < self.rect.bottom)
    
    def _get_scrollbar_rect(self):
        """Calcule le rectangle de la barre de défilement."""
        scrollbar_height = self._get_scrollbar_height()
        scrollbar_pos = self.rect.right - self.scroll_bar_width
        scrollbar_y = self.rect.top
        if self.max_scroll > 0:
            scroll_ratio = self.scroll_y / self.max_scroll
            scrollbar_y += scroll_ratio * (self.height - scrollbar_height)
        return pygame.Rect(scrollbar_pos, scrollbar_y, self.scroll_bar_width, scrollbar_height)
    
    def _get_scrollbar_height(self):
        """Calcule la hauteur de la barre de défilement en fonction du contenu."""
        if self.content_height <= self.height:
            return self.height  # Pas de défilement nécessaire
        return max(30, int(self.height * (self.height / self.content_height)))  # Min 30px pour la facilité de clic
    
    def toggle_debug(self):
        """Active ou désactive le mode de débogage visuel."""
        self.debug = not self.debug
        return self.debug

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

class Oscilloscope:
    """Un graphique pour afficher les courbes de croissance en temps réel avec historique."""
    
    def __init__(self, x, y, width, height, title="Fonctions de croissance", history_size=20):
        """
        Initialise un oscilloscope.
        
        Args:
            x (int): Position X du graphique
            y (int): Position Y du graphique
            width (int): Largeur du graphique
            height (int): Hauteur du graphique
            title (str, optional): Titre du graphique
            history_size (int, optional): Nombre de courbes à conserver dans l'historique
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.font = pygame.font.SysFont('Arial', 14)
        self.title_font = pygame.font.SysFont('Arial', 16, bold=True)
        self.colors = [
            (255, 0, 0),    # Rouge
            (0, 200, 0),    # Vert
            (0, 0, 255),    # Bleu
            (255, 255, 0),  # Jaune
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 128, 0),  # Orange
            (128, 0, 255),  # Violet
            (0, 128, 0),    # Vert foncé
            (128, 128, 0)   # Olive
        ]
        # Pour stocker l'historique des min/max y pour une mise à l'échelle plus fluide
        self.y_min = -1.0
        self.y_max = 1.0
        self.smoothing_factor = 0.9  # Facteur de lissage pour l'adaptation de l'échelle
        
        # Attributs pour l'historique des courbes
        self.history_size = history_size
        self.curve_history = []  # Liste pour stocker l'historique des courbes
        self.history_labels = []  # Liste pour stocker les labels correspondants
        self.history_enabled = True  # Option pour activer/désactiver l'historique
        self.history_opacity_step = 0.8  # Facteur de réduction d'opacité pour les courbes historiques
    
    def add_to_history(self, functions, labels=None, x_range=(0, 1)):
        """
        Ajoute les courbes actuelles à l'historique.
        
        Args:
            functions (list): Liste des fonctions à ajouter à l'historique
            labels (list, optional): Liste des noms des fonctions
            x_range (tuple, optional): Plage de valeurs x (min, max)
        """
        if not self.history_enabled or not functions:
            return
            
        # Calculer les points pour chaque fonction
        curves = []
        for func in functions:
            points = []
            for j in range(100):
                x_val = x_range[0] + j * (x_range[1] - x_range[0]) / 99
                y_val = func(x_val)
                points.append((x_val, y_val))
            curves.append(points)
            
        # Ajouter les courbes à l'historique
        self.curve_history.append(curves)
        
        # Ajouter les labels à l'historique si fournis
        if labels:
            self.history_labels.append(labels)
        else:
            self.history_labels.append([f"Courbe {i+1}" for i in range(len(functions))])
            
        # Limiter la taille de l'historique
        if len(self.curve_history) > self.history_size:
            self.curve_history.pop(0)
            self.history_labels.pop(0)
        
    def draw(self, surface, functions, labels=None, x_range=(0, 1)):
        """
        Dessine les courbes sur la surface.
        
        Args:
            surface (pygame.Surface): Surface sur laquelle dessiner
            functions (list): Liste des fonctions à tracer
            labels (list, optional): Liste des noms des fonctions
            x_range (tuple, optional): Plage de valeurs x (min, max)
        """
        # Ajouter les courbes actuelles à l'historique avant de les dessiner
        self.add_to_history(functions, labels, x_range)
        
        # Dessiner le fond
        pygame.draw.rect(surface, (240, 240, 240), self.rect)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 2)
        
        # Dessiner le titre
        title_surf = self.title_font.render(self.title, True, BLACK)
        title_rect = title_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 5))
        surface.blit(title_surf, title_rect)
        
        # Définir la zone de tracé (avec des marges)
        margin = 30
        plot_rect = pygame.Rect(
            self.rect.left + margin, 
            self.rect.top + margin + 10,
            self.rect.width - 2 * margin,
            self.rect.height - 2 * margin - 10
        )
        
        # Si aucune fonction n'est fournie, sortir après avoir dessiné les axes
        if not functions and not self.curve_history:
            # Dessiner les axes
            pygame.draw.line(
                surface, BLACK,
                (plot_rect.left, plot_rect.centery),
                (plot_rect.right, plot_rect.centery), 1
            )
            pygame.draw.line(
                surface, BLACK,
                (plot_rect.left, plot_rect.top),
                (plot_rect.left, plot_rect.bottom), 1
            )
            
            no_data = self.font.render("Aucune fonction active", True, BLACK)
            no_data_rect = no_data.get_rect(center=plot_rect.center)
            surface.blit(no_data, no_data_rect)
            return
        
        # Calculer les valeurs min et max pour l'échelle Y automatique
        all_values = []
        
        # Inclure les valeurs des fonctions actuelles
        if functions:
            for func in functions:
                # Échantillonner la fonction sur la plage X
                for j in range(20):  # Moins de points pour l'analyse, plus rapide
                    x_val = x_range[0] + j * (x_range[1] - x_range[0]) / 19
                    y_val = func(x_val)
                    all_values.append(y_val)
        
        # Inclure les valeurs de l'historique
        for curves in self.curve_history:
            for points in curves:
                for _, y_val in points:
                    all_values.append(y_val)
        
        # Calculer les bornes min et max actuelles
        current_min = min(all_values) if all_values else -1.0
        current_max = max(all_values) if all_values else 1.0
        
        # Assurer une plage minimale pour éviter les divisions par zéro
        if abs(current_max - current_min) < 0.1:
            current_min -= 0.05
            current_max += 0.05
            
        # Lisser l'adaptation de l'échelle pour éviter les changements brusques
        self.y_min = self.y_min * self.smoothing_factor + current_min * (1 - self.smoothing_factor)
        self.y_max = self.y_max * self.smoothing_factor + current_max * (1 - self.smoothing_factor)
        
        # Ajouter une marge de 10% au-dessus et en-dessous
        y_range = self.y_max - self.y_min
        y_min_display = self.y_min - 0.1 * y_range
        y_max_display = self.y_max + 0.1 * y_range
        
        # Assurer que 0 est toujours visible sur l'axe Y
        if y_min_display > 0:
            y_min_display = -0.1 * y_range
        if y_max_display < 0:
            y_max_display = 0.1 * y_range
            
        # Dessiner les axes
        pygame.draw.line(
            surface, BLACK,
            (plot_rect.left, plot_rect.centery - (0 - y_min_display) * plot_rect.height / (y_max_display - y_min_display)),
            (plot_rect.right, plot_rect.centery - (0 - y_min_display) * plot_rect.height / (y_max_display - y_min_display)), 1
        )
        pygame.draw.line(
            surface, BLACK,
            (plot_rect.left, plot_rect.top),
            (plot_rect.left, plot_rect.bottom), 1
        )
        
        # Dessiner les graduations sur l'axe x
        for i in range(5):
            x = plot_rect.left + i * plot_rect.width / 4
            y_zero = plot_rect.centery - (0 - y_min_display) * plot_rect.height / (y_max_display - y_min_display)
            pygame.draw.line(surface, BLACK, (x, y_zero - 3), (x, y_zero + 3), 1)
            
            # Valeur sur l'axe x
            x_val = x_range[0] + i * (x_range[1] - x_range[0]) / 4
            x_label = self.font.render(f"{x_val:.1f}", True, BLACK)
            surface.blit(x_label, (x - 10, y_zero + 5))
        
        # Dessiner les graduations sur l'axe y
        y_step = (y_max_display - y_min_display) / 4
        for i in range(5):
            y_val = y_min_display + i * y_step
            y = plot_rect.bottom - i * plot_rect.height / 4
            pygame.draw.line(surface, BLACK, (plot_rect.left - 3, y), (plot_rect.left + 3, y), 1)
            
            # Valeur sur l'axe y
            y_label = self.font.render(f"{y_val:.2f}", True, BLACK)
            surface.blit(y_label, (plot_rect.left - 45, y - 7))
        
        # Dessiner l'historique des courbes avec une opacité décroissante
        if self.history_enabled and self.curve_history:
            for history_index, (curves, history_labels) in enumerate(zip(self.curve_history, self.history_labels)):
                # Calculer l'opacité en fonction de l'âge de la courbe
                opacity = max(0.1, self.history_opacity_step ** (len(self.curve_history) - history_index - 1))
                
                for i, points in enumerate(curves):
                    if i >= len(self.colors):
                        continue
                        
                    # Obtenir la couleur de base et appliquer l'opacité
                    base_color = self.colors[i % len(self.colors)]
                    color = (base_color[0], base_color[1], base_color[2], int(255 * opacity))
                    
                    # Convertir les points en coordonnées d'écran
                    screen_points = []
                    for x_val, y_val in points:
                        x_pix = plot_rect.left + (x_val - x_range[0]) * plot_rect.width / (x_range[1] - x_range[0])
                        y_pix = plot_rect.bottom - (y_val - y_min_display) * plot_rect.height / (y_max_display - y_min_display)
                        
                        # S'assurer que y_pix reste dans les limites du graphique
                        y_pix = max(plot_rect.top, min(plot_rect.bottom, y_pix))
                        
                        screen_points.append((x_pix, y_pix))
                    
                    # Tracer la courbe historique
                    if len(screen_points) > 1:
                        # Créer une surface temporaire pour dessiner la courbe avec transparence
                        temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                        pygame.draw.lines(temp_surface, color, False, screen_points, 1)
                        surface.blit(temp_surface, (0, 0))
        
        # Dessiner chaque courbe actuelle
        if functions:
            for i, func in enumerate(functions):
                color = self.colors[i % len(self.colors)]
                points = []
                
                # Calculer les points de la courbe
                for j in range(100):
                    x_val = x_range[0] + j * (x_range[1] - x_range[0]) / 99
                    y_val = func(x_val)
                    
                    # Convertir en coordonnées d'écran
                    x_pix = plot_rect.left + j * plot_rect.width / 99
                    y_pix = plot_rect.bottom - (y_val - y_min_display) * plot_rect.height / (y_max_display - y_min_display)
                    
                    # S'assurer que y_pix reste dans les limites du graphique
                    y_pix = max(plot_rect.top, min(plot_rect.bottom, y_pix))
                    
                    points.append((x_pix, y_pix))
                
                # Tracer la courbe actuelle (plus épaisse que les courbes historiques)
                if len(points) > 1:
                    pygame.draw.lines(surface, color, False, points, 2)
                
        # Dessiner la légende si des labels sont fournis
        if labels:
            # Calculer la hauteur de la légende en fonction du nombre d'entrées
            rows = (len(labels) + 4) // 5  # 5 entrées par ligne
            legend_height = rows * 20 + 10  # 20 pixels par entrée + 10 de padding
            
            legend_y = self.rect.bottom - legend_height
            legend_x = self.rect.left + 10
            
            # Dessiner le fond de la légende
            legend_width = self.rect.width - 20
            legend_rect = pygame.Rect(legend_x, legend_y, legend_width, legend_height)
            pygame.draw.rect(surface, (250, 250, 250), legend_rect)
            pygame.draw.rect(surface, DARK_GRAY, legend_rect, 1)
            
            # Dessiner chaque entrée de légende
            for i, label in enumerate(labels[:min(len(labels), len(functions))]):
                color = self.colors[i % len(self.colors)]
                
                # Position de cette entrée de légende
                row = i // 5
                col = i % 5
                item_width = legend_width / 5
                item_x = legend_x + col * item_width
                item_y = legend_y + row * 20 + 5
                
                # Dessiner le segment de couleur
                pygame.draw.line(
                    surface, color,
                    (item_x + 5, item_y + 10),
                    (item_x + 20, item_y + 10), 2
                )
                
                # Dessiner le texte (tronqué si trop long)
                max_label_width = item_width - 30
                label_surf = self.font.render(label, True, BLACK)
                if label_surf.get_width() > max_label_width:
                    # Tronquer le texte
                    truncated = label.split('(')[0] + "..."  # Garder le nom de la fonction et ajouter "..."
                    label_surf = self.font.render(truncated, True, BLACK)
                
                surface.blit(label_surf, (item_x + 25, item_y + 3))
                
    def toggle_history(self):
        """Active ou désactive l'affichage de l'historique des courbes."""
        self.history_enabled = not self.history_enabled
        
    def clear_history(self):
        """Efface l'historique des courbes."""
        self.curve_history = []
        self.history_labels = []
        
    def set_history_size(self, size):
        """
        Définit la taille maximale de l'historique.
        
        Args:
            size (int): Nombre maximal de courbes à conserver dans l'historique
        """
        self.history_size = max(1, size)
        
        # Tronquer l'historique si nécessaire
        while len(self.curve_history) > self.history_size:
            self.curve_history.pop(0)
            self.history_labels.pop(0)

class InteractionMatrix:
    """Widget pour afficher et modifier la matrice d'interaction entre canaux."""
    
    def __init__(self, x, y, width, height, matrix, channels_colors=None, title="Matrice d'interaction", channel_names=None):
        """
        Initialise le widget de matrice d'interaction.
        
        Args:
            x (int): Position X du widget
            y (int): Position Y du widget
            width (int): Largeur du widget
            height (int): Hauteur du widget
            matrix (numpy.ndarray): Matrice d'interaction (3x3 pour RGB)
            channels_colors (list, optional): Liste des couleurs pour chaque canal
            title (str, optional): Titre du widget
            channel_names (list, optional): Noms des canaux à afficher (par défaut ["Rouge", "Vert", "Bleu"])
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.matrix = matrix.copy()
        self.title = title
        self.font = pygame.font.SysFont('Arial', 12)  # Réduit de 14 à 12
        self.title_font = pygame.font.SysFont('Arial', 18, bold=True)  # Réduit de 20 à 18
        self.button_font = pygame.font.SysFont('Arial', 12, bold=True)  # Police pour les boutons + et -
        
        self.channels_colors = channels_colors or [
            (255, 50, 50),    # Rouge
            (50, 255, 50),    # Vert
            (50, 50, 255)     # Bleu
        ]
        
        self.channel_names = channel_names or ["Rouge", "Vert", "Bleu"]
        
        # Optimisation des espacements
        header_space = 50  # Réduit de 60 à 50
        side_header_space = 80  # Réduit de 100 à 80
        
        available_width = width - side_header_space
        available_height = height - header_space - 30  # Réduit de 40 à 30 pixels pour le titre
        
        self.cell_size = min(available_width // 3, available_height // 3)
        self.cell_size = max(self.cell_size, 90)  # Réduit de 110 à 90
        
        self.matrix_x = self.rect.x + side_header_space
        self.matrix_y = self.rect.y + header_space + 30
        
        # Création des sliders pour chaque cellule de la matrice
        self.sliders = []
        # Nouveaux tableaux pour les boutons + et -
        self.plus_buttons = []
        self.minus_buttons = []
        
        for i in range(3):  # Pour chaque ligne (destination)
            row_sliders = []
            row_plus_buttons = []
            row_minus_buttons = []
            
            for j in range(3):  # Pour chaque colonne (source)
                # Position du slider
                slider_x = self.matrix_x + j * self.cell_size + 10
                slider_y = self.matrix_y + i * self.cell_size + self.cell_size // 2
                
                # Largeur du slider
                slider_width = self.cell_size - 20
                
                # Créer une fonction de callback pour ce slider
                def create_callback(row, col):
                    def callback(value):
                        self.set_value(row, col, value)
                    return callback
                
                # Créer le slider
                slider = Slider(
                    slider_x, slider_y, 
                    slider_width, 10, 
                    min_val=-1.0, max_val=1.0, 
                    initial_val=self.matrix[i, j],
                    on_change=create_callback(i, j)
                )
                
                # Position des boutons + et - (en dessous du slider)
                button_width = 20
                button_height = 20
                button_spacing = 10
                
                # Créer les fonctions de callback pour les boutons
                def create_increment_callback(row, col, amount):
                    def callback():
                        self.increment_value(row, col, amount)
                    return callback
                
                # Bouton -
                minus_button = Button(
                    slider_x, slider_y + 20,
                    button_width, button_height,
                    "-", self.button_font,
                    create_increment_callback(i, j, -0.1)
                )
                
                # Bouton +
                plus_button = Button(
                    slider_x + slider_width - button_width, slider_y + 20,
                    button_width, button_height,
                    "+", self.button_font,
                    create_increment_callback(i, j, 0.1)
                )
                
                row_sliders.append(slider)
                row_plus_buttons.append(plus_button)
                row_minus_buttons.append(minus_button)
            
            self.sliders.append(row_sliders)
            self.plus_buttons.append(row_plus_buttons)
            self.minus_buttons.append(row_minus_buttons)
    
    def increment_value(self, i, j, amount):
        """Incrémente la valeur à la position (i, j) de la matrice."""
        self.matrix[i, j] = max(-1.0, min(1.0, self.matrix[i, j] + amount))
        # Mettre à jour le curseur correspondant
        self.sliders[i][j].set_value(self.matrix[i, j])
        
    def set_value(self, i, j, value):
        """Définit la valeur à la position (i, j) de la matrice."""
        self.matrix[i, j] = value
    
    def get_matrix(self):
        """Retourne la matrice d'interaction modifiée."""
        return self.matrix
        
    def update(self, event_list):
        """Met à jour l'état des boutons et curseurs."""
        # Mise à jour des sliders
        for row in self.sliders:
            for slider in row:
                slider.update(event_list)
                
        # Mise à jour des boutons +
        for i, row in enumerate(self.plus_buttons):
            for j, button in enumerate(row):
                button.update(event_list)
                
        # Mise à jour des boutons -
        for i, row in enumerate(self.minus_buttons):
            for j, button in enumerate(row):
                button.update(event_list)
            
    def draw(self, surface):
        """Dessine la matrice d'interaction sur la surface."""
        # Dessiner le fond
        pygame.draw.rect(surface, (240, 240, 240), self.rect)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 2)
        
        # Dessiner le titre
        title_surf = self.title_font.render(self.title, True, BLACK)
        title_rect = title_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 8))  # Réduit de 10 à 8
        surface.blit(title_surf, title_rect)
        
        # Dessiner un encadrement pour la matrice
        matrix_rect = pygame.Rect(
            self.matrix_x - 5,
            self.matrix_y - 5,
            3 * self.cell_size + 10,
            3 * self.cell_size + 10
        )
        pygame.draw.rect(surface, (220, 220, 220), matrix_rect)
        pygame.draw.rect(surface, DARK_GRAY, matrix_rect, 1)
        
        # Dessiner les en-têtes de colonnes (source)
        col_header_y = self.matrix_y - 25  # Réduit de 30 à 25
        pygame.draw.line(surface, DARK_GRAY, 
                        (self.matrix_x - 5, col_header_y - 5),
                        (self.matrix_x + 3 * self.cell_size + 5, col_header_y - 5), 1)
                        
        header_font = pygame.font.SysFont('Arial', 14, bold=True)  # Réduit de 16 à 14
        source_header = header_font.render("Source", True, BLACK)
        source_rect = source_header.get_rect(midtop=(self.matrix_x + 1.5 * self.cell_size, self.rect.top + 35))  # Réduit de 40 à 35
        surface.blit(source_header, source_rect)
        
        # Dessiner les en-têtes de lignes (destination)
        row_header_x = self.matrix_x - 10
        pygame.draw.line(surface, DARK_GRAY, 
                        (row_header_x - 5, self.matrix_y - 5),
                        (row_header_x - 5, self.matrix_y + 3 * self.cell_size + 5), 1)
                        
        dest_header = header_font.render("Destination", True, BLACK)
        # Rotation du texte pour l'afficher verticalement
        dest_header = pygame.transform.rotate(dest_header, 90)
        dest_rect = dest_header.get_rect(midright=(self.matrix_x - 15, self.matrix_y + 1.5 * self.cell_size))
        surface.blit(dest_header, dest_rect)
        
        # Dessiner les noms des canaux pour les colonnes
        for j in range(3):
            # Couleur du canal
            color = self.channels_colors[j]
            
            # Nom du canal
            channel_name = self.channel_names[j]
            
            # Rendu du texte
            text_surf = self.font.render(channel_name, True, color)
            text_rect = text_surf.get_rect(midtop=(
                self.matrix_x + j * self.cell_size + self.cell_size // 2,
                col_header_y - 20  # Réduit l'espacement
            ))
            surface.blit(text_surf, text_rect)
            
            # Dessiner un petit carré de couleur à côté du nom
            color_rect = pygame.Rect(
                text_rect.right + 5,
                text_rect.centery - 5,
                10, 10
            )
            pygame.draw.rect(surface, color, color_rect)
            pygame.draw.rect(surface, BLACK, color_rect, 1)
        
        # Dessiner les noms des canaux pour les lignes
        for i in range(3):
            # Couleur du canal
            color = self.channels_colors[i]
            
            # Nom du canal
            channel_name = self.channel_names[i]
            
            # Rendu du texte
            text_surf = self.font.render(channel_name, True, color)
            text_rect = text_surf.get_rect(midright=(
                row_header_x - 10,
                self.matrix_y + i * self.cell_size + self.cell_size // 2
            ))
            surface.blit(text_surf, text_rect)
            
            # Dessiner un petit carré de couleur à côté du nom
            color_rect = pygame.Rect(
                text_rect.left - 15,
                text_rect.centery - 5,
                10, 10
            )
            pygame.draw.rect(surface, color, color_rect)
            pygame.draw.rect(surface, BLACK, color_rect, 1)
        
        # Dessiner les cellules de la matrice
        for i in range(3):
            for j in range(3):
                # Position et taille de cette cellule
                cell_x = self.matrix_x + j * self.cell_size
                cell_y = self.matrix_y + i * self.cell_size
                cell_rect = pygame.Rect(cell_x, cell_y, self.cell_size, self.cell_size)
                
                # Couleur de fond basée sur la valeur
                val = self.matrix[i, j]
                
                # Calculer la couleur de la cellule basée sur la valeur
                if val > 0:  # Influence positive (renforcement)
                    # Dégradé de blanc à la couleur de destination (vert plus intense)
                    intensity = min(255, int(128 + 127 * val))
                    cell_color = tuple(max(0, min(255, c * intensity // 255)) for c in self.channels_colors[i])
                    cell_color = (255 - intensity + cell_color[0] * intensity // 255,
                                 255 - intensity + cell_color[1] * intensity // 255,
                                 255 - intensity + cell_color[2] * intensity // 255)
                else:  # Influence négative (inhibition)
                    # Dégradé de blanc à gris
                    intensity = int(255 * (1 + val))
                    cell_color = (intensity, intensity, intensity)
                
                # Dessiner le fond de la cellule
                pygame.draw.rect(surface, cell_color, cell_rect)
                pygame.draw.rect(surface, DARK_GRAY, cell_rect, 1)
                
                # Afficher la valeur numérique
                value_text = f"{val:.2f}"
                value_color = BLACK if intensity > 128 else WHITE
                value_surf = self.font.render(value_text, True, value_color)
                value_rect = value_surf.get_rect(center=(cell_x + self.cell_size // 2, cell_y + 15))
                surface.blit(value_surf, value_rect)
        
        # Dessiner les sliders
        for i, row in enumerate(self.sliders):
            for j, slider in enumerate(row):
                slider.draw(surface)
                
        # Dessiner les boutons +
        for i, row in enumerate(self.plus_buttons):
            for j, button in enumerate(row):
                button.draw(surface)
                
        # Dessiner les boutons -
        for i, row in enumerate(self.minus_buttons):
            for j, button in enumerate(row):
                button.draw(surface)

class Slider:
    """Un curseur pour sélectionner une valeur dans une plage."""
    
    def __init__(self, x, y, width, height, min_val=-1.0, max_val=1.0, initial_val=0.0, on_change=None):
        """
        Initialise un curseur.
        
        Args:
            x (int): Position X du curseur
            y (int): Position Y du curseur
            width (int): Largeur du curseur
            height (int): Hauteur du curseur
            min_val (float, optional): Valeur minimale
            max_val (float, optional): Valeur maximale
            initial_val (float, optional): Valeur initiale
            on_change (function, optional): Fonction à appeler quand la valeur change
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.on_change = on_change
        self.dragging = False
        self.hover = False
        
        # Calcul de la position initiale du curseur
        self.handle_radius = height // 2
        self.track_rect = pygame.Rect(
            x + self.handle_radius, 
            y + (height - 4) // 2, 
            width - 2 * self.handle_radius, 
            4
        )
        self.update_handle_pos()
        
    def update_handle_pos(self):
        """Met à jour la position du curseur basée sur la valeur."""
        val_range = self.max_val - self.min_val
        if val_range == 0:
            rel_pos = 0.5
        else:
            rel_pos = (self.value - self.min_val) / val_range
        
        self.handle_pos = (
            self.track_rect.left + int(rel_pos * self.track_rect.width),
            self.rect.centery
        )
        
    def set_value(self, value):
        """Définit la valeur et met à jour la position du curseur."""
        self.value = max(self.min_val, min(self.max_val, value))
        self.update_handle_pos()
        
    def update(self, event_list):
        """Met à jour l'état du curseur en fonction des événements."""
        mouse_pos = pygame.mouse.get_pos()
        handle_rect = pygame.Rect(
            self.handle_pos[0] - self.handle_radius,
            self.handle_pos[1] - self.handle_radius,
            self.handle_radius * 2,
            self.handle_radius * 2
        )
        
        self.hover = handle_rect.collidepoint(mouse_pos)
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if handle_rect.collidepoint(mouse_pos):
                    self.dragging = True
                elif self.track_rect.collidepoint(mouse_pos):
                    # Clic direct sur la piste
                    rel_pos = (mouse_pos[0] - self.track_rect.left) / self.track_rect.width
                    new_value = self.min_val + rel_pos * (self.max_val - self.min_val)
                    self.set_value(new_value)
                    
                    if self.on_change:
                        self.on_change(self.value)
                    
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
                
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                # Calculer la nouvelle position relative
                rel_pos = max(0, min(1, (mouse_pos[0] - self.track_rect.left) / self.track_rect.width))
                
                # Calculer la nouvelle valeur
                new_value = self.min_val + rel_pos * (self.max_val - self.min_val)
                self.set_value(new_value)
                
                if self.on_change:
                    self.on_change(self.value)
                    
        return False
        
    def draw(self, surface):
        """Dessine le curseur sur la surface."""
        # Dessiner la piste
        pygame.draw.rect(surface, GRAY, self.track_rect)
        pygame.draw.rect(surface, DARK_GRAY, self.track_rect, 1)
        
        # Dessiner la partie de la piste correspondant à la valeur
        zero_pos = self.track_rect.left + int((-self.min_val) / (self.max_val - self.min_val) * self.track_rect.width)
        
        if self.value > 0:
            # Partie positive (de zéro à la position actuelle)
            pos_rect = pygame.Rect(
                zero_pos,
                self.track_rect.top,
                max(0, self.handle_pos[0] - zero_pos),
                self.track_rect.height
            )
            if pos_rect.width > 0:
                pygame.draw.rect(surface, GREEN, pos_rect)
        else:
            # Partie négative (de la position actuelle à zéro)
            neg_rect = pygame.Rect(
                self.handle_pos[0],
                self.track_rect.top,
                max(0, zero_pos - self.handle_pos[0]),
                self.track_rect.height
            )
            if neg_rect.width > 0:
                pygame.draw.rect(surface, (200, 50, 50), neg_rect)
        
        # Dessiner la position zéro
        if self.min_val < 0 < self.max_val:
            pygame.draw.line(
                surface, 
                BLACK, 
                (zero_pos, self.track_rect.top - 2), 
                (zero_pos, self.track_rect.bottom + 2), 
                2
            )
        
        # Dessiner le curseur
        handle_color = BLUE if self.hover or self.dragging else DARK_GRAY
        pygame.draw.circle(surface, handle_color, self.handle_pos, self.handle_radius)
        pygame.draw.circle(surface, WHITE, self.handle_pos, self.handle_radius - 2)
        
        # Afficher la valeur avec une police plus petite et un format plus compact
        value_text = f"{self.value:.2f}"
        font = pygame.font.SysFont('Arial', 10)  # Police plus petite
        
        # Créer un fond pour le texte pour améliorer la lisibilité
        text_surf = font.render(value_text, True, BLACK)
        text_rect = text_surf.get_rect(midtop=(self.handle_pos[0], self.handle_pos[1] + self.handle_radius + 1))
        
        # Ajouter un petit fond blanc semi-transparent pour améliorer la lisibilité
        bg_rect = text_rect.inflate(4, 2)
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surf.fill((255, 255, 255, 200))  # Blanc semi-transparent
        surface.blit(bg_surf, bg_rect)
        
        # Afficher le texte
        surface.blit(text_surf, text_rect) 