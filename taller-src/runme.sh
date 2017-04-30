#!/bin/bash

echo
# Ruta a la libreria para capturar las articulaciones de la mano
export MBV_LIBS=/home/fer/MBV_PythonAPI_Linux_1.1

echo "MBV_LIBS Environment variable should point to the MBV libraries folder."
echo "MBV_LIBS" $MBV_LIBS
echo 

export TALLER_SRC=/home/fer/kinect/taller-src
echo "TALLER_SRC Fuentes para modelado de Posicion"
echo "TALLER_SRC" $TALLER_SRC
echo

echo "Directorio donde se generan las capturas"
export SALIDAS_DIR=/home/fer/kinect/salidas
echo "SALIDAS_DIR" $SALIDAS_DIR
echo

echo "Setting LD_LIBRARY_PATH and PYTHONPATH"
export LD_LIBRARY_PATH=$MBV_LIBS/libs:$LD_LIBRARY_PATH
export PYTHONPATH=$MBV_LIBS/python_libs:$TALLER_SRC:$PYTHONPATH
echo

echo "Running the Single Hand Tracker script..."
python /home/fer/HandTracker/src/SingleHandTracking.py
