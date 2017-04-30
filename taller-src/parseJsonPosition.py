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
def graficar(xs,ys,zs):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs, ys, zs, c='r', marker='o')
    plt.show()


# Grafica los puntos que conforman el plano
# asociado a la palma de la mano de de una
# determinada posicion
def graficarPlanoPalma(position):
    xs = []
    ys = []
    zs = []
    
    xs.append(position.p_palmPos1.x)
    ys.append(position.p_palmPos1.y)
    zs.append(position.p_palmPos1.z)

    xs.append(position.p_palmPos2.x)
    ys.append(position.p_palmPos2.y)
    zs.append(position.p_palmPos2.z)

    xs.append(position.p_palmPos3.x)
    ys.append(position.p_palmPos3.y)
    zs.append(position.p_palmPos3.z)
    
    xs.append(position.p_baseAnular.x)
    ys.append(position.p_baseAnular.y)
    zs.append(position.p_baseAnular.z)

    xs.append(position.p_baseMayor.x)
    ys.append(position.p_baseMayor.y)
    zs.append(position.p_baseMayor.z)

    graficar (xs, ys, zs)
    

# Grafica los 22 puntos correspondientes a los centros
# de las esferas que modelan los 20 joints de los dedos 
# mas los 2 puntos de la palma y el punto de la palma 
# del modelo de los 27 parametros
def graficarJoints(position):
    xs = []
    ys = []
    zs = []

    for p in position.centros:        
        xs.append(p[0])
        ys.append(p[1])
        zs.append(p[2])

    xs.append(position.p_palmPos1.x)
    ys.append(position.p_palmPos1.y)
    zs.append(position.p_palmPos1.z)

    graficar (xs, ys, zs)

    
if __name__ == '__main__':
    """
        Dado un archivo que contiene posiciones en formato JSON, 
        las extrae y permite mostrarlas en pantalla con indentacion y orden de sus atributos 
        asi como tambien graficar sus puntos.        
    """

    if len(sys.argv) < 3:
        print "\nInvocacion: "
        print "            python " + sys.argv[0] + " rutaArchivoJson Modo[1: parse y prettyPrint | 2: parse, prettyPrint y Grafica]\n" 
        sys.exit(1)

    POSITIONS_FILE = sys.argv[1]

    # MODE: 1 - imprime
    #       2 - imprime y dibuja
    MODE = sys.argv[2]
    
    archivo = open(POSITIONS_FILE, 'r')
    for line in archivo:
        d = json.loads(line)
        position = Position(d["currentHandPose"], d["centros"], d["fechaHora"])
        print  position.toPrettyJson()
        
        if MODE == '2':
            graficarPlanoPalma(position)
            graficarJoints(position)

