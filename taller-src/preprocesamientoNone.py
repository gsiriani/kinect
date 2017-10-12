path_proyecto = '/home/fer/kinect/'
import json   
import sys
import math
import numpy as np
from datetime import datetime 
from HandPosition import Position
from HandPosition import Point3D
from PosicionProcesada import PosicionProcesada, Intencion, Caso



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
	intencion = archivo.readline().strip()
	posiciones = []
	validos = []
	for line in archivo:
		if line[0]=='-':
			d = json.loads(line[1:])
			position = Position(d["currentHandPose"], d["centros"], d["fechaHora"], d["id_posicion"])
			validos.append(None)
		else:
			d = json.loads(line)
			position = Position(d["currentHandPose"], d["centros"], d["fechaHora"], d["id_posicion"])
			validos.append(position)
		posiciones.append(position)
	archivo.close()

	# print 'Total de posiciones en archivo: ' + str(len(posiciones))


	# FILTRADO
	# --------

	# WARNING: Se asume que cada archivo tiene al menos 3 posiciones. 

	delta = 0.01 # distancia minima para considerar que la mano se mueve

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
	validos = validos[ind_posicion_inicial+1:ind_posicion_final]

	posicion_inicial = posiciones[0]
	posiciones=validos[1:]

	# Obtengo cantidad de posiciones y conservo 10 posiciones distribuidas uniformemente
	total_posiciones = len(posiciones)
	print 'Cantidad de posiciones seleccionadas: ' + str(total_posiciones)
	indices_seleccionados = []
	for i in range(10):
		indices_seleccionados.append(total_posiciones*i/10)

	# Evaluo y corrigo posiciones descartadas
	posiciones_seleccionadas = []
	for indice in indices_seleccionados:
		if posiciones[indice] is None:
			# Busco indice minimo
			indice_menor = indice - 1
			while indice_menor >= 0 and posiciones[indice_menor] is None:
				indice_menor -= 1
			# Busco indice mayor
			indice_mayor = indice + 1
			while indice_mayor < len(posiciones) and posiciones[indice_mayor] is None:
				indice_mayor += 1
			# Evaluo indices auxiliares obtenidos
			if indice_menor == -1:
				if indice_mayor == len(posiciones):
					print 'ERROR: Todas las posiciones han sido descartadas'
					return 0
				else:
					posiciones_seleccionadas.append({'min':posiciones[indice_mayor], 'max':posiciones[indice_mayor]})
			else:
				if indice_mayor == len(posiciones):
					posiciones_seleccionadas.append({'min':posiciones[indice_menor], 'max':posiciones[indice_menor]})
				else:
					posiciones_seleccionadas.append({'min':posiciones[indice_menor], 'max':posiciones[indice_mayor]})
		else:
			posiciones_seleccionadas.append({'min':posiciones[indice], 'max':posiciones[indice]})
		
	# EXTRACCION
	# ----------

	# Todo: Atender las posiciones que son None

	procesados = []
	posicion_anterior = posicion_inicial
	for posicion in posiciones_seleccionadas:
		# Distancia entre pulgar e indice
		dist_ind_pulg_min =	dist_vectores(posicion['min'].ft_pulgar, posicion['min'].ft_indice)
		dist_ind_pulg_max =	dist_vectores(posicion['max'].ft_pulgar, posicion['max'].ft_indice)
		dist_ind_pulg = (dist_ind_pulg_min + dist_ind_pulg_max) / 2
	
		# La coordenada que corrsponde a la altura depende de la posicion del kinect.
		altura_min = posicion['min'].p_palmPos1.y / posicion['min'].p_palmPos1.w
		altura_max = posicion['max'].p_palmPos1.y / posicion['max'].p_palmPos1.w
		altura = (altura_min + altura_max) / 2

		# Velocidad instantanea
		velocidad_min = dist_vectores(posicion_anterior.p_palmPos1, posicion['min'].p_palmPos1) / (datetime.strptime(posicion_anterior.fechaHora, '%Y-%m-%d %H:%M:%S:%f') - datetime.strptime(posicion['min'].fechaHora, '%Y-%m-%d %H:%M:%S:%f')).microseconds
		velocidad_min = velocidad_min if not math.isnan(velocidad_min) else 0
		velocidad_max = dist_vectores(posicion_anterior.p_palmPos1, posicion['max'].p_palmPos1) / (datetime.strptime(posicion_anterior.fechaHora, '%Y-%m-%d %H:%M:%S:%f') - datetime.strptime(posicion['max'].fechaHora, '%Y-%m-%d %H:%M:%S:%f')).microseconds
		velocidad_max = velocidad_max if not math.isnan(velocidad_max) else 0
		velocidad = (velocidad_min + velocidad_max) / 2
		posicion_anterior = posicion['max']

		# Rotaciones
		w_min = posicion['min'].p_palmPosQuat.w
		x_min = posicion['min'].p_palmPosQuat.x
		y_min = posicion['min'].p_palmPosQuat.y
		z_min = posicion['min'].p_palmPosQuat.z
		roll_min = quaternion_a_roll(w_min,x_min,y_min,z_min)
		pitch_min = quaternion_a_pitch(w_min,x_min,y_min,z_min)
		yaw_min = quaternion_a_yaw(w_min,x_min,y_min,z_min)
		w_max = posicion['max'].p_palmPosQuat.w
		x_max = posicion['max'].p_palmPosQuat.x
		y_max = posicion['max'].p_palmPosQuat.y
		z_max = posicion['max'].p_palmPosQuat.z
		roll_max = quaternion_a_roll(w_max,x_max,y_max,z_max)
		pitch_max = quaternion_a_pitch(w_max,x_max,y_max,z_max)
		yaw_max = quaternion_a_yaw(w_max,x_max,y_max,z_max)
		roll = (roll_min + roll_max) / 2
		pitch = (pitch_min + pitch_max) / 2
		yaw = (yaw_min + yaw_max) / 2
	
		procesados.append(PosicionProcesada(dist_ind_pulg=dist_ind_pulg, altura=altura, velocidad=velocidad, roll=roll, pitch=pitch, yaw=yaw))
	
	if intencion == 'COMPETITIVA':
		intencion_aux = Intencion.Competitiva
	else:
		intencion_aux = Intencion.Colaborativa
	return Caso(procesados, intencion_aux)


	




