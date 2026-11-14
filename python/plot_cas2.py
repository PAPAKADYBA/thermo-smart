"""Profil et carte de temperature du cas test 2 (mur composite)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from results_reader import read_temperature

x, y, T = read_temperature("data/results/cas2_T.txt")

# Profil a y = 0.5 m
mask = np.isclose(y, 0.5)
xs, Ts = x[mask], T[mask]
order = np.argsort(xs)
xs, Ts = xs[order], Ts[order]

# Solution exacte aux interfaces (resistances thermiques en serie)
xe = np.array([0.0, 0.20, 0.30, 0.32])
Te = np.array([34.8595, 34.3579, 25.5794, 25.4389])

print("Nombre de points :", T.size)
print("Points du profil :", xs.size)
print("Ecart max aux interfaces (C) :", np.abs(np.interp(xe, xs, Ts) - Te).max())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5),
                               gridspec_kw={"width_ratios": [2, 1]})

layers = [(0.00, 0.20, "Béton", "#bdbdbd"),
          (0.20, 0.30, "Isolant", "#ffe08a"),
          (0.30, 0.32, "Plâtre", "#d8c3a5")]
for a, b, name, col in layers:
    ax1.axvspan(a, b, color=col, alpha=0.6, label=name)

ax1.axhline(35, color="red", ls=":", lw=1)
ax1.axhline(25, color="blue", ls=":", lw=1)
ax1.plot(xs, Ts, "k-", lw=2, label="Calcul P1")
ax1.plot(xe, Te, "ro", label="Solution exacte")
ax1.set_xlabel("x (m) : extérieur vers intérieur")
ax1.set_ylabel("Température (°C)")
ax1.set_title("Profil de température à travers le mur")
ax1.legend(loc="center left")

c = ax2.tricontourf(x, y, T, levels=20, cmap="coolwarm")
fig.colorbar(c, ax=ax2, label="Température (°C)")
ax2.set_xlabel("x (m)")
ax2.set_ylabel("y (m)")
ax2.set_title("Carte de température")
ax2.set_aspect("equal")

fig.tight_layout()
fig.savefig("data/results/cas2_profil.png", dpi=150)
print("Image enregistrée : data/results/cas2_profil.png")
