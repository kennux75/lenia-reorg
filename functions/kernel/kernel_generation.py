#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Générateur de kernels
--------------------
Ce module contient les fonctions pour générer les kernels utilisés dans la simulation Lenia.
"""

import numpy as np
from config.simulation_config import N, M, bs, rs, kernel_mu, kernel_sigma
from functions.growth.growth_functions import gauss, multi_peak_soft_growth

def generate_kernels(shape=None, active_indices=None):
    """
    Génère les kernels pour la simulation Lenia.
    
    Args:
        shape (tuple, optional): Forme des kernels (hauteur, largeur). Si None, utilise (N, M).
        active_indices (list, optional): Indices des kernels à générer. Si None, génère tous les kernels.
    
    Returns:
        list: Liste des transformées de Fourier des kernels actifs
    """
    # Définir la forme par défaut si non spécifiée
    if shape is None:
        shape = (N, M)
        
    height, width = shape
    
    # Si aucun indice n'est spécifié, générer tous les kernels
    if active_indices is None:
        active_indices = list(range(len(bs)))
    
    # Initialisation
    fhs_y = height // 2    # Filter half size (hauteur)
    fhs_x = width // 2    # Filter half size (largeur)
    y, x = np.ogrid[-fhs_y:fhs_y, -fhs_x:fhs_x]
    
    # Génération et transformation de Fourier des kernels actifs
    fKs = []
    for i in active_indices:
        b = bs[i]
        r = rs[i]
        
        distance = np.sqrt(x**2 + y**2) / r * len(b)
        K = np.zeros_like(distance)
        
        for j in range(len(b)):
            mask = (distance.astype(int) == j)
            K += mask * b[j] * gauss(distance % 1, kernel_mu, kernel_sigma)
            # Alternative commentée:
            # K += mask * b[j] * multi_peak_soft_growth(distance % 1, kernel_mu, kernel_sigma)
        
        # Normalisation du kernel
        K = K / np.sum(K)
        
        # Transformation de Fourier
        fK = np.fft.fft2(np.fft.fftshift(K))
        fKs.append(fK)
    
    return fKs

def plot_kernels(Ks):
    """
    Génère des visualisations des kernels.
    
    Args:
        Ks (list): Liste des kernels
        
    Note:
        Cette fonction est principalement utilisée pour le débogage et l'analyse.
    """
    import matplotlib.pyplot as plt
    
    # Plot the cross section of the different K in Ks
    plt.figure(figsize=(10, 10))
    for i, K in enumerate(Ks):
        plt.plot(K[K.shape[0]//2, :], label=f"Kernel {i}")
    plt.legend()
    plt.xlim(K.shape[1]//2 - 20, K.shape[1]//2 + 20)
    plt.title("Coupe transversale des kernels")
    plt.xlabel("Position")
    plt.ylabel("Valeur")
    plt.grid(True)
    plt.savefig("kernel_cross_sections.png")
    plt.close()
    
    # Affichage des kernels en 2D
    plt.figure(figsize=(15, 5))
    for i, K in enumerate(Ks[:min(3, len(Ks))]):  # Afficher au plus 3 kernels
        plt.subplot(1, 3, i+1)
        plt.imshow(K, cmap='viridis')
        plt.colorbar()
        plt.title(f"Kernel {i}")
    plt.tight_layout()
    plt.savefig("kernel_2d.png")
    plt.close() 