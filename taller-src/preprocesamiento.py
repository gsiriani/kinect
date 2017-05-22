import json   
import sys
import math
import numpy as np
from datetime import datetime 
from HandPosition import Position
from HandPosition import Point3D
from PosicionProcesada import PosicionProcesada

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


# Obtener Roll a partir de Quaternion (rotacion eje x)
def quaternion_a_roll(w,x,y,z):
	t0 = 2.0 * (w * x + y * z)
	t1 = 1.0 - 2.0 * (x * x + y * y)
	return math.atan2(t0, t1)

# Obtener Pitch a partir de Quaternion (rotacion eje y)
def quaternion_a_pitch(w,x,y,z):
	t = 2.0 * (w * y - z * x)
	t = 1.0 if t > 1.0 else t
	t = -1.0 if t < -1.0 else t
	return math.asin(t)

# Obtener Yaw a partir de Quaternion (rotacion eje z)
def quaternion_a_yaw(w,x,y,z):
	t0 = 2.0 * (w * z + x * y)
	t1 = 1.0 - 2.0 * (y * y + z * z)
	return math.atan2(t0, t1)
	

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

	# Rotaciones
	w = posicion.p_palmPosQuat.w
	x = posicion.p_palmPosQuat.x
	y = posicion.p_palmPosQuat.y
	z = posicion.p_palmPosQuat.z
	roll = quaternion_a_roll(w,x,y,z)
	pitch = quaternion_a_pitch(w,x,y,z)
	yaw = quaternion_a_yaw(w,x,y,z)
	
	procesados.append(PosicionProcesada(dist_ind_pulg=dist_ind_pulg, altura=altura, velocidad=velocidad, roll=roll, pitch=pitch, yaw=yaw))
	
print 'Cantidad de posiciones seleccionadas: ' + str(len(procesados))
print '0-\n-------'
print procesados[0]
print str(len(procesados) - 1) + '-\n-------'
print procesados[-1]


	




