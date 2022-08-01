from  typing import Callable
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QScrollArea,QGridLayout,QPushButton
from PyQt5.QtCore import Qt, pyqtSignal,QObject
import pandas as pd

###############################################################
#  MIS LIBRERIAS...
##############################################################
from recursos import HuellaAplicacion


class BotonCoordenada(QObject):
    '''
    Crea instancias que representan un punto de un mapa.
    Por ejemplo:
    - Si el mapa fuera el de una red de transporte de un metro,
      cada instancia de esta clase pudiera interpretarse como
      cada estación de la red del metro
    - Si el mapa fuera el mapa de la distribución de todos los locales
      de una pizzeria, cada instancia de esta clase pudiera interpretarse
      como cada sucursal de la pizzeria.
    - Si el mapa fuera el mapa de la distribución de escuelas de un municipio,
      cada instancia de esta clase pudiera interpretarse como cada escuela
      de ese municipio.

    Por lo mencionado anteriormente, cada instancia de esta clase, esta compuesta
    de un nombre, un boton y una función que se ejecutara cada vez que se oprima
    el boton.
    '''

    DISENO_ESTADO_NORMAL="border: 1px solid blue;border-radius:5px;"
    DISENO_ESTADO_SELECCIONADO="border: 1px solid blue;border-radius:5px; background-color:red;"


    def __init__(self,nombre:str,boton:QPushButton,funcion: Callable[ [str],None ]):
        '''
        Parámetros:
            nombre:  Nombre de lo que representa la instancia(una estacion de metro, una 
                     pizzeria, un escuela, etc. )
            boton:   Boton que representa a la instancia(una estacion de metro, una pizzeria,
                     un escuela, etc. )
            funcion: Funcion que se ejecutara cuando se precione el boton de la instancia. 
                     Dicha función  exigira recibir como parametro el nombre de lo que representa 
                     la instancia(una estacion de metro, una pizzeria,un escuela, etc. ) 
        '''

        QObject.__init__(self)
        self.nombre=nombre
        self.boton=boton
        self.boton.clicked.connect(  lambda: funcion(self.nombre)   )
        self.poner_en_estado_normal()


    def poner_en_estado_normal(self):
        '''
        Cambiara el diseño del boton que representa a la instancia(una estacion de metro, 
        una pizzeria,un escuela, etc.) a un diseño que represente que NO FORMA parte de
        ninguna ruta.
        '''

        self.boton.setStyleSheet(self.DISENO_ESTADO_NORMAL)
        
    def poner_en_estado_destacado(self):
        '''
        Cambiara el diseño del boton que representa a la instancia(una estacion de metro, 
        una pizzeria,un escuela, etc.) a un diseño que represente que SI FORMA parte a 
        un ruta, es decir que esta instancia representa a un conjunto de instancia que 
        representan una ruta.
        '''

        self.boton.setStyleSheet(self.DISENO_ESTADO_SELECCIONADO)
            


