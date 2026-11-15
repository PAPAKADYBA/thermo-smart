"""Lance les scenarios C0 a C4 (cycle jour/nuit sur la piece 2D) et compare les resultats."""
import json
import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["lamBeton", "lamIso", "lamPlat", "rcIso", "absorp", "achDay", "achNight"]


def write_params(params, tag):
    lines = [f"{k} {params[k]}" for k in ORDER] + [f"tag {tag}"]
    (ROOT / "config" / "cycle_params.txt").write_text("\n".join(lines) + "\n")


def run_freefem():
    res = subprocess.run(["FreeFem++", "-nw", "freefem/08_room2d_cycle.edp"],
                         cwd=ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError("FreeFem++ a échoué :\n" + res.stdout[-1500:] + res.stderr[-500:])


def read_summary(tag):
    f = (ROOT / "data" / "results" / f"cycle_summary_{tag}.txt").read_text().split()
    names = ["tag", "Tmean", "Tmax", "Tmin", "hmax", "DH28", "DH30", "Qext", "Qint", "dp", "res"]
    return {n: (v if n == "tag" else float(v)) for n, v in zip(names, f)}


def main():
    cfg = json.loads((ROOT / "config" / "cycle_scenarios.json").read_text(encoding="utf-8"))
    rows = []
    for sc in cfg["scenarios"]:
        params = {**cfg["base"], **sc["changes"]}
        tag = sc["tag"]
        print(f"Calcul du scénario {tag} ({sc['nom']}) ... (25 jours simulés)")
        write_params(params, tag)
        run_freefem()
        s = read_summary(tag)
        rows.append({
            "Scénario": tag, "Nom": sc["nom"],
            "T air moy (C)": s["Tmean"], "T air max (C)": s["Tmax"], "T air min (C)": s["Tmin"],
            "Amplitude (C)": (s["Tmax"] - s["Tmin"]) / 2, "Heure du max (h)": s["hmax"],
            "DH>28 (C.h)": s["DH28"], "DH>30 (C.h)": s["DH30"],
            "Périodicité (C)": s["dp"],
            "Bilan flux (%)": 100 * abs(s["Qext"] - s["Qint"]) / abs(s["Qext"]),
        })

    df = pd.DataFrame(rows)
    ref = df.loc[df["Scénario"] == "C0"].iloc[0]
    df.insert(4, "Ecart T moy vs C0 (C)", df["T air moy (C)"] - ref["T air moy (C)"])
    df.insert(10, "Ecart DH>30 vs C0 (%)", 100 * (df["DH>30 (C.h)"] - ref["DH>30 (C.h)"]) / ref["DH>30 (C.h)"])

    out = ROOT / "data" / "results" / "cycle_table.csv"
    df.to_csv(out, index=False)

    pd.set_option("display.width", 300)
    pd.set_option("display.max_columns", 30)
    print()
    print(df.to_string(index=False, float_format=lambda v: f"{v:.4g}"))
    print("\nTable enregistrée :", out)

    # Controles automatiques de convergence
    bad = df[(df["Périodicité (C)"] > 0.05) | (df["Bilan flux (%)"] > 0.5)]
    if bad.empty:
        print("Contrôles : tous les scénarios sont périodiques (< 0,05 C) et équilibrés (< 0,5 %).")
    else:
        print("ATTENTION, scénarios non convergés :", ", ".join(bad["Scénario"]))

    # On remet le fichier de parametres sur la reference
    base_ref = {**cfg["base"], **cfg["scenarios"][0]["changes"]}
    write_params(base_ref, cfg["scenarios"][0]["tag"])


if __name__ == "__main__":
    main()
