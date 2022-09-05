import pickle
import socket
import threading

import networkx as nx
import pandas as pd


class ServerSocket:
    def __init__(
        self,
        file_separacion_estaciones: str,
        ip_server: str = "127.0.0.1",
        port_server: int = 1111,
    ):
        """
        NOTE: Los puertos libres son: 1,024 a 49,151
        """

        self.ip_server = ip_server
        self.port_server = port_server
        self.servidor = self.crear_conectar_socket()
        self.red_metro = self.get_red_metro(file_separacion_estaciones)

    def crear_conectar_socket(self) -> socket.socket:
        my_socket = socket.socket(
            family=socket.AF_INET,  # socket.AF_INET = Internet protocol IPv4
            # socket.AF_INET6 = Internet protocol IPv6
            type=socket.SOCK_STREAM  # socket.SOCK_STREAM = Protocol TCP
            # socket.AF_INET6 = Protocol UDP
        )

        my_socket.bind((self.ip_server, self.port_server))
        my_socket.listen()

        return my_socket

    def get_red_metro(self, file_separacion_estaciones):
        """
        Cargara los datos de las separación de cada estación del red del metro, porteriormente
        utilizara dichos datos para obtener un objeto de tipo 'networkx'.
        """

        # columnas del archivo: 'origen'     	'destino'     	'longitud de interestacion'
        tabla_separacion = pd.read_excel(file_separacion_estaciones)
        red_de_metro = nx.from_pandas_edgelist(
            tabla_separacion,
            source="origen",
            target="destino",
            edge_attr="longitud de interestacion",
        )
        return red_de_metro

    def retornar_ruta_mas_corta(self, cliente, addres, origen, destino):
        ruta_seguir = nx.dijkstra_path(
            self.red_metro,
            source=origen,
            target=destino,
            weight="longitud de interestacion",
        )
        no_estaciones_ruta = len(ruta_seguir) - 1
        distancia_recorrer = nx.dijkstra_path_length(
            self.red_metro,
            source=origen,
            target=destino,
            weight="longitud de interestacion",
        )
        tupla_datos = (ruta_seguir, no_estaciones_ruta, distancia_recorrer)

        tupla_fragmentada = pickle.dumps(tupla_datos)
        tupla_bytes = bytes(tupla_fragmentada)

        direccion_ip, puerto = addres
        print("*" * 100)
        print(
            f"Cliente con direccion IPV4: '{direccion_ip}' desde el puerto: '{puerto}'"
        )
        print(
            f"requiere la ruta mas corta entre las estaciones:'{origen}' y '{destino}'"
        )

        cliente.send(tupla_bytes)
        cliente.close()

    def ejeuctar_servidor(self):
        while True:
            try:
                cliente, addres = self.servidor.accept()
                datos_recividos = cliente.recv(1024)
                datos_recividos = pickle.loads(datos_recividos)
                origen = datos_recividos["origen"]
                destino = datos_recividos["destino"]

                hilo = threading.Thread(
                    target=self.retornar_ruta_mas_corta,
                    args=(cliente, addres, origen, destino),
                )
                hilo.start()

            except KeyboardInterrupt:
                self.servidor.close()
                break
