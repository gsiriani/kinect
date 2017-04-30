import json   
import sys
import math
import numpy as np
from datetime import datetime 
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
posicion_inicial = posiciones[0]
posiciones = posiciones[1:]

# Obtengo cantidad de posiciones y conservo 10 posiciones distribuidas uniformemente
total_posiciones = len(posiciones)
posiciones_seleccionadas = []
for i in range(10):
	posiciones_seleccionadas.append(posiciones[total_posiciones*i/10])

# EXTRACCION
# ----------

procesados = []
posicion_anterior = posicion_inicial
for posicion in posiciones_seleccionadas:
	# Distancia entre pulgar e indice
	dist_ind_pulg =	dist_vectores(posicion.ft_pulgar, posicion.ft_indice)
	
	# La coordenada que corrsponde a la altura depende de la posicion del kinect.
	# TODO: corroborar cual es cada coordenada
	altura = posicion.p_palmPos1.y / posicion.p_palmPos1.w

	# Velocidad instantanea
	velocidad = dist_vectores(posicion_anterior.p_palmPos1, posicion.p_palmPos1) / (datetime.strptime(posicion_anterior.fechaHora, '%Y-%m-%d %H:%M:%S:%f') - datetime.strptime(posicion.fechaHora, '%Y-%m-%d %H:%M:%S:%f')).microseconds
	velocidad = velocidad if not math.isnan(velocidad) else 0
	posicion_anterior = posicion

	print 'Distancia Pulgar-Indice: ' + str(dist_ind_pulg)
	print 'Altura mano: ' + str(altura)
	print 'Velocidad: ' + str(velocidad)

	




