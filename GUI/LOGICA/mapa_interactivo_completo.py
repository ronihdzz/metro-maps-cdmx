
from email.charset import QP
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QScrollArea,QGridLayout,QPushButton
from PyQt5.Qt import Qt
import sys
import pandas as pd
from PyQt5.QtCore import Qt, pyqtSignal,QObject

###############################################################
#  MIS LIBRERIAS...
##############################################################
from recursos import HuellaAplicacion


class BotonCoordenada(QObject):
    def __init__(self,nombre:str,boton:QPushButton,funcion):
        '''
        nombre:  Nombre de la estacion que representa el punto
        boton:   Objeto QPushButton que representa el punto
        funcion: Funcion que se ejecutara cuando se precione el boton
                 del punto.Dicha función  exigira recibir como parametro
                 el nombre de la estacion que representa el punto
        '''
        QObject.__init__(self)
        self.nombre=nombre
        self.boton=boton
        self.boton.clicked.connect(  lambda: funcion(self.nombre)   )


class MapaInteractivoCompleto(QMainWindow,HuellaAplicacion):
    senal_punto_panel_clic= pyqtSignal(str)

    ESTILO_ESTACIONES="border: 1px solid blue;border-radius:5px;"
    ESTILO_RUTA_ESTACIONES="border: 1px solid blue;border-radius:5px; background-color:red;"

    def __init__(self,file_lat_long_red):
        QMainWindow.__init__(self)
        HuellaAplicacion.__init__(self)


        self.ANCHO_PANEL=2000
        self.ALTO_PANEL=800
        self.MARGEN_PANEL=20


        # self.ANCHO_CONTENEDOR_PANEL=1000
        # self.ALTO_CONTENEDOR_PANEL=600
        # self.setGeometry(60, 60,self.ANCHO_CONTENEDOR_PANEL,self.ALTO_CONTENEDOR_PANEL)

        
        self.panel_mapa=None 
        self.mostrador_panel_mapa=None
        self.file_lat_long_red=None
        self.lista_estaciones_ultima_ruta=[]


        # creara el atributo de instancia: self.mostrador_panel_mapa
        self.crear_mostrador_panel()

        self.panel_mapa=QMainWindow()
        self.fijar_tamano_panel_mapa(
            ancho=self.ANCHO_PANEL,
            alto=self.ALTO_PANEL,
            margen=self.MARGEN_PANEL
        )
        self.cargar_contenido_panel_mapa(file_lat_long_red)
        self.mostrador_panel_mapa.addWidget(self.panel_mapa)

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


    def crear_mostrador_panel(self):
        '''
        Creara 3 atributos de instancia cuyo objetivo sera mostrar los 'itemDeber' que el usuario vaya
        creando y en dado caso que el espacio ya no alcance para mostrarlos todos  'itemDeber', debera 
        aparecer una barra lateral que permitira visualizar todos los 'itemDeber'.Los 3 atributos de instancia
        trabajan en conjunto para cumplir lo mencionado anteriormente.Los atributos de instancia que se
        crearan son los siguientes:
            A) Nombre: self.scroll  ¿que es? un objeto de la clase QScrollArea()
            B) Nombre: self.widget  ¿que es? un objeto de la clase QWidget()
            C) Nombre: self.mostrador_panel  ¿que es? un objeto de la clase QGridLayout() 
        '''

        self.scroll = QScrollArea()
        self.scroll.setStyleSheet("""
                            *{
                            border:none;
                            background:#FFFFFF;
                            }
                            QScrollArea{
                                border-radius:20%;
                                padding:10px;
                                margin-bottom:15px;
                            }
                            QScrollBar{
                            background:#F7E5E5;
                            }
                            QScrollBar::handle{
                            background :#979797;
                            }
                            QScrollBar::handle::pressed{
                            background :  #193b58;
                            }
        """) 

        self.widget = QWidget()   
        self.mostrador_panel_mapa = QGridLayout()     
        self.widget.setLayout(self.mostrador_panel_mapa)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)


    def fijar_tamano_panel_mapa(self,ancho:int,alto:int,margen:int):
        '''
        - Creara  o modificara los valores de las varaibles de instancia: 
            A) 'self.ANCHO_PANEL'
            B) 'self.ALTO_PANEL'
            C) 'self.MARGEN_PANEL'
        - Cambiara el tamaño del panel donde se muestra la red del metro, a los
        tamaños establecido en los parametros 'ancho', 'alto', 'margen'

        Parámetros:
            ancho:  Representa el ancho que tendra el panel en donde se muestra la
                    red del metro de la CDMX
            alto:   Representa el alto que tendra el panel en donde se muestra la 
                    red del metro de la CDMX
            margen: Representa el margen interior que tendra el panel en donde se muestra la 
                    red del metro de la CDMX
        '''

        self.ANCHO_PANEL=ancho
        self.ALTO_PANEL=alto
        self.MARGEN_PANEL=margen
    
        self.panel_mapa.setMaximumWidth(self.ANCHO_PANEL)
        self.panel_mapa.setMaximumHeight(self.ALTO_PANEL)
        self.panel_mapa.setMinimumSize(self.ANCHO_PANEL,self.ALTO_PANEL) 



    def cargar_contenido_panel_mapa(self,file_lat_long_red:str):
        '''
        - Leera el archivo excel 'file_lat_long_red' el cual contiene las latitudes,longitudes 
          y nombres de cada estacion de la red
        - Normalizara todas las latitudes y longitudes del archivo
        - Creara el mapa apartir de las longitudes y latitudes
        - Almacenara en el diccionario: 'self.dict_puntos' todos los puntos de cada estacion de la red
          donde cada key del diccionario sera el nombre de cada estacion, y cada value del diccionario
          correspondera al punto de la estación.

        Parámetro:
            file_lat_long_red: Nombre del archivo excel el cual contiene las latitudes,longitudes 
                               y nombres de cada estacion de la red

                               Las columnas que contiene el archivo deberan ser:
                                * name
                                * lat
                                * lng
        '''

        # columnas: name        lat      lng
        tabla_ubicaciones=pd.read_excel(file_lat_long_red)

        # funcion con la cual normalizare las latitudes y longitudes
        normalizar=lambda data:  (data-data.min())/ (data.max() - data.min())

        tabla_ubicaciones["lat"]= normalizar(tabla_ubicaciones["lat"])
        tabla_ubicaciones["lng"] = normalizar(tabla_ubicaciones["lng"])


        # latitudes=x    logitudes=y 
        latitudes_adapatadas=(  tabla_ubicaciones["lat"]*(self.ANCHO_PANEL-2*self.MARGEN_PANEL) ) +self.MARGEN_PANEL
        longitudes_adaptadas= ( tabla_ubicaciones["lng"]*(self.ALTO_PANEL-2*self.MARGEN_PANEL) )+self.MARGEN_PANEL

        # graficando los puntos 
        self.dict_puntos={}
        for nombre,x,y in zip(tabla_ubicaciones.nombre, latitudes_adapatadas,longitudes_adaptadas ):
            punto_estacion_red=BotonCoordenada(
                nombre=nombre,
                boton=QPushButton("",self.panel_mapa),
                funcion=lambda nombre_x : self.senal_punto_panel_clic.emit(nombre_x)   
            )
            # fijando el boton en la coordenada respectiva
            punto_estacion_red.boton.move(int(x),int(y))
            # estableciendo un tamaño fijo al boton
            punto_estacion_red.boton.resize(15,15)
            # asignandole estilo correspondiente al boton
            punto_estacion_red.boton.setStyleSheet(self.ESTILO_ESTACIONES)

            # guardando boton en diccionario
            self.dict_puntos[nombre]=punto_estacion_red



if __name__ == "__main__":        
    # creando aplicacion pyqt5
    App = QApplication(sys.argv)
    window = MapaInteractivoCompleto()

    # inciando aplicacion de escritorio
    sys.exit(App.exec())