import numpy as np
import matplotlib.colors as colors

def applyGradient(perlinNoise, gradient):
    w,h = np.shape(perlinNoise)
    image = np.zeros((h,w,3))
    for i in range(w):
        for j in range(h):
            image[j][i] = gradient(perlinNoise[i][j])
    return image

def colorGradient(x):
    t=x*16777216
    t = int(t)
    r=(t >> 16) & 0xFF
    g = (t >> 8) & 0xFF
    b = t & 0xFF
    return [r/256.,g/256.,b/256.]


def blackAndWhiteGradient(x):
    return [x,x,x]