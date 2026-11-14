# Cas test n°4 : coupe de pièce 2D, régime stationnaire

## Géométrie (coupe verticale, en m, origine en bas à gauche)
Domaine complet : 4,64 x 3,32. Pièce intérieure (air) : x de 0,32 à 4,32, y de 0,20 à 3,00 (4,00 x 2,80).

| Élément        | Position              | Composition (extérieur vers intérieur)          |
|----------------|-----------------------|--------------------------------------------------|
| Mur gauche     | x de 0 à 0,32         | béton 0,20 / isolant 0,10 / plâtre 0,02          |
| Mur droit      | x de 4,32 à 4,64      | plâtre 0,02 / isolant 0,10 / béton 0,20          |
| Toit           | y de 3,00 à 3,32      | plâtre 0,02 / isolant 0,10 / béton 0,20          |
| Plancher       | y de 0 à 0,20         | dalle de béton 0,20                              |

Propriétés : voir cas_test_3.md (béton 1,4 ; isolant 0,04 ; plâtre 0,5 W/(m.K)).

## Équation
-div(lambda grad T) = 0, lambda constant par matériau.

## Conditions aux limites
- Faces extérieures (gauche, droite, haut) : Robin, T_ext = 35 °C, h_ext = 25 W/(m2.K)
- Toutes les surfaces intérieures (murs, plafond, sol de la pièce) : Robin, T_int = 25 °C, h_int = 8 W/(m2.K)
- Bas du plancher (y = 0) : flux nul (première simplification)

## Maillage
Mailles de 2 cm : toutes les interfaces tombent sur des arêtes du maillage.
La pièce intérieure est un trou dans le maillage (l'air est une condition aux limites).

## Validations prévues
1. Loin des coins, au milieu d'un mur (y = 1,6 m), la surface intérieure retrouve le cas test 2 : environ 25,44 °C.
2. Idem au milieu du toit (x = 2,32 m, y = 3,00 m) : environ 25,44 °C.
3. Bilan de flux global : flux entrant par l'extérieur = flux sortant par les surfaces intérieures.
4. La carte 2D montre un effet de pont thermique dans les coins.
