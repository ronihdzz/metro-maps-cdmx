from PyQt5.QtWidgets import  QDialog,QApplication
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMessageBox,QButtonGroup,QDialog)
from PyQt5.QtCore import Qt, pyqtSignal,QObject
from PyQt5.QtGui import QIcon

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from  CUERPO.DISENO.SISTEMA_CONTROL.datosCreador_dise import Ui_Dialog
###############################################################
#  MIS LIBRERIAS...
##############################################################
from recursos import HuellaAplicacion,App_datosCreador


class Dialog_datosCreador(QtWidgets.QDialog, Ui_Dialog,HuellaAplicacion):
    '''
    La finalidad de esta clase es proporcionar los contactos del programador
    asi como los accesos directos a sus redes sociales.
    '''


    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        HuellaAplicacion.__init__(self)

        nombre=App_datosCreador.NOMBRE_PROGRAMADOR

        likedin=App_datosCreador.LIKEDIN_NOMBRE
        likedin_link=App_datosCreador.LIKEDIN_LINK

        github=App_datosCreador.GITHUB_NOMBRE
        github_link=App_datosCreador.GITHUB_LINK

        repositorio=App_datosCreador.REPOSITORIO_PROYECTO_NOMBRE
        repositorio_link=App_datosCreador.REPOSITORIO_PROYECTO_LINK

        fotoProgramador=App_datosCreador.FOTO_PROGRAMADOR

        gmails=App_datosCreador.GMAILS
        subject=App_datosCreador.GMAIL_SUBJECT
        body=App_datosCreador.GMAIL_CUERPO
        

        gmail_html=f'<span style=" font-size:13px;font-family:TamilSangamMN;"><a href="mailto:{",".join(gmails)}?subject={subject}&body={body}" style="color:black;text-decoration:none;">{gmails[0]}</a></span>'
        likedin_html=f'<span style=" font-size:13px;font-family:TamilSangamMN;"><a href="{likedin_link}" style="color:black;text-decoration:none;">{likedin}</a></span>'
        github_html=f'<span style=" font-size:13px;font-family:TamilSangamMN;"><a href="{github_link}" style="color:black;text-decoration:none;">{github}</a></span>'

        self.textBrowser_repositorio.setOpenLinks(True)
        self.textBrowser_repositorio.setOpenExternalLinks(True)

        # hace que el texto pueda ser seleccionado
        #self.bel_gmail.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.textBrowser_repositorio.setHtml(f"""
            <span style=" font-size:13px;font-family: TamilSangamMN;">Repositorio de todo el proyecto</span></p>
            <span style=" font-size:13px;font-family: TamilSangamMN;"><a href="{repositorio_link}"  style="color:black;"> <b>{repositorio}<\b> </a></span>
        """)

        self.textBrowser_nombreProgra.setHtml(f"""
        <p align="center"><span style="font-size:13px; font-family:TamilSangamMN; style='text-align:center">Desarrollador</span>
        <br>
        <span style="font-size:16px;font-family: TamilSangamMN;text-align:center;"><b>{nombre}</b></span>
        </p>""")


        self.bel_fotoProgramador.setStyleSheet(f"""
                    border-image: url({fotoProgramador});
                    border-radius:87%;""")
        

        self.bel_likedin.setOpenExternalLinks(True)
        self.bel_github.setOpenExternalLinks(True)
        self.bel_gmail.setOpenExternalLinks(True)

        self.bel_likedin.setText(likedin_html)
        self.bel_github.setText(github_html)
        self.bel_gmail.setText(gmail_html)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Dialog_datosCreador()
    application.show()
    app.exec()
    #sys.exit(app.exec())
