#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration de la simulation
-----------------------------
Ce fichier contient les paramètres de configuration pour la simulation Lenia.
"""

import numpy as np

# Dimensions de la grille
N = 384  # Hauteur de la grille
M = int(np.ceil((16*N)/9))  # Largeur de la grille (ratio 16:9)
if M % 2 != 0:
    M += 1  # Force M à être pair pour optimiser les calculs FFT

# Paramètres temporels
dt = 0.5  # Pas de temps pour l'évolution

# Rayon de base pour les kernels
R = 12  # Rayon de base pour les kernels

# Matrice d'interaction entre canaux
# interaction_matrix[i,j] indique l'influence du canal j sur le canal i
interaction_matrix = np.array([
    [0.3, 0.45, 0.37],   # rouge
    [-0.2, 0.35, 0.03],  # vert
    [0.25, -0.22, 0.3]   # bleu
])

# Paramètres des kernels
# b: poids des anneaux, m: moyenne, s: écart-type, h: hauteur, r: rayon relatif, c0: canal source, c1: canal destination
kernels = [
    {"b":[1], "m":0.272, "s":0.0595, "h":0.138, "r":0.91, "c0":0, "c1":0},  
    {"b":[1], "m":0.349, "s":0.1585, "h":0.48, "r":0.62, "c0":0, "c1":0},  
    {"b":[1,1/4], "m":0.2, "s":0.0332, "h":0.284, "r":0.5, "c0":0, "c1":0},  
    {"b":[0,1], "m":0.114, "s":0.0528, "h":0.256, "r":0.97, "c0":1, "c1":1},  
    {"b":[1], "m":0.447, "s":0.0777, "h":0.5, "r":0.72, "c0":1, "c1":1},  
    {"b":[5/6,1], "m":0.247, "s":0.0342, "h":0.622, "r":0.8, "c0":1, "c1":1},  
    {"b":[1], "m":0.21, "s":0.0617, "h":0.35, "r":0.96, "c0":2, "c1":2},  
    {"b":[1], "m":0.462, "s":0.1192, "h":0.218, "r":0.56, "c0":2, "c1":2},  
    {"b":[1], "m":0.446, "s":0.1793, "h":0.556, "r":0.78, "c0":2, "c1":2},  
    {"b":[11/12,1], "m":0.327, "s":0.1408, "h":0.344, "r":0.79, "c0":0, "c1":1},  
    {"b":[3/4,1], "m":0.476, "s":0.0995, "h":0.456, "r":0.5, "c0":0, "c1":2},  
    {"b":[11/12,1], "m":0.379, "s":0.0697, "h":0.67, "r":0.72, "c0":1, "c1":0},  
    {"b":[1], "m":0.262, "s":0.0877, "h":0.42, "r":0.68, "c0":1, "c1":2},  
    {"b":[1/6,1,0], "m":0.412, "s":0.1101, "h":0.43, "r":0.82, "c0":2, "c1":0},  
    {"b":[1], "m":0.201, "s":0.0786, "h":0.278, "r":0.82, "c0":2, "c1":1},  
    {"b":[1/4, 1], "m":0.3, "s":0.1, "h":-0.4, "r":1.2, "c0":0, "c1":0},  
    {"b":[1/10, 1], "m":0.3, "s":0.2, "h":-0.6, "r":2.0, "c0":1, "c1":1},  
    {"b":[3/4, 1], "m":0.15, "s":0.05, "h":-0.5, "r":6.0, "c0":2, "c1":2},  
    {"b":[3/4, 1], "m":0.15, "s":0.05, "h":-0.5, "r":6.0, "c0":0, "c1":0},  
    {"b":[1, 1/4], "m":0.3, "s":0.1, "h":-0.2, "r":2.5, "c0":0, "c1":1},  
    {"b":[1, 1/4], "m":0.3, "s":0.1, "h":-0.1, "r":2.5, "c0":1, "c1":0},  
    {"b":[1, 1/6], "m":0.3, "s":0.15, "h":0.4, "r":3.0, "c0":2, "c1":0},  
    {"b":[1, 1/6], "m":0.3, "s":0.15, "h":0.4, "r":2.0, "c0":2, "c1":0},  
    {"b":[1, 1/6], "m":0.3, "s":0.15, "h":-0.1, "r":3.0, "c0":2, "c1":2},  
    {"b":[1, 1/6], "m":0.3, "s":0.15, "h":0.5, "r":3.0, "c0":0, "c1":0},  
]

# Extraction des paramètres des kernels pour faciliter l'accès
bs = [k["b"] for k in kernels]  # Poids des anneaux
rs = [R * k["r"] for k in kernels]  # Rayons absolus
ms = [k["m"] for k in kernels]  # Moyennes
ss = [k["s"] for k in kernels]  # Écarts-types
hs = [k["h"] for k in kernels]  # Hauteurs
sources = [k["c0"] for k in kernels]  # Canaux sources
destinations = [k["c1"] for k in kernels]  # Canaux destinations

# Paramètres pour la génération des kernels
kernel_mu = 0.5  # Moyenne pour la fonction gaussienne dans les kernels
kernel_sigma = 0.15  # Écart-type pour la fonction gaussienne dans les kernels 