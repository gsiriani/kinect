path_proyecto = '/home/fer/kinect/'
import json   
import sys
import math
import numpy as np
from datetime import datetime 
from HandPosition import Position
from HandPosition import Point3D
from PosicionProcesada import PosicionProcesada, Intencion, Caso

POSITIONS_FILE = path_proyecto + 'salidas/jointsTrack_2'


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
	
# #############################
# 			MAIN
# #############################
def preprocesar_archivo(archivo):
	# LECTURA
	# -------
	# Abro archivo a procesar y almaceno las posiciones de la mano en un vector
	posiciones = []
	for line in archivo:
		d = json.loads(line)
		position = Position(d["currentHandPose"], d["centros"], d["fechaHora"])
		posiciones.append(position)
	archivo.close()

	# print 'Total de posiciones en archivo: ' + str(len(posiciones))


	# FILTRADO
	# --------

	# WARNING: Se asume que cada archivo tiene al menos 3 posiciones. 

	delta = 1 # distancia minima para considerar que la mano se mueve

	# Determino posicion inicial
	ind_posicion_inicial = 0
	pos_1 = posiciones[ind_posicion_inicial].p_palmPos1
	pos_2 = posiciones[ind_posicion_inicial + 1].p_palmPos1
	dif_X = math.fabs(pos_1.x - pos_2.x)
	dif_Y = math.fabs(pos_1.y - pos_2.y)
	dif_Z = math.fabs(pos_1.z - pos_2.z)
	diferencia = max([dif_X, dif_Y, dif_Z])

	while (diferencia < delta) and (ind_posicion_inicial + 3 < len(posiciones)):
		ind_posicion_inicial += 1
		pos_1 = posiciones[ind_posicion_inicial].p_palmPos1
		pos_2 = posiciones[ind_posicion_inicial + 1].p_palmPos1
		dif_X = math.fabs(pos_1.x - pos_2.x)
		dif_Y = math.fabs(pos_1.y - pos_2.y)
		dif_Z = math.fabs(pos_1.z - pos_2.z)
		diferencia = max([dif_X, dif_Y, dif_Z])
	
	# Determino posicion final
	ind_posicion_final = ind_posicion_inicial + 1
	pos_1 = posiciones[ind_posicion_final].p_palmPos1
	pos_2 = posiciones[ind_posicion_final + 1].p_palmPos1
	dif_X = math.fabs(pos_1.x - pos_2.x)
	dif_Y = math.fabs(pos_1.y - pos_2.y)
	dif_Z = math.fabs(pos_1.z - pos_2.z)
	diferencia = max([dif_X, dif_Y, dif_Z])

	while (diferencia > delta) and (ind_posicion_final + 2 < len(posiciones)):
		ind_posicion_final += 1
		pos_1 = posiciones[ind_posicion_final].p_palmPos1
		pos_2 = posiciones[ind_posicion_final + 1].p_palmPos1
		dif_X = math.fabs(pos_1.x - pos_2.x)
		dif_Y = math.fabs(pos_1.y - pos_2.y)
		dif_Z = math.fabs(pos_1.z - pos_2.z)
		diferencia = max([dif_X, dif_Y, dif_Z])
	 
	posicion_inicial = posiciones[ind_posicion_inicial]
	posiciones = posiciones[ind_posicion_inicial+1:ind_posicion_final]

	#posicion_inicial = posiciones[0]
	#posiciones=posiciones[1:]

	# Obtengo cantidad de posiciones y conservo 10 posiciones distribuidas uniformemente
	total_posiciones = len(posiciones)
	# print 'Cantidad de posiciones seleccionadas: ' + str(total_posiciones)
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
	
	return Caso(procesados, Intencion.Competitiva)


	




