# THERMO-SMART

**Plateforme de simulation thermique et d'optimisation énergétique des bâtiments.**

THERMO-SMART simule la distribution de température dans une coupe de bâtiment par la méthode des
éléments finis (P1, FreeFem++), puis compare des solutions pour améliorer le confort thermique et
limiter la surchauffe : isolation, protection solaire du toit, ventilation nocturne.

> Les simulations sont des modèles simplifiés : une aide à l'étude, pas un outil de certification
> réglementaire. Hypothèses et limites en fin de document.

## Ce que fait la plateforme

- Équation de la chaleur en régime stationnaire et transitoire, éléments finis P1 (FreeFem++).
- Parois multi-matériaux (béton, isolant, plâtre) avec convection de Robin sur les deux faces.
- Coupe de pièce en 2D avec ponts thermiques (jonctions murs, toit et plancher).
- Comparaison de scénarios : sans isolant, isolant performant, toit clair, toit au soleil.
- Cycle jour/nuit sur une journée type, air intérieur libre, ventilation de jour et de nuit,
  indicateur de surchauffe en degrés-heures.
- Interface web (Streamlit) pour changer les paramètres et relancer les calculs.

## Résultats vérifiés

Chaque étape est validée par un cas à solution connue avant d'être utilisée.

| Vérification | Résultat |
|---|---|
| Convergence du solveur P1 (solution fabriquée) | ordre 2 en norme L2, ordre 1 en norme H1 |
| Mur de 3 couches, régime stationnaire | températures d'interface égales à la solution exacte ; flux entrant = flux sortant = 3,51141 W/m2 |
| Régime transitoire du mur (96 h) | retour au régime stationnaire à 5,4e-4 °C près |
| Cycle jour/nuit sur le mur (5 jours) | périodicité 3,4e-3 °C ; flux moyen 1,7557 W/m2 comme calculé à la main |
| Pièce 2D, régime stationnaire | bilan de flux à 1,4e-12 près ; valeurs 1D retrouvées loin des coins |
| Cycle jour/nuit sur la pièce (25 jours) | périodicité 2,6e-5 °C ; bilan discret pas à pas à 5e-11 W/m |

**Ponts thermiques.** Dans la pièce de référence, les jonctions et le plancher ajoutent environ
13 W/m de flux entrant (de 12,9 à 14,6 W/m selon le scénario), soit près de 28 % du flux total :
cette part ne dépend presque pas de l'isolant des murs.

**Scénarios en régime stationnaire** (flux total entrant, par mètre de profondeur) :

| Scénario | Flux (W/m) | Écart |
|---|---|---|
| S0 Référence | 46,6 | - |
| S1 Sans isolant | 243,6 | +423 % |
| S2 Isolant performant | 35,1 | -25 % |
| S3 Toit au soleil | 74,0 | +59 % |
| S4 Toit clair | 60,3 | +29 % |

**Confort sur une journée** (pièce non climatisée, extérieur de 25 à 35 °C) :

| Scénario | Air moyen | Degrés-heures > 30 °C | Écart |
|---|---|---|---|
| C0 Référence | 31,04 °C | 24,9 | - |
| C1 Sans isolant | 32,13 °C | 51,1 | +105 % |
| C2 Isolant performant | 30,79 °C | 18,9 | -24 % |
| C3 Toit clair | 30,52 °C | 12,5 | -50 % |
| C4 Ventilation nocturne | 29,41 °C | 2,4 | -90 % |

Dans ce modèle, la ventilation nocturne est la mesure la plus efficace. Le classement des solutions
est plus fiable que les valeurs absolues.

## Installation (Ubuntu, y compris sous WSL)

    sudo apt update
    sudo apt install freefem++ python3 python3-venv python3-pip git
    git clone https://github.com/TON-PSEUDO/thermo-smart.git
    cd thermo-smart
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Vérification de FreeFem++ :

    which FreeFem++

## Utilisation

Toutes les commandes se lancent depuis la racine du projet. Les résultats sont écrits dans
`data/results/` (non versionné : on le régénère avec les scripts).

1. Maillage, solveur stationnaire et carte de température du cas 1 :

        FreeFem++ -nw freefem/01_mesh.edp
        FreeFem++ -nw freefem/02_stationary.edp
        python python/plots.py

2. Étude de convergence :

        FreeFem++ -nw tests/convergence_P1.edp

3. Mur multi-matériaux (stationnaire, transitoire, cycle jour/nuit) :

        FreeFem++ -nw freefem/02b_wall_stationary.edp
        python python/plot_cas2.py
        FreeFem++ -nw freefem/03_transient.edp
        python python/plot_cas3.py
        FreeFem++ -nw freefem/07_wall_daily_cycle.edp
        python python/plot_cas5.py

4. Pièce 2D et scénarios en régime stationnaire :

        FreeFem++ -nw freefem/05_room2d.edp
        python python/plot_cas4.py
        python python/run_scenarios.py
        python python/plot_scenarios.py

5. Confort sur 24 h (plusieurs minutes : 25 jours simulés par scénario) :

        python python/run_cycles.py
        python python/plot_cycles.py

6. Interface web :

        streamlit run python/app.py --server.headless true --server.address 127.0.0.1 --server.port 8601

   puis ouvrir http://localhost:8601 dans le navigateur. Le port peut être changé s'il est déjà utilisé.

Les scénarios se définissent dans `config/scenarios.json` (régime stationnaire) et
`config/cycle_scenarios.json` (cycle jour/nuit). Les définitions de chaque cas test sont dans `docs/`.

## Structure du dépôt

    thermo-smart/
    |-- README.md, requirements.txt, .gitignore
    |-- config/      scenarios.json, cycle_scenarios.json, room_params.txt, cycle_params.txt
    |-- docs/        cas_test_1.md ... cas_test_6.md, scenarios.md
    |-- freefem/     scripts FreeFem++ (maillage, solveurs, mur, pièce 2D, cycle jour/nuit)
    |-- python/      lecture des résultats, graphiques, lancement des scénarios, interface Streamlit
    |-- tests/       convergence_P1.edp
    |-- data/        input/ et results/ (résultats générés, non versionnés)

## Hypothèses et limites

- Coupe 2D simplifiée d'une pièce de 4,00 m x 2,80 m : résultats par mètre de profondeur, pas de maison en 3D.
- Pas de fenêtre, pas de rayonnement solaire sur les murs, pas d'apports internes (personnes, appareils).
- Air intérieur sans inertie propre : la température de l'air est une moyenne pondérée entre les surfaces
  et l'extérieur. Le changement brutal de ventilation à 6 h et à 20 h produit de petites marches sur les courbes.
- Le bas du plancher est supposé sans échange de chaleur (première simplification).
- Humidité et échanges radiatifs complexes non représentés.
- Léger dépassement numérique (environ 0,003 °C) sur la tranche du toit, où l'isolant touche l'extérieur,
  dû à l'intégration de la convection en éléments finis P1.
- Propriétés des matériaux : valeurs courantes de la littérature, à remplacer par des données mesurées pour une étude réelle.

## Auteur

Papa Kady BA. Projet étudiant (UFR STA, Université Amadou Mahtar Mbow).

## Licence3 Mathématiques et Modélisation.
