#! /usr/bin/env python3

import os
import sys

from PyQt5.QtWidgets import QApplication

import recursos
from GUI.LOGICA.main_metro_maps import MetroMaps
from GUI.LOGICA.socket_client import ClientSocket

if __name__ == "__main__":

    ##############################################################################################
    # CREANDO CLIENTE QUE CONSULTARA A SERVIDOR
    # ############################################################################################

    cliente = ClientSocket(
        ip_server=recursos.App_Principal.SERVER_IP,
        port_server=recursos.App_Principal.SERVER_PORT,
    )

    ##############################################################################################
    # CREANDO LA GUI
    # ############################################################################################

    direccionTotal = sys.argv[0]

    direccionPartes = os.path.normpath(direccionTotal)
    direccionPartes = direccionPartes.split(os.sep)
    ruta_direccionTotal = os.sep.join(direccionPartes[:-1])
    if len(direccionPartes) > 1:
        ruta_direccionTotal += os.sep

    recursos.App_Principal.actualizarUbicaciones(ubicacion=ruta_direccionTotal)

    # crear aplicacion
    App = QApplication(sys.argv)
    window = MetroMaps(
        socket_client=cliente,
        archivo_ubicaciones_estaciones=recursos.App_Principal.ARCHIVO_UBICACIONES_ESTACIONES,
        carpeta_imagenes_estaciones=recursos.App_Principal.RUTA_IMAGENES_METRO,
        carpeta_audios_estaciones=recursos.App_Principal.CARPETA_AUDIOS_ESTACIONES,
        audio_frase_inicio=recursos.App_Principal.FRASE_INICIO,
        audio_frase_intermedia=recursos.App_Principal.FRASE_INTERMEDIA,
        ancho_panel=2000,
        alto_panel=800,
        margen_panel=20,
    )

    # iniciado app
    sys.exit(App.exec())
