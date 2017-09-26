from perlinnoise import *
from gradient import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

np.random.seed()
pn = makePerlinNoise(800,600,8,1.0,0.5)


def plot2D() :
    img = applyGradient(pn,blackAndWhiteGradient)
    imgplot = plt.imshow(img)
    plt.show()

def plot3D():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    Y = np.arange(0, 800, 1)
    X = np.arange(0, 600, 1)
    X, Y = np.meshgrid(X, Y)

    Z=pn

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

plot2D()
plot3D()