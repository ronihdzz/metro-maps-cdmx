import matplotlib.pyplot as plt
import pandas as pd
import unidecode

# separacion de estaciones de metro...
# fuente de informacion: https://github.com/IgorEM/Melhor-Rota---Metro-da-cidade-do-Mexico---Dijkstra-
# https://github.com/IgorEM/Melhor-Rota---Metro-da-cidade-do-Mexico---Dijkstra-/blob/main/183arestasOrigDestPesoVirgulasSemEspacoNaoDirecional.txt

file_ubicaciones_estaciones = "datos/procesados/estaciones_ubicacion_2.xlsx"
file_separacion_estaciones = "datos/procesados/estaciones_separacion.xlsx"


# origen	    destino      	longitud de interestacion
tabla_separacion = pd.read_excel(file_separacion_estaciones)

nombres_estaciones = {}
# poner nombres en minusculas y quitar acentos
for nombre in tabla_separacion.origen:
    if not nombres_estaciones.get(nombre, False):
        nombres_estaciones[nombre] = True
lista_nombres_estaciones_by_separacion = list(nombres_estaciones.keys())


print("C O M P R O B A N D O    M I S M O    N U M E R O    D E    D A T O  S ")
print(
    "Numero de estaciones registradas en tabla_separacion:",
    len(lista_nombres_estaciones_by_separacion),
)


# columna: 'lng' 'lat'  'nombre'
tabla_ubicacion = pd.read_excel(file_ubicaciones_estaciones)

print(
    "Numero de estaciones registradas en tabla_ubicacion:", len(tabla_ubicacion.nombre)
)


print(
    "D I F E R E N C I A S    E N  T R E    N O M B  R E  S      D  E     E  S T  A C I O  N E S "
)
print(
    "Nombre de estaciones que no hay en la tabla de separacion pero si en la de ubicacion"
)
diferencia = set(tabla_ubicacion.nombre) - set(lista_nombres_estaciones_by_separacion)
print("No= ", len(diferencia))
print(diferencia)

print("*" * 150)

print(
    "Nombre de estaciones que no hay en la tabla de ubicacion pero si en la de separacion"
)
diferencia = set(lista_nombres_estaciones_by_separacion) - set(tabla_ubicacion.nombre)
print("No= ", len(diferencia))
print(diferencia)
