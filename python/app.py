"""THERMO-SMART : interface de demonstration (Streamlit)."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.tri import Triangulation

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_scenarios import (ROOT, write_params, run_freefem, read_summary,
                           interior_surface_stats, expected_1d)
import ui_confort

BASE = dict(lamBeton=1.4, lamIso=0.04, lamPlat=0.5, Text=35.0, TextRoof=35.0,
            Tint=25.0, hext=25.0, hint=8.0)


def calculer(params):
    """Ecrit les parametres, lance FreeFem++, lit les resultats, remet le fichier de reference."""
    write_params(params, "APP")
    try:
        run_freefem()
    finally:
        write_params(BASE, "S0")
    s = read_summary("APP")
    tmin_i, tmax_i = interior_surface_stats("APP")
    d = np.loadtxt(ROOT / "data" / "results" / "room_APP_T.txt")
    tri = np.loadtxt(ROOT / "data" / "results" / "room_APP_tri.txt", dtype=int)
    q1d_wall, q1d_roof = expected_1d(params)
    return {"s": s, "tmin_i": tmin_i, "tmax_i": tmax_i, "data": d, "tri": tri,
            "q1d_wall": q1d_wall, "q1d_roof": q1d_roof}


def flux_reference():
    try:
        return read_summary("S0")["qext"]
    except Exception:
        return None


st.set_page_config(page_title="THERMO-SMART", layout="wide")
st.title("THERMO-SMART")
st.caption("Plateforme de simulation thermique et d'optimisation énergétique des bâtiments. "
           "Version de démonstration : aide à l'étude, pas une certification réglementaire.")

tab1, tab2, tab3 = st.tabs(["Pièce (régime stationnaire)", "Confort sur 24 h", "Hypothèses et limites"])

with tab1:
    col_in, col_out = st.columns([1, 2])

    with col_in:
        st.subheader("Paramètres")
        sans_iso = st.checkbox("Sans isolant (couche remplacée par du béton)", value=False)
        lam_iso = st.slider("Conductivité de l'isolant (W/(m·K))", 0.020, 0.100, 0.040, 0.005,
                            disabled=sans_iso)
        Text = st.slider("Température de l'air extérieur (°C)", 25.0, 45.0, 35.0, 0.5)
        Tint = st.slider("Température intérieure maintenue (°C)", 18.0, 30.0, 25.0, 0.5)
        sun = st.slider("Ensoleillement sur le toit (W/m²)", 0, 1000, 0, 50)
        absorp = st.slider("Absorption solaire du toit (0,1 = très clair, 0,9 = très sombre)",
                           0.1, 0.9, 0.6, 0.1)
        hext = st.slider("Convection extérieure, vent (W/(m²·K))", 10.0, 40.0, 25.0, 1.0)
        go = st.button("Calculer", type="primary")

        text_roof = Text + absorp * sun / hext
        st.caption(f"Température équivalente du toit (air + soleil) : {text_roof:.1f} °C")

    if go:
        params = dict(BASE)
        params.update(lamIso=1.4 if sans_iso else float(lam_iso), Text=float(Text),
                      TextRoof=float(text_roof), Tint=float(Tint), hext=float(hext))
        with st.spinner("Calcul en cours..."):
            try:
                st.session_state["res"] = calculer(params)
                st.session_state["params"] = params
            except Exception as e:
                st.session_state.pop("res", None)
                st.error(f"Le calcul a échoué : {e}")

    with col_out:
        res = st.session_state.get("res")
        if res is None:
            st.info("Règle les paramètres à gauche, puis clique sur « Calculer ».")
        else:
            s = res["s"]
            ref = flux_reference()
            c1, c2, c3 = st.columns(3)
            delta = None
            if ref:
                delta = f"{100 * (s['qext'] - ref) / ref:+.0f} % par rapport à la référence"
            c1.metric("Flux entrant (W/m)", f"{s['qext']:.1f}",
                      delta=delta, delta_color="inverse")
            c2.metric("T moyenne des surfaces intérieures", f"{s['Tmean']:.2f} °C")
            c3.metric("T maximale des surfaces intérieures", f"{res['tmax_i']:.2f} °C")

            d, tri = res["data"], res["tri"]
            T = d[:, 2]
            if T.max() - T.min() < 0.01:
                levels = np.linspace(T.min() - 0.5, T.max() + 0.5, 11)
            else:
                levels = 40
            fig, ax = plt.subplots(figsize=(8, 5.6))
            c = ax.tricontourf(Triangulation(d[:, 0], d[:, 1], tri), T, levels=levels, cmap="coolwarm")
            fig.colorbar(c, ax=ax, label="Température (°C)")
            ax.set_aspect("equal")
            ax.set_xlabel("x (m)")
            ax.set_ylabel("y (m)")
            ax.set_title("Coupe de la pièce : température (régime stationnaire)")
            st.pyplot(fig)
            plt.close(fig)

            with st.expander("Vérifications du calcul"):
                bilan = 100 * abs(s["qext"] - s["qint"]) / abs(s["qext"])
                st.write(f"- Bilan de flux (entrant contre sortant) : écart de {bilan:.2g} %")
                st.write(f"- Flux au milieu d'un mur : {s['Fwall']:.3f} W/m² "
                         f"(valeur 1D attendue : {res['q1d_wall']:.3f})")
                st.write(f"- Flux au milieu du toit : {s['Froof']:.3f} W/m² "
                         f"(valeur 1D attendue : {res['q1d_roof']:.3f})")
                st.caption("Loin des coins, le calcul 2D doit retrouver la valeur 1D. "
                           "L'écart restant aux coins est l'effet des ponts thermiques.")

with tab2:
    ui_confort.render()

with tab3:
    st.markdown("""
**Ce que le modèle représente** : une coupe 2D d'une pièce de 4,00 m × 2,80 m, avec murs et toit
(béton, isolant, plâtre), calculée par éléments finis P1 avec FreeFem++.

**Limites à garder en tête**
- Coupe 2D simplifiée : résultats par mètre de profondeur, pas de maison 3D.
- Pas de fenêtre, pas de rayonnement solaire sur les murs, pas d'apports internes.
- Plancher dont le bas ne reçoit aucun échange : première simplification.
- Les ponts thermiques sont représentés dans la coupe, mais pas l'humidité ni les échanges radiatifs complexes.
- Un très léger dépassement numérique (de l'ordre de 0,003 °C) existe sur la tranche du toit.
- Les résultats sont une aide à l'étude : ils ne remplacent pas un calcul réglementaire.
""")
