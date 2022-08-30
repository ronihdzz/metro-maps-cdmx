import sys

from PyQt5.QtWidgets import  QApplication,QMessageBox,QCompleter,QComboBox
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

import pandas as pd


from GUI.DISENO.main_dise import Ui_Form
from recursos import HuellaAplicacion

from GUI.LOGICA.utils import ListaInteractivaNombres,ListaReproduccion
from GUI.LOGICA.mapa_interactivo_completo import MapaInteractivoCompleto
from GUI.LOGICA.datosCreador import Dialog_datosCreador
from GUI.LOGICA.socket_client import ClientSocket


class MetroMaps(QtWidgets.QWidget, Ui_Form,HuellaAplicacion):

    def __init__(self,socket_client:ClientSocket,archivo_ubicaciones_estaciones:str,carpeta_imagenes_estaciones:str,carpeta_audios_estaciones:str,audio_frase_inicio:str,audio_frase_intermedia:str,
    ancho_panel:int=2000,alto_panel:int=800,margen_panel:int=20):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        HuellaAplicacion.__init__(self)

        
        self.socket_client=socket_client
        self.archivo_ubicaciones_estaciones=archivo_ubicaciones_estaciones
        self.carpeta_imagenes_estaciones=carpeta_imagenes_estaciones
        self.carpeta_audios_estaciones=carpeta_audios_estaciones
        self.audio_frase_inicio=audio_frase_inicio
        self.audio_frase_intermedia=audio_frase_intermedia

        self.reproductora_sonidos=ListaReproduccion()
        self.ventana_datos_creador=Dialog_datosCreador()

        ###############################################################################
        # CREANDO EL PANEL INTERACTIVO DE LAS ESTACIONES DEL METRO
        ###############################################################################

        # creando el objeto panel donde se representara con puntos cada estacion del metro
        self.mapa_red_metro_cdmx=MapaInteractivoCompleto(
            file_lat_long_red=self.archivo_ubicaciones_estaciones,
            ancho=ancho_panel,
            alto=alto_panel,
            margen=margen_panel
        )
        
        # incrustando el objeto panel en un lugar visible
        self.stack_panel_metro.addWidget(self.mapa_red_metro_cdmx)        
        self.stack_panel_metro.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )


        ###############################################################################
        # CREANDO LISTAS INTERACTIVAS DE ESTACIONES DEL METRO
        ###############################################################################

        lista_nombres_estaciones=self.get_nombres_estaciones()

        # creando lista interactiva de estaciones origen
        self.lista_interactiva_estaciones_origen=ListaInteractivaNombres(
            lista_nombres_validos=lista_nombres_estaciones,
            cmb_box_mostrador_lista=self.cmb_box_origen
        )
        
        # creando lista interactiva de estaciones destino
        self.lista_interactiva_estaciones_destino=ListaInteractivaNombres(
            lista_nombres_validos=lista_nombres_estaciones,
            cmb_box_mostrador_lista=self.cmb_box_destino
        )

        ###############################################################################
        # CONECTANDO LAS SEÑALES DE CADA OBJETO
        ###############################################################################

        self.mapa_red_metro_cdmx.senal_clic_punto_mapa.connect(self.mostrar_imagen_estacion_clic)
        self.lista_interactiva_estaciones_origen.senal_cambio_nombre.connect(self.mostrar_imagen_estacion_origen)
        self.lista_interactiva_estaciones_destino.senal_cambio_nombre.connect(self.mostrar_imagen_estacion_destino)
        self.btn_buscar.clicked.connect(self.obtener_ruta_mas_cercana)
        self.btn_info.clicked.connect(lambda : self.ventana_datos_creador.show() )


        self.show()


    def mostrar_imagen_estacion_clic(self,nombre_estacion):
        '''
        - En la Qlabel donde se muestra la imagen de la estacion a la que el usuario le de clic
        izquierdo en el mapa, este metodo  cargara la imagen de la estacion cuyo nombre es el 
        representado por el parametro:'nombre_estacion'
        - Si el audio esta habilitado se reproducira en audio el nombre de la estacion a la
        que se le dio clic izquierdo en el mapa. 
        '''

        imagen=self.carpeta_imagenes_estaciones+nombre_estacion+".png"
        self.bel_estacion_clic.setStyleSheet(f"image: url(:/{imagen});")

        if self.rb_con_sonido.isChecked():
            sonido_nombre_completo=self.carpeta_audios_estaciones+nombre_estacion+".mp3"
            self.reproductora_sonidos.reproducir_un_sonido(nombre_sonido=sonido_nombre_completo)


    def obtener_ruta_mas_cercana(self)->None:
        '''
        - Obtendra los nombres seleccionados como estacion origen, estacion destino.
        - Posteriormente por medio de un client socket hara una peticion al servidor
        para obtener la ruta mas corta a seguir entre la estacion origen y estacion
        destino.
        - Una vez obtenida la ruta a seguir entre la estacion origen y estacion
        destino proseguira a mostrar la ruta a seguir en el mapa,  asi como reproducir
        en audio la ruta a seguir si el audio esta habilitado. 
        '''

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

                respuesta=self.socket_client.get_server_para_obtener_ruta(
                    nombre_estacion_origen=nombre_origen,
                    nombre_estacion_destino=nombre_destino
                )
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

                # mostrando los datos de la ruta a seguir en los labels respectivos
                self.bel_dst_ruta.setText(str(distancia_recorrer))
                self.bel_no_estaciones.setText( str(no_estaciones_ruta) )

                ventanaDialogo.setText(mensaje)
                ventanaDialogo.setStandardButtons(QMessageBox.Ok)
                btn_ok = ventanaDialogo.button(QMessageBox.Ok)
                btn_ok.setText('Entendido')
                ventanaDialogo.exec_()

                # mostrando la ruta a seguir en el mapa
                self.mapa_red_metro_cdmx.destacar_puntos_mapa(lista_nombres_puntos=ruta_seguir)

                # si esta habilitado el sonido se reproducira la ruta a seguir en audio
                if self.rb_con_sonido.isChecked():
                    self.reproducir_en_voz_ruta(ruta_estaciones=ruta_seguir)

    def reproducir_en_voz_ruta(self,ruta_estaciones:list)->None:
        '''
        Reproducira en audio la ruta de estaciones que debera seguir el usuario para
        llegar a la estacion destino partiendo de la estacion origen.
        Parametros:
            ruta_estaciones: Representa la lista de los nombres de las estaciones
            que conforman la ruta que debera seguir el usuario para llegar de la
            estacion origen a la estacion destino   
        '''

        self.reproductora_sonidos.borrar_lista_sonidos()
        self.reproductora_sonidos.agregar_sonido( nombre_sonido=self.audio_frase_inicio  )
        
        for nombre_estacion in ruta_estaciones:
            sonido_nombre_completo=self.carpeta_audios_estaciones+nombre_estacion+".mp3"
            self.reproductora_sonidos.agregar_sonido(nombre_sonido=sonido_nombre_completo)
            if nombre_estacion!=ruta_estaciones[-1]:
                self.reproductora_sonidos.agregar_sonido( nombre_sonido=self.audio_frase_intermedia )

        self.reproductora_sonidos.reproducir_lista_sonidos()


    def mostrar_imagen_estacion_origen(self,nombre_estacion:str)->None:
        '''
        En la Qlabel donde se muestra la imagen de la estacion origen, cargara
        la imagen de la estacion cuyo nombre es el representado por el parametro:
        'nombre_estacion'.
        '''

        imagen=self.carpeta_imagenes_estaciones+nombre_estacion+".png"
        self.bel_estacion_origen.setStyleSheet(f"image: url(:/{imagen});")
       
       
    def mostrar_imagen_estacion_destino(self,nombre_estacion:str)->None:
        '''
        En la Qlabel donde se muestra la imagen de la estacion destino, cargara
        la imagen de la estacion cuyo nombre es el representado por el parametro:
        'nombre_estacion'.
        '''
        imagen=self.carpeta_imagenes_estaciones+nombre_estacion+".png"
        self.bel_estacion_destino.setStyleSheet(f"image: url(:/{imagen});")


    def get_nombres_estaciones(self)->list:
        '''
        Del archivo representado por el atributo de instancia: 'self.archivo_ubicaciones_estaciones'
        obtendra todos los nombres de las estaciones del metro CDMX, posteriormente los almacenara
        en una lista y retornara dicha lista
        Returns:
            Lista de todos los nombres de las estaciones del metro de la CDMX
        '''

        # columnas del archivo: 'name'    'lat'    'lng'
        tabla_ubicaciones=pd.read_excel(self.archivo_ubicaciones_estaciones)
        lista_nombres_estaciones=[nombre for nombre in tabla_ubicaciones.nombre]
        return lista_nombres_estaciones
    

    def closeEvent(self,event):
        '''
        Cuando el usuario le de clic izquierdo sobre el boton de cerrar el programa, el metodo
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

