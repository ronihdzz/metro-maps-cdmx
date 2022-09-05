import pickle
import socket


class ClientSocket:
    def __init__(self, ip_server: str = "127.0.0.1", port_server: int = 1111):
        """
        NOTE: Los puertos libres son: 1,024 a 49,151
        """

        self.ip_server = ip_server
        self.port_server = port_server

    def crear_conectar_socket(self) -> socket.socket:
        my_socket = socket.socket(
            family=socket.AF_INET,  # socket.AF_INET = Internet protocol IPv4
            # socket.AF_INET6 = Internet protocol IPv6
            type=socket.SOCK_STREAM  # socket.SOCK_STREAM = Protocol TCP
            # socket.AF_INET6 = Protocol UDP
        )
        my_socket.connect((self.ip_server, self.port_server))
        return my_socket

    def get_server_para_obtener_ruta(
        self, nombre_estacion_origen: str, nombre_estacion_destino: str
    ) -> list:

        cliente = self.crear_conectar_socket()
        datos_de_consulta = {
            "origen": nombre_estacion_origen,
            "destino": nombre_estacion_destino,
        }

        datos_de_consulta = pickle.dumps(datos_de_consulta)
        cliente.send(bytes(datos_de_consulta))

        respuesta_server = cliente.recv(10000)
        ruta_seguir = pickle.loads(respuesta_server)

        cliente.close()

        return ruta_seguir
