import pandas as pd
import networkx as nx
import socket 
import threading
import pickle



class Servidor():

    def __init__(self,file_separacion_estaciones,host="127.0.0.1",port=55555):

        self.servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.servidor.bind( (host,port) )
        self.servidor.listen()

        self.red_metro=self.get_red_metro(file_separacion_estaciones)
    

    def get_red_metro(self,file_separacion_estaciones):
        '''
        Cargara los datos de las separación de cada estación del red del metro, porteriormente
        utilizara dichos datos para obtener un objeto de tipo 'networkx'.
        '''

        # columanas: origen     	destino     	longitud de interestacion
        tabla_separacion = pd.read_excel(file_separacion_estaciones)
        red_de_metro = nx.from_pandas_edgelist(tabla_separacion,source='origen',target='destino',edge_attr='longitud de interestacion')
        return red_de_metro


    def retornar_ruta_mas_corta(self,cliente,addres,origen,destino):
        ruta_seguir= nx.dijkstra_path(self.red_metro, source=origen, target=destino, weight='longitud de interestacion')
        no_estaciones_ruta=len(ruta_seguir)-1
        distancia_recorrer=nx.dijkstra_path_length(self.red_metro, source=origen, target=destino, weight='longitud de interestacion')
        tupla_datos=(ruta_seguir,no_estaciones_ruta,distancia_recorrer)

        tupla_fragmentada=pickle.dumps(tupla_datos)
        tupla_bytes=bytes(tupla_fragmentada)

        print(f"Cliente: {addres} solicita saber la mas corta entre las estaciones:\n")

        cliente.send( tupla_bytes )
        cliente.close()


    def ejeuctar_servidor(self):
        while True:
            try:
                cliente,addres=self.servidor.accept()
                datos_recividos=cliente.recv(1024)
                datos_recividos=pickle.loads(datos_recividos)
                origen=datos_recividos['origen']
                destino=datos_recividos['destino']

                hilo=threading.Thread(
                    target=self.retornar_ruta_mas_corta,
                    args=(cliente,addres,origen,destino)
                )
                hilo.start()

            except KeyboardInterrupt:
                self.servidor.close()
                break


if __name__ == "__main__":
    print("S E R V E R    M E T R O ")
    servidor_metro=Servidor(
        file_separacion_estaciones="../procesamiento_datos/datos/procesados/estaciones_separacion.xlsx",
        host="127.0.0.1",
        port=55555
    )

    # ejecutando el servidor...
    servidor_metro.ejeuctar_servidor()

