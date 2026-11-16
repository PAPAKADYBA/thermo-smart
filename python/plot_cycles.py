"""Courbes de confort sur 24 h pour les scenarios C0 a C4 (dernier jour simule)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("data/results/cycle_table.csv")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), gridspec_kw={"width_ratios": [2, 1]})

t_ext = None
for _, row in df.iterrows():
    tag = row["Scénario"]
    d = np.loadtxt(f"data/results/cycle_{tag}_t.txt")      # l'en-tete (#) est ignore
    last = d[:, 0] > d[-1, 0] - 24.0                      # dernier jour
    hod = d[last, 0] - (d[-1, 0] - 24.0)
    ax1.plot(hod, d[last, 3], lw=2, label=f"{tag} : {row['Nom']}")
    if t_ext is None:
        t_ext = (hod, d[last, 1])

ax1.plot(t_ext[0], t_ext[1], "k--", lw=1.5, label="Extérieur (air)")
ax1.axhline(30, color="gray", ls=":", lw=1)
ax1.axhline(28, color="gray", ls=":", lw=1)
ax1.text(0.2, 30.1, "30 °C", color="gray", fontsize=8)
ax1.text(0.2, 28.1, "28 °C", color="gray", fontsize=8)
ax1.set_xlim(0, 24)
ax1.set_xticks(range(0, 25, 3))
ax1.set_xlabel("Heure de la journée (h)")
ax1.set_ylabel("Température (°C)")
ax1.set_title("Température de l'air intérieur sur 24 h (régime périodique)")
ax1.legend(fontsize=8, loc="upper left")

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
bars = ax2.bar(df["Scénario"], df["DH>30 (C.h)"], color=colors[:len(df)])
for b, pct in zip(bars, df["Ecart DH>30 vs C0 (%)"]):
    label = "réf." if abs(pct) < 1e-9 else f"{pct:+.0f} %"
    ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 1, label, ha="center", fontweight="bold")
ax2.set_ylabel("Degrés-heures au-dessus de 30 °C (°C·h par jour)")
ax2.set_title("Surchauffe journalière")

fig.tight_layout()
fig.savefig("data/results/cycle_comparaison.png", dpi=150)
print("Image enregistrée : data/results/cycle_comparaison.png")
