"""Onglet 'Confort sur 24 h' de l'interface THERMO-SMART."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

import run_cycles as rc

RES = rc.ROOT / "data" / "results"
BASE_C0 = dict(lamBeton=1.4, lamIso=0.04, lamPlat=0.5, rcIso=42000,
               absorp=0.6, achDay=1.0, achNight=1.0)


def load_last_day(tag):
    """Heure de la journee, T exterieure et T air du dernier jour simule."""
    d = np.loadtxt(RES / f"cycle_{tag}_t.txt")
    t_end = d[-1, 0]
    last = d[:, 0] > t_end - 24.0
    return d[last, 0] - (t_end - 24.0), d[last, 1], d[last, 3]


def lancer_personnalise(params):
    rc.write_params(params, "CUSTOM")
    try:
        rc.run_freefem()
    finally:
        rc.write_params(BASE_C0, "C0")
    s = rc.read_summary("CUSTOM")
    hod, text, tair = load_last_day("CUSTOM")
    return {"s": s, "hod": hod, "text": text, "tair": tair}


def render():
    st.markdown(
        "Température de l'air d'une pièce **non climatisée** sur une journée type de Dakar : "
        "extérieur de 25 à 35 °C (maximum à 15 h), soleil sur le toit, ventilation. "
        "Les courbes montrent le **régime périodique** établi (25 jours simulés)."
    )

    table_path = RES / "cycle_table.csv"
    if not table_path.exists():
        st.warning("Les scénarios précalculés sont absents. Lance `python python/run_cycles.py` "
                   "(quelques minutes), puis recharge la page.")
        return
    df = pd.read_csv(table_path)

    labels = [f"{t} : {n}" for t, n in zip(df["Scénario"], df["Nom"])]
    choix = st.multiselect("Scénarios précalculés à afficher", labels, default=labels)
    tags = [c.split(" : ")[0] for c in choix]

    with st.expander("Scénario personnalisé (calcul d'environ 1 à 2 minutes)"):
        c1, c2 = st.columns(2)
        with c1:
            sans = st.checkbox("Sans isolant (couche remplacée par du béton)", value=False, key="cust_sans")
            lam = st.slider("Conductivité de l'isolant (W/(m·K))", 0.020, 0.100, 0.040, 0.005,
                            disabled=sans, key="cust_lam")
            absorp = st.slider("Absorption solaire du toit (0,1 = très clair)", 0.1, 0.9, 0.6, 0.1,
                               key="cust_abs")
        with c2:
            ach_day = st.slider("Renouvellements d'air par heure (jour)", 0.5, 10.0, 1.0, 0.5,
                                key="cust_day")
            ach_night = st.slider("Renouvellements d'air par heure (nuit, de 20 h à 6 h)",
                                  0.5, 10.0, 1.0, 0.5, key="cust_night")
        go = st.button("Lancer le calcul (25 jours simulés)", type="primary")
        if go:
            params = dict(BASE_C0, lamIso=1.4 if sans else float(lam),
                          rcIso=1936000 if sans else 42000,
                          absorp=float(absorp), achDay=float(ach_day), achNight=float(ach_night))
            with st.spinner("Calcul en cours (1 à 2 minutes)..."):
                try:
                    st.session_state["custom"] = lancer_personnalise(params)
                except Exception as e:
                    st.session_state.pop("custom", None)
                    st.error(f"Le calcul a échoué : {e}")

        custom = st.session_state.get("custom")
        if custom is not None:
            s = custom["s"]
            m1, m2, m3 = st.columns(3)
            m1.metric("T air moyenne", f"{s['Tmean']:.2f} °C")
            m2.metric("Amplitude", f"{(s['Tmax'] - s['Tmin']) / 2:.2f} °C")
            m3.metric("Degrés-heures > 30 °C", f"{s['DH30']:.1f}")
            bilan = 100 * abs(s["Qext"] - s["Qint"]) / abs(s["Qext"])
            if s["dp"] > 0.05 or bilan > 0.5:
                st.warning(f"Régime périodique non atteint (écart {s['dp']:.3g} °C, bilan {bilan:.2g} %) : "
                           "résultat à interpréter avec prudence.")
            else:
                st.caption(f"Vérifications : périodicité {s['dp']:.2g} °C, bilan de flux {bilan:.2g} %.")

    custom = st.session_state.get("custom")

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    t_ext = None
    for tag in tags:
        hod, text, tair = load_last_day(tag)
        nom = df.loc[df["Scénario"] == tag, "Nom"].iloc[0]
        ax.plot(hod, tair, lw=2, label=f"{tag} : {nom}")
        if t_ext is None:
            t_ext = (hod, text)
    if custom is not None:
        ax.plot(custom["hod"], custom["tair"], "k-", lw=2.8, label="Personnalisé")
        if t_ext is None:
            t_ext = (custom["hod"], custom["text"])
    if t_ext is not None:
        ax.plot(t_ext[0], t_ext[1], "k--", lw=1.3, label="Extérieur (air)")
    ax.axhline(30, color="gray", ls=":", lw=1)
    ax.axhline(28, color="gray", ls=":", lw=1)
    ax.text(0.2, 30.1, "30 °C", color="gray", fontsize=8)
    ax.text(0.2, 28.1, "28 °C", color="gray", fontsize=8)
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25, 3))
    ax.set_xlabel("Heure de la journée (h)")
    ax.set_ylabel("Température de l'air (°C)")
    ax.set_title("Température de l'air intérieur sur 24 h")
    if tags or custom is not None:
        ax.legend(fontsize=8, loc="upper left")
    st.pyplot(fig)
    plt.close(fig)

    if tags:
        cols = ["Scénario", "Nom", "T air moy (C)", "Amplitude (C)", "Heure du max (h)",
                "DH>28 (C.h)", "DH>30 (C.h)", "Ecart DH>30 vs C0 (%)"]
        st.dataframe(df[df["Scénario"].isin(tags)][cols].round(2), hide_index=True)
    st.caption("DH>30 = degrés-heures au-dessus de 30 °C sur la journée. Sans apports internes, "
               "sans fenêtre et avec un air sans inertie propre : le classement des solutions est "
               "plus fiable que les valeurs absolues.")
