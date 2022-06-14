#! /usr/bin/env python3


import sys


from PyQt5.QtWidgets import  QApplication,QMessageBox,QCompleter
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


import datetime
import os
import pandas as pd


from GUI.DISENO.main_dise import Ui_Form
from recursos import HuellaAplicacion,App_Principal
from GUI.LOGICA.mapa_interactivo_completo import MapaInteractivoCompleto


from servidor_networkx.servidor_red_metro import Servidor


file_separacion_estaciones="procesamiento_datos\datos\procesados\estaciones_separacion.xlsx"

SERVIDOR=Servidor(file_separacion_estaciones=file_separacion_estaciones)


class Proyecto(QtWidgets.QWidget, Ui_Form,HuellaAplicacion):
    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        HuellaAplicacion.__init__(self)

        MARGEN=50
        ANCHO_PANTALLA=980
        ALTO_PANTALLA=530

    
        self.file_ubicaciones= "procesamiento_datos/datos/procesados/estaciones_ubicacion_2.xlsx"
        
        # setting  the geometry of window
        self.setGeometry(60, 60,ANCHO_PANTALLA,ALTO_PANTALLA)

        self.area=MapaInteractivoCompleto()
        self.stack_notas.addWidget(self.area)
        
        self.stack_notas.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        #self.btn_recargar.clicked.connect(lambda : self.area.recargar_mapa() )

        # show all the widgets

        self.lista_nombres_estaciones=self.get_nombres_estaciones()
        self.no_estaciones=len(self.lista_nombres_estaciones)



        # acompletador de las estaciones de metro

        # origen...
        acompletador=QCompleter(self.lista_nombres_estaciones)
        acompletador.setCaseSensitivity(Qt.CaseInsensitive)
        self.indice_estacion_origen = -1
        self.cmb_box_origen.setEditable(True)
        self.cmb_box_origen.addItems(self.lista_nombres_estaciones)
        self.cmb_box_origen.setCompleter(acompletador)
        self.cmb_box_origen.currentIndexChanged.connect(self.registrar_origen)


        # destino...
        acompletador_2=QCompleter(self.lista_nombres_estaciones)
        acompletador_2.setCaseSensitivity(Qt.CaseInsensitive)
        self.indice_estacion_destino = -1
        self.cmb_box_destino.setEditable(True)
        self.cmb_box_destino.addItems(self.lista_nombres_estaciones)
        self.cmb_box_destino.setCompleter(acompletador_2)        
        self.cmb_box_destino.currentIndexChanged.connect(self.registrar_destino)


        # botones de accion...
        self.btn_buscar.clicked.connect(self.obtener_ruta_mas_cercana)



        self.show()

    def obtener_ruta_mas_cercana(self):
        if self.indice_estacion_destino>0 and self.indice_estacion_origen>0:

            nombre_origen=self.lista_nombres_estaciones[self.indice_estacion_origen]
            nombre_destino=self.lista_nombres_estaciones[self.indice_estacion_destino]

            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Question)
            ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            mensaje=(
                    "Antes de iniciar la consulta por favor confirmma que\n"
                    "los siguientes datos son correctos:\n"
                    f" * Estacion origen: {nombre_origen}\n"
                    f" * Estacion destino: {nombre_destino}\n"
                    "¿son correctos los datos?"
                    )

            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            btn_yes = ventanaDialogo.button(QMessageBox.Yes)
            btn_yes.setText('Si')
            btn_no = ventanaDialogo.button(QMessageBox.No)
            btn_no.setText('No')
            ventanaDialogo.exec_()
            if ventanaDialogo.clickedButton()  ==  btn_yes:

                respuesta=SERVIDOR.get_ruta_mas_cercana(origen=nombre_origen,destino=nombre_destino)
                ruta_seguir,no_estaciones_ruta,distancia_recorrer=respuesta



                ruta_seguir_str="\n -".join(['']+ruta_seguir)
                ventanaDialogo = QMessageBox()
                ventanaDialogo.setIcon(QMessageBox.Information)
                ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
                ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)
                mensaje=(
                        f"No estaciones a recorrer: {no_estaciones_ruta}\n"
                        f"Distancia a recorrer: {distancia_recorrer} [m]\n"
                        "La ruta a seguir es la siguiente: \n"
                        f"{ruta_seguir_str}" 
                        )
                        
                ventanaDialogo.setText(mensaje)
                ventanaDialogo.setStandardButtons(QMessageBox.Ok)
                btn_ok = ventanaDialogo.button(QMessageBox.Ok)
                btn_ok.setText('Entendido')
                ventanaDialogo.exec_()

                self.area.colorear_ruta_seguir(nombre_estaciones=ruta_seguir)
                

    def registrar_origen(self,index):
        if index>=self.no_estaciones:
            
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Critical)
            ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)
            mensaje=(
                    "No existe usuario cuyo \n"
                    f"nombre sea:{self.cmb_box_origen.currentText()}" 
                    )

            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()


            self.cmb_box_origen.removeItem(index)
        elif self.indice_estacion_origen!=index:
            self.indice_estacion_origen=index
            print("Estacion del metro elegida: ",self.lista_nombres_estaciones[index])



    def registrar_destino(self,index):
        if index>=self.no_estaciones:
            
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Critical)
            ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)
            mensaje=(
                    "No existe usuario cuyo \n"
                    f"nombre sea:{self.cmb_box_destino.currentText()}" 
                    )

            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()


            self.cmb_box_destino.removeItem(index)
        elif self.indice_estacion_destino!=index:
            self.indice_estacion_destino=index
            print("Estacion del metro elegida: ",self.lista_nombres_estaciones[index])




    def get_nombres_estaciones(self):
        '''
        Leera el archivo que contiene las latitudes,longitudes y nombres de 
        todas las lineas del metro.
        Normalizara todas las latitudes y longitudes del archivo
        Creara la variable de instancia: 'self.tabla_ubicaciones' que contendra
        la informacion mencionada anteriormente
        '''


        # columnas: name        lat      lng
        tabla_ubicaciones=pd.read_excel(self.file_ubicaciones)

        lista_nombres_estaciones=[nombre for nombre in tabla_ubicaciones.nombre]

        return lista_nombres_estaciones
    

    def resizeEvent(self, event):
        '''
        Cada vez que se detecta un cambio en el tamaño del programa, se actualizaran los tamaños
        que le pertenecen al widget que muestra las alarmas y al widget que muestra los deberes,
        con la finalidad de que ambos conserven el mismo tamaño y asi NINGUNO sea mas grande que
        otro y crezcan de igual forma.
        '''

        print("Window has been resized")
        print(self.width(),self.height())
        #QtWidgets.QWidget.resizeEvent(self, event)



    def closeEvent(self,event):
        '''
        Cuando el usuario le de clic izquierdo sobre el boton de cerra el programa, el metodo
        que se llamara es este, el cual le preguntara al usuario si esta seguro de cerrar el
        programa, en caso de que su respuesta sea afirmativa se cerrara el programa.
        '''

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        ventanaDialogo.setText("¿Seguro que quieres salir?")
        ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton()  ==  btn_yes:
            event.accept()
        else:
            event.ignore()  # No saldremos del evento


if __name__ == "__main__":        
    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = Proyecto()

    # start the app
    sys.exit(App.exec())

