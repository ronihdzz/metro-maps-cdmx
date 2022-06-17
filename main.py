#! /usr/bin/env python3


from pickle import MEMOIZE
import sys


from PyQt5.QtWidgets import  QApplication,QMessageBox,QCompleter
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


import os
import pandas as pd


from GUI.DISENO.main_dise import Ui_Form
from recursos import HuellaAplicacion,App_Principal
from GUI.LOGICA.mapa_interactivo_completo import MapaInteractivoCompleto
from GUI.LOGICA.datosCreador import Dialog_datosCreador
from GUI.LOGICA import cliente_metro
import recursos
import pygame  

file_separacion_estaciones="procesamiento_datos\datos\procesados\estaciones_separacion.xlsx"

RUTA_IMGENES_METRO="estaciones_metro/multimedia/imagenes/estaciones_metro/todas/"



#self.bel_estadoVenti.setStyleSheet("image: url(:/estaciones_metro/multimedia/imagenes/estaciones_metro/todas/sanlazaro.png);")


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
        self.stack_panel_metro.addWidget(self.area)
        
        self.stack_panel_metro.setSizePolicy(
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
        self.area.panel.senal_punto_clic.connect(self.mostrar_estacion_clic)


        self.ventana_datos_creador=Dialog_datosCreador()
        self.btn_info.clicked.connect(lambda : self.ventana_datos_creador.show() )



        pygame.init()



        self.show()
    
    def mostrar_estacion_clic(self,nombre_estacion):
        print(nombre_estacion)
    
        imagen=RUTA_IMGENES_METRO+nombre_estacion+".png"
        self.bel_estacion_clic.setStyleSheet(f"image: url(:/{imagen});")


        if self.rb_con_sonido.isChecked():
            carpeta=recursos.App_Principal.CARPETA_AUDIOS_ESTACIONES
            sonido=carpeta+nombre_estacion+".mp3"

            pygame.mixer.init() 
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.load( sonido  )
            pygame.mixer.music.play()   



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

                #respuesta=SERVIDOR.get_ruta_mas_cercana(origen=nombre_origen,destino=nombre_destino)
                respuesta=cliente_metro.consultar_servidor(origen=nombre_origen,destino=nombre_destino)
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
                
                # cargando ruta en combo box
                self.cmb__box_ruta.clear()
                self.cmb__box_ruta.addItems(ruta_seguir)

                self.bel_dst_ruta.setText(str(distancia_recorrer))
                self.bel_no_estaciones.setText( str(no_estaciones_ruta) )

                ventanaDialogo.setText(mensaje)
                ventanaDialogo.setStandardButtons(QMessageBox.Ok)
                btn_ok = ventanaDialogo.button(QMessageBox.Ok)
                btn_ok.setText('Entendido')
                ventanaDialogo.exec_()

                self.area.colorear_ruta_seguir(nombre_estaciones=ruta_seguir)


                if self.rb_con_sonido.isChecked():
                    self.reproducir_en_voz_ruta(ruta=ruta_seguir)

    def reproducir_en_voz_ruta(self,ruta):
        
        carpeta=recursos.App_Principal.CARPETA_AUDIOS_ESTACIONES


        lista_sonidos=[]


        lista_sonidos.append( recursos.App_Principal.FRASE_INICIO  )

        #MIXER.init()
        #MIXER.music.load( recursos.App_Principal.FRASE_INICIO  )

        for n,estacion in enumerate(ruta):
            sonido=carpeta+estacion+".mp3"

            lista_sonidos.append(sonido)
            # MIXER.music.load( sonido  )

            if not estacion==ruta[-1]:
                lista_sonidos.append( recursos.App_Principal.FRASE_INTERMEDIA   )
                #MIXER.music.load( recursos.App_Principal.FRASE_INTERMEDIA  )
        
        self.start_playlist(lista_sonidos)


    def insert_into_playlist(self,playlist, music_file):
        
        # Adding songs file in our playlist
        playlist.append(music_file)
    
    
    def start_playlist(self,playList):
        
        # Loading first audio file into our player
        pygame.mixer.music.load(playList[0])
        
        # Removing the loaded song from our playlist list
        playList.pop(0)
    
        # Playing our music
        pygame.mixer.music.play()
    
        # Queueing next song into our player
        pygame.mixer.music.queue(playList[0])
        playList.pop(0)
    
        # setting up an end event which host an event
        # after the end of every song
        pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
    
        # Playing the songs in the background
        running = True
        while running:
            
            # checking if any event has been
            # hosted at time of playing
            for event in pygame.event.get():
                
                # A event will be hosted
                # after the end of every song
                if event.type ==  pygame.USEREVENT+1:
                    print('Song Finished')
                    
                    # Checking our playList
                    # that if any song exist or
                    # it is empty
                    if len(playList) > 0:
                        
                        # if song available then load it in player
                        # and remove from the player
                        pygame.mixer.music.queue(playList[0])
                        playList.pop(0)
    
                # Checking whether the 
                # player is still playing any song
                # if yes it will return true and false otherwise
                if not pygame.mixer.music.get_busy():
                    print("Playlist completed")
                    
                    # When the playlist has
                    # completed playing successfully
                    # we'll go out of the
                    # while-loop by using break
                    running = False
                    break
    







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

            nombre_estacion=self.lista_nombres_estaciones[index]
            imagen=RUTA_IMGENES_METRO+nombre_estacion+".png"
            self.bel_estacion_origen.setStyleSheet(f"image: url(:/{imagen});")
            print("Imagen: ",imagen)



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
            nombre_estacion=self.lista_nombres_estaciones[index]
            imagen=RUTA_IMGENES_METRO+nombre_estacion+".png"
            self.bel_estacion_destino.setStyleSheet(f"image: url(:/{imagen});")
            print("Imagen: ",imagen)



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

    #print("Nombre completo del programa que se esta ejecutando: ",sys.argv)
    direccionTotal=sys.argv[0]

    direccionPartes=os.path.normpath(direccionTotal)
    direccionPartes=direccionPartes.split(os.sep)
    ruta_direccionTotal = os.sep.join( direccionPartes[:-1] )
    if len(direccionPartes)>1:
        ruta_direccionTotal+=os.sep
    #print("dirreccionPartes:",direccionPartes)
    #print("ruta total: ",ruta_direccionTotal)
    #ubicacionPrograma=direccionTotal[ :direccionTotal.find("mainFast.py") ]

    recursos.App_Principal.actualizarUbicaciones(ubicacion=ruta_direccionTotal)

    # crear aplicacion
    App = QApplication(sys.argv)
    window = Proyecto()
    # iniciado app
    sys.exit(App.exec())

