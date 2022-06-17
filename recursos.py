
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon



class App_Principal():

    ARCHIVO_UBICACIONES_ESTACIONES=""
    ARCHIVO_SEPARACION_ESTACIONES=""

    @classmethod
    def actualizarUbicaciones(cls,ubicacion):
        cls.ARCHIVO_UBICACIONES_ESTACIONES=ubicacion+cls.ARCHIVO_UBICACIONES_ESTACIONES
        cls.ARCHIVO_SEPARACION_ESTACIONES=ubicacion+cls.ARCHIVO_SEPARACION_ESTACIONES





class App_Principal():

    NOMBRE_APLICACION="metro-maps-cdmx"
    ICONO_APLICACION=":/app/multimedia/imagenes/app/icono.png"
    IMAGEN_SPLASH_SCREEN=":/app/multimedia/imagenes/app/icono.png"

    ARCHIVO_UBICACIONES_ESTACIONES="multimedia/archivos/estaciones_ubicacion_2.xlsx"
    ARCHIVO_SEPARACION_ESTACIONES="multimedia/archivos/estaciones_separacion.xlsx"

    CARPETA_AUDIOS_ESTACIONES="multimedia/audios_estaciones_metro/"
    CARPETA_FRASES="multimedia/audios_frases/"

    FRASE_INICIO=CARPETA_FRASES+"frase_inicio.mp3"
    FRASE_INTERMEDIA=CARPETA_FRASES+"frase_intermedia.mp3"


    @classmethod
    def actualizarUbicaciones(cls,ubicacion):
        cls.ARCHIVO_UBICACIONES_ESTACIONES=ubicacion+cls.ARCHIVO_UBICACIONES_ESTACIONES
        cls.ARCHIVO_SEPARACION_ESTACIONES=ubicacion+cls.ARCHIVO_SEPARACION_ESTACIONES



class App_datosCreador():

    NOMBRE_PROGRAMADOR="Roni Hernández"


    LIKEDIN_NOMBRE="Roni Hernández"
    LIKEDIN_LINK="https://www.linkedin.com/in/ronihernandez99/"
    
    GITHUB_NOMBRE="RoniHernandez99"
    GITHUB_LINK="https://github.com/RoniHernandez99"
    
    REPOSITORIO_PROYECTO_NOMBRE="metro-maps-cdmx"
    REPOSITORIO_PROYECTO_LINK="https://github.com/RoniHernandez99/metro-maps-cdmx"

    FOTO_PROGRAMADOR=":/autor/multimedia/imagenes/autor/roni_code_99.jpg"


    # Datos del mensaje que se mandaria al programador 
    GMAILS=["roni.hernandez.1999@gmail.com"]
    GMAIL_SUBJECT=f"Comentarios acerca de: {REPOSITORIO_PROYECTO_NOMBRE}"
    GMAIL_CUERPO=f"Hola {NOMBRE_PROGRAMADOR} espero tengas un buen dia, el motivo del mensaje es:"





#class HuellaAplicacion(QtCore.QObject):
class HuellaAplicacion(QtCore.QObject):
    NOMBRE_APLICACION=App_Principal.NOMBRE_APLICACION
    ICONO_APLICACION=App_Principal.ICONO_APLICACION

    def __init__(self):
        #NO USAMOS EL CONSTRUCTOR DEL PADRE POR LO TANTO NO HACEMOS SUS CONFIGURACIONES DEFAULT
        self.dejarHuella()
    

    def dejarHuella(self):
        self.setWindowTitle(self.NOMBRE_APLICACION)
        self.setWindowIcon( QIcon(self.ICONO_APLICACION) )  
