


class App_Principal():

    ARCHIVO_ESTADOS_SENSORES="CUERPO/RECURSOS/DATOS/estadosSensores.txt"
    SONIDO_INCENDIO="CUERPO/RECURSOS/SONIDOS_SISTEMA/fuego_detectado.wav"

    ARDUINO_NANO_EXTENSION="COM3"
    BLUETOOTH_HC05="COM4"

    ICONO_APLICACION=":/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/RoniHernandez99_IoT_domotica_128px.png"
    NOMBRE_APLICACION="RoniHernandez99/IoT_domotica"
    IMAGEN_SPLASH_SCREEN=":/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/RoniHernandez99_IoT_domotica_256px.png"


    NOMBRE_ARCHIVO_LOG='depuracionPrograma.log'
    
    @classmethod
    def actualizarUbicaciones(cls,ubicacion):
        cls.ARCHIVO_ESTADOS_SENSORES=ubicacion+cls.ARCHIVO_ESTADOS_SENSORES
        cls.SONIDO_INCENDIO=ubicacion+cls.SONIDO_INCENDIO
        cls.NOMBRE_ARCHIVO_LOG=ubicacion+cls.NOMBRE_ARCHIVO_LOG


class App_datosCreador():

    NOMBRE_PROGRAMADOR="Roni Hernández"


    LIKEDIN_NOMBRE="Roni Hernández"
    LIKEDIN_LINK="https://www.linkedin.com/in/ronihernandez99/"
    
    GITHUB_NOMBRE="RoniHernandez99"
    GITHUB_LINK="https://github.com/RoniHernandez99"
    
    REPOSITORIO_PROYECTO_NOMBRE="IoT_domotica"
    REPOSITORIO_PROYECTO_LINK="https://github.com/RoniHernandez99/IoT_domotica"

    FOTO_PROGRAMADOR=":/SISTEMA_CONTROL/IMAGENES/SISTEMA_CONTROL/yoMero2.jpg"


    # Datos del mensaje que se mandaria al programador 
    GMAILS=["roni.hernandez.1999@gmail.com"]
    GMAIL_SUBJECT=f"Comentarios acerca de: {REPOSITORIO_PROYECTO_NOMBRE}"
    GMAIL_CUERPO=f"Hola {NOMBRE_PROGRAMADOR} espero tengas un buen dia, el motivo del mensaje es:"


class App_Alarmas():

    NOMBRE_BASE_DATOS_ALARMAS="CUERPO/RECURSOS/DATOS/BaseDatosAlarma.db"

    CARPETA_MUSICA="CUERPO/RECURSOS/MUSICA/"
    CARPETA_MUSICA_DEFAULT="DEFAULT/"
    CARPETA_MUSICA_MIA="MIA/"
    
    NOMBRE_SONIDO_NULL="SIN MUSICA"
    AUDIO_YA_DESPIERTA="CUERPO/RECURSOS/SONIDOS_SISTEMA/hora_despertar.wav"
    AUDIO_IR_DORMIR="CUERPO/RECURSOS/SONIDOS_SISTEMA/hora_dormir.wav"
    AUDIO_HAZ_DEBERES="CUERPO/RECURSOS/SONIDOS_SISTEMA/hora_deberes.wav"

    @classmethod
    def actualizarUbicaciones(cls,ubicacion):

        cls.NOMBRE_BASE_DATOS_ALARMAS=ubicacion+cls.NOMBRE_BASE_DATOS_ALARMAS
        cls.CARPETA_MUSICA=ubicacion+cls.CARPETA_MUSICA

        cls.AUDIO_YA_DESPIERTA=ubicacion+cls.AUDIO_YA_DESPIERTA
        cls.AUDIO_IR_DORMIR=ubicacion+cls.AUDIO_IR_DORMIR
        cls.AUDIO_HAZ_DEBERES=ubicacion+cls.AUDIO_HAZ_DEBERES



class App_Deberes():
    ARCHIVO_DEBERES="CUERPO/RECURSOS/DATOS/deberes.txt"
    SEPARADOR_DEBERES='^'

    @classmethod
    def actualizarUbicaciones(cls,ubicacion):
        cls.ARCHIVO_DEBERES=ubicacion+cls.ARCHIVO_DEBERES


from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon


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
