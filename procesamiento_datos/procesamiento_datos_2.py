
import matplotlib.pyplot as plt
import pandas as pd 
import unidecode 



def normalizar_str(dato_str):
    '''
    Convierte el parametro 'data_str' en minusculas
    Quita los espacios laterales del parametro 'data_str'
    Quita tildes y acentos del parametro 'data_str'

    Parámetros:
        -dato_str: Dato de tipo 'str' que se quiere normalizar
    
    Returns:
        - Un dato de tipo 'str' que representa al parametro 'data_str'
        normalizado
    '''

    dato_str=dato_str.strip()
    dato_str=dato_str.lower()
    dato_str=unidecode.unidecode(dato_str) 

    return dato_str


# separacion de estaciones de metro... 
# fuente de informacion: https://github.com/IgorEM/Melhor-Rota---Metro-da-cidade-do-Mexico---Dijkstra-
# https://github.com/IgorEM/Melhor-Rota---Metro-da-cidade-do-Mexico---Dijkstra-/blob/main/183arestasOrigDestPesoVirgulasSemEspacoNaoDirecional.txt


file_separacion_estaciones="datos/crudos/estaciones_separacion.txt"
file_limpio="datos/procesados/estaciones_separacion.xlsx"

# Origen	    Destino      	Longitud de interestación
tabla_separacion=pd.read_csv(file_separacion_estaciones)

tabla_separacion_limpia={'origen':[],'destino':[]}
# poner nombres en minusculas y quitar acentos
for nombre_origen,nombre_destino in zip(tabla_separacion.Origen,tabla_separacion.Destino):
    nombre_origen=normalizar_str(nombre_origen)
    nombre_destino=normalizar_str(nombre_destino)
    tabla_separacion_limpia['origen'].append(nombre_origen)
    tabla_separacion_limpia['destino'].append(nombre_destino)


# creando un DataFrame con los datos corregidos...
tabla_separacion_limpia=pd.DataFrame(tabla_separacion_limpia)
tabla_separacion_limpia['longitud de interestacion']=tabla_separacion['Longitud de interestación']


#print( tabla_separacion_limpia.head() )

# creando tabla con datos limpios sin los indices de esta...
tabla_separacion_limpia.to_excel(file_limpio, encoding='utf-8',index=False)





