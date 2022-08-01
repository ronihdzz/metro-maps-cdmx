import sys


from PyQt5.QtWidgets import  QApplication,QMessageBox,QCompleter,QComboBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt,pyqtSignal,QObject
from PyQt5.QtGui import QIcon

import pandas as pd


from GUI.DISENO.main_dise import Ui_Form
from recursos import HuellaAplicacion,App_Principal

from GUI.LOGICA.utils import ListaInteractivaNombres,ListaReproduccion
from GUI.LOGICA.mapa_interactivo_completo import MapaInteractivoCompleto
from GUI.LOGICA.datosCreador import Dialog_datosCreador
from GUI.LOGICA import cliente_metro

import recursos


class MetroMaps(QtWidgets.QWidget, Ui_Form,HuellaAplicacion):

    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        HuellaAplicacion.__init__(self)

        ANCHO_PANEL=2000
        ALTO_PANEL=800
        MARGEN_PANEL=20


        self.reproductora_sonidos=ListaReproduccion()


        self.mapa_red_metro_cdmx=MapaInteractivoCompleto(
            file_lat_long_red=recursos.App_Principal.ARCHIVO_UBICACIONES_ESTACIONES,
            ancho=ANCHO_PANEL,
            alto=ALTO_PANEL,
            margen=MARGEN_PANEL
        )
        self.mapa_red_metro_cdmx.senal_clic_punto_mapa.connect(self.mostrar_estacion_clic)

        self.stack_panel_metro.addWidget(self.mapa_red_metro_cdmx)        
        self.stack_panel_metro.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )




        lista_nombres_estaciones=self.get_nombres_estaciones()

        # lista de estaciones origen
        self.lista_interactiva_estaciones_origen=ListaInteractivaNombres(
            lista_nombres_validos=lista_nombres_estaciones,
            cmb_box_mostrador_lista=self.cmb_box_origen
        )
        self.lista_interactiva_estaciones_origen.senal_cambio_nombre.connect(self.registrar_estacion_origen)


        # lista de estaciones destino
        self.lista_interactiva_estaciones_destino=ListaInteractivaNombres(
            lista_nombres_validos=lista_nombres_estaciones,
            cmb_box_mostrador_lista=self.cmb_box_destino
        )
        self.lista_interactiva_estaciones_destino.senal_cambio_nombre.connect(self.registrar_estacion_destino)


        # boton para ver ruta mas cercana
        self.btn_buscar.clicked.connect(self.obtener_ruta_mas_cercana)

        # boton para ver datos de creador del sofware
        self.ventana_datos_creador=Dialog_datosCreador()
        self.btn_info.clicked.connect(lambda : self.ventana_datos_creador.show() )


        self.show()


    def mostrar_estacion_clic(self,nombre_estacion):
        print(nombre_estacion)
    
        imagen=recursos.App_Principal.RUTA_IMAGENES_METRO+nombre_estacion+".png"
        self.bel_estacion_clic.setStyleSheet(f"image: url(:/{imagen});")

        if self.rb_con_sonido.isChecked():
            sonido_nombre_completo=recursos.App_Principal.CARPETA_AUDIOS_ESTACIONES+nombre_estacion+".mp3"
            self.reproductora_sonidos.reproducir_un_sonido(nombre_sonido=sonido_nombre_completo)


    def obtener_ruta_mas_cercana(self):

        nombre_origen=self.lista_interactiva_estaciones_origen.get_nombre_seleccionado()
        nombre_destino=self.lista_interactiva_estaciones_destino.get_nombre_seleccionado()
        
        if nombre_destino and nombre_origen:
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

                self.mapa_red_metro_cdmx.destacar_puntos_mapa(lista_nombres_puntos=ruta_seguir)

                if self.rb_con_sonido.isChecked():
                    self.reproducir_en_voz_ruta(ruta_estaciones=ruta_seguir)

    def reproducir_en_voz_ruta(self,ruta_estaciones):

        self.reproductora_sonidos.borrar_lista_sonidos()
        
        self.reproductora_sonidos.agregar_sonido( nombre_sonido=recursos.App_Principal.FRASE_INICIO  )
        
        for nombre_estacion in ruta_estaciones:
            sonido_nombre_completo=recursos.App_Principal.CARPETA_AUDIOS_ESTACIONES+nombre_estacion+".mp3"
            self.reproductora_sonidos.agregar_sonido(nombre_sonido=sonido_nombre_completo)
        
            if nombre_estacion!=ruta_estaciones[-1]:
                self.reproductora_sonidos.agregar_sonido( nombre_sonido=recursos.App_Principal.FRASE_INTERMEDIA )
               
        self.reproductora_sonidos.reproducir_lista_sonidos()


    def registrar_estacion_origen(self,lista_datos):
        '''
        Parámetros:
            lista_datos:
                elemento 1: Numero de indice seleccionado
                elemento 2: Nombre del elemento de la lista seleccionado
        '''
        _,nombre_estacion=lista_datos
        imagen=recursos.App_Principal.RUTA_IMAGENES_METRO+nombre_estacion+".png"
        self.bel_estacion_origen.setStyleSheet(f"image: url(:/{imagen});")
       
       
    def registrar_estacion_destino(self,lista_datos):
        '''
        Parámetros:
            lista_datos:
                elemento 1: Numero de indice seleccionado
                elemento 2: Nombre del elemento de la lista seleccionado
        '''
        _,nombre_estacion=lista_datos
        imagen=recursos.App_Principal.RUTA_IMAGENES_METRO+nombre_estacion+".png"
        self.bel_estacion_destino.setStyleSheet(f"image: url(:/{imagen});")


    def get_nombres_estaciones(self):
        '''
        Leera el archivo que contiene las latitudes,longitudes y nombres de 
        todas las lineas del metro.
        Normalizara todas las latitudes y longitudes del archivo
        Creara la variable de instancia: 'self.tabla_ubicaciones' que contendra
        la informacion mencionada anteriormente
        '''

        # columnas: name        lat      lng
        tabla_ubicaciones=pd.read_excel(recursos.App_Principal.ARCHIVO_UBICACIONES_ESTACIONES)
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
            sys.exit()
        else:
            event.ignore()  # No saldremos del evento


if __name__ == "__main__":        

    # crear aplicacion
    App = QApplication(sys.argv)
    window = MetroMaps()
    # iniciado app
    sys.exit(App.exec())

