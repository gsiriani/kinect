import os
import preprocesamientoNone as pp

path_entrada = '/home/fer/kinect/salidas-test-none/'
path_salida = '/home/fer/kinect/casos/casos.txt'

jsonFile = open(path_salida, "w")
cantidad_casos = 0

for filename in os.listdir(path_entrada):
	archivo = open(path_entrada + filename, 'r')
	caso = pp.preprocesar_archivo(archivo)
	jsonFile.write(caso.toTrainJson()) 
	cantidad_casos += 1
	jsonFile.write('\n')
	jsonFile.flush()

jsonFile.close() 
print 'Se han procesado ' + str(cantidad_casos) + ' casos'
