import json   
import sys
import numpy as np

from HandPosition import Position
from HandPosition import Point3D

POSITIONS_FILE = '/home/fer/kinect/salidas/jointsTrack_0'


# FUNCIONES AUXILIARES
# --------------------

# Distancia entre vectores 3D con coordenadas homogeneas
def dist_vectores(v1,v2):
	v1 = convertir_homogenea_a_euclidea(v1)
	v2 = convertir_homogenea_a_euclidea(v2)
	return np.linalg.norm(v1 - v2)	

# Convertir un vector 3D en coordenadas homogeneas a un vector 3D euclideo
def convertir_homogenea_a_euclidea(v):
	x = v.x
	y = v.y
	z = v.z
	w = v.w
	return np.array([x/w, y/w, z/w])

# LECTURA
# -------

# Abro archivo a procesar y almaceno las posiciones de la mano en un vector
archivo = open(POSITIONS_FILE, 'r')
posiciones = []
for line in archivo:
	d = json.loads(line)
	position = Position(d["currentHandPose"], d["centros"], d["fechaHora"])
	posiciones.append(position)
archivo.close()


# FILTRADO
# --------

# TODO: Determinar inicio y fin del recorrido

# Obtengo cantidad de posiciones y conservo 10 posiciones distribuidas uniformemente
total_posiciones = len(posiciones)
posiciones_seleccionadas = []
for i in range(10):
	posiciones_seleccionadas.append(posiciones[total_posiciones*i/10])

# EXTRACCION
# ----------

procesados = []
for posicion in posiciones_seleccionadas:
	dist_ind_pulg =	dist_vectores(posicion.ft_pulgar, posicion.ft_indice)
	print dist_ind_pulg
	
