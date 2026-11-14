# Cas test n°1 : plaque rectangulaire, régime stationnaire

- Domaine : rectangle [0, L] x [0, H], L = 4 m, H = 3 m
- Équation : -div(lambda grad T) = 0, lambda = 1,0 W/(m.K), pas de source
- CL : T = 30 °C en x = 0 ; T = 20 °C en x = L ; flux nul en y = 0 et y = H
- Solution exacte : T(x) = 30 - 2,5 x (en °C, x en m)
- Attendu : le calcul P1 reproduit cette droite
