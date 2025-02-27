import matplotlib
matplotlib.use("Agg")  # Force le backend Agg (compatible avec tostring_rgb)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

#import matplotlib.animation as animation
import scipy as scipy
import scipy.fftpack  # ou np.fft
import random
import time
import pygame

paused = False

DPI = 100  # DPI de la fenêtre
width, height = 1280, 720  # Résolution en pixels de la fenêtre
# Calculer la taille de la figure en pouces
figsize = (width / DPI, height / DPI)
#figsize = (width, height)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lenia Simulation")

def gauss(x, mu, sigma):
    return np.exp(-0.5 * ((x-mu)/sigma)**2)

def sigmoid(x, mu, sigma):
    return 1 / (1 + np.exp(- (x - mu) / sigma))

def sinusoidal(x, mu, sigma):
    return np.sin(np.pi * (x - mu) / sigma) ** 2

def multi_peak_growth(x, mu1=0.15, sigma1=0.02, mu2=0.6, sigma2=0.05):
    return np.exp(-0.5 * ((x - mu1) / sigma1) ** 2) + np.exp(-0.5 * ((x - mu2) / sigma2) ** 2)

def soft_growth(x, mu=0.15, sigma1=0.02, sigma2=0.05):
    return np.exp(-0.5 * ((x - mu) / sigma1)**2) + 0.3 * np.exp(-0.5 * ((x - 0.5) / sigma2)**2)

def multi_peak_soft_growth(x, mu1=0.15, sigma1=0.02, mu2=0.6, sigma2=0.05):
    return np.exp(-0.5 * ((x - mu) / sigma1)**2) + 0.3 * np.exp(-0.5 * ((x - 0.5) / sigma2)**2) + 0.3

# Définir une matrice d'interaction (exemple)
# Ici, interaction_matrix[i,j] indique l'influence du canal j sur le canal i.
interaction_matrix = np.array([
    [0.0, -0.02, 0.03],
    [-0.07, 0.0, 0.08],
    [0.01, -0.02, 0.0]
])
interaction_matrix = np.array([
     [0.3, 0.45, 0.37],             # rouge
     [-0.2, 0.35, 0.03],            # vert
     [0.25, -0.22, 0.3]            # bleu
])

def produce_movie_multi(Xs, evolve, interpolation = 'bicubic'):
    running = True
    paused = False
    clock = pygame.time.Clock()

    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    figsize = (width, height)
    fig, ax = plt.subplots(figsize=figsize, dpi=DPI)
    #ax.set_position([0, 0, 1, 1])
    #plt.axis('off')  # En option, pour masquer les axes

    canvas = FigureCanvas(fig)  # Utilisation du bon backend
    #im = plt.imshow(np.dstack(Xs), interpolation='bicubic')
    im = ax.imshow(np.dstack(Xs), interpolation=interpolation)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_a:  # Si la touche 'a' est pressée
                    Xs = inject_aquarium(Xs)
                if event.key == pygame.K_r:  # Si la touche 'a' est pressée
                    init_grid()
        if not paused:
            Xs = evolve(Xs)
            # Conversion directe de la simulation en image
            # Ici, on suppose que np.dstack(Xs) renvoie un tableau de forme (N, M, 3)
            data = np.dstack(Xs)
            # Si data est en flottant [0,1], convertir en uint8 [0,255]
            data_uint8 = (255 * np.clip(data, 0, 1)).astype(np.uint8)
            #colors = [np.clip(Xs[i] * 255, 0, 255) for i in range(3)]
            #final_image = np.stack(colors, axis=-1)  # Combiner en une image couleur
        
            # Créer une surface pygame (attention : pygame.surfarray.make_surface attend un tableau (width, height, 3))
            # On échange les axes si nécessaire
            #surface = pygame.surfarray.make_surface(final_image.swapaxes(0, 1))
            surface = pygame.surfarray.make_surface(data_uint8.swapaxes(0, 1))
            scaled_surface = pygame.transform.smoothscale(surface, (width, height))

            #screen.blit(frame, (0, 0))
            screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            clock.tick(25)
    pygame.quit()


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

R = 12

bs = [k["b"] for k in kernels]
rs = [R * k["r"] for k in kernels]
ms = [k["m"] for k in kernels]
ss = [k["s"] for k in kernels]
hs = [k["h"] for k in kernels]
sources = [k["c0"] for k in kernels]
destinations = [k["c1"] for k in kernels]

