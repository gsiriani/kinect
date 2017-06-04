import os
import preprocesamiento as pp

path_entrada = '/home/fer/kinect/salidas/'
path_salida = '/home/fer/kinect/casos/casos.txt'

jsonFile = open(path_salida, "w")

for filename in os.listdir(path_entrada):
	archivo = open(path_entrada + filename, 'r')
	caso = pp.preprocesar_archivo(archivo)
	jsonFile.write(caso.toJson()) 
	jsonFile.write('\n')
	jsonFile.flush()

jsonFile.close() 
