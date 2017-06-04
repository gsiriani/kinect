from enum import Enum
import json

# Permite serializar en formato Json un objeto
# de una clase
def jsonDefault(object):
    return object.__dict__

class PosicionProcesada():
	'''
	Clase que almacena los parametros que describen la posicion de la mano
	que seran considerados para el entrenamiento
	'''
	
	def __init__(self, dist_ind_pulg, altura, velocidad, roll, pitch, yaw):
		'''
		dist_ind_pulg:	float que contiene la distancia entre el dedo indice y el pulgar
		altura:		float que contiene la altura de la mano
		velocidad:	float que contiene la velocidad de la mano
		roll:		float que representa la rotacion en grados sobre el eje x
		pitch:		float que representa la rotacion en grados sobre el eje y
		yaw:		float que representa la rotacion en grados sobre el eje z	
		'''
		
		self.dist_ind_pulg = dist_ind_pulg
		self.altura = altura
		self.velocidad = velocidad
		self.roll = roll
		self.pitch = pitch
		self.yaw = yaw
		
		
	def __str__(self):
		texto = 'Posicion:'
		texto = texto + '\nDistancia Pulgar-Indice: ' + str(self.dist_ind_pulg)
		texto = texto + '\nAltura mano: ' + str(self.altura)
		texto = texto + '\nVelocidad: ' + str(self.velocidad)
		texto = texto + '\nRoll: ' + str(self.roll)
		texto = texto + '\nPitch: ' + str(self.pitch)
		texto = texto + '\nYaw: ' + str(self.yaw)
		return texto
		
	def __repr__(self):
		return str(self.__dict__)

    # Retorna la serializacion del objeto en formato JSON
	def toJson(self):
		return json.dumps(self, default=jsonDefault, sort_keys=True, indent=4)
		
		
class Intencion(Enum):
	Competitiva = 1
	Colaborativa = 2

class Caso():
	'''
	Clase que almacena un caso de entrenamiento.
	Cada caso se compone de 10 posiciones procesadas (PosicionProcesada) y una
	intencion (competitiva / colaborativa)
	'''
	
	def __init__(self, posiciones, intencion):
		self.posiciones = posiciones
		self.intencion = intencion
		
	def __str__(self):
		return str(self.__dict__)

	def __repr__(self):
		return str(self.__dict__)

    # Retorna la serializacion del objeto en formato JSON
	def toJson(self):
		return json.dumps(self, default=jsonDefault, sort_keys=True, indent=4)
	'''
		lista = []
		for pos in self.posiciones:
			lista.append(pos.toJson())
			
		dicc = {'posiciones' : lista, 'intencion' : self.intencion.name}
		return dicc
	'''	
		
		
		
	
