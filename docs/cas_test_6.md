# Cas test n°6 : pièce 2D, cycle jour/nuit, air intérieur libre

Base : cas test 4 (géométrie, matériaux) avec les capacités thermiques du cas test 3.

## Air intérieur
L'air n'est plus imposé à 25 °C : il évolue librement. Modèle simple sans inertie de l'air :
T_air = (h_int A_int T_surf + C_v T_ext) / (h_int A_int + C_v)
- A_int = 13,6 m (périmètre intérieur par mètre de profondeur), h_int = 8 W/(m2.K)
- T_surf = température moyenne des surfaces intérieures
- C_v = rho_air c_air Q, avec Q = n V / 3600 (V = 11,2 m3 par mètre de profondeur, n = renouvellements d'air par heure)

## Conditions extérieures
- T_ext(t) = 30 + 5 cos(2 pi (t - 15 h) / 24 h), h_ext = 25 W/(m2.K)
- Soleil sur le toit : T_air-soleil = T_ext + alpha I(t) / h_ext
  I(t) = 800 sin(pi (h - 6)/12) W/m2 entre 6 h et 18 h, nul sinon ; alpha = 0,6

## Simulation
Pas de 10 min, 25 jours (3600 pas), départ à 31 °C partout. Analyse du dernier jour (la masse intérieure a une constante de temps de plusieurs jours).

## Scénarios

| N° | Scénario            | Changement                                                  |
|----|---------------------|-------------------------------------------------------------|
| C0 | Référence           | alpha 0,6 ; isolant 0,04 ; 1 renouvellement d'air/h         |
| C1 | Sans isolant        | isolant remplacé par du béton (lambda et rho c du béton)    |
| C2 | Isolant performant  | lambda de l'isolant : 0,025                                 |
| C3 | Toit clair          | alpha = 0,3                                                 |
| C4 | Ventilation nocturne| 5 renouvellements d'air/h de 20 h à 6 h, 1 sinon            |

## Indicateurs (dernier jour)
Température de l'air : moyenne, maximale, amplitude, heure du maximum ;
degrés-heures au-dessus de 28 °C (et de 30 °C) : somme de max(0, T_air - seuil) dt.

## Vérifications
1. Périodicité : le dernier jour répète la veille (écart sur T_air de l'ordre de 0,01 à 0,05 °C).
2. Bilan énergétique : flux entrant par l'extérieur = flux sortant vers l'air, en moyenne sur un jour ;
   le bilan discret pas à pas est vérifié à la précision machine.
3. Cohérence physique : sans isolant, l'air suit l'extérieur de plus près ;
   la ventilation nocturne refroidit l'air la nuit.

## Limites
Pas de fenêtre, pas de rayonnement solaire sur les murs, pas d'apports internes, air et mobilier sans inertie.
