import pandas as pd
import matplotlib.pyplot as plt


MARGEN=50
ANCHO_PANTALLA=1200
ALTO_PANTALLA=600
  



file_ubicaciones="datos/procesados/estaciones_ubicacion_2.xlsx"
# _id	id	geo_point_2d	geo_shape	name	detalle
tabla_ubicaciones=pd.read_excel(file_ubicaciones)


plt.scatter(tabla_ubicaciones["lat"],tabla_ubicaciones["lng"])
plt.show()

normalizar=lambda data:  (data-data.min())/ (data.max() - data.min())

tabla_ubicaciones["lat"]= normalizar(tabla_ubicaciones["lat"])
tabla_ubicaciones["lng"] = normalizar(tabla_ubicaciones["lng"])

plt.scatter(tabla_ubicaciones["lat"],tabla_ubicaciones["lng"])
plt.show()



# LATITUDE=x    LONGITUDE=y 
tabla_ubicaciones["lat"]=( tabla_ubicaciones["lat"]*(ANCHO_PANTALLA-2*MARGEN) ) +MARGEN
tabla_ubicaciones["lng"]= ( tabla_ubicaciones["lng"]*(ALTO_PANTALLA-2*MARGEN) )+MARGEN

plt.scatter(tabla_ubicaciones["lat"],tabla_ubicaciones["lng"])
plt.show()


