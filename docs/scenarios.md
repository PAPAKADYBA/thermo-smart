# Scénarios comparés sur la pièce 2D (régime stationnaire)

Base : cas test 4 (docs/cas_test_4.md).

| N° | Scénario            | Changement par rapport à la référence                              |
|----|---------------------|--------------------------------------------------------------------|
| S0 | Référence           | cas test 4                                                         |
| S1 | Sans isolant        | couche isolante remplacée par du béton (lambda = 1,4)              |
| S2 | Isolant performant  | lambda de l'isolant : 0,04 -> 0,025 W/(m.K)                        |
| S3 | Toit au soleil      | toit à 54,2 °C (température air-soleil : 35 + 0,6 x 800 / 25)      |
| S4 | Toit clair          | toit à 44,6 °C (température air-soleil : 35 + 0,3 x 800 / 25)      |

## Indicateurs
- flux total entrant (W par mètre de profondeur)
- température moyenne et maximale des surfaces intérieures
- écart de flux par rapport à la référence (%)

## Vérifications 1D loin des coins (résistances thermiques en série)

| Scénario | Flux attendu (W/m2) |
|----------|---------------------|
| S0       | 3,51                |
| S1       | environ 23,9        |
| S2       | environ 2,30        |
| S3       | environ 10,25 (toit) |
| S4       | environ 6,88 (toit)  |

## Limite
Le régime stationnaire donne l'équilibre, sans inertie du bâtiment : il compare
les solutions mais ne décrit pas encore le confort sur une journée.
