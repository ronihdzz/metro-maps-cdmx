import os
import sys

import recursos
from GUI.LOGICA.socket_server import ServerSocket

direccionTotal = sys.argv[0]

direccionPartes = os.path.normpath(direccionTotal)
direccionPartes = direccionPartes.split(os.sep)
ruta_direccionTotal = os.sep.join(direccionPartes[:-1])
if len(direccionPartes) > 1:
    ruta_direccionTotal += os.sep

recursos.App_Principal.actualizarUbicaciones(ubicacion=ruta_direccionTotal)


print("S E R V E R    M E T R O ")
servidor_metro = ServerSocket(
    ip_server=recursos.App_Principal.SERVER_IP,
    port_server=recursos.App_Principal.SERVER_PORT,
    file_separacion_estaciones=recursos.App_Principal.ARCHIVO_SEPARACION_ESTACIONES,
)

# ejecutando el servidor...
servidor_metro.ejeuctar_servidor()
