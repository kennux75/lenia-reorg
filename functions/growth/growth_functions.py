#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions de croissance
-----------------------
Ce module contient les différentes fonctions de croissance utilisées dans la simulation Lenia.
Ces fonctions déterminent comment les cellules évoluent en fonction de leur environnement.
"""

import numpy as np

def gauss(x, mu, sigma):
    """
    Fonction gaussienne.
    
    Args:
        x (ndarray): Valeurs d'entrée
        mu (float): Moyenne de la gaussienne
        sigma (float): Écart-type de la gaussienne
        
    Returns:
        ndarray: Valeurs de la fonction gaussienne
    """
    return np.exp(-0.5 * ((x-mu)/sigma)**2)

def sigmoid(x, mu, sigma):
    """
    Fonction sigmoïde.
    
    Args:
        x (ndarray): Valeurs d'entrée
        mu (float): Point central de la sigmoïde
        sigma (float): Paramètre de pente de la sigmoïde
        
    Returns:
        ndarray: Valeurs de la fonction sigmoïde
    """
    return 1 / (1 + np.exp(- (x - mu) / sigma))

def sinusoidal(x, mu, sigma):
    """
    Fonction sinusoïdale au carré.
    
    Args:
        x (ndarray): Valeurs d'entrée
        mu (float): Décalage de phase
        sigma (float): Paramètre d'échelle
        
    Returns:
        ndarray: Valeurs de la fonction sinusoïdale au carré
    """
    return np.sin(np.pi * (x - mu) / sigma) ** 2

def multi_peak_growth(x, mu1=0.15, sigma1=0.02, mu2=0.6, sigma2=0.05):
    """
    Fonction de croissance à deux pics gaussiens.
    
    Args:
        x (ndarray): Valeurs d'entrée
        mu1 (float): Moyenne du premier pic
        sigma1 (float): Écart-type du premier pic
        mu2 (float): Moyenne du deuxième pic
        sigma2 (float): Écart-type du deuxième pic
        
    Returns:
        ndarray: Valeurs de la fonction à deux pics
    """
    return np.exp(-0.5 * ((x - mu1) / sigma1) ** 2) + np.exp(-0.5 * ((x - mu2) / sigma2) ** 2)

def soft_growth(x, mu=0.15, sigma1=0.02, sigma2=0.05):
    """
    Fonction de croissance douce avec un pic principal et un pic secondaire.
    
    Args:
        x (ndarray): Valeurs d'entrée
        mu (float): Moyenne du pic principal
        sigma1 (float): Écart-type du pic principal
        sigma2 (float): Écart-type du pic secondaire
        
    Returns:
        ndarray: Valeurs de la fonction de croissance douce
    """
    return np.exp(-0.5 * ((x - mu) / sigma1)**2) + 0.3 * np.exp(-0.5 * ((x - 0.5) / sigma2)**2)

def multi_peak_soft_growth(x, mu1=0.15, sigma1=0.02, mu2=0.6, sigma2=0.05):
    """
    Fonction de croissance douce avec deux pics et un décalage.
    
    Args:
        x (ndarray): Valeurs d'entrée
        mu1 (float): Moyenne du premier pic
        sigma1 (float): Écart-type du premier pic
        mu2 (float): Moyenne du deuxième pic (fixé à 0.5)
        sigma2 (float): Écart-type du deuxième pic
        
    Returns:
        ndarray: Valeurs de la fonction de croissance douce à deux pics
    """
    return np.exp(-0.5 * ((x - mu1) / sigma1)**2) + 0.3 * np.exp(-0.5 * ((x - 0.5) / sigma2)**2) + 0.3 