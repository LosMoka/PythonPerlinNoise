import numpy as np


def Interpolate(x,y,blend):
    return x * (1 - blend) + blend * y

#Génére un tableau de nombre aléatoire entre 0 et 1
def makeNoise(w,h):
    return np.random.rand(w, h)

# Calcul un bruit à la bonne résulution à partir du bruit de base en faisant un sous-échantiollnage du bruit.
# C'est-à-dire, calcul la version "zommé" du bruit de base
def makeSmoothNoise(baseNoise,octave):
    noise = np.zeros_like(baseNoise)                                # 1)Créer un tableau vide à la bonne taille
    w,h = np.shape(baseNoise)

    samplePeriod = pow(2, octave)                                   # 2)Période d'échantiollnage : correspond à de combien l'image sera zommé, on prend un point tous les samplePeriod
    sampleFrequency = 1.0 / samplePeriod

    for i in range(w):                                              # 3)On définie un rectangle (sample_i0,sample_j0),(sample_i1,sample_j0),(sample_i1,sample_j1),(sample_i0,sample_j1)
                                                                    # Ce rectangle désigne l'ensemble des points qui vont être regroupé en un seul pixel lors du zoom
                                                                    # Cependant comme la version zoomé doit être de la même taille que l'image de base, on va, pour chaque point de ce rectangle,
                                                                    # calculer sa valeur en fonction de sa distance par rapport aux quatre sommet du rectangle

        sample_i0 = (i // samplePeriod) * samplePeriod              # On prend un point tous les samplePeriod
        sample_i1 = (sample_i0 + samplePeriod) % w                  # Prochain point, pour former le rectangle à transformer
        horizontal_blend = (i - sample_i0) * sampleFrequency        # Coefficient barycentrique, représente si le point qu'on est en train de traiter est plus proche de sample_i0 ou de sample_i1

        for j in range(h):
            sample_j0 = (j // samplePeriod) * samplePeriod          #idem mais pour l'axe des y
            sample_j1 = (sample_j0 + samplePeriod) % h
            vertical_blend = (j - sample_j0) * sampleFrequency

            # On calcul la moyenne pondérée des points (sample_i0,sample_j0) et (sample_i1,sample_j0).
            # On pondère par la distance horisontal du point qu'on est en trait de traiter, (i,j) par rapport à (sample_i0,sample_j0) et (sample_i1,sample_j0)
            top = Interpolate(baseNoise[sample_i0][sample_j0],baseNoise[sample_i1][sample_j0], horizontal_blend)

            # idem que pour top, mais avec les points (sample_i0,sample_j1) et (sample_i1,sample_j1).
            bottom = Interpolate(baseNoise[sample_i0][sample_j1],baseNoise[sample_i1][sample_j1], horizontal_blend)

            # On calcul la moyenne pondérée (on interpole) des valeurs calculées avant en pondérant pas la distance vertical de (i,j) par rapport aux sommets du rectangle
            noise[i][j] = Interpolate(top, bottom, vertical_blend);

    return noise

# Calcul le perlin noise
def makePerlinNoise(w,h, octave, amplitude, persistance):
    baseNoise = makeNoise(w,h)                                      # Génére un bruit aléatoire de taille w,h
    smoothNoises = []
    amplitudeTot = 0
    perlinNoise = np.zeros_like(baseNoise)

    for i in range(octave):                                         # Calcul toutes les versions zoomées du bruit de base
        smoothNoises.append(makeSmoothNoise(baseNoise,i))

    for k in reversed(range(octave)):                               # Fusion des versions zoomées
        amplitude*=persistance                                      # Chaque zoom est de moins en moins pris en compte (persistance < 1)
        amplitudeTot+=amplitude

        for i in range(w):
            for j in range(h):
                perlinNoise[i][j] += amplitude*smoothNoises[k][i][j] # On attenue l'effet de chaque zoom en multipliant ces valeurs pas amplitude

    for i in range(w):
        for j in range(h):
            perlinNoise[i][j]/=amplitudeTot                         # On normalise

    return perlinNoise