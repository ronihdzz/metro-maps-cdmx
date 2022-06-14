import pandas as pd 


# articulo interesante.... https://www.chilango.com/general/estaciones-del-metro-que-pokevolucionaron/ 


#Nombre de estaciones que no hay en la tabla de separacion pero si en la de ubicacion
#No=  11
#   {
#       'tecnologico',
#       'bosque de aragon',
#       'blvd. puerto aereo',
#       'hospital 20 de nov.',
#       'etiopia / plaza de la transpatencia',
#       'uam-i', 'r. flores magon',
#       'periferico ote',
#       'viveros',
#       'la villa - basilica',
#       'mixhuca'
#   }
# ******************************************************************************************************************************************************
#Nombre de estaciones que no hay en la tabla de ubicacion pero si en la de separacion
#No=  11
#   {
#       'ricardo flores magon',
#       'boulevard puerto aereo',
#       'etiopia/plaza de la transparencia',
#       'periferico oriente',
#       'ecatepec',
#       'bosques de aragon',
#       'uam i', 
#       'viveros/derechos humanos',
#       'mixiuhca',
#       'hospital 20 de noviembre',
#       'la villa-basilica'
#   }



file_ubicaciones_estaciones="datos/procesados/estaciones_ubicacion.xlsx"
file_ubicaciones_estaciones_estandarizado="datos/procesados/estaciones_ubicacion_2.xlsx"


# columna: 'lng' 'lat'  'nombre'
tabla_ubicacion=pd.read_excel(file_ubicaciones_estaciones)


relacion_remplazo_nombres={
    'tecnologico':'ecatepec',
    'bosque de aragon':'bosques de aragon',
    'blvd. puerto aereo':'boulevard puerto aereo',
    'hospital 20 de nov.':'hospital 20 de noviembre',
    'etiopia / plaza de la transpatencia':'etiopia/plaza de la transparencia',
    'uam-i':'uam i', 
    'r. flores magon':'ricardo flores magon',
    'periferico ote':'periferico oriente',
    'viveros':'viveros/derechos humanos',
    'la villa - basilica':'la villa-basilica',
    'mixhuca':'mixiuhca'
}


lista_nombres_actualizados=[]
for nombre in  tabla_ubicacion.nombre:
    nuevo_nombre=relacion_remplazo_nombres.get(nombre,None)
    if nuevo_nombre:
        nombre=nuevo_nombre
    lista_nombres_actualizados.append(nombre)

tabla_ubicacion['nombre']=lista_nombres_actualizados

print(tabla_ubicacion.head())

# creando tabla con datos limpios sin los indices de esta...
tabla_ubicacion.to_excel(file_ubicaciones_estaciones_estandarizado, encoding='utf-8',index=False)

