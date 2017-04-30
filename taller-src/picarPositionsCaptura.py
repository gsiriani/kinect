import json   
import sys

from HandPosition import Position

DIR_SALIDAS_VAR = "SALIDAS_DIR"
FILE_PREFIX = "position_"
FILE_SUFFIX = ".json"
    
# Dado un archivo de salida de captura del SingleHAndTracking
# extrae todas las posiciones y guarda cada un en un archivo 
# con nombre position_n.json donde n es un secuencial que arranca en 0
if __name__ == '__main__':

    if len(sys.argv) < 3:
        print "\nInvocacion: "
        print "            python " + sys.argv[0] + " rutaArchivoJson DIR_SALIDAS\n" 
        sys.exit(1)

    POSITIONS_FILE = sys.argv[1]

    # MODE: 1 - imprime
    #       2 - imprime y dibuja
    DIR_SALIDAS = sys.argv[2]
    
    archivo = open(POSITIONS_FILE, 'r')
    secuenciaArchivo = 0
    for line in archivo:
        d = json.loads(line)
        position = Position(d["currentHandPose"], d["centros"], d["fechaHora"])
        
        jsonFile = open(DIR_SALIDAS + "/" + FILE_PREFIX + str(secuenciaArchivo) + FILE_SUFFIX, "w")        
        jsonFile.write(position.toJson()) 
        jsonFile.close()
        secuenciaArchivo = secuenciaArchivo + 1

