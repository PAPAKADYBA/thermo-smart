"""Analyse du cycle jour/nuit sur le mur composite (cas test 5), dernier jour."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("data/results/cas5_t.txt")   # l'en-tete (#) est ignore
t = data[:, 0]
mask = t > 96.0                                 # 5e jour : de 96 h a 120 h
hod = t[mask] - 96.0                            # heure de la journee (0 a 24 h)

names = ["Extérieur (air)", "x = 0 (face ext.)", "x = 0,20 m (béton/isolant)",
         "x = 0,30 m (isolant/plâtre)", "x = 0,32 m (face int.)"]
cols = [1, 2, 3, 4, 5]

print("Nombre de pas sur le dernier jour :", int(mask.sum()))
print()
print("%-30s %9s %9s %12s %10s" % ("Point", "Moyenne", "Amplitude", "Heure du max", "Retard (h)"))
amps, lags = [], []
tmax_ext = None
for name, c in zip(names, cols):
    y = data[mask, c]
    amp = (y.max() - y.min()) / 2
    tmax = float(hod[np.argmax(y)])
    if tmax_ext is None:
        tmax_ext = tmax
    lag = (tmax - tmax_ext) % 24
    amps.append(amp)
    lags.append(lag)
    print("%-30s %9.3f %9.3f %12.2f %10.2f" % (name, y.mean(), amp, tmax, lag))

print()
print("Flux moyen entrant (W/m2) : %.4f   (attendu 1.7557)" % data[mask, 6].mean())
print("Flux moyen sortant (W/m2) : %.4f   (attendu 1.7557)" % data[mask, 7].mean())
print("Flux sortant : min %.3f, max %.3f W/m2" % (data[mask, 7].min(), data[mask, 7].max()))
print("Amplitude décroissante de l'extérieur vers l'intérieur :", all(a >= b for a, b in zip(amps[1:], amps[2:])))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

ax1.plot(hod, data[mask, 1], "k--", lw=1.5, label=names[0])
for name, c in zip(names[1:], cols[1:]):
    ax1.plot(hod, data[mask, c], lw=2, label=name)
ax1.set_xlabel("Heure de la journée (h)")
ax1.set_ylabel("Température (°C)")
ax1.set_title("Température dans le mur sur 24 h (régime périodique)")
ax1.set_xlim(0, 24)
ax1.set_xticks(range(0, 25, 3))
ax1.legend(fontsize=8, loc="center right")

ax2.plot(hod, data[mask, 6], lw=2, label="Flux entrant (face ext.)")
ax2.plot(hod, data[mask, 7], lw=2, label="Flux sortant (face int.)")
ax2.axhline(1.7557, color="k", ls=":", lw=1, label="Moyenne attendue (1,7557 W/m²)")
ax2.set_xlabel("Heure de la journée (h)")
ax2.set_ylabel("Flux (W/m²)")
ax2.set_title("Flux thermique sur 24 h")
ax2.set_xlim(0, 24)
ax2.set_xticks(range(0, 25, 3))
ax2.legend(fontsize=8)

fig.tight_layout()
fig.savefig("data/results/cas5_journee.png", dpi=150)
print("Image enregistrée : data/results/cas5_journee.png")
