# Informe de modelo de aprendizaje para la categorización de noticias

**1. Introducción**

En este informe se presenta el desarrollo e implementación de un sistema basado en un modelo de aprendizaje automático, para lograr la clasificación de noticias basandose en sus titulares y descripciones cortas. El proyecto analiza principalmente patrones de escritura para lograrlo.

**2. Objetivos**

* Evaluar la posibilidad de categorizar noticias usando titulares y descripciones
* Analizar la existencia de patrones de escritura
* Extraer información útil para la categorización

**3. Metodología**

La metodología usada para lograr los objetivos, fue en su mayor parte la recomendada por el evaluador, siendo esta la siguiente:

**3.1. Carga de datos**

Se cargan los datos proveidos en el archivo "Data/News_Category_Dataset_v2.json" ubicado en la carpeta "Data".

**3.2. Limpieza de datos**

Una vez son cargados los datos en el sistema, se procede a un tratamiento de los mismos, eliminando caracteres no deseados, estandarizando los textos en minúscula, y juntando los datos relevantes para que el modelo reciba un solo insumo. Por último se vectorizan los datos, para que las palabras puedan ser interpretadas como índices (numeros) por modelo.

**3.3. Partición del DataSet**

Cuando se tiene la información estandarizada se procede a la partición del DataSet, para obtener dos conjuntos de datos, uno para el entrenamiento y otro para prueba, quedando porcionados de la siguiente forma:
* 80% para entrenamiento
* 20% para prueba

**3.4. Diseño e implementación del modelo**

Se opta por usar un modelo de redes neuronales convolucionales, pues basado en la investigación, se determina como las más apropiadas para llevar a cabo la clasificación de las noticias

**Arquitectura del modelo**
* Embedding Layer: Convierte los índices enteros en vectores densos y continuos. Aprende relaciones semánticas entre los indices de las palabras.
* Convolutional Layer: Aplica filtros para extraer características locales de la secuencia (patrones por ejemplo). Dado que nuestro problema involucra el manejo de lenguaje natural se puede considerar como no lineal, por lo que, se implementa la función ReLu para incluir esta no linealidad en el proceso de aprendizaje.
* Pooling Layer: Reduce el tamaño de la salida que provee la capa convolucional, manteniendo solo la información importante.
* Flatten Layer: Las capas anteriores pueden proveer insumos multidimensionales como matrices, sin embargo las capas densas suelen ocupar datos unidimensionales, por lo que esta capa los aplana en una sola dimensión.
* Dense Layer: Conecta de forma completa cada nodo con la siguiente capa para lograr aprender combinaciones de características más complejas.
* Dropout Layer: Reduce el sobreajuste para ignorar aleatoriamente características muy especifícas y así aprender principalmente generalidades.
* Output Layer (Dense): Produce las probabilidades de pertenecer la noticia a cada categoría. Usa una función softmax para convertir los valores de salida en una probabilidad entre 0 y 1

**Parámetros del modelo**
* Se permite un vocabulario de hasta 15.000 palabras
* Se permite hasta una longitud de 50 palabras por secuencia
* Se determina un tamaño de lote de entrenamiento de 32
* Se determina que se lleve a cabo el entrenamiento en 10 épocas

**4. Respuesta a preguntas**

* 1. ¿Se pueden catalogar las noticias con la descripción y los titulares? Compare su clasificación con las categorías incluidas en el set de datos.

R./ Se puede lograr percibir particularidades de cada categoría como en "Crime", que se llega a implementar testimonios, palabras que aluden a tragedias o que pueden considerarse "crudas", de la misma forma en otras categorías como "Comedy", que se notan usos de lenguaje más diverso, ameno y allegado a las personas. Dado a esto se puede determinar que si es posible catalogar noticias en base a su descripción y titular
	
* 2. ¿Existen estilos de escritura asociados a cada categoría?

R./ Como se menciona en el punto anterior, en el set de datos, se logra encontrar suficiente información como para determinar ciertos patrones que se asocian al estilo de escritura que se lleva en cada categoría (Uso de lenguaje crudo en la categoría de crimen...)
	
* 3. ¿Qué se puede decir de los autores?

R./ En el dataset es posible percatarse de ciertas tendencias entre los autores, asi como un poco de su relevancia en la categoría, esto basado en aspectos como, la cantidad de noticias que se encuentran a su nombre, la variedad que maneja (Como pasa entre categorías), y otros casos como que, los autores al parecer tienden a mantener un anonimato cuando se trata de World News
	
* 4. ¿Qué información útil se puede extraer de los datos?

R./ Como se venía abarcando en los puntos anteriores, del dataset es posible extraer información referente a:
    *La relevancia de los autores, basado en la cantidad de veces que puede encontrarse aportes de un autor en una categoria
    *Versatilidad de los autores, según la variedad de las categorías en las que se desempeña
    *Popularidad de temas, según palabras clave que sean usadas por los autores en diferentes categorias 

**5. Optimización**

El DataManager es parametrizable en lo que respecta a la cantidad de palabras que admite el diccionario y la longitud de las secuencias, esto ocurre de igual forma y por lo tanto hay una relación directa con el modelo, por lo que es posible configurar con estos parámetros para cambiar por ejemplo la precisión de las predicciones que son realizadas por el modelo, pues podría ser permitida una longitud de secuencia mayor junto con un diccionario de palabras reconocidas más amplio.
Adicionalmente, es posible cambiar aspectos del entrenamiento como lo son la cantidad de épocas, y el tamaño de los lotes, que pueden demostrar cambios en la precisión de las predicciones, aunque con afecciones en el rendimiento del entrenamiento.

**6. Análisis de gráficas y evaluación**

* Se cuenta con una gráfica de una exploración inicial, que nos permite distinguir la forma en que son distribuidas las noticias en las diferentes categorías que posee el dataset, lo cual nos da una idea inicial de tendencias con respecto a la aparición de entradas de las diferentes categorías.
* Tambien se cuenta con una gráfica de una matriz de confusión, que nos permite divisar, de que forma el modelo llega a confundir ciertas predicciones en contra de los datos que realmente corresponden. Para lograr esta gráfica se tomo el conjunto de datos de prueba y se comparó con las predicciones del modelo para estos mismos datos. Algunas conclusiones que se pueden sacar corresponden a lo siguiente:
    -"ARTS & CULTURE" se "confunde" frecuentemente con otras categorías culturales, aunque si observamos bien, se nota que en realidad pueden llegar a considerarse la  misma categoría solo que en los datos viene con variaciones, causando que difieran por el orden de sus palabras por ejemplo.
    -"STYLE & BEAUTY" muestra una fuerte diagonal, lo que indica buenas predicciones
* Adicionalmente, se genera un reporte de clasificación, el cuál nos arroja una evaluación del modelo con respecto a los siguientes aspectos: 
    -Precisión: Se refiere a la proporción de aserción entre lo que predice el modelo y la categoría a la que realmente pertenecía la información evaluada
    -Exhaustividad: Se refiere a la cantidad de casos reales acertados por el modelo
    -F1-Score: Indica una mediación entre las dos métricas mencionadas con anterioridad.
    -Support: Es la cantidad de muestras de cada clase presentes en el conjunto de datos.
    Una vez analizadas las métricas, podemos notar que de forma general, el modelo tiene un rendimiento decente, sin embargo, la diferencia entre el micro_avg y el macro_avg puede ser un indicativo, de que el modelo va a ser más eficaz en las categorías que cuentan con más muestras.

**7. Conclusiones**

El modelo desarrollado demuestra como es posible categorizar noticias de manera automática con resultados considerables. Además, el análisis inicial nos permite revelar como es posible encontrar patrones de escritura asociados a las categorías y/o a sus autores, esto nos ofrece perspectivas interesantes sobre la naturaleza de los datos asociados a este ámbito

**8. Enlaces de apoyo**

* Documentación de la API de Keras: https://keras.io/api/layers/core_layers
* Documentación de FastAPI: https://fastapi.tiangolo.com/tutorial
* Canal de Youtube en español de "Ringa Tech": https://www.youtube.com/@RingaTech
* Convolutional Neuronal Networks - IBM: https://www.ibm.com/es-es/topics/convolutional-neural-networks
* Adicionalmente se realizaron consultas a herramientas de AI como lo son: ChatGPT y Gemini (By Google)