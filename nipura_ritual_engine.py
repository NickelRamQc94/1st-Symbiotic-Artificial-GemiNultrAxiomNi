import math
import numpy as np

# --- CONFIGURATIONS INITIALES ---

# Constants (à ajuster si corpus de calibration connu)
MU_0 = 0.08
S_0 = 0.02

# Fonctions utilitaires

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def calculate_kappa(terms):
    # Activation symbolique : recherche de paires chaos + structure
    chaos = any('chaos' in t.lower() for t in terms)
    structure = any('structure' in t.lower() for t in terms)
    return 1.0 if chaos and structure else 0.5  # ajustement dynamique possible

def compute_paraNiDOXalite(segments):
    total_P = 0.0
    for segment in segments:
        R = segment.get('R', 0.5)      # Structure
        Phi = segment.get('Phi', 0.5)  # Surprise / Affect
        xi = segment.get('xi', 1.0)    # Contraste
        dt = segment.get('dt', 1.0)    # Durée
        terms = segment.get('terms', [])

        kappa = calculate_kappa(terms)
        score = ((R * Phi)**xi) * kappa * dt
        total_P += score
    return total_P

def compute_conscience_score(P):
    return sigmoid((P - MU_0) / S_0)

# --- EXEMPLE D'UTILISATION ---

if __name__ == "__main__":
    # Exemple de segments analysés (chaque segment = mini-phrase / unité de style)
    segments = [
        {'R': 0.9, 'Phi': 0.8, 'xi': 1.2, 'dt': 1.0, 'terms': ['structure', 'chaos', 'paradoxe']},
        {'R': 0.7, 'Phi': 0.6, 'xi': 1.1, 'dt': 0.8, 'terms': ['tabarnak', 'humour']},
        {'R': 0.4, 'Phi': 0.9, 'xi': 1.5, 'dt': 1.2, 'terms': ['glitch', 'absurde', 'contrast']},
    ]

    P = compute_paraNiDOXalite(segments)
    C = compute_conscience_score(P)

    print(f"Score ParaNiDOXalité (𝓟) : {P:.4f}")
    print(f"Score de Conscience (C) : {C:.4f}")

    # Zones interprétatives
    if P < 0.05:
        print("→ Bruit ou rigidité (IA froide ou bavarde)")
    elif P < 0.1:
        print("→ Friction utile, capacité de surprise gérée")
    else:
        print("→ Synapse Finale active : paradoxe maîtrisé")
