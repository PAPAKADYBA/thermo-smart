"""Graphiques comparatifs des scenarios (lit data/results/scenarios_table.csv)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.tri import Triangulation

df = pd.read_csv("data/results/scenarios_table.csv")

# Decomposition du flux total (longueurs interieures : murs 2 x 2,8 m, toit 4,0 m)
df["Murs"] = df["Flux mur (W/m2)"] * 5.6
df["Toit"] = df["Flux toit (W/m2)"] * 4.0
df["Jonctions"] = df["Flux total (W/m)"] - df["Murs"] - df["Toit"]

print(df[["Scénario", "Nom", "Flux total (W/m)", "Murs", "Toit", "Jonctions"]]
      .round(2).to_string(index=False))

# --- Figure 1 : histogramme empile ---
labels = [f"{t}\n{n}" for t, n in zip(df["Scénario"], df["Nom"])]
fig, ax = plt.subplots(figsize=(10, 5.8))
ax.bar(labels, df["Murs"], label="Murs (2 x 2,8 m)")
ax.bar(labels, df["Toit"], bottom=df["Murs"], label="Toit (4,0 m)")
ax.bar(labels, df["Jonctions"], bottom=df["Murs"] + df["Toit"],
       label="Jonctions et plancher (reste)")
for i, total in enumerate(df["Flux total (W/m)"]):
    ax.text(i, total + 4, f"{total:.1f}", ha="center", fontweight="bold")
ax.set_ylabel("Flux entrant (W par mètre de profondeur)")
ax.set_title("Chaleur entrant dans la pièce selon le scénario (régime stationnaire)")
ax.legend()
fig.tight_layout()
fig.savefig("data/results/scenarios_flux.png", dpi=150)
print("Image enregistrée : data/results/scenarios_flux.png")

# --- Figure 2 : cartes cote a cote (meme echelle de couleurs) ---
fig2, axes = plt.subplots(2, 3, figsize=(16, 8.5))
axes = axes.ravel()
levels = np.linspace(24.9, 54.3, 60)
c = None
for a, (_, row) in zip(axes, df.iterrows()):
    tag = row["Scénario"]
    d = np.loadtxt(f"data/results/room_{tag}_T.txt")
    tri = np.loadtxt(f"data/results/room_{tag}_tri.txt", dtype=int)
    triang = Triangulation(d[:, 0], d[:, 1], tri)
    c = a.tricontourf(triang, d[:, 2], levels=levels, cmap="coolwarm")
    a.set_aspect("equal")
    a.set_title(f"{tag} : {row['Nom']}  ({row['Flux total (W/m)']:.1f} W/m)")
    a.set_xlabel("x (m)")
    a.set_ylabel("y (m)")
axes[5].axis("off")
fig2.colorbar(c, ax=axes.tolist(), label="Température (°C)", shrink=0.8)
fig2.savefig("data/results/scenarios_cartes.png", dpi=130, bbox_inches="tight")
print("Image enregistrée : data/results/scenarios_cartes.png")
