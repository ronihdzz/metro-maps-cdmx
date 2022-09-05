import matplotlib.pyplot as plt
import pandas as pd

from GUI.LOGICA.utils import normalizar_por_escalado_de_variables

MARGEN = 50
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 600


file_ubicaciones = "datos/procesados/estaciones_ubicacion_2.xlsx"
# _id	id	geo_point_2d	geo_shape	name	detalle
tabla_ubicaciones = pd.read_excel(file_ubicaciones)


plt.scatter(tabla_ubicaciones["lat"], tabla_ubicaciones["lng"])
plt.show()

tabla_ubicaciones["lat"] = normalizar_por_escalado_de_variables(
    valores=tabla_ubicaciones["lat"],
    valor_min=tabla_ubicaciones["lat"].min(),
    valor_max=tabla_ubicaciones["lat"].max(),
)
tabla_ubicaciones["lng"] = normalizar_por_escalado_de_variables(
    valores=tabla_ubicaciones["lng"],
    valor_min=tabla_ubicaciones["lng"].min(),
    valor_max=tabla_ubicaciones["lng"].max(),
)

plt.scatter(tabla_ubicaciones["lat"], tabla_ubicaciones["lng"])
plt.show()


# LATITUDE=x    LONGITUDE=y
tabla_ubicaciones["lat"] = (
    tabla_ubicaciones["lat"] * (ANCHO_PANTALLA - 2 * MARGEN)
) + MARGEN
tabla_ubicaciones["lng"] = (
    tabla_ubicaciones["lng"] * (ALTO_PANTALLA - 2 * MARGEN)
) + MARGEN

plt.scatter(tabla_ubicaciones["lat"], tabla_ubicaciones["lng"])
plt.show()
