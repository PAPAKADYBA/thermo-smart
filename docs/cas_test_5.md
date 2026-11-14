# Cas test n°5 : mur composite avec cycle jour/nuit

## Mur
Celui du cas test 3 (béton 0,20 / isolant 0,10 / plâtre 0,02, mêmes lambda, rho, c).
Côté intérieur : T_int = 25 °C constant, h_int = 8 W/(m2.K).

## Température extérieure (journée type)
T_ext(t) = 30 + 5 cos(2 pi (t - 15 h) / 24 h), h_ext = 25 W/(m2.K)
Minimum 25 °C à 3 h, maximum 35 °C à 15 h, moyenne 30 °C.

## Simulation
5 jours (120 h), pas de 10 min (720 pas), départ à 25 °C partout.
Analyse du dernier jour (régime périodique établi).

## Mesures (x = 0 ; 0,20 ; 0,30 ; 0,32 m)
- amplitude de la variation de température sur 24 h
- décalage de l'heure du maximum par rapport à l'extérieur
- flux entrant et sortant au cours de la journée

## Vérifications
1. Périodicité : le 5e jour répète le 4e à moins de 0,01 °C environ.
2. Bilan énergétique : flux moyen sur un jour = (30 - 25) / R_tot = 1,7557 W/m2,
   en entrée comme en sortie (R_tot = 2,8479 m2.K/W).
3. L'amplitude décroît et le retard augmente de l'extérieur vers l'intérieur.
