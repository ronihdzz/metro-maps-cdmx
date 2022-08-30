from PyQt5.QtWidgets import  QMessageBox,QCompleter,QComboBox
from PyQt5.QtCore import Qt,pyqtSignal,QObject
from PyQt5.QtGui import QIcon
from recursos import HuellaAplicacion
import pygame


class ListaInteractivaNombres(HuellaAplicacion):
    senal_cambio_nombre = pyqtSignal(str)
    
    def __init__(self,lista_nombres_validos:list,cmb_box_mostrador_lista:QComboBox):
        QObject.__init__(self)
        HuellaAplicacion.__init__(self,is_windows=False)

        self.cmb_box=cmb_box_mostrador_lista
        self.cmb_box.setEditable(True)
        self.cargar_lista_nombres(lista_nombres=lista_nombres_validos)
        self.cmb_box.currentIndexChanged.connect( lambda index_select:self.validar_nombre_elegido(index_select) )

    def cargar_lista_nombres(self,lista_nombres):

        self.lista_nombres_validos=lista_nombres
        self.no_elementos_lista=len(self.lista_nombres_validos)
        
        # borrando todos los items del QComboBox que muestra los nombres de la lista
        self.cmb_box.clear()
        
        acompletador=QCompleter(self.lista_nombres_validos)
        acompletador.setCaseSensitivity(Qt.CaseInsensitive)
        self.index_lista_seleccionado = -1
        self.cmb_box.addItems(self.lista_nombres_validos)
        self.cmb_box.setCompleter(acompletador)


    def validar_nombre_elegido(self,index):

        if index>=self.no_elementos_lista:
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Critical)
            ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)
            mensaje=(
                    "No existe un elemento en la lista cuyo \n"
                    f"valor sea:'{self.cmb_box.currentText()}' " 
                    )
            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()
            self.cmb_box.removeItem(index)

        elif self.index_lista_seleccionado!=index:
            self.index_lista_seleccionado=index
            nombre_elemento_lista_selec=self.lista_nombres_validos[index]
            self.senal_cambio_nombre.emit( nombre_elemento_lista_selec )

    def get_nombre_seleccionado(self)->str:
        if self.index_lista_seleccionado>-1:
            return self.lista_nombres_validos[self.index_lista_seleccionado]


class ListaReproduccion():
    pygame.init()
    pygame.mixer.init() 
    pygame.mixer.music.set_volume(1)


    def __init__(self):
        self.lista_nombres_sonidos=[]
        self.numero_sonidos=0
    
    def cargar_lista_sonidos(self,lista_nombres_sonidos):
        self.lista_nombres_sonidos=lista_nombres_sonidos
        self.numero_sonidos=len(self.lista_nombres_sonidos)
    
    def borrar_lista_sonidos(self):
        self.lista_nombres_sonidos=[]
        self.numero_sonidos=0
    

    def reproducir_un_sonido(self,nombre_sonido):

        pygame.mixer.music.load( nombre_sonido  )
        pygame.mixer.music.play()   

    def agregar_sonido(self,nombre_sonido):
        self.lista_nombres_sonidos.append(nombre_sonido)
        self.numero_sonidos+=1

    def reproducir_lista_sonidos(self):
        if self.numero_sonidos>1:
            playList=self.lista_nombres_sonidos
            
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
