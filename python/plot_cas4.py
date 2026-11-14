"""Carte de temperature de la piece 2D (cas test 4) avec zooms sur les coins."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation

data = np.loadtxt("data/results/cas4_T.txt")
x, y, T = data[:, 0], data[:, 1], data[:, 2]
tri = np.loadtxt("data/results/cas4_tri.txt", dtype=int)

print("Noeuds     :", x.size)
print("Triangles  :", tri.shape[0])
print("Tmin, Tmax :", T.min(), T.max())
i = int(np.argmax(T))
print("Maximum atteint en (x, y) = (%.2f, %.2f) m, T = %.4f C" % (x[i], y[i], T[i]))

triang = Triangulation(x, y, tri)
levels = np.linspace(24.99, 35.01, 41)

fig = plt.figure(figsize=(13, 7))
gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1])
ax = fig.add_subplot(gs[:, 0])
axz1 = fig.add_subplot(gs[0, 1])
axz2 = fig.add_subplot(gs[1, 1])

for a in (ax, axz1, axz2):
    c = a.tricontourf(triang, T, levels=levels, cmap="coolwarm")
    a.set_aspect("equal")
    a.set_xlabel("x (m)")
    a.set_ylabel("y (m)")

ax.set_title("Coupe de la pièce : température (régime stationnaire)")
axz1.set_xlim(0, 0.9)
axz1.set_ylim(2.5, 3.32)
axz1.set_title("Zoom : coin haut gauche (mur / toit)")
axz2.set_xlim(0, 0.9)
axz2.set_ylim(0, 0.8)
axz2.set_title("Zoom : coin bas gauche (mur / plancher)")

fig.colorbar(c, ax=[ax, axz1, axz2], label="Température (°C)", shrink=0.8)
fig.savefig("data/results/cas4_carte.png", dpi=150, bbox_inches="tight")
print("Image enregistrée : data/results/cas4_carte.png")
