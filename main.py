from perlinnoise import *
from gradient import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

np.random.seed()
pn = makePerlinNoise(800,600,8,1.0,0.5)
img = applyGradient(pn,blackAndWhiteGradient)
imgplot = plt.imshow(img)
plt.show()