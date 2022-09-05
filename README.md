<hr>

# **Metro maps cdmx**
#### Autor: David Roni Hernández Beltrán
<hr>

<br>

Video de la explicación del proyecto en español:

[![Alt text](https://img.youtube.com/vi/uFwvX6JYM38/0.jpg)](https://www.youtube.com/watch?v=uFwvX6JYM38)


Video de la explicación del proyecto en ingles:

[![Alt text](https://img.youtube.com/vi/uFwvX6JYM38/0.jpg)](https://www.youtube.com/watch?v=uFwvX6JYM38)


## **Menu**
<hr>

* [1) Prerrequisitos](#1-prerrequisitos)
    * [1.1) Sistemas operativos](#13-sistemas-operativos)
    * [1.2) Instalación de paquetes de python](#11-instalación-de-paquetes-de-python)

<hr>

## **1) Prerrequisitos**
<div class="myWrapper" markdown="1" align="left">

[Regresar al menu principal](#menu)
</div>


<hr>


### **1.1) Sistemas operativos**
<div class="myWrapper" markdown="1" align="left">

[Regresar al menu principal](#menu)
</div>


El programa es multiplataforma por lo cual deberia minimo funcionar en: Windows,Linux y Mac.

El programa ha sido probado con exito en los siguientes sistemas operativos:

* Windows 10

Sin embargo por cuestiones de disponibilidad de equipo no ha podido ser probada en otras versiones de los sitemas operativos, sin embargo deberia funcionar en otros sistemas operativas y versiones de estos, debido a que la aplicación es multiplataforma.


### **1.2) Instalación de paquetes de python**
<div class="myWrapper" markdown="1" align="left">

[Regresar al menu principal](#menu)
</div>

A continuación se enlistan los prerrequisitos para poder ejecutar el sofware:

* Python 3 instalado en la computadora
* La herramienta de gestión de paquetes pip3


Para poder ejecutar el programa es necesario tener python 3 instalado, asi como
tambien instalar los siguientes paquetes:

* pyqt5
* pyqt5-tools
* pytest
* pandas
* openpyxl
* pygame
* networkx
* unidecode
* mutagen
* gTTS


Recomendación: Instalar los paquetes  en un **virtualenv** la cual  es una herramienta para crear entornos Python aislados, con el fin de evitar problemas  de dependencias y versiones, si desea consultar información de como instalar un entorno virtual recomiendo el siguiente link: https://docs.python.org/es/3/tutorial/venv.html

A continuación se muestra como poder instalar los paquetes antes mencionados:

### Windows/Mac
* **Alternativa numero 1:** Instalar cada paquete de forma individual

* Instalando pyqt5:

    <pre><code>pip3 install pyqt5</code></pre>


* Instalando pytest:

    <pre><code>pip3 install pytest</code></pre>


* Instalando pandas:

    <pre><code>pip3 install pandas</code></pre>

* Instalando openpyxl:

    <pre><code>pip3 install openpyxl</code></pre>

* Instalando pygame:

    <pre><code>pip3 install pygame</code></pre>

* Instalando networkx:

    <pre><code>pip3 install networkx</code></pre>


* Instalando unidecode:

    <pre><code>pip3 install unidecode</code></pre>

* Instalando mutagen:

    <pre><code>pip3 install mutagen</code></pre>


* Instalando gTTS:
    <pre><code>pip3 install gTTS</code></pre>



* **Alternativa numero 2:** Instalar todos los paquetes con ayuda del archivo **requirements.txt**

    <pre><code>pip3 install -r requirements.txt</code></pre>


### Linux

* Instalando pyqt5:

    <pre><code>sudo apt update</code></pre>
    <pre><code>sudo apt upgrade</code></pre>
    <pre><code>sudo apt install python3-pyqt5</code></pre>

* Instalando pytest:

    <pre><code>pip3 install pytest</code></pre>


* Instalando pandas:

    <pre><code>pip3 install pandas</code></pre>

* Instalando openpyxl:

    <pre><code>pip3 install openpyxl</code></pre>

* Instalando pygame:

    <pre><code>pip3 install pygame</code></pre>

* Instalando networkx:

    <pre><code>pip3 install networkx</code></pre>


* Instalando unidecode:

    <pre><code>pip3 install unidecode</code></pre>

* Instalando mutagen:

    <pre><code>pip3 install mutagen</code></pre>


* Instalando gTTS:
    <pre><code>pip3 install gTTS</code></pre>



## **2) Como ejecutar el proyecto**

Para poder ejecutar el proyecto es importante saber que:
metro maps es un proyecto conformado de dos partes:

* **El cliente**: el programa con el que interactuara la persona para obtener la ruta más cercana.
* **El servidor**: el programa que estara ejecutando una computadora y que sera el encargado de  calcular la ruta mas cercana para cada persona.

**NOTA:** El cliente y el servidor pueden ejecutarse en una misma computadora, pero lo ideal seria que se ejecutaran en una distinta computara.El programa del cliente puede ejecutarse en distintas computadoras.El programa del servidor solo se ejecutara en una computadora.

¿Como ejecutar el proyecto?

Si los scripts: cliente y servidor se ejecutaran en distintas maquinas y dichas maquinas estan conectadas a la misma red:

* **PASO 1** Cerciorarse que las computadoras que correran el programa de cliente esten conectados en la misma red de la computadora que ejecutara el programa del servidor.
* **PASO 2** Obten la direccion IPv4 de la computadora que ejecutara el programa del servidor:
    * Para obtener la direccion IPV4 en linux/mac, escribir lo siguiente en consola:

        <pre><code>ifconfig</code></pre>

    * Para obtener la direccion IPV4 en windows, escribir lo siguiente en consola:

        <pre><code>ipconfig</code></pre>

* **PASO 3** En el script **<<recursos.py>>** del proyecto:

    ```
    ├── METRO-MAPS-CDMX
    │   ├── GUI
    │   │   ├── ...
    │   │   ├── ...
    │   │   ├── ...
    │   ├── multimedia
    │   │   ├── ...
    │   │   ├── ...
    │   │   ├── ...
    │   ├── procesamiento_datos
    │   │   ├── ...
    │   │   ├── ...
    │   │   ├── ...
    │   │   ├── ...
    │   ├── tests
    │   │   ├── ...
    │   │   ├── ...
    │   │   ├── ...
    │   │   ├── ...
    │   ├── .gitignore
    │   ├── images_rc.py
    │   ├── images.qrc
    │   ├── LICENSE
    │   ├── main_cliente.py
    │   ├── main_servidor
    │   ├──    ...
    │   ├──    ...
    │   ├── recursos.py <============
    │   ├── requirements.txt
    ```

    Modicar los valores de lo señalado por las flechas:

    ```{python}
    from PyQt5 import QtCore
    from PyQt5.QtGui import QIcon


    class App_Principal():

        ###############################################
        # DATOS DEL SERVER QUE EJECUTA EL SERVICIO
        #     QUE LA  GUI  CONSUMIRA
        ###############################################

        SERVER_IP="127.0.0.1"  <===================== editar valor
        SERVER_PORT=1111       <===================== editar valor

        #################################################
        # DATOS  QUE  REQUIERE  LA  GUI
        #################################################

    ```

    ¿que valores se deben poner en las variables señaladas por las flechas?

    En la variable: **<<SERVER_IP>>** igualarla a un string que contenga la direccion IPV4 de la computadora que ejecutara el programa del servidor.

    En la variable  **<<SERVER_PORT>>** igualarlo a un dato de tipo entero que contenga el numero de puerto en el que se ejecutara el socket del servidor.Es importante recordar que los por lo general libres son los puertos en el ragno de: 1024 a 49151.


* **PASO 4** Guardar los cambios del proyecto realizados en el paso anterior.

* **PASO 5** Copiar el proyecto con los cambios realizados del paso 3, en las computadoras que ejecutaran la aplicacion de cliente y en la computadora que ejecutara la aplicacion de servidor.


* **PASO 6** En la computadora que ejecutara la aplicacion del servidor, ubicarse en la carpeta que esta almacenado el script: **<<main_servidor.py>>** y posteriormente ejecutar el siguiente comando:

    <pre><code>python main_servidor.py</code></pre>



* **PASO 7** En las computadoras que ejecutaran la aplicacion del cliente, ubicarse en la carpeta que esta almacenado el script: **<<main_cliente.py>>** y posteriormente ejecutar el siguiente comando:

    <pre><code>python main_cliente.py</code></pre>


Si los scripts: cliente y servidor se ejecutaran en la misma maquina:

* **PASO 1** Abrir una terminal en la computadora, ubicarse en la carpeta que esta almacenado el script: **<<main_servidor.py>>** y posteriormente ejecutar el siguiente comando:

    <pre><code>python main_servidor.py</code></pre>


* **PASO 2** Abrir otra terminal en la computadora, ubicarse en la carpeta que esta almacenado el script: **<<main_cliente.py>>** y posteriormente ejecutar el siguiente comando:

    <pre><code>python main_cliente.py</code></pre>


## **3) Funcionamiento del proyecto**

Funcionamiento del programa del cliente:

El programa es una GUI de escritorio pensada para que el usuario la pueda usar y obtener la ruta a seguir. Lo que tendra que hacer el usuario es lo siguiente:

¿Que debera hacer el usuario para obtener la ruta a seguir?

* Seleccionar la estacion origen
* Seleccionar la estacion destino
* Dar clic sobre el boton con la leyenda: **<<obtener>>**

Con los pasos anteriores el usuario:

* Vera los nombres de las estaciones de la ruta a seguir


* Vera la cantidad de estaciones a recorrer:


* Vera la distancia total a reccorer:


* Vera la ruta a seguir marcada en el mapa de puntos



Si el usuario desea escuchar en audio la ruta a seguir
debera hacer lo siguiente:

* Seleccionar la estacion origen si no se ha seleccionado
* Seleccionar la estacion destino si no se ha seleccionado
* Cersiorarse que este habilitado el sonido y si no esta habilitado
habilitarlo, dando clic izquierdo sobre el circulo que tiene en la
parte inferior la leyenda: **<<Con sonido>>**
* Dar clic sobre el boton con la leyenda: **<<obtener>>**


El usuario puede explorar cada punto del mapa y ver que estacion de
metro representa dando clic izquierdo sobre el punto respectivo.Cuando
el usuario de clic sobre el punto respectivo, vera en la parte superior
izquierda de la GUI la imagen de la estacion del metro que representa dicho punto



NOTA: Si el usuario tiene habilitado el sonido, entonces cada vez que de clic sobre un punto
del mapa tambien escuchara en audio el nombre de la estacion del metro que representa dicho punto.


El usuario podra  ver los contactos del desarrollador de este proyecto:


La aplicacion de cliente metro-maps-cdmx ofrece un apartado en donde el usuario pueda ver los contactos del programador, es decir mis datos de contacto personales, tambien muestra un link de acceso al repositorio de todo este proyecto, lo único que se tendrá que hacer es dar clic izquierdo sobre el icono con signo de exclamación e inmediatamente se desplegara una ventana con dichos datos.

A continuación de muestra como:




Funcionamiento del programa del servidor:

Este programa mostrara en consola los datos(direccion IP, puerto, nombre estacion origen, nombre estacion destino,etc. ) de cada cliente que desea obtener la ruta mas cercana entre su estacion origen y estacion destino.


## **4) Ejecutar los tests**
<div class="myWrapper" markdown="1" align="left">

Debido a que todos los audios, imagenes y archivos que contienen informacion de cada estacion del metro se creo el siguiente tests que se encarga de verificar que todos los audios imagenes y archivos contengan los mismos nombres de estaciones de metro y la misma cantidad de estaciones de metro.

Para ejecutar los tests debera ubicarse a la altura del **<<main_gui.py>>**  y a la altura del **<<main_server.py>>** y ejecutar el siguiente comando:

<pre><code>pytest tests</code></pre>

## Agregar nuevo codigo

Si deseas contribuir al proyecto no olvidar pre-formatear tu codigo con ayuda de pre-commit:}

<pre><code>pre-commit install</code></pre>

<pre><code>pre-commit run --all-files</code></pre>

<pre><code>git commit -m "blablabla" --no-verify</code></pre>


## **5) Fuentes de informacion**

* Imagenes de las estaciones del metro: https://metro.cdmx.gob.mx/la-red/linea-1

* Latitudes y longitudes del metro: https://datos.cdmx.gob.mx/gl/dataset/lineas-y-estaciones-del-metro/resource/0869e0dd-6876-4446-a199-8f670a359c00

* Distancias entre cada estación del metro: https://github.com/IgorEM/Melhor-Rota---Metro-da-cidade-do-Mexico---Dijkstra-/blob/main/183arestasOrigDestPesoVirgulasSemEspacoNaoDirecional.txt

* Script reproductor de listas de audio: https://stackoverflow.com/questions/58630700/utilising-the-pygame-mixer-music-get-endevent
