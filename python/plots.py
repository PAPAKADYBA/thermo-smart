"""Carte de température du cas test 1 + vérification par la solution exacte."""
import matplotlib
matplotlib.use("Agg")  # pas de fenêtre : on enregistre une image
import matplotlib.pyplot as plt
import numpy as np

from results_reader import read_temperature

L, Tleft, Tright = 4.0, 30.0, 20.0

x, y, T = read_temperature("data/results/cas1_T.txt")

# Vérification côté Python
T_exact = Tleft - (Tleft - Tright) / L * x
print("Nombre de points :", T.size)
print("Tmin, Tmax (C)   :", T.min(), T.max())
print("Ecart max (C)    :", np.abs(T - T_exact).max())

# Carte de température
fig, ax = plt.subplots(figsize=(7, 5))
c = ax.tricontourf(x, y, T, levels=20, cmap="coolwarm")
fig.colorbar(c, ax=ax, label="Température (°C)")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_title("Cas test 1 : température (régime stationnaire)")
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig("data/results/cas1_carte.png", dpi=150)
print("Image enregistrée : data/results/cas1_carte.png")