# Compute the (FFT of) the kernel filters, each being made of several rings
N = 384
M = int(np.ceil((16*N)/9))
if M % 2 != 0:
    M += 1  # force M à être pair

X = np.zeros((N, M))

fhs_y = N // 2    # Filter half size
fhs_x = M // 2
y, x = np.ogrid[-fhs_y:fhs_y, -fhs_x:fhs_x]

Ks = []
for b,r in zip(bs,rs):
    distance = np.sqrt(x**2 + y**2) / r * len(b)
    K = np.zeros_like(distance)
    mu = 0.5
    sigma = 0.15
    for i in range(len(b)):
        mask = (distance.astype(int) == i)
        K += mask * b[i] * gauss(distance%1, mu, sigma)
        #K += mask * b[i] * sinusoidal(distance%1, mu, sigma)
        #K += mask * b[i] * soft_growth(distance%1, mu, sigma)
        K += mask * b[i] * multi_peak_soft_growth(distance%1, mu, sigma)
    Ks.append(K/np.sum(K))

fKs = []
for K in Ks:
    fK = np.fft.fft2(np.fft.fftshift(K))
    fKs.append(fK)

# Plot the cross section of the different K in Ks
plt.figure(figsize=(10,10))
for i,K in enumerate(Ks):
    plt.plot(K[N//2,:], label = i)
plt.legend()
plt.xlim(M//2 - 20, M//2 + 20)

# Plot the growth function associated to the different ms and ss
plt.figure(figsize=(10,10))
for m,s,h in zip(ms,ss,hs):
#    plt.plot(np.linspace(0,1,100), h*(2 * soft_growth(np.linspace(0,1,100), m, s) - 1))
#    plt.plot(np.linspace(0,1,100), h*(2 * multi_peak_soft_growth(np.linspace(0,1,100), m, s) - 1))
    plt.plot(np.linspace(0,1,100), h*(2 * gauss(np.linspace(0,1,100), m, s) - 1))

dt = 0.5

def evolve_multi_channels(Xs):
    fXs = [np.fft.fft2(X) for X in Xs]
    # For each kernel we compute the convolution with the corresponding source channel
    Us = [np.real(np.fft.ifft2(fK * fXs[source])) for fK,source in zip(fKs,sources)]
    # We compute the activation associated to each of those convolutions
    #As = [2*multi_peak_soft_growth(U, ms[i], ss[i]) - 1 for i,U in enumerate(Us)]
    As = [2*gauss(U, ms[i], ss[i]) - 1 for i,U in enumerate(Us)]
    #As = [2*gauss(U, ms[i], ss[i]) - 1 for i,U in enumerate(Us)]
    # Then we apply this activation to the corresponding destination channel with the corresponding strength
    Gs = np.zeros_like(Xs)
    for destination, h, A in zip(destinations, hs, As):
        Gs[destination] += h * A
    # Finally we update the channels
    Xs = [np.clip(X + dt * G, 0, 1) for X,G in zip(Xs,Gs)]
    return Xs

def evolve_multi_channels_interactions(Xs):
    # Calculer les FFT de chaque canal
    fXs = [np.fft.fft2(X) for X in Xs]
    # Convolutions pour chaque kernel selon le canal source associé
    Us = [np.real(np.fft.ifft2(fK * fXs[source])) for fK, source in zip(fKs, sources)]
    # Calculer la fonction de croissance (activation) pour chaque kernel
    #As = [2 * multi_peak_soft_growth(U, ms[i], ss[i]) - 1 for i, U in enumerate(Us)]
    #As = [2 * soft_growth(U, ms[i], ss[i]) - 1 for i, U in enumerate(Us)]
    As = [2 * gauss(U, ms[i], ss[i]) - 1 for i, U in enumerate(Us)]
    #As = [2 * sinusoidal(U, ms[i], ss[i]) - 1 for i, U in enumerate(Us)]
    # Initialiser le terme de croissance pour chaque canal
    Gs = [np.zeros_like(X) for X in Xs]
    # Contribution des kernels vers le canal de destination
    for destination, h, A in zip(destinations, hs, As):
        Gs[destination] += h * A
    # Ajouter un terme d'interaction entre les canaux
    for i in range(len(Xs)):
        interaction_term = np.zeros_like(Xs[i])
        for j in range(len(Xs)):
            if i != j:
                # L'influence de Xs[j] sur le canal i est pondérée par le coefficient de la matrice
                interaction_term += interaction_matrix[i, j] * Xs[j]
        # Ajouter ce terme d'interaction à la variation de Xs[i]
        Gs[i] += interaction_term
    # Mise à jour des canaux avec le pas de temps dt
    Xs = [np.clip(X + dt * G, 0, 1) for X, G in zip(Xs, Gs)]
    return Xs

aquarium = [[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.49,1.0,0,0.03,0.49,0.49,0.28,0.16,0.03,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0.6,0.47,0.31,0.58,0.51,0.35,0.28,0.22,0,0,0,0,0], [0,0,0,0,0,0,0.15,0.32,0.17,0.61,0.97,0.29,0.67,0.59,0.88,1.0,0.92,0.8,0.61,0.42,0.19,0,0,0], [0,0,0,0,0,0,0,0.25,0.64,0.26,0.92,0.04,0.24,0.97,1.0,1.0,1.0,1.0,0.97,0.71,0.33,0.12,0,0], [0,0,0,0,0,0,0,0.38,0.84,0.99,0.78,0.67,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.95,0.62,0.37,0,0], [0,0,0,0,0.04,0.11,0,0.69,0.75,0.75,0.91,1.0,1.0,0.89,1.0,1.0,1.0,1.0,1.0,1.0,0.81,0.42,0.07,0], [0,0,0,0,0.44,0.63,0.04,0,0,0,0.11,0.14,0,0.05,0.64,1.0,1.0,1.0,1.0,1.0,0.92,0.56,0.23,0], [0,0,0,0,0.11,0.36,0.35,0.2,0,0,0,0,0,0,0.63,1.0,1.0,1.0,1.0,1.0,0.96,0.49,0.26,0], [0,0,0,0,0,0.4,0.37,0.18,0,0,0,0,0,0.04,0.41,0.52,0.67,0.82,1.0,1.0,0.91,0.4,0.23,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0.05,0.45,0.89,1.0,0.66,0.35,0.09,0], [0,0,0.22,0,0,0,0.05,0.36,0.6,0.13,0.02,0.04,0.24,0.34,0.1,0,0.04,0.62,1.0,1.0,0.44,0.25,0,0], [0,0,0,0.43,0.53,0.58,0.78,0.9,0.96,1.0,1.0,1.0,1.0,0.71,0.46,0.51,0.81,1.0,1.0,0.93,0.19,0.06,0,0], [0,0,0,0,0.23,0.26,0.37,0.51,0.71,0.89,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.42,0.06,0,0,0], [0,0,0,0,0.03,0,0,0.11,0.35,0.62,0.81,0.93,1.0,1.0,1.0,1.0,1.0,0.64,0.15,0,0,0,0,0], [0,0,0,0,0,0,0.06,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0.05,0.09,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
  [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02,0.28,0.42,0.44,0.34,0.18,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.34,1.0,1.0,1.0,1.0,1.0,0.91,0.52,0.14,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.17,0.75,1.0,1.0,1.0,1.0,1.0,1.0,0.93,0.35,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.22,0.92,1.0,1.0,1.0,1.0,1.0,1.0,0.59,0.09], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.75,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.71,0.16], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.67,0.83,0.85,1.0,1.0,1.0,1.0,1.0,1.0,0.68,0.17], [0,0,0,0,0,0,0,0,0,0,0,0,0.21,0.04,0.12,0.58,0.95,1.0,1.0,1.0,1.0,1.0,0.57,0.13], [0,0,0,0,0,0,0,0,0,0,0,0.07,0,0,0,0.2,0.64,0.96,1.0,1.0,1.0,0.9,0.24,0.01], [0,0,0,0,0,0,0,0,0,0,0.13,0.29,0,0,0,0.25,0.9,1.0,1.0,1.0,1.0,0.45,0.05,0], [0,0,0,0,0,0,0,0,0,0,0.13,0.31,0.07,0,0.46,0.96,1.0,1.0,1.0,1.0,0.51,0.12,0,0], [0,0,0,0,0,0,0,0,0.26,0.82,1.0,0.95,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.3,0.05,0,0,0], [0,0,0,0,0,0,0,0,0.28,0.74,1.0,0.95,0.87,1.0,1.0,1.0,1.0,1.0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.07,0.69,1.0,1.0,1.0,1.0,1.0,0.96,0.25,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0.4,0.72,0.9,0.83,0.7,0.56,0.43,0.14,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
  [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.04,0.25,0.37,0.44,0.37,0.24,0.11,0.04,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.19,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.75,0.4,0.15,0,0,0,0], [0,0,0,0,0,0,0,0,0.14,0.48,0.83,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.4,0,0,0,0], [0,0,0,0,0,0,0,0,0.62,0.78,0.94,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.64,0,0,0,0], [0,0,0,0,0,0,0,0.02,0.65,0.98,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.78,0,0,0,0], [0,0,0,0,0,0,0,0.15,0.48,0.93,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.79,0.05,0,0,0], [0,0,0,0,0,0,0.33,0.56,0.8,1.0,1.0,1.0,0.37,0.6,0.94,1.0,1.0,1.0,1.0,0.68,0.05,0,0,0], [0,0,0,0,0.35,0.51,0.76,0.89,1.0,1.0,0.72,0.15,0,0.29,0.57,0.69,0.86,1.0,0.92,0.49,0,0,0,0], [0,0,0,0,0,0.38,0.86,1.0,1.0,0.96,0.31,0,0,0,0,0.02,0.2,0.52,0.37,0.11,0,0,0,0], [0,0,0.01,0,0,0.07,0.75,1.0,1.0,1.0,0.48,0.03,0,0,0,0,0,0.18,0.07,0,0,0,0,0], [0,0.11,0.09,0.22,0.15,0.32,0.71,0.94,1.0,1.0,0.97,0.54,0.12,0.02,0,0,0,0,0,0,0,0,0,0], [0.06,0.33,0.47,0.51,0.58,0.77,0.95,1.0,1.0,1.0,1.0,0.62,0.12,0,0,0,0,0,0,0,0,0,0,0], [0.04,0.4,0.69,0.88,0.95,1.0,1.0,1.0,1.0,1.0,0.93,0.68,0.22,0.02,0,0,0.01,0,0,0,0,0,0,0], [0,0.39,0.69,0.91,1.0,1.0,1.0,1.0,1.0,0.85,0.52,0.35,0.24,0.17,0.07,0,0,0,0,0,0,0,0,0], [0,0,0.29,0.82,1.0,1.0,1.0,1.0,1.0,1.0,0.67,0.29,0.02,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.2,0.51,0.77,0.96,0.93,0.71,0.4,0.16,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.08,0.07,0.03,0,0,0,0,0,0,0,0,0,0,0,0,0]]]

# Fonction pour générer des positions aléatoires sans dépasser les bords
def get_random_position():
    max_xa = N - aquarium[0].shape[0]
    max_ya = M - aquarium[0].shape[1]
    pos_xa = random.randint(0, max_xa)
    pos_ya = random.randint(0, max_ya)
    return pos_xa, pos_ya

# Fonction pour injecter l'aquarium dans la simulation à une position aléatoire
def inject_aquarium(Xs):
    pos_xa, pos_ya = get_random_position()
    for c in range(3):
        # Insertion de l'aquarium dans Xs à la position aléatoire
        Xs[c][pos_xa:pos_xa + aquarium[c].shape[0], pos_ya:pos_ya + aquarium[c].shape[1]] = aquarium[c]
    return Xs

aquarium = [np.array(aquarium[c]) for c in range(3)]

# Initialisation de la grille avec l'injection de 2 object de type aquarium
def init_grid():
    Xs = [np.zeros((N, M)) for _ in range(3)]
    pos_xa, pos_ya = get_random_position()
    pos_xa2, pos_ya2 = get_random_position()
    for c in range(3):
        Xs[c][pos_xa:pos_xa + aquarium[c].shape[0], pos_ya:pos_ya + aquarium[c].shape[1]] = aquarium[c]
        Xs[c][pos_xa2:pos_xa2 + aquarium[c].shape[0], pos_ya2:pos_ya2 + aquarium[c].shape[1]] = aquarium[-c]
    
    return Xs

Xs = init_grid()
#produce_movie_multi(Xs, evolve_multi_channels, "toto", 0)
produce_movie_multi(Xs, evolve_multi_channels_interactions) 