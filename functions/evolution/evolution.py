#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions d'évolution de Lenia
------------------------------
Ce module contient les fonctions pour faire évoluer le système Lenia.
"""

import numpy as np
from functions.kernel.kernel_generation import generate_kernels
from functions.growth.growth_functions import gauss
from config.simulation_config import dt, ms, ss, hs, sources, destinations, interaction_matrix

def evolve_single_channel(X, R, dt, kernel_core, growth_func=gauss):
    """
    Fait évoluer une grille Lenia avec un seul canal.
    
    Args:
        X (numpy.ndarray): Grille à faire évoluer
        R (float): Rayon du kernel
        dt (float): Pas de temps
        kernel_core (numpy.ndarray): Noyau du kernel
        growth_func (function, optional): Fonction de croissance à utiliser. Par défaut gauss.
    
    Returns:
        numpy.ndarray: Grille évoluée
    """
    # Calculer la convolution
    FFT = np.fft.fft2
    IFFT = np.fft.ifft2
    K = np.real(IFFT(FFT(kernel_core) * FFT(X)))
    
    # Calculer la mise à jour
    G = dt * growth_func(K, kernel_mu, kernel_sigma)
    X = np.clip(X + G, 0, 1)
    
    return X

def evolve_multi_channels(Xs, active_indices, growth_func=gauss):
    """
    Fait évoluer un système Lenia avec plusieurs canaux.
    
    Args:
        Xs (list): Liste des grilles pour chaque canal
        active_indices (list): Liste des indices des kernels actifs
        growth_func (function, optional): Fonction de croissance à utiliser. Par défaut gauss.
    
    Returns:
        list: Liste des grilles évoluées
    """
    # Générer les kernels
    kernels_fft = generate_kernels(
        Xs[0].shape, 
        active_indices
    )
    
    # Calculer les FFT des canaux
    fXs = [np.fft.fft2(X) for X in Xs]
    
    # Initialiser les termes de croissance pour chaque canal
    Gs = [np.zeros_like(X) for X in Xs]
    
    # Appliquer les kernels actifs
    for idx, i in enumerate(active_indices):
        fK = kernels_fft[idx]
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

def evolve_multi_channels_interactions(Xs, active_indices, growth_func=gauss, interaction_mat=None):
    """
    Fait évoluer un système Lenia avec plusieurs canaux et des interactions entre canaux.
    
    Args:
        Xs (list): Liste des grilles pour chaque canal
        active_indices (list): Liste des indices des kernels actifs
        growth_func (function, optional): Fonction de croissance à utiliser. Par défaut gauss.
        interaction_mat (numpy.ndarray, optional): Matrice d'interaction entre canaux. Par défaut None, utilise interaction_matrix.
    
    Returns:
        list: Liste des grilles évoluées
    """
    # Si aucune matrice d'interaction n'est fournie, utiliser celle par défaut
    if interaction_mat is None:
        interaction_mat = interaction_matrix
        
    # Générer les kernels
    kernels_fft = generate_kernels(
        Xs[0].shape, 
        active_indices
    )
    
    # Calculer les FFT des canaux
    fXs = [np.fft.fft2(X) for X in Xs]
    
    # Initialiser les termes de croissance pour chaque canal
    Gs = [np.zeros_like(X) for X in Xs]
    
    # Appliquer les kernels actifs
    for idx, i in enumerate(active_indices):
        fK = kernels_fft[idx]
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
                interaction_term += interaction_mat[i, j] * Xs[j]
        # Ajout de ce terme d'interaction à la variation de Xs[i]
        Gs[i] += interaction_term
    
    # Mise à jour des canaux avec le pas de temps dt
    Xs = [np.clip(X + dt * G, 0, 1) for X, G in zip(Xs, Gs)]
    
    return Xs 