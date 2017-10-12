import json
from datetime import datetime 


#------------------------------------------------------------------------------
# Funciones axiliares


# Permite serializar en formato Json un objeto
# de una clase
def jsonDefault(object):
    return object.__dict__

# Retorna la fecha hora con formato yyyy/mm/dd/hh:mm:ss
def fechaActual():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

#------------------------------------------------------------------------------


"""
    Posiciones de los 4 centros coorespondientes a cada
    articulacion para cada dedo en el array de centros:    

        pulgar: 18, 19, 20, 21 -> fingertip -> 21
        indice: 14, 15, 16, 17 -> fingertip -> 17
        mayor: 10, 11, 12, 13  -> fingertip -> 13
        Anular:  6, 7, 8, 9    -> fingertip -> 9
        menique: 2, 3, 4, 5    -> fingertip -> 5
"""


# Posiciones de las yemas de los dedos en el array de centros 
# de las esferas que modelan los joints de los dedos y 2 puntos de 
# la palma
PULGAR_FT_POS  = 21
INDICE_FT_POS  = 17
MAYOR_FT_POS   = 13
ANULAR_FT_POS  =  9 
MENIQUE_FT_POS =  5

# Posicion de los dos puntos de la palma
# en el array de centros
PALM_POS_2_CENTER = 0
PALM_POS_3_CENTER = 1

# Posicion de la base de los dedos 
# anular y mayor
BASE_ANULAR_POS = 6
BASE_MAYOR_POS = 10


# Clase que modela la posicion de la mano en un instante dado
class Position():

    def __init__(self, currentHandPose, centros, fechaHora, id_posicion=0):
        """
        currentHandPose: Array conteniendo los 27 parametros del modelo
                centros: Array con los centros de las 22 esferas utilizadas para dibujar la mano
                         Cada centro es un punto con coordenadas homogeneas 
                         representado como una lista de 4 coordenadas: [x, y, z, w]
              fechaHora: Fecha hora de creacion del objeto
              id_posicion: Numero que identifica la posicion dentro de una captura 
        """

        # Array con los 27 parametros de la posicion del modelo
        self.currentHandPose = currentHandPose
        
        # Centros de las esferas asociadas al modelo
        # 20 joints de los dedos + 2 puntos de la mano = 22 puntos
        self.centros = centros

        # palmPos1 es el punto de la palma de los 27 params del modelo
        # Sus coordenadas son los primeros 3 elementos del array de parametros currentHandPose
        self.p_palmPos1 = Point3D(self.currentHandPose[0], self.currentHandPose[1], self.currentHandPose[2], 1)

        # palmPosQuat es el quaternion de los 27 params del modelo
        self.p_palmPosQuat = Point3D(self.currentHandPose[3], self.currentHandPose[4], self.currentHandPose[5], self.currentHandPose[6])

        # Puntos de la palma obtenidos de la transformacion de los 27 parametros en puntos con coordenadas homogeneas 
        self.p_palmPos2 = Point3D(self.centros[PALM_POS_2_CENTER][0], self.centros[PALM_POS_2_CENTER][1], self.centros[PALM_POS_2_CENTER][2], self.centros[PALM_POS_2_CENTER][3])
        self.p_palmPos3 = Point3D(self.centros[PALM_POS_3_CENTER][0], self.centros[PALM_POS_3_CENTER][1], self.centros[PALM_POS_3_CENTER][2], self.centros[PALM_POS_3_CENTER][3]) 
        
        # Los puntos de la base de los dedos mayor y anular. En general se mantienen en el mismo plano
        self.p_baseAnular = Point3D(self.centros[BASE_ANULAR_POS][0], self.centros[BASE_ANULAR_POS][1], self.centros[BASE_ANULAR_POS][2], self.centros[BASE_ANULAR_POS][3]) 
        self.p_baseMayor = Point3D(self.centros[BASE_MAYOR_POS][0], self.centros[BASE_MAYOR_POS][1], self.centros[BASE_MAYOR_POS][2], self.centros[BASE_MAYOR_POS][3]) 

        # Las yemas de los dedos
        self.ft_pulgar = Point3D(self.centros[PULGAR_FT_POS][0], self.centros[PULGAR_FT_POS][1], self.centros[PULGAR_FT_POS][2], self.centros[PULGAR_FT_POS][3])
        self.ft_indice = Point3D(self.centros[INDICE_FT_POS][0], self.centros[INDICE_FT_POS][1], self.centros[INDICE_FT_POS][2], self.centros[INDICE_FT_POS][3])
        self.ft_mayor = Point3D(self.centros[MAYOR_FT_POS][0], self.centros[MAYOR_FT_POS][1], self.centros[MAYOR_FT_POS][2], self.centros[MAYOR_FT_POS][3])
        self.ft_anular = Point3D(self.centros[ANULAR_FT_POS][0], self.centros[ANULAR_FT_POS][1], self.centros[ANULAR_FT_POS][2], self.centros[ANULAR_FT_POS][3])
        self.ft_menique = Point3D(self.centros[MENIQUE_FT_POS][0], self.centros[MENIQUE_FT_POS][1], self.centros[MENIQUE_FT_POS][2], self.centros[MENIQUE_FT_POS][3])

        # Fecha hora de creacion del objeto
        self.fechaHora = fechaHora

        # Numero que identifica la posicion dentro de una captura 
        self.id_posicion = id_posicion

    def __str__(self):
        return str(self.__dict__)


    def __repr__(self):
        return str(self.__dict__)

    # Retorna la serializacion del objeto en formato JSON
    def toJson(self):
        return json.dumps(self, default=jsonDefault)

    # Retorna la serializacion del objeto en format JSON con indentacion y orden
    def toPrettyJson(self):
        return json.dumps(self, default=jsonDefault, sort_keys=True, indent=4)



# Clase que representa las coordenadas homogeneas de un punto  
class Point3D():

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return  str(self.__dict__)


