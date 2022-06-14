import pandas as pd
import networkx as nx


file_separacion_estaciones="procesamiento_datos/procesados/estaciones_separacion.xlsx"



class Servidor():
    def __init__(self,file_separacion_estaciones):
        self.red_metro=self.get_red_metro(file_separacion_estaciones)
        

    def get_red_metro(self,file_separacion_estaciones):
        # columanas: origen     	destino     	longitud de interestacion
        tabla_separacion = pd.read_excel(file_separacion_estaciones)
        red_de_metro = nx.from_pandas_edgelist(tabla_separacion,source='origen',target='destino',edge_attr='longitud de interestacion')
        return red_de_metro


    def get_ruta_mas_cercana(self,origen,destino):
        ruta_seguir= nx.dijkstra_path(self.red_metro, source=origen, target=destino, weight='longitud de interestacion')
        no_estaciones_ruta=len(ruta_seguir)-1
        distancia_recorrer=nx.dijkstra_path_length(self.red_metro, source=origen, target=destino, weight='longitud de interestacion')


        return ruta_seguir,no_estaciones_ruta,distancia_recorrer

