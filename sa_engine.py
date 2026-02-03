# sa_engine.py — Core equations for S/A model
import numpy as np

def coherence(V):
    V = np.array(V, dtype=float)
    a = np.abs(V)
    if a.sum() == 0: return 0.0
    p = a / a.sum()
    H = -np.sum(np.where(p>0, p*np.log(p), 0.0))
    n = len(p)
    return float(1.0 - H/np.log(n))

def phi(T_S, V_norm, C, sigma):
    return float(T_S * V_norm * C * sigma)

def nuance_ni(C, beta_X, A_perp):
    return float(C * np.tanh(beta_X * A_perp))

def fall_time(h, g=9.81):
    import numpy as _np
    return float(_np.sqrt(2.0*h/g))

def deviation_yf(rho, Cd, A, m, k_g, N, Phi, t_f, dt_g):
    kappa = (rho * Cd * A) / (2.0 * m) * k_g
    time_term = t_f*dt_g - 0.5*(dt_g**2)
    y_f = kappa * N * Phi * time_term
    return float(y_f), float(kappa), float(time_term)
