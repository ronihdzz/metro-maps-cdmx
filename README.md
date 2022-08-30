<hr>

# **Metro maps cdmx**
#### Autor: David Roni Hernández Beltrán
<hr>

<br><br>

Explicación del proyecto en español:

[![Alt text](https://img.youtube.com/vi/uFwvX6JYM38/0.jpg)](https://www.youtube.com/watch?v=uFwvX6JYM38)


Explicación del proyecto en ingles:

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


## **2) Funcionamiento**


## **3) Ejecutar los tests**
<div class="myWrapper" markdown="1" align="left">

Para ejecutar los tests debera ubicarse a la altura del main_gui.py 
y a la altura del main_server.py y ejecutar el siguiente comando:

<pre><code>pytest tests</code></pre>


## **4) Fuentes de informacion**

* Imagenes de las estaciones del metro: https://metro.cdmx.gob.mx/la-red/linea-1

* Latitudes y longitudes del metro: https://datos.cdmx.gob.mx/gl/dataset/lineas-y-estaciones-del-metro/resource/0869e0dd-6876-4446-a199-8f670a359c00


* Distancias entre cada estación del metro: 
    * https://github.com/IgorEM/Melhor-Rota---Metro-da-cidade-do-Mexico---Dijkstra-

    * https://github.com/IgorEM/Melhor-Rota---Metro-da-cidade-do-Mexico---Dijkstra-/blob/main/183arestasOrigDestPesoVirgulasSemEspacoNaoDirecional.txt


* Script reproductor de listas de audio: https://stackoverflow.com/questions/58630700/utilising-the-pygame-mixer-music-get-endevent