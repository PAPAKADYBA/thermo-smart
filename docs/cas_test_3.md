# Cas test n°3 : mur composite en régime transitoire

## Géométrie et conditions
Même mur que le cas test 2 (voir cas_test_2.md) : coupe de 0,32 m x 1 m,
trois couches, convection de Robin sur les faces extérieure et intérieure,
flux nul en haut et en bas.

## Propriétés thermiques

| Couche  | lambda (W/(m.K)) | rho (kg/m3) | c (J/(kg.K)) |
|---------|------------------|-------------|--------------|
| Béton   | 1,4              | 2200        | 880          |
| Isolant | 0,04             | 30          | 1400         |
| Plâtre  | 0,5              | 850         | 1000         |

## Équation
rho c dT/dt - div(lambda grad T) = 0

Schéma d'Euler implicite : (M/dt + K) T^(n+1) = (M/dt) T^n + termes de Robin

## Scénario
- Condition initiale : T = 25 °C partout à t = 0
- À partir de t = 0 : T_ext = 35 °C constante (échelon), T_int = 25 °C
- Pas de temps : dt = 600 s (10 min)
- Durée simulée : 96 h (576 pas)

## Vérifications prévues
1. À t = 0, la température est uniforme à 25 °C.
2. Le béton chauffe progressivement (constante de temps estimée de l'ordre de 10 h),
   l'intérieur reste proche de 25 °C grâce à l'isolant.
3. À t = 96 h, le champ retrouve le cas test 2 (écart inférieur à 0,05 °C environ) :
   34,8595 ; 34,3579 ; 25,5794 ; 25,4389 °C en x = 0 ; 0,20 ; 0,30 ; 0,32 m.
4. Le flux entrant tend vers 3,5114 W/m2.
