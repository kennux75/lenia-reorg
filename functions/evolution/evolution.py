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

def evolve_multi_channels(Xs):
    """
    Fait évoluer le système Lenia avec plusieurs canaux sans interactions entre canaux.
    
    Args:
        Xs (list): Liste des grilles pour chaque canal
        
    Returns:
        list: Liste des grilles mises à jour
    """
    # Calcul des transformées de Fourier de chaque canal
    fXs = [np.fft.fft2(X) for X in Xs]
    
    # Pour chaque kernel, calcul de la convolution avec le canal source correspondant
    Us = [np.real(np.fft.ifft2(fK * fXs[source])) for fK, source in zip(fKs, sources)]
    
    # Calcul de l'activation associée à chaque convolution
    As = [2 * gauss(U, ms[i], ss[i]) - 1 for i, U in enumerate(Us)]
    
    # Initialisation du terme de croissance pour chaque canal
    Gs = np.zeros_like(Xs)
    
    # Application de l'activation au canal de destination correspondant avec la force correspondante
    for destination, h, A in zip(destinations, hs, As):
        Gs[destination] += h * A
    
    # Mise à jour des canaux avec le pas de temps dt
    Xs = [np.clip(X + dt * G, 0, 1) for X, G in zip(Xs, Gs)]
    
    return Xs

def evolve_multi_channels_interactions(Xs):
    """
    Fait évoluer le système Lenia avec plusieurs canaux et interactions entre canaux.
    
    Args:
        Xs (list): Liste des grilles pour chaque canal
        
    Returns:
        list: Liste des grilles mises à jour
    """
    # Calcul des transformées de Fourier de chaque canal
    fXs = [np.fft.fft2(X) for X in Xs]
    
    # Convolutions pour chaque kernel selon le canal source associé
    Us = [np.real(np.fft.ifft2(fK * fXs[source])) for fK, source in zip(fKs, sources)]
    
    # Calcul de la fonction de croissance (activation) pour chaque kernel
    As = [2 * gauss(U, ms[i], ss[i]) - 1 for i, U in enumerate(Us)]
    
    # Initialisation du terme de croissance pour chaque canal
    Gs = [np.zeros_like(X) for X in Xs]
    
    # Contribution des kernels vers le canal de destination
    for destination, h, A in zip(destinations, hs, As):
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