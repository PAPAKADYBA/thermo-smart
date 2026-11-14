"""Lance les scenarios de config/scenarios.json sur la piece 2D et compare les resultats."""
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PARAM_ORDER = ["lamBeton", "lamIso", "lamPlat", "Text", "TextRoof", "Tint", "hext", "hint"]


def write_params(params, tag):
    lines = [f"{k} {params[k]}" for k in PARAM_ORDER] + [f"tag {tag}"]
    (ROOT / "config" / "room_params.txt").write_text("\n".join(lines) + "\n")


def run_freefem():
    res = subprocess.run(["FreeFem++", "-nw", "freefem/06_room2d_param.edp"],
                         cwd=ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError("FreeFem++ a échoué :\n" + res.stdout[-1500:] + res.stderr[-500:])


def read_summary(tag):
    f = (ROOT / "data" / "results" / f"room_summary_{tag}.txt").read_text().split()
    names = ["tag", "qext", "qint", "Tmean", "Fwall", "Froof", "Tmin", "Tmax"]
    return {n: (v if n == "tag" else float(v)) for n, v in zip(names, f)}


def interior_surface_stats(tag):
    """T min et max sur les surfaces interieures (bord du trou de la piece)."""
    d = np.loadtxt(ROOT / "data" / "results" / f"room_{tag}_T.txt")
    x, y, T = d[:, 0], d[:, 1], d[:, 2]
    tol = 1e-6
    on_walls = (np.isclose(x, 0.32) | np.isclose(x, 4.32)) & (y >= 0.20 - tol) & (y <= 3.00 + tol)
    on_floor_roof = (np.isclose(y, 0.20) | np.isclose(y, 3.00)) & (x >= 0.32 - tol) & (x <= 4.32 + tol)
    mask = on_walls | on_floor_roof
    return float(T[mask].min()), float(T[mask].max())


def expected_1d(p):
    """Flux 1D (W/m2) loin des coins : resistances en serie (beton 0,20 / isolant 0,10 / platre 0,02)."""
    R = 1 / p["hext"] + 0.20 / p["lamBeton"] + 0.10 / p["lamIso"] + 0.02 / p["lamPlat"] + 1 / p["hint"]
    return (p["Text"] - p["Tint"]) / R, (p["TextRoof"] - p["Tint"]) / R


def main():
    cfg = json.loads((ROOT / "config" / "scenarios.json").read_text(encoding="utf-8"))
    rows = []
    for sc in cfg["scenarios"]:
        params = {**cfg["base"], **sc["changes"]}
        tag = sc["tag"]
        print(f"Calcul du scénario {tag} ({sc['nom']}) ...")
        write_params(params, tag)
        run_freefem()
        s = read_summary(tag)
        tmin_i, tmax_i = interior_surface_stats(tag)
        q1d_wall, q1d_roof = expected_1d(params)
        rows.append({
            "Scénario": tag, "Nom": sc["nom"],
            "Flux total (W/m)": s["qext"],
            "Bilan (%)": 100 * abs(s["qext"] - s["qint"]) / s["qext"],
            "T moy int (C)": s["Tmean"], "T max int (C)": tmax_i,
            "Flux mur (W/m2)": s["Fwall"], "1D mur": q1d_wall,
            "Flux toit (W/m2)": s["Froof"], "1D toit": q1d_roof,
        })

    df = pd.DataFrame(rows)
    ref = df.loc[df["Scénario"] == "S0", "Flux total (W/m)"].iloc[0]
    df.insert(4, "Ecart vs S0 (%)", 100 * (df["Flux total (W/m)"] - ref) / ref)

    out = ROOT / "data" / "results" / "scenarios_table.csv"
    df.to_csv(out, index=False)

    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 20)
    print()
    print(df.to_string(index=False, float_format=lambda v: f"{v:.4g}"))
    print("\nTable enregistrée :", out)

    # On remet le fichier de parametres sur la reference
    write_params({**cfg["base"], **cfg["scenarios"][0]["changes"]}, cfg["scenarios"][0]["tag"])


if __name__ == "__main__":
    main()
