import pandas as pd
from gtts import gTTS

import recursos


def hacer_audios_estaciones():
    # columnas: 'nombre' 'lng' 'lat'
    tabla_archivo_ubicaciones = pd.read_excel(
        recursos.App_Principal.ARCHIVO_UBICACIONES_ESTACIONES
    )
    print(tabla_archivo_ubicaciones.columns)
    nombres_estaciones = tabla_archivo_ubicaciones.nombre

    nombre_carpeta = recursos.App_Principal.CARPETA_AUDIOS_ESTACIONES
    extension_archivo_audio = ".mp3"

    # creando los audios de cada estacion del metro...
    for nombre_estacion in nombres_estaciones:
        archivo_audio = nombre_carpeta + nombre_estacion + extension_archivo_audio

        print("Creando:", archivo_audio)
        tts = gTTS(nombre_estacion, lang="es-us")
        tts.save(archivo_audio)


def crear_audio_frase(frase, nombre_archivo_audio):
    nombre_carpeta = recursos.App_Principal.CARPETA_FRASES
    extension_archivo_audio = ".mp3"
    archivo_audio = nombre_carpeta + nombre_archivo_audio + extension_archivo_audio

    tts = gTTS(frase, lang="es-us")
    tts.save(archivo_audio)


hacer_audios_estaciones()
crear_audio_frase("Iniciamos en...", "frase_inicio")
crear_audio_frase("Despues vamos a...", "frase_intermedia")
