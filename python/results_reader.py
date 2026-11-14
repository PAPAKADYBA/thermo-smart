"""Lecture des fichiers de résultats exportés par FreeFem++."""
import numpy as np
def read_temperature(path):
    """Lit un fichier 'x y T' et renvoie trois tableaux x, y, T."""
    data = np.loadtxt(path)
    return data[:, 0], data[:, 1], data[:, 2]
