import json   
import sys

from HandPosition import Position
from HandPosition import Point3D

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt


# Grafica una posicion de la mano.
def graficar(position):
    # Inicializo la grafica
    # ---------------------

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = []
    ys = []
    zs = []

    # Uno los joints de cada dedo
    # ---------------------------

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
    # --------------------------

    for i in range(0,4):
        pos1=i*4+2
        pos2=pos1+4
        ax.plot([position.centros[pos1][0], position.centros[pos2][0]],
                [position.centros[pos1][1], position.centros[pos2][1]],
                [position.centros[pos1][2], position.centros[pos2][2]],
                c='g')

    # Agrego todos los puntos disponibles
    # -----------------------------------

    xs = []
    ys = []
    zs = []

    for p in position.centros:        
        xs.append(p[0])
        ys.append(p[1])
        zs.append(p[2])

    ax.scatter(xs, ys, zs, c='b', marker='x')

    # Muestro la grafica.
    # -------------------

    plt.show()


if __name__ == '__main__':
    """
        Dado un archivo que contiene posiciones en formato JSON, 
        las extrae grafica sus puntos.        
    """

    if len(sys.argv) < 2:
        print "\nInvocacion: "
        print "            python " + sys.argv[0] + " rutaArchivoJson\n" 
        sys.exit(1)

    POSITIONS_FILE = sys.argv[1]

    archivo = open(POSITIONS_FILE, 'r')
    _ = archivo.readline() # Ignoro la intencion, que es la primer lina del archivo
    for line in archivo:
        d = json.loads(line)
        position = Position(d["currentHandPose"], d["centros"], d["fechaHora"])
        graficar(position)
