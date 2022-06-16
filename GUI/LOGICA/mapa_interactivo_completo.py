
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QScrollArea,QGridLayout
from PyQt5.Qt import Qt
import sys


###############################################################
#  MIS LIBRERIAS...
##############################################################
from .mapa_interactivo import MapaInteractivo 
from recursos import HuellaAplicacion



class MapaInteractivoCompleto(QMainWindow,HuellaAplicacion):

    def __init__(self):
        QMainWindow.__init__(self)
        HuellaAplicacion.__init__(self)

        ancho=1000
        alto=600

        self.setGeometry(60, 60,ancho,alto)
        self.crear_pantallaMostradora()
        
        self.panel=MapaInteractivo(
                    ancho=1500*1.5,
                    alto=700*1.5,
                    margen=20,
                    file_ubicaciones="procesamiento_datos/datos/procesados/estaciones_ubicacion_2.xlsx"
        )
        self.vbox.addWidget(self.panel)

        self.show()

    def colorear_ruta_seguir(self,nombre_estaciones):
        self.panel.colorear_ruta_seguir(nombre_estaciones=nombre_estaciones)


    def crear_pantallaMostradora(self):
        '''
        Creara 3 atributos de instancia cuyo objetivo sera mostrar los 'itemDeber' que el usuario vaya
        creando y en dado caso que el espacio ya no alcance para mostrarlos todos  'itemDeber', debera 
        aparecer una barra lateral que permitira visualizar todos los 'itemDeber'.Los 3 atributos de instancia
        trabajan en conjunto para cumplir lo mencionado anteriormente.Los atributos de instancia que se
        crearan son los siguientes:
            A) Nombre: self.scroll  ¿que es? un objeto de la clase QScrollArea()
            B) Nombre: self.widget  ¿que es? un objeto de la clase QWidget()
            C) Nombre: self.vbox    ¿que es? un objeto de la clase QVBoxLayout() 
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
        """) #sin borde

        self.widget = QWidget()    # Widget que contendra al 'QVBoxLayout'
        self.vbox = QGridLayout()  # El 'QVBoxLayout' que almacenara todos los 'itemDeber' que el usuario cree
                
        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)



if __name__ == "__main__":        
    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = MapaInteractivoCompleto()

    # start the app
    sys.exit(App.exec())