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

def generate_kernels():
    """
    Génère les kernels pour la simulation Lenia.
    
    Returns:
        tuple: (Ks, fKs) où Ks est la liste des kernels et fKs est la liste des transformées de Fourier des kernels
    """
    # Initialisation
    fhs_y = N // 2    # Filter half size (hauteur)
    fhs_x = M // 2    # Filter half size (largeur)
    y, x = np.ogrid[-fhs_y:fhs_y, -fhs_x:fhs_x]
    
    # Génération des kernels
    Ks = []
    for b, r in zip(bs, rs):
        distance = np.sqrt(x**2 + y**2) / r * len(b)
        K = np.zeros_like(distance)
        
        for i in range(len(b)):
            mask = (distance.astype(int) == i)
            K += mask * b[i] * gauss(distance % 1, kernel_mu, kernel_sigma)
            # Alternatives commentées:
            # K += mask * b[i] * sinusoidal(distance % 1, kernel_mu, kernel_sigma)
            # K += mask * b[i] * soft_growth(distance % 1, kernel_mu, kernel_sigma)
            K += mask * b[i] * multi_peak_soft_growth(distance % 1, kernel_mu, kernel_sigma)
        
        # Normalisation du kernel
        Ks.append(K / np.sum(K))
    
    # Calcul des transformées de Fourier des kernels
    fKs = []
    for K in Ks:
        fK = np.fft.fft2(np.fft.fftshift(K))
        fKs.append(fK)
    
    return Ks, fKs

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
        plt.plot(K[N//2, :], label=i)
    plt.legend()
    plt.xlim(M//2 - 20, M//2 + 20)
    plt.title("Coupe transversale des kernels")
    plt.xlabel("Position")
    plt.ylabel("Valeur")
    plt.grid(True)
    plt.savefig("kernel_cross_sections.png")
    plt.close() 