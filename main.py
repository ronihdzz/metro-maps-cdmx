#! /usr/bin/env python3

import sys
from PyQt5.QtWidgets import  QApplication

import os

from GUI.LOGICA.main_metro_maps import MetroMaps
import recursos



if __name__ == "__main__":        

    direccionTotal=sys.argv[0]

    direccionPartes=os.path.normpath(direccionTotal)
    direccionPartes=direccionPartes.split(os.sep)
    ruta_direccionTotal = os.sep.join( direccionPartes[:-1] )
    if len(direccionPartes)>1:
        ruta_direccionTotal+=os.sep
   
    recursos.App_Principal.actualizarUbicaciones(ubicacion=ruta_direccionTotal)

    # crear aplicacion
    App = QApplication(sys.argv)
    window = MetroMaps()
    # iniciado app
    sys.exit(App.exec())