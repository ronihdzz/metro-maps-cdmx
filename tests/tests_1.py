import unittest
import matplotlib.pyplot as plt
import pandas as pd 
import os
    


FILE_UBICACION_ESTACIONES="./procesamiento_datos/datos/procesados/estaciones_ubicacion_2.xlsx"
FILE_SEPARACION_ESTACIONES="./procesamiento_datos/datos/procesados/estaciones_separacion.xlsx"
CARPETA_IMAGENES_ESTACIONES="./multimedia/imagenes/estaciones_metro/todas"

class TestSum(unittest.TestCase):
        

    def setUp(self):
        self.tabla_separacion=None
        self.lista_nombres_estaciones_by_separacion=None
        self.tabla_ubicacion=None
        file_separacion_estaciones=FILE_SEPARACION_ESTACIONES

        # origen	    destino      	longitud de interestacion
        self.tabla_separacion=pd.read_excel(file_separacion_estaciones)

        nombres_estaciones={}
        # poner nombres en minusculas y quitar acentos
        for nombre in self.tabla_separacion.origen:
            if not nombres_estaciones.get(nombre,False):
                nombres_estaciones[nombre]=True
        self.lista_nombres_estaciones_by_separacion=list(nombres_estaciones.keys())

        # columna: 'lng' 'lat'  'nombre'
        self.tabla_ubicacion=pd.read_excel(FILE_UBICACION_ESTACIONES)


        self.lista_nombres_imagenes=os.listdir(CARPETA_IMAGENES_ESTACIONES)


    def test_todas_imagenes_png(self):
        todas_estan_en_png=True
        imagenes_no_cumplen=[]
        for nombre in self.lista_nombres_imagenes:
            if not nombre.endswith('.png'):
                imagenes_no_cumplen.append(nombre)
                todas_estan_en_png=False

        self.assertTrue(
            todas_estan_en_png,
            "Toda la imagenes de las estaciones deben estar en formato png \n"
            f"se detecto que las siguientes imagenes no estan en formato png: {imagenes_no_cumplen}"
            )


    def test_nombres_columnas_tabla_separacion(self):
        nombres_columnas_esperados=('origen','destino','longitud de interestacion')
        diferencia_1=set(nombres_columnas_esperados)-set(self.tabla_separacion.columns)
        diferencia_2=set(nombres_columnas_esperados)-set(self.tabla_separacion.columns)

        numero_diferencias=len(diferencia_1)+len(diferencia_2)

        self.assertEqual(
            numero_diferencias,
            0,
            f"Los nombres de las columnas de la tabla de separacion se esperan sen:{nombres_columnas_esperados}\n"
            f"sin embargo los nombres de estas fueron: {self.tabla_separacion.columns}"
        )

    def test_nombres_columnas_tabla_ubicacion(self):
        nombres_columnas_esperados=('lng','lat','nombre')

        diferencia_1=set(nombres_columnas_esperados)-set(self.tabla_ubicacion.columns)
        diferencia_2=set(nombres_columnas_esperados)-set(self.tabla_ubicacion.columns)

        numero_diferencias=len(diferencia_1)+len(diferencia_2)

        self.assertEqual(
            numero_diferencias,
            0,
            f"Los nombres de las columnas de la tabla de separacion se esperan sen:{nombres_columnas_esperados}\n"
            f"sin embargo los nombres de estas fueron: {self.tabla_ubicacion.columns}"
        )


    def test_misma_cantidad_datos_files(self):
        no_by_file_separacion=len(self.lista_nombres_estaciones_by_separacion)
        no_by_file_ubicacion=len(self.tabla_ubicacion.nombre)
        no_by_directory_images=len(self.lista_nombres_imagenes)


        self.assertTrue(
            no_by_file_separacion==no_by_file_ubicacion==no_by_directory_images,
            msg="La cantidad de estaciones en: el archivo de separaciones,ubicaciones y en la carpeta\n"
            "de imagenes de estaciones deberia ser el mismo, sin embargo: \n"
            f"\t-archivo de separacion tiene registradas ={no_by_file_separacion}\n"
            f"\t-archivo de ubicacion tiene registradas ={no_by_file_ubicacion}\n"
            f"\t-La carpeta de imagenes tiene registradas ={no_by_directory_images}\n"
        )

    
    def test_mismos_nombres_estaciones_files(self):
        diferencia_1=set(self.tabla_ubicacion.nombre)-set( self.lista_nombres_estaciones_by_separacion )
        diferencia_2=set( self.lista_nombres_estaciones_by_separacion )-set(self.tabla_ubicacion.nombre)

        numero_diferencias=len(diferencia_1)+len(diferencia_2)

        self.assertEqual(
            numero_diferencias,
            0,
            "La tabla que contiene la distancia de separacion de estaciones no tienen las estaciones:\n"
            f"{diferencia_1} las cuales si las tiene la tabla que contiene la ubicacion de estaciones\n"
            "La tabla que conteine la ubicacion de estaciones no tiene las estaciones:\n"
            f"{diferencia_2} las cuales si las tiene la tabla que conteine la distancia de separacion de estaciones"
        )



    def test_mismos_nombres_estaciones_imagenes(self):

        # quitando el png a cada nombre de estacion
        nombres_imagenes_estaciones=[ nombre[:-4] for  nombre in self.lista_nombres_imagenes]
        
        diferencia_1=set(self.tabla_ubicacion.nombre)-set( nombres_imagenes_estaciones )
        diferencia_2=set( nombres_imagenes_estaciones )-set( self.tabla_ubicacion.nombre )

        numero_diferencias=len(diferencia_1)+len(diferencia_2)

        self.assertEqual(
            numero_diferencias,
            0,
            "La carpeta que almacena las imagenes de las estacion no tienen las estaciones:\n"
            f"{diferencia_1} las cuales si las tiene la tabla que contiene la ubicacion de estaciones\n"
            "La tabla que conteine la ubicacion de estaciones no tiene las estaciones:\n"
            f"{diferencia_2} las cuales si las tiene la carpeta que almacena las imagenes de las estaciones"
        )




if __name__ == '__main__':
    unittest.main()






