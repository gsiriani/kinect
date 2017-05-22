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
