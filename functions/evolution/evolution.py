#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions d'évolution
--------------------
Ce module contient les fonctions qui définissent l'évolution du système Lenia.
"""

import numpy as np
from config.simulation_config import dt, ms, ss, hs, sources, destinations, interaction_matrix
from functions.growth.growth_functions import gauss
from functions.evolution.kernel_generator import generate_kernels

# Génération des kernels et de leurs transformées de Fourier
_, fKs = generate_kernels()

def evolve_multi_channels(Xs, active_indices=None, growth_func=None):
    """
    Fait évoluer le système Lenia avec plusieurs canaux sans interactions entre canaux.
    
    Args:
        Xs (list): Liste des grilles pour chaque canal
        active_indices (list, optional): Indices des kernels actifs. Par défaut tous les kernels sont actifs.
        growth_func (function, optional): Fonction de croissance à utiliser. Par défaut gauss.
        
    Returns:
        list: Liste des grilles mises à jour
    """
    # Si aucun indice actif n'est spécifié, on utilise tous les kernels
    if active_indices is None:
        active_indices = list(range(len(fKs)))
        
    # Si aucune fonction de croissance n'est spécifiée, on utilise gauss
    if growth_func is None:
        growth_func = gauss
        
    # Calcul des transformées de Fourier de chaque canal
    fXs = [np.fft.fft2(X) for X in Xs]
    
    # Initialisation du terme de croissance pour chaque canal
    Gs = [np.zeros_like(X) for X in Xs]
    
    # Pour chaque kernel actif, calcul de la convolution avec le canal source correspondant
    for i in active_indices:
        # Récupération des paramètres du kernel
        fK = fKs[i]
        source = sources[i]
        destination = destinations[i]
        m = ms[i]
        s = ss[i]
        h = hs[i]
        
        # Calcul de la convolution
        U = np.real(np.fft.ifft2(fK * fXs[source]))
        
        # Calcul de l'activation avec la fonction de croissance spécifiée
        A = 2 * growth_func(U, m, s) - 1
        
        # Application de l'activation au canal de destination
        Gs[destination] += h * A
    
    # Mise à jour des canaux avec le pas de temps dt
    Xs = [np.clip(X + dt * G, 0, 1) for X, G in zip(Xs, Gs)]
    
    return Xs

def evolve_multi_channels_interactions(Xs, active_indices=None, growth_func=None):
    """
    Fait évoluer le système Lenia avec plusieurs canaux et interactions entre canaux.
    
    Args:
        Xs (list): Liste des grilles pour chaque canal
        active_indices (list, optional): Indices des kernels actifs. Par défaut tous les kernels sont actifs.
        growth_func (function, optional): Fonction de croissance à utiliser. Par défaut gauss.
        
    Returns:
        list: Liste des grilles mises à jour
    """
    # Si aucun indice actif n'est spécifié, on utilise tous les kernels
    if active_indices is None:
        active_indices = list(range(len(fKs)))
        
    # Si aucune fonction de croissance n'est spécifiée, on utilise gauss
    if growth_func is None:
        growth_func = gauss
        
    # Calcul des transformées de Fourier de chaque canal
    fXs = [np.fft.fft2(X) for X in Xs]
    
    # Initialisation du terme de croissance pour chaque canal
    Gs = [np.zeros_like(X) for X in Xs]
    
    # Pour chaque kernel actif, calcul de la convolution avec le canal source correspondant
    for i in active_indices:
        # Récupération des paramètres du kernel
        fK = fKs[i]
        source = sources[i]
        destination = destinations[i]
        m = ms[i]
        s = ss[i]
        h = hs[i]
        
        # Calcul de la convolution
        U = np.real(np.fft.ifft2(fK * fXs[source]))
        
        # Calcul de l'activation avec la fonction de croissance spécifiée
        A = 2 * growth_func(U, m, s) - 1
        
        # Application de l'activation au canal de destination
        Gs[destination] += h * A
    
    # Ajout d'un terme d'interaction entre les canaux
    for i in range(len(Xs)):
        interaction_term = np.zeros_like(Xs[i])
        for j in range(len(Xs)):
            if i != j:
                # L'influence de Xs[j] sur le canal i est pondérée par le coefficient de la matrice
                interaction_term += interaction_matrix[i, j] * Xs[j]
        # Ajout de ce terme d'interaction à la variation de Xs[i]
        Gs[i] += interaction_term
    
    # Mise à jour des canaux avec le pas de temps dt
    Xs = [np.clip(X + dt * G, 0, 1) for X, G in zip(Xs, Gs)]
    
    return Xs 