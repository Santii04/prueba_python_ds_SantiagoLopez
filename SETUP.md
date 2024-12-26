# Ejecución del proyecto

**Pre-requisitos**

Antes de comenzar la instalación de paquetería, se recomienda usar un entorno virtual de Python, para evitar la instalación global de las mismas, y mantenerlas aísladas en el proyecto mismo, para lograr esto, siga los siguientes pasos:

1. Posicionese en la carpeta del proyecto y ejecute el siguiente comando `python3 -m venv ./dir_para_env`
2. Inicie el entorno virtual usando el comando `source <env>/bin/activate` en sistemas UNIX ó `<env>/bin/activate.bat` en sistemas Windows
3. Una vez iniciado el entorno virtual, puede proseguir con la instalación de dependencias

Para una debida ejecución del proyecto se requiere de los siguientes paquetes:
1. pandas
2. matplotlib
3. seaborn
4. re
5. tensorflow
6. numpy
7. fastapi
8. fastapi[standard]
9. scikit

Asegurese de instalar los paquetes usando el comando `pip install <paquete>`
ó
instale todos los paquetes que se exportan en el archivo "requirements.txt" usando el siguiente comando `pip install -r ruta/archivo/requirements.txt`

**Ejecución**

Una vez preparado el entorno virtual con sus respectivos paquetes, se puede proseguir con la ejecución del proyecto.
El proyecto está basado en la exposición de un endpoint para su consumo usando FastAPI, por lo que, ejecutaremos el archivo main.py, usando el comando `fastapi dev ruta/archivo/main.py`. Por ejemplo, estando posicionado en la raíz del proyecto, ejecutará el siguiente comando en la terminal `fastapi dev src/main.py --no-reload`. Nota: Dada la naturaleza del repositorio al contener un directorio que almacena las gráficas generadas por la aplicación, es necesario especificar --no-reload para que esto no afecte el recargue de la aplicación.
Esto iniciará el entrenamiento del modelo, basado en las caracteristicas establecidas, y usando el archivo .JSON proveido por el evaluador.

Una vez el entrenamiento concluye y el servidor se despliega, es posible acceder a la documentación de los endpoints, a través del url: "http://127.0.0.1:8000/docs", en cualquier navegador local. Desde aquí será posible llevar a cabo un consumo prematuro de los endpoints, y ver el funcionamiento de las predicciones del modelo ML.
