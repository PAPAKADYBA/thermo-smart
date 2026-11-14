# Cas test n°2 : mur composite multi-matériaux, régime stationnaire

## Géométrie
Coupe du mur : x = épaisseur (0 à 0,32 m, de l'extérieur vers l'intérieur), y = hauteur (0 à 1 m).

| Couche  | x (m)         | Épaisseur (m) | lambda (W/(m.K)) |
|---------|---------------|---------------|------------------|
| Béton   | 0 à 0,20      | 0,20          | 1,4              |
| Isolant | 0,20 à 0,30   | 0,10          | 0,04             |
| Plâtre  | 0,30 à 0,32   | 0,02          | 0,5              |

## Équation
-div(lambda grad T) = 0 (pas de source), lambda constant par couche.

## Conditions aux limites
- Face extérieure (x = 0) : -lambda dT/dn = h_ext (T - T_ext), T_ext = 35 °C, h_ext = 25 W/(m2.K)
- Face intérieure (x = 0,32) : -lambda dT/dn = h_int (T - T_int), T_int = 25 °C, h_int = 8 W/(m2.K)
- Haut (y = 1) et bas (y = 0) : flux nul

## Solution exacte (résistances thermiques en série)
R_tot = 1/25 + 0,20/1,4 + 0,10/0,04 + 0,02/0,5 + 1/8 = 2,8479 m2.K/W
Flux q = (35 - 25) / R_tot = 3,5114 W/m2

Températures attendues (°C) :
- surface extérieure (x = 0) : 34,8595
- interface béton/isolant (x = 0,20) : 34,3579
- interface isolant/plâtre (x = 0,30) : 25,5794
- surface intérieure (x = 0,32) : 25,4389

## Attendu
Le calcul P1 reproduit ces valeurs (solution linéaire par morceaux) à condition que les interfaces coïncident avec des arêtes du maillage.
