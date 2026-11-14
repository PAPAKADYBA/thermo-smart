"""Evolution temporelle du mur composite (cas test 3)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("data/results/cas3_t.txt")   # la ligne d'en-tête (#) est ignorée
t = data[:, 0]

points = [("x = 0 (face extérieure)", 1, 34.8595),
          ("x = 0,20 m (béton/isolant)", 2, 34.3579),
          ("x = 0,30 m (isolant/plâtre)", 3, 25.5794),
          ("x = 0,32 m (face intérieure)", 4, 25.4389)]

print("Nombre de pas lus :", t.size)
print("Durée simulée (h) :", t[-1])

# Constante de temps du béton : temps pour atteindre 63,2 % de la variation totale à x = 0,20 m
T020 = data[:, 2]
cible = T020[0] + 0.632 * (34.3579 - T020[0])
t63 = np.interp(cible, T020, t)
print("Constante de temps du béton (h) :", round(float(t63), 1))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

for label, col, steady in points:
    (line,) = ax1.plot(t, data[:, col], label=label)
    ax1.axhline(steady, color=line.get_color(), ls=":", lw=1)
ax1.axvline(t63, color="gray", ls="--", lw=1)
ax1.set_xlabel("Temps (h)")
ax1.set_ylabel("Température (°C)")
ax1.set_title("Évolution de la température dans le mur")
ax1.legend(loc="center right", fontsize=8)

ax2.plot(t, data[:, 5], label="Flux entrant (face ext.)")
ax2.plot(t, data[:, 6], label="Flux sortant (face int.)")
ax2.axhline(3.5114, color="k", ls=":", lw=1, label="Régime stationnaire (3,51 W/m²)")
ax2.set_ylim(0, 12)
ax2.set_xlabel("Temps (h)")
ax2.set_ylabel("Flux (W/m²)")
ax2.set_title("Flux thermique (pic initial ~250 W/m² hors graphique)")
ax2.legend(fontsize=8)

fig.tight_layout()
fig.savefig("data/results/cas3_temps.png", dpi=150)
print("Image enregistrée : data/results/cas3_temps.png")
