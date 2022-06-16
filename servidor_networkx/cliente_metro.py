import socket 
import pickle


def consultar_servidor(origen,destino):
    
    host="127.0.0.1"
    puerto=55555

    cliente_pregunton=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cliente_pregunton.connect( (host,puerto) )

    dict_datos_pregunta_cliente={
        'origen':origen,
        'destino':destino
    }

    dict_datos_pregunta_cliente=pickle.dumps(dict_datos_pregunta_cliente)
    cliente_pregunton.send( bytes(dict_datos_pregunta_cliente) )

    datos_recibidos=cliente_pregunton.recv(65507)
    ruta_seguir=pickle.loads(datos_recibidos)
    
    cliente_pregunton.close()

    return ruta_seguir


if __name__ == "__main__":

    while True:
        print("\n*********************************************************************************")
        origen,destino=input("Ingresa origen,destino: ").split(',')
        
        ruta_seguir=consultar_servidor(origen=origen,destino=destino)
        
        print("Datos recibidos...",ruta_seguir)

        