class MapaInteractivoCompleto(QMainWindow,HuellaAplicacion):
    senal_clic_punto_mapa= pyqtSignal(str)


    def __init__(self,file_lat_long_red:str,ancho:int,alto:int,margen:int):
        '''
        Parámetros:
            file_lat_long_red:  Representa el nombre de archivo excel que contiene la latitud 
                                longitud y nombre de cada estacion del mapa.El archivo excel 
                                debe contar solo con las siguientes columnas: 'name'  'lat'  'lng' 
            ancho:  Representa el ancho que tendra el panel en donde se  mostrara
                    cada punto del mapa
            alto:   Representa el alto que tendra el panel en donde se mostrara 
                    cada punto del mapa
            margen: Representa el margen interior que tendra el panel en donde se 
                    muestra cada punto del mapa
        '''
        
        QMainWindow.__init__(self)
        HuellaAplicacion.__init__(self)


        # Contendra las instancias de los puntos destacados del mapa.
        self.puntos_destacados_del_mapa=[]

        # 'self.panel_mapa':Representa el objeto que contendra cada punto del mapa
        self.panel_mapa=QMainWindow()

        self.dar_scroll_view_al_panel_mapa()

        self.fijar_tamano_panel_mapa(
            ancho=ancho,
            alto=alto,
            margen=margen
        )
        
        self.cargar_contenido_panel_mapa(file_lat_long_red)
        
        self.show()


    #colorear_ruta_seguir
    def destacar_puntos_mapa(self,lista_nombres_puntos:list)->None:
        '''
        1-. Primero se serciorara que todos los puntos(botones) del mapa(self.panel_mapa)
        esten en modo normal(diseño de punto normal).
        2-. Despues pondra en estado destacado(diseño de punto destacado) a cada punto cuyo
        nombre esta contenido en el parametro: 'lista_nombres_puntos', de tal manera que los 
        unicos puntos destacado en el mapa, sean los puntos cuyos nombres estan contenidos en
        el parametro: lista_nombres_puntos
        3-. Finalmente almacenara en el atributo de instancia: 'self.puntos_destacados_del_mapa'
        las instancias de puntos del mapa que fueron puestas en modo destacado

        Parámetros:
            lista_nombres_puntos: Lista de los nombres de los puntos del mapa que desean
            ser destacados con respecto a los demas puntos del mapa.

        '''

        # regresando a la normalidad las estaciones de la ultima ruta
        for punto in self.puntos_destacados_del_mapa:
            punto.poner_en_estado_normal()
        self.puntos_destacados_del_mapa=[]

        # remarcando las estaciones que conforman la ruta
        for nombre in lista_nombres_puntos:
            punto_interes=self.dict_puntos[nombre]
            if punto_interes:
                self.puntos_destacados_del_mapa.append(punto_interes)
                punto_interes.poner_en_estado_destacado()


    def dar_scroll_view_al_panel_mapa(self)->None:
        '''
        Le dara al objeto 'self.panel_mapa' la posibilidad de que pueda ser visualizado
        no importando lo grande que este sea pues, si es muy grande se hara uso de scroll view
        para su visualizacion

        Creara 3 atributos de instancia cuyo objetivo sera mostrar el objeto 'self.panel_mapa'
        no importando el tamaño que tenga dicho objeto.Los atributos de instancia que se crearan
        son los siguientes
            A) Nombre: 'self.scroll'  ¿que es? un objeto de la clase QScrollArea()
            B) Nombre: 'self.widget'  ¿que es? un objeto de la clase QWidget()
            C) Nombre: 'self.mostrador_panel'  ¿que es? un objeto de la clase QGridLayout() 
        
        El atributo de instancia 'self.mostrador_panel'  es el que mostrara el objeto 'self.panel_mapa'
        no importando si el objeto 'self.panel_mapa' es inclusive mas grande que 'self.mostrador_panel',
        ya que si 'self.panel_mapa' es mas grande  entonces 'self.mostrador_panel'  aplicara un scroll 
        para que 'self.panel_mapa' pueda ser visualizado, una analogia seria la siguiente: 
            - Si  'self.panel_mapa' fuera una foto, entonces 'self.mostrador_panel_mapa' 
              seria el portoretratos en donde sera colocada la foto.
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
        self.mostrador_panel_mapa.addWidget(self.panel_mapa)


    def fijar_tamano_panel_mapa(self,ancho:int,alto:int,margen:int)->None:
        '''
        - Cambiara el tamaño del panel donde se muestra cada punto del mapa 
        a los tamaños establecidos en los parametros 'ancho', 'alto', 'margen'

        - Creara  o modificara los valores de las variables de instancia: 
            A) 'self.ANCHO_PANEL'
            B) 'self.ALTO_PANEL'
            C) 'self.MARGEN_PANEL'

        Parámetros:
            ancho:  Representa el ancho que tendra el panel en donde se  mostrara
                    cada punto del mapa
            alto:   Representa el alto que tendra el panel en donde se mostrara 
                    cada punto del mapa
            margen: Representa el margen interior que tendra el panel en donde se 
                    muestra cada punto del mapa
        '''

        self.ANCHO_PANEL=ancho
        self.ALTO_PANEL=alto
        self.MARGEN_PANEL=margen
    
        self.panel_mapa.setMaximumWidth(self.ANCHO_PANEL)
        self.panel_mapa.setMaximumHeight(self.ALTO_PANEL)
        self.panel_mapa.setMinimumSize(self.ANCHO_PANEL,self.ALTO_PANEL) 



    def cargar_contenido_panel_mapa(self,file_lat_long_red:str)->None:
        '''
        - Leera el archivo excel 'file_lat_long_red' el cual contiene las latitudes,longitudes 
          y nombres de cada estacion de la red
        - Normalizara todas las latitudes y longitudes del archivo
        - Una vez normalizados los valores de las las latitudes y longitudes del archivo ahora
          proseguira a pasar a cada valor a la siguiente escala: 
                * las latitudes estaran definidos dentro del rango: 
                    ['self.MARGEN_PANEL'  ,  'self.ANCHO_PANEL'-'self.MARGEN_PANEL']
                * Las longitudes estaran definidos dentro del rando: 
                    ['self.MARGEN_PANEL'  ,  'self.ALTO_PANEL'-'self.MARGEN_PANEL']
        - Cargara en el objeto: 'self.panel_mapa' los puntos respectivos que seran localizados en 
          los nuevos valores de latitudes y longitudes que fueron obtenidos en el paso anterior
        - Almacenara en el diccionario: 'self.dict_puntos' todos los puntos de cada estacion del mapa
          donde cada key del diccionario sera el nombre de cada estacion, y cada value del diccionario
          correspondera al punto de la estación.

        Parámetros:
            file_lat_long_red:  Representa el nombre de archivo excel que contiene la latitud 
                                longitud y nombre de cada estacion del mapa.El archivo excel 
                                debe contar solo con las siguientes columnas: 'name'  'lat'  'lng' 
        '''

        # columnas: 'name'   'lat'      'lng'
        tabla_ubicaciones=pd.read_excel(file_lat_long_red)

        # funcion con la cual normalizara las latitudes y longitudes
        normalizar=lambda data:  (data-data.min())/ (data.max() - data.min())

        tabla_ubicaciones["lat"]= normalizar(tabla_ubicaciones["lat"])
        tabla_ubicaciones["lng"] = normalizar(tabla_ubicaciones["lng"])


        # latitudes representan el eje x (eje horizontal)     
        # estaran definidos dentro del rango: 
        # ['self.MARGEN_PANEL'  ,  'self.ANCHO_PANEL'-'self.MARGEN_PANEL']
        latitudes_adapatadas=(  tabla_ubicaciones["lat"]*(self.ANCHO_PANEL-2*self.MARGEN_PANEL) ) +self.MARGEN_PANEL
        
        # logitudes representan el eje y (eje vertical) 
        # estaran definidos dentro del rango: 
        # ['self.MARGEN_PANEL'  ,  'self.ALTO_PANEL'-'self.MARGEN_PANEL']
        longitudes_adaptadas= ( tabla_ubicaciones["lng"]*(self.ALTO_PANEL-2*self.MARGEN_PANEL) )+self.MARGEN_PANEL

        # graficando los puntos 
        self.dict_puntos={}
        for nombre,x,y in zip(tabla_ubicaciones.nombre, latitudes_adapatadas,longitudes_adaptadas ):
            punto_estacion_red=BotonCoordenada(
                nombre=nombre,
                boton=QPushButton("",self.panel_mapa),
                funcion=lambda nombre_x : self.senal_clic_punto_mapa.emit(nombre_x)   
            )

            # fijando el boton en la coordenada respectiva
            punto_estacion_red.boton.move(int(x),int(y))
            
            # estableciendo un tamaño fijo al boton
            punto_estacion_red.boton.resize(15,15)
            
            # guardando boton en diccionario
            self.dict_puntos[nombre]=punto_estacion_red



if __name__ == "__main__":        
    # creando aplicacion pyqt5
    App = QApplication(sys.argv)
    window = MapaInteractivoCompleto()
    # inciando aplicacion de escritorio
    sys.exit(App.exec())