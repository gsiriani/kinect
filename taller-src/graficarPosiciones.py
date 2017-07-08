import json   
import sys

from HandPosition import Position
from HandPosition import Point3D

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt


# Grafica un conjunto de puntos.
# Recibe ua lista con las coordenadas por cada eje:
#        xs: Lista de coordenadas x
#        ys: Lista de coordenadas y
#        zs: Lista de coordenadas z
def graficar(position):
    # Inicializo la grafica
    # ---------------------

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = []
    ys = []
    zs = []

    # Uno los joints de cada dedo
    for i in range(0,5):
        for j in range(0,4):
            pos=4*i+2+j
            xs.append(position.centros[pos][0])
            ys.append(position.centros[pos][1])
            zs.append(position.centros[pos][2])

        ax.plot(xs, ys, zs, c='r', marker='o')
        xs = []
        ys = []
        zs = []

    # Uno las bases de los dedos
    for i in range(0,4):
        pos1=i*4+2
        pos2=pos1+4
        ax.plot([position.centros[pos1][0], position.centros[pos2][0]],
                [position.centros[pos1][1], position.centros[pos2][1]],
                [position.centros[pos1][2], position.centros[pos2][2]],
                c='g')

    xs = []
    ys = []
    zs = []

    for p in position.centros:        
        xs.append(p[0])
        ys.append(p[1])
        zs.append(p[2])

    ax.scatter(xs, ys, zs, c='b', marker='x')


    plt.show()


