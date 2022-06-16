from PyQt5.QtWidgets import QLabel,QMainWindow,QApplication, QPushButton
import sys
from PyQt5.QtCore import Qt, pyqtSignal,QObject


import pandas as pd
import matplotlib.pyplot as plt



class BotonCoordenada(QObject):
    suHoraMorir= pyqtSignal(int)#indicara quien es el objeto que quiere morir...
    clickBotonPregunta=pyqtSignal(int)#indicara el id del boton
    def __init__(self,nombre,boton,funcion):
        QObject.__init__(self)
        self.nombre=nombre
        self.boton=boton
        self.boton.clicked.connect(  lambda: funcion(self.nombre)   )


class MapaInteractivo(QMainWindow):

    senal_punto_clic= pyqtSignal(str)

    def __init__(self,file_ubicaciones,ancho,alto,margen):
        super().__init__()

        self.ESTILO_ESTACIONES="border: 1px solid blue;border-radius:5px;"
        self.ESTILO_RUTA_ESTACIONES="border: 1px solid blue;border-radius:5px; background-color:red;"
        self.lista_estaciones_ultima_ruta=[]




        
        self.file_ubicaciones=file_ubicaciones

        # creara las variables: 'self.ANCHO', 'self.ALTO'
        # fijara la ventana al tamaño especificado
        self.fijar_tamano_ventana(ancho,alto,margen)

        # cargar del archivo de ubicaciones de estaciones
        # los normalizara y almacenara en 'self.tabla_ubicaciones'
        self.procesar_coordenadas()

        # mostrara la widget con los puntos respectivos
        self.recargar_mapa()

        self.show()

    
    def colorear_ruta_seguir(self,nombre_estaciones):
        # regresando a la normalidad las estaciones de la ultima ruta
        for punto in self.lista_estaciones_ultima_ruta:
            punto.boton.setStyleSheet(self.ESTILO_ESTACIONES)
        self.lista_estaciones_ultima_ruta=[]

        # remarcando las estaciones que conforman la ruta
        for nombre in nombre_estaciones:
            punto_interes=self.dict_puntos.get(nombre,None)
            if punto_interes:
                self.lista_estaciones_ultima_ruta.append(punto_interes)
                punto_interes.boton.setStyleSheet(self.ESTILO_RUTA_ESTACIONES)


    def fijar_tamano_ventana(self,ancho,alto,margen):
        '''
        - Creara las variables de instancia: 'self.ANCHO', 'self.ALTO'
        - Redimensionara la ventana a los valores indicados
        '''

        self.ANCHO=ancho
        self.ALTO=alto
        self.MARGEN=margen
    
        self.setMaximumWidth(self.ANCHO)
        self.setMaximumHeight(self.ALTO)
        self.setMinimumSize(self.ANCHO,self.ALTO) 
        
        #self.setFixedWidth(ANCHO_PANTALLA)
        #self.setFixedHeight(ALTO_PANTALLA)

    def procesar_coordenadas(self):
        '''
        Leera el archivo que contiene las latitudes,longitudes y nombres de 
        todas las lineas del metro.
        Normalizara todas las latitudes y longitudes del archivo
        Creara la variable de instancia: 'self.tabla_ubicaciones' que contendra
        la informacion mencionada anteriormente
        '''

        # columnas: name        lat      lng
        self.tabla_ubicaciones=pd.read_excel(self.file_ubicaciones)
        normalizar=lambda data:  (data-data.min())/ (data.max() - data.min())
        self.tabla_ubicaciones["lat"]= normalizar(self.tabla_ubicaciones["lat"])
        self.tabla_ubicaciones["lng"] = normalizar(self.tabla_ubicaciones["lng"])
    

    def recargar_mapa(self):
        '''
        Creara el mapa apartir de las longitudes y latitudes
        Almacenara en la lista: 'self.lista_puntos' todos los puntos de cada estacion
        '''

        # latitudes=x    logitudes=y 
        latitudes_adapatadas=( self.tabla_ubicaciones["lat"]*(self.ANCHO-2*self.MARGEN) ) +self.MARGEN
        longitudes_adaptadas= ( self.tabla_ubicaciones["lng"]*(self.ALTO-2*self.MARGEN) )+self.MARGEN

        # eliminando los labels creados previamente...
        #for punto in self.lista_puntos:
        #    punto.deleteLater()

        # graficando los puntos 
        self.dict_puntos={}
        for nombre,x,y in zip(self.tabla_ubicaciones.nombre, latitudes_adapatadas,longitudes_adaptadas ):
            punto_boton=self.graficar_punto(nombre,x,y)


            objeto=BotonCoordenada(nombre,punto_boton, lambda nombre : self.senal_punto_clic.emit(nombre)   )

            self.dict_puntos[nombre]=objeto


    def graficar_punto(self,nombre,x,y):

        # creating a label widget
        # by default label will display at top left corner
        #label_1 =QLabel("", self)
        label_1= QPushButton("",self)
        # moving position
        label_1.move(int(x),int(y))
  
        # making label square in size
        label_1.resize(15,15)
  
        # setting up border and radius
        #self.label_1.setStyleSheet("border: 3px solid blue;border-radius: 1000px;")
        label_1.setStyleSheet(self.ESTILO_ESTACIONES)
        return label_1
   


if __name__ == "__main__":        
    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = MapaInteractivo(
        ancho=1200,
        alto=600,
        margen=50,
        file_ubicaciones="procesamiento_datos/datos/procesados/estaciones_ubicacion_2.xlsx"
    )


    # start the app
    sys.exit(App.exec())