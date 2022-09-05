import matplotlib.pyplot as plt
import pandas as pd
import unidecode


def normalizar_str(dato_str):
    """
    Convierte el parametro 'data_str' en minusculas
    Quita los espacios laterales del parametro 'data_str'
    Quita tildes y acentos del parametro 'data_str'

    Parámetros:
        -dato_str: Dato de tipo 'str' que se quiere normalizar

    Returns:
        - Un dato de tipo 'str' que representa al parametro 'data_str'
        normalizado
    """

    dato_str = dato_str.strip()
    dato_str = dato_str.lower()
    dato_str = unidecode.unidecode(dato_str)

    return dato_str


# link de consulta de datos
# https://datos.cdmx.gob.mx/gl/dataset/lineas-y-estaciones-del-metro/resource/0869e0dd-6876-4446-a199-8f670a359c00


# paso 1: obtener las longitudes y latitudes de solo las estaciones del metro
file_datos_pagina_oficial = "datos/crudos/estaciones_ubicacion.csv"
file_datos_limpios = "datos/procesados/estaciones_ubicacion.xlsx"

# _id	id	geo_point_2d	geo_shape	name	detalle
tabla = pd.read_csv(file_datos_pagina_oficial)

tabla_nueva = {"lng": [], "lat": [], "nombre": {}}

# algoritmo para limpiar los datos ....
for punto, nombre in zip(tabla["geo_point_2d"], tabla["name"]):
    nombre = nombre.split("_")[0]
    nombre = normalizar_str(nombre)

    if not nombre.startswith("linea") and not tabla_nueva["nombre"].get(nombre, False):
        tabla_nueva["nombre"][nombre] = True
        x, y = punto.split(",")
        tabla_nueva["lng"].append(float(x))
        tabla_nueva["lat"].append(float(y))

tabla_nueva["nombre"] = tabla_nueva["nombre"].keys()
tabla_nueva = pd.DataFrame(tabla_nueva)

# visualiando dataframe para comprobar que todo marcha bien
# print(tabla_nueva.head())


# creando tabla con datos limpios sin los indices de esta y con los nombre de
# columnas: 'lng' 'lat'  'nombre'
tabla_nueva.to_excel(file_datos_limpios, encoding="utf-8", index=False)
