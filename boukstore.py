# -*- coding: utf-8 -*-
"""Trabajo Final de ML - Lautaro Barceló y jose zambrano.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hbAxPTY3mwkBXZyvnbaCq6meBodY0Ffi

# **Proyecto de Machine Learning para pequeña librería Bokstoure** #
### Sistema de Recomendación: Filtrado basado en Contenido ###
#### Licenciatura en IA - Aprendizaje de Máquina - Prof. Darío Príncipi
#### Alumnos: Lautaro Barceló y Jose Zambrano

## **Definición del problema**
El objetivo principal es desarrollar un sistema de recomendación de libros para una librería que tiene tienda física y va a incursionar en el mundo online. El problema se puede dividir en dos fases. En la primera fase (MVP), se quiere crear un sistema que recomiende libros basándose en el género literario y que presente estas recomendaciones ordenadas por un ranking de popularidad. También crearemos un segundo modelo de filtrado colaborativo que recomiende en base a los gustos del usuario.
También haremos un prototipo que permita predecir que rating le asignaría un usuario a un libro que aún no leyó, lo que permitiría, entre otras cosas, agregar un elemento lúdico a la relación entre el usuario y la tienda online: una especie de bola del futuro.

## **Objetivos específicos**:
Desarrollar un modelo de recomendación basado en género literario.
Crear un ranking de popularidad para los libros.
Escalar el modelo para incluir recomendaciones basadas las reseñas de usuarios.

## **Restricciones**:
Utilizar recursos computacionales de manera eficiente, especialmente en la fase inicial (MVP).
Asegurar que las recomendaciones sean relevantes y útiles para los usuarios.
Mantener la escalabilidad para futuras expansiones del modelo.

## **Exploración y análisis de datos:**
#### Adquisición de datos:
Para presentar el prototipo, utilizamos el dataset de Amazon Books Reviews https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews
Utilizaremos solamente el archivo books.csv para el MVP, y los ratings para generar recomendaciones en base a las reseñas que han dejado los usuarios.
#### Exploración de datos:
Identificar las características disponibles en la base de datos, como título del libro, autor, género, etc.
Analizar la distribución de géneros y tags para entender la diversidad de la colección.
Revisar la calidad de los datos para manejar posibles valores nulos o inconsistentes.
#### Preprocesamiento de datos:
Limpiar y preprocesar los datos eliminando duplicados, valores nulos o inconsistentes.
Transformar los datos en un formato adecuado para el entrenamiento del modelo, como matrices de características.
#### Visualización de datos:
Utilizar gráficos y visualizaciones para entender mejor la distribución de géneros, la popularidad de los libros y cualquier patrón evidente.

## **Selección del modelo:**
Elegir un modelo adecuado para recomendaciones basadas en género.

#### Preparación de datos:
Dividir el conjunto de datos en conjuntos de entrenamiento y prueba para evaluar el rendimiento del modelo.
Representar los datos en un formato compatible con el modelo seleccionado.

#### Diseño del modelo:
Definir la arquitectura del modelo, teniendo en cuenta la entrada (título del libro) y la salida (recomendación/es).
d. Entrenamiento del modelo:

#### Utilizar el conjunto de entrenamiento para ajustar los parámetros del modelo:
Supervisar el rendimiento del modelo utilizando el conjunto de prueba.

#### Validación del modelo:
Evaluar la capacidad del modelo para hacer recomendaciones precisas basadas en género.
Ajustar hiperparámetros si es necesario para mejorar el rendimiento.

## **Análisis exploratorio de datos** ##

## Importar dataset y librerías ##
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Se debe ingresar el path donde se encuentra el archivo books_data.csv
books = pd.read_csv('/Users/lautarobarcelo/Downloads/archive/books_data.csv')
#books = pd.read_csv('/content/drive/MyDrive/csv/books_data.csv')

rating=pd.read_csv('/content/drive/MyDrive/csv/Books_rating.csv')

rating.head()

"""Aquí podemos observar de qué consta el dataset y cuáles son los datos en sus columnas. Como podemos ver, algunas columnas tienen valores nulos o mal ingresados."""

books.head(10)

"""## Importar librería para preprocesar el dato de interés, que en este caso es Categories ##

Utizamos la librería "ast" para convertir los strings que componen los valores del DataFrame "books" y que imitan la fórmula de una lista en Python.
"""

import ast

def process_categories(categories):
    try:
        categories_list = ast.literal_eval(categories)  # Intenta convertir la cadena en una lista
        if isinstance(categories_list, list) and len(categories_list) > 0:
            return categories_list[0]  # Devuelve el primer elemento de la lista
        else:
            return None  # Devuelve None si la cadena parece ser una lista pero está vacía
    except (ValueError, SyntaxError):
        return None  # Devuelve None si no se puede convertir a lista

# Aplica la función a la columna 'categories'
books['categories'] = books['categories'].apply(process_categories)

"""Una vez procesadas las categorías, seguimos con eliminar las categorías nulas para poder generar un modelo que funcione solamente con aquellos libros a los que se les ha asignado una categoría."""

# Eliminar nulos
books.dropna(subset=['categories'], inplace=True)

"""Ahora "books" no cuenta con valores nulos."""

books.head(10)

"""Para poder utilizar el filtrado basado en contenido, antes de terminar el preprocesamiento debemos convertir todos los valores de books['categories'] a str."""

# Convertir tipo de dato de object a str
books['categories'] = books['categories'].astype(str)

books.head()

"""### Filtrado basado en contenido ###

El filtrado basado en contenido permite personalizar las recomendaciones en función de los gustos y preferencias de los usuarios. Al centrarse en el género literario, se garantiza que las sugerencias estén directamente alineadas con los intereses individuales de los lectores.

**Eficiencia en la Fase Inicial (MVP):**

Dado que la fase inicial se enfoca en la implementación de un producto mínimo viable (MVP), el filtrado basado en contenido basado en género literario es eficiente en términos de recursos computacionales. La representación de los libros por género es una tarea computacionalmente liviana y permite una implementación rápida y eficiente. Contando con los datos de Amazon, podemos lograr recomendaciones a pesar del arranque en frío.

**Ranking de Popularidad Incorporado:**

El modelo de filtrado basado en contenido puede integrar de manera natural un ranking de popularidad para los libros. Al considerar la popularidad dentro de cada género, se garantiza que las recomendaciones no solo sean personalizadas, sino también respaldadas por la preferencia general de los lectores.


**Mantenimiento de Escalabilidad para Futuras Expansiones:**

El filtrado basado en contenido es inherentemente escalable. A medida que la librería crece y se diversifica, la adición de nuevos géneros literarios o tags se puede realizar de manera sencilla sin afectar significativamente el rendimiento del sistema.

**Requisitos de Recursos Computacionales:**

El enfoque basado en contenido es menos intensivo en recursos en comparación con otros métodos de recomendación, como el filtrado colaborativo, lo que cumple con la restricción de utilizar eficientemente los recursos computacionales, especialmente durante la fase inicial del proyecto.
Es importante que para poder calcular la similitud de coseno entre todos los libros en nuestro equipo local, no podemos utilizar una muestra demasiado grande. Por eso la partimos a la casi la mitad.
"""

merged_data = pd.merge(rating, books, on='Title', how='inner')

# Agrega impresiones para depuración
print("Número total de calificaciones:", len(rating))
print("Número total de libros en books_sample:", len(books))
print("Número total de calificaciones después del filtrado:", len(merged_data))

"""Este código en Python utiliza la biblioteca `pandas` para realizar una **fusión interna** de dos conjuntos de datos (`rating` y `books`) basándose en el título. Las siguientes líneas de código imprimen información sobre el tamaño de los conjuntos de datos antes y después de la fusión, lo cual es útil para la **depuración del código**.

"""

merged_data.head()

ratings = merged_data[['Id','User_id','review/score','Title','review/text','authors','image']]

"""Este código en Python crea un nuevo DataFrame llamado 'ratings' al seleccionar columnas específicas del DataFrame fusionado 'merged_data'. Las columnas seleccionadas incluyen 'Id', 'User_id', 'review/score', 'Title' y 'review/text'. Esta operación permite filtrar y retener solo las columnas de interés para su posterior análisis.

"""

ratings.rename(columns={'Id':'book_id','User_id':'user_id','review/score':'rating','Title':'title','review/text':'review'},inplace=True)

"""Este código en Python utiliza el método `rename` de pandas para cambiar los nombres de las columnas en el DataFrame 'ratings'. Las columnas 'Id', 'User_id', 'review/score', 'Title', y 'review/text' se renombran respectivamente a 'book_id', 'user_id', 'rating', 'title' y 'review'. El parámetro `inplace=True` indica que los cambios deben realizarse directamente en el DataFrame original 'ratings'.

"""

ratings.shape

"""Tenemos demasiados datos, empezaremos filtrando"""

x = ratings.groupby('user_id').count()['rating'] > 75

considerable_users = x[x].index

considerable_users

"""Este código en Python realiza las siguientes operaciones:

1. **Agrupación y Conteo:** Agrupa el DataFrame 'ratings' por la columna 'user_id' y cuenta el número de elementos en cada grupo ('rating'). El resultado se almacena en la Serie booleana 'x', indicando si el usuario ha realizado más de 75 valoraciones.

2. **Filtrado de Usuarios Considerados:** Filtra los usuarios cuyo número de valoraciones es mayor que 75 y almacena sus 'user_id' en la variable 'considerable_users'.

3. **Impresión de Usuarios Considerados:** Imprime la lista de 'user_id' de los usuarios considerados en base al filtro anterior.

"""

filtered_rating = ratings[ratings['user_id'].isin(considerable_users)]

"""Este código en Python crea un nuevo DataFrame llamado 'filtered_rating' al filtrar las valoraciones en el DataFrame original 'ratings'. Se seleccionan solo aquellas valoraciones realizadas por usuarios que fueron identificados como considerables previamente (almacenados en la variable 'considerable_users') mediante la función `isin`. Esto permite trabajar únicamente con las valoraciones de los usuarios que han realizado más de 75 valoraciones.

"""

filtered_rating

y = filtered_rating.groupby('title').count()['rating']>=25
famous_books = y[y].index

"""Este código en Python realiza las siguientes operaciones:

1. **Agrupación y Conteo de Valoraciones por Libro:** Agrupa el DataFrame 'filtered_rating' por la columna 'title' y cuenta el número de valoraciones ('rating') para cada libro. El resultado se almacena en la Serie booleana 'y', indicando si un libro tiene al menos 25 valoraciones.

2. **Filtrado de Libros Famosos:** Filtra los libros que tienen al menos 25 valoraciones y almacena los títulos de estos libros en la variable 'famous_books'. Esto proporciona una lista de libros que son considerados "famosos" en base al criterio de tener un número significativo de valoraciones.

"""

final_ratings = filtered_rating[filtered_rating['title'].isin(famous_books)]

"""Este código en Python crea un nuevo DataFrame llamado 'final_ratings' al filtrar las valoraciones en el DataFrame 'filtered_rating'. Se seleccionan solo aquellas valoraciones que corresponden a libros considerados "famosos" según el criterio de tener al menos 25 valoraciones, y cuyos títulos están almacenados en la variable 'famous_books'. Esto ayuda a reducir el conjunto de datos a las valoraciones asociadas con libros que cumplen con el criterio de ser considerados "famosos".

"""

final_ratings

final_ratings.to_csv('final_Dataset.csv',index=False)

import pandas as pd
import numpy as np

df = pd.read_csv('final_Dataset.csv')

"""Este código en Python realiza las siguientes operaciones:

1. **Guardado en un Archivo CSV:** La función `to_csv` de pandas se utiliza para guardar el DataFrame 'final_ratings' en un archivo CSV llamado 'final_Dataset.csv'. El parámetro `index=False` indica que no se debe incluir el índice del DataFrame en el archivo CSV.

2. **Lectura desde un Archivo CSV:** La función `read_csv` de pandas se utiliza para leer el archivo CSV recién creado ('final_Dataset.csv') y cargar los datos en un nuevo DataFrame llamado 'df'. Esto permite trabajar con los datos almacenados en el archivo CSV en futuras operaciones.

"""

df.info()

df['review'] = df['review'].str.replace(',', '')
df['review'] = df['review'].str.replace('\d+', '', regex=True)

"""Este código en Python realiza las siguientes operaciones en el DataFrame 'df':

1. **Eliminación de Comas:** En la columna 'review', utiliza el método `str.replace` para eliminar las comas. Esto es útil si las comas no son necesarias en el contexto de las revisiones y se desean eliminar.

2. **Eliminación de Dígitos:** En la misma columna 'review', utiliza nuevamente `str.replace` con una expresión regular (`'\d+'`) para eliminar todos los dígitos. Esto puede ser útil si se desea eliminar números de las revisiones, por ejemplo, si no son relevantes para el análisis que se va a realizar.

"""

df.head()

!pip install scikit-surprise

from surprise import Dataset
from surprise import Reader
from surprise import KNNWithMeans
from surprise import KNNBaseline
from surprise import KNNBasic
from surprise import accuracy
from surprise.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['user_id', 'book_id', 'rating']], reader)

"""Este código utiliza la biblioteca `surprise`, que es una herramienta para construir y analizar sistemas de recomendación.

1. **Creador de Lectores (`Reader`):** Se crea un objeto `Reader` con la escala de calificación especificada de 1 a 5. El `Reader` ayuda a cargar datos en el formato requerido por `surprise`.

2. **Carga de Datos (`Dataset.load_from_df`):** Se carga un conjunto de datos (`data`) desde el DataFrame 'df' utilizando `Dataset.load_from_df` de `surprise`. Se seleccionan las columnas 'user_id', 'book_id', y 'rating' del DataFrame para construir el conjunto de datos necesario para el análisis y construcción de modelos de recomendación.

"""

from numpy.random.mtrand import random
trainset, testset = train_test_split(data, test_size=0.3, random_state=42)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['review'])

"""Este código utiliza la biblioteca `scikit-learn` y la clase `TfidfVectorizer` para realizar la transformación TF-IDF (Term Frequency-Inverse Document Frequency) en las revisiones de un DataFrame.

1. **Creador de Vectorizador (`TfidfVectorizer`):** Se crea un objeto `TfidfVectorizer`, que convierte una colección de documentos de texto en una matriz de características TF-IDF. TF-IDF es una medida estadística que evalúa la importancia de una palabra en un documento en relación con su frecuencia en el conjunto de documentos.

2. **Transformación de Revisiones a Matriz TF-IDF:** Utilizando el método `fit_transform`, se aplica el vectorizador a la columna 'review' del DataFrame 'df'. El resultado, `tfidf_matrix`, es una matriz donde cada fila representa una revisión y cada columna representa una palabra en el conjunto total de revisiones, ponderada por su importancia TF-IDF.

"""

import numpy as np
batch_size = 250
num_books = tfidf_matrix.shape[0]

# Inicializar la matriz de similitud de coseno
cosine_sim = np.zeros((num_books, num_books))

# Calcular la similitud de coseno por lotes
for i in range(0, num_books, batch_size):
    end = min(i + batch_size, num_books)
    cosine_sim[i:end, i:end] = cosine_similarity(tfidf_matrix[i:end, :])

"""Este código utiliza lotes (o batches) para calcular la similitud de coseno entre los libros representados en la matriz TF-IDF. Aquí está la explicación:

### Tamaño del Lote (`batch_size`):
Se establece el tamaño del lote en 250. Esto significa que el cálculo se realiza en bloques de 250 libros a la vez.

### Inicialización de Variables:
Se inicializa la matriz de similitud de coseno (`cosine_sim`) como una matriz de ceros con dimensiones `(num_books, num_books)`.

### Cálculo de Similitud de Coseno por Lotes:
Se utiliza un bucle `for` para iterar a través de la matriz de similitud de coseno por lotes. En cada iteración, se calcula la similitud de coseno para un bloque específico de libros (definido por el tamaño del lote) utilizando la función `cosine_similarity` de scikit-learn. Los resultados se almacenan en la matriz `cosine_sim`.

# **KNN (Vecinos más Cercanos)**

El algoritmo KNN es un método de recomendación basado en la proximidad entre usuarios o ítems. Funciona identificando vecinos más cercanos en función de la similitud de sus historiales de interacción. Para recomendaciones de ítems, se seleccionan los ítems más similares a los que le gustaron al usuario; para recomendaciones de usuarios, se identifican usuarios con historiales de interacción similares. KNN es simple pero efectivo, ya que confía en la similitud entre elementos para hacer predicciones personalizadas.
"""

similarity_options = {'name': 'cosine', 'user_based': True, 'user_item_similarities': cosine_sim}
baseline_options = {'method': 'als_sgd', 'learning_rate': 0.003}

"""Este código define dos diccionarios, `similarity_options` y `baseline_options`, que se utilizan para configurar opciones en el contexto de sistemas de recomendación.

Opciones de Similitud (`similarity_options`):
- **`name`:** Se especifica el método de similitud como 'cosine', lo que indica que se utilizará la similitud de coseno. Esta medida de similitud cuantifica la relación angular entre dos vectores y es comúnmente utilizada en sistemas de recomendación.
- **`user_based`:** Se establece en `True`, indicando que se está construyendo un modelo basado en usuarios. En sistemas de recomendación, esto significa que las recomendaciones se realizarán en función de la similitud entre usuarios.
- **`user_item_similarities`:** Se establece en la matriz de similitud de coseno previamente calculada (`cosine_sim`). Esta matriz contiene las similitudes de coseno entre los usuarios (filas) y los elementos (libros en este caso).

Opciones del Modelo Baseline (`baseline_options`):
- **`method`:** Se especifica el método del modelo baseline como 'als_sgd'. Esto podría referirse a Alternating Least Squares con Stochastic Gradient Descent, un enfoque comúnmente utilizado en sistemas de recomendación para factorización de matrices.
- **`learning_rate`:** Se establece en 0.003, que representa la tasa de aprendizaje utilizada en el proceso de optimización. Ajustar la tasa de aprendizaje puede afectar la convergencia y el rendimiento del modelo.

"""

model1 = KNNWithMeans(k=10, min_k=7, sim_options=similarity_options,)
model1.fit(trainset)

"""Este código utiliza la biblioteca `surprise` para crear y entrenar un modelo de filtrado colaborativo basado en el algoritmo K-Nearest Neighbors (KNN) con promedios ponderados.

Creación del Modelo (`KNNWithMeans`):
- **`KNNWithMeans`:** Es un modelo de filtrado colaborativo basado en KNN que tiene en cuenta la media de las calificaciones. Esto significa que, para hacer recomendaciones, considerará las calificaciones medias de los usuarios y elementos.

Parámetros del Modelo:
- **`k=10`:** Especifica que se utilizarán los 10 vecinos más cercanos para calcular la similitud.
- **`min_k=7`:** Establece un requisito mínimo de 7 vecinos para realizar una predicción.
- **`sim_options=similarity_options`:** Utiliza las opciones de similitud definidas anteriormente en `similarity_options`.

Entrenamiento del Modelo (`model1.fit(trainset)`):
- **`trainset`:** Se asume que es un conjunto de entrenamiento preparado en el formato específico de `surprise`.
- **`fit()`:** Método que entrena el modelo utilizando el conjunto de entrenamiento proporcionado (`trainset`).

Este modelo entrenado (`model1`) puede luego utilizarse para realizar predicciones y generar recomendaciones basadas en similitud entre usuarios o elementos.

"""

predictions1 = model1.test(testset)

predictions1[:5]

rmse = accuracy.rmse(predictions1)
mse = accuracy.mse(predictions1)
mae = accuracy.mae(predictions1)

"""Este código utiliza la función `accuracy` de la biblioteca `surprise` para calcular diferentes métricas de evaluación del modelo de recomendación construido y evaluado previamente.

Métricas de Evaluación:
- **RMSE (Root Mean Squared Error):** Mide la raíz cuadrada de la media de los errores cuadrados entre las predicciones y los valores reales. En este caso, el valor obtenido es 0.7419.
- **MSE (Mean Squared Error):** Es la media de los errores cuadrados entre las predicciones y los valores reales. En este caso, el valor obtenido es 0.5504.
- **MAE (Mean Absolute Error):** Mide la media de las diferencias absolutas entre las predicciones y los valores reales. En este caso, el valor obtenido es 0.5099.

Interpretación de los Resultados:
- **RMSE:** Cuanto más cercano a cero, mejor. Indica la raíz cuadrada promedio de los errores.
- **MSE:** Cuanto más cercano a cero, mejor. Es el promedio de los errores cuadrados.
- **MAE:** Cuanto más cercano a cero, mejor. Representa la media de las diferencias absolutas.

En este contexto, valores más bajos para estas métricas indican un mejor rendimiento del modelo, ya que implican una menor diferencia entre las predicciones y los valores reales.

#**KNN Baseline (Vecinos más Cercanos con Línea de Base):**

El algoritmo KNN Baseline combina el enfoque de Vecinos más Cercanos (KNN) con la Línea de Base para recomendaciones. Utiliza la información de los vecinos más cercanos en función de la similitud entre usuarios o ítems, ajustando las predicciones basándose en las tendencias globales de calificación (línea de base). Esto permite tener en cuenta las preferencias individuales mientras considera el comportamiento general de los usuarios o ítems en el conjunto de datos.
"""

similarity_options = {'name': 'cosine', 'user_based': True, 'user_item_similarities': cosine_sim}
baseline_options = {'method': 'sgd', 'learning_rate': 0.001}

model2 = KNNBaseline(k=10, min_k=4, sim_options=similarity_options, bsl_options=baseline_options)
model2.fit(trainset)

"""Este código utiliza la biblioteca `surprise` para crear y entrenar otro modelo de filtrado colaborativo basado en el algoritmo K-Nearest Neighbors (KNN), pero en este caso, incorpora el modelo baseline.

Creación del Modelo (`KNNBaseline`):
- **`KNNBaseline`:** Es un modelo de filtrado colaborativo basado en KNN que tiene en cuenta la media de las calificaciones y un modelo baseline. Combina la similitud de coseno con un modelo de baseline para realizar predicciones.

Parámetros del Modelo:
- **`k=10`:** Especifica que se utilizarán los 10 vecinos más cercanos para calcular la similitud.
- **`min_k=4`:** Establece un requisito mínimo de 4 vecinos para realizar una predicción.
- **`sim_options=similarity_options`:** Utiliza las opciones de similitud definidas anteriormente en `similarity_options`.
- **`bsl_options=baseline_options`:** Utiliza las opciones del modelo baseline definidas anteriormente en `baseline_options`.

Entrenamiento del Modelo (`model2.fit(trainset)`):
- **`trainset`:** Se asume que es un conjunto de entrenamiento preparado en el formato específico de `surprise`.
- **`fit()`:** Método que entrena el modelo utilizando el conjunto de entrenamiento proporcionado (`trainset`).

Este nuevo modelo entrenado (`model2`) incorpora la información del modelo baseline, lo que podría mejorar las predicciones en comparación con un modelo KNN simple.

"""

predictions2 = model2.test(testset)

predictions2[:5]

rmse = accuracy.rmse(predictions2)
mse = accuracy.mse(predictions2)
mae = accuracy.mae(predictions2)

"""Este código utiliza la función `accuracy` de la biblioteca `surprise` para calcular diferentes métricas de evaluación del segundo modelo de recomendación construido y evaluado previamente.

Métricas de Evaluación:
- **RMSE (Root Mean Squared Error):** Mide la raíz cuadrada de la media de los errores cuadrados entre las predicciones y los valores reales. En este caso, el valor obtenido es 0.7544.
- **MSE (Mean Squared Error):** Es la media de los errores cuadrados entre las predicciones y los valores reales. En este caso, el valor obtenido es 0.5691.
- **MAE (Mean Absolute Error):** Mide la media de las diferencias absolutas entre las predicciones y los valores reales. En este caso, el valor obtenido es 0.5345.

Interpretación de los Resultados:
- **RMSE:** Cuanto más cercano a cero, mejor. Indica la raíz cuadrada promedio de los errores.
- **MSE:** Cuanto más cercano a cero, mejor. Es el promedio de los errores cuadrados.
- **MAE:** Cuanto más cercano a cero, mejor. Representa la media de las diferencias absolutas.

En comparación con los resultados del primer modelo, estos resultados indican que el segundo modelo tiene un rendimiento razonable, con valores de métricas similares o ligeramente diferentes. Es importante considerar el contexto y los requisitos específicos del problema para determinar qué modelo es más adecuado.

# **SVD**

Funky SVD Recommendation Algorithm

El algoritmo Funky Singular Value Decomposition (Funky SVD) puede ser adaptado para sistemas de recomendación por contenido, donde se buscan prever las preferencias de los usuarios basándose en las características intrínsecas de los ítems

Al utilizar Funky SVD en sistemas de recomendación por contenido, se busca mejorar la precisión y la relevancia de las sugerencias al considerar de manera efectiva las características intrínsecas de los ítems. Este enfoque es útil en entornos donde la información sobre el contenido es esencial para entender las preferencias de los usuarios.
"""

from surprise import SVDpp

# Crear el modelo FunkSVD (SVDpp)
algo_funk_svd = SVDpp(n_factors=100, lr_all=0.005, reg_all=0.02, n_epochs=20)

"""Este código utiliza la biblioteca `surprise` para crear un modelo Funk Singular Value Decomposition (FunkSVD), específicamente utilizando la clase `SVDpp`.

Creación del Modelo (`SVDpp`):
- **`SVDpp`:** Es una implementación del algoritmo de descomposición de valores singulares (SVD) mejorado con factores de persistencia. Este modelo es una extensión del modelo SVD clásico.

Parámetros del Modelo:
- **`n_factors=100`:** Especifica la cantidad de factores latentes en el modelo. Cuanto mayor sea este valor, más complejo será el modelo, pero también puede aumentar la capacidad para capturar patrones en los datos.
- **`lr_all=0.005`:** Establece la tasa de aprendizaje para el proceso de optimización. Ajustar la tasa de aprendizaje puede afectar la convergencia y el rendimiento del modelo.
- **`reg_all=0.02`:** Controla la regularización de todos los términos en el modelo. La regularización ayuda a prevenir el sobreajuste y mejora la generalización del modelo.
- **`n_epochs=20`:** Especifica la cantidad de épocas o iteraciones del proceso de entrenamiento. Un mayor número de épocas permite que el modelo ajuste mejor los datos, pero también puede aumentar el riesgo de sobreajuste.

Este modelo `algo_funk_svd` ahora está listo para ser entrenado utilizando un conjunto de entrenamiento específico.

"""

# Ajustar el modelo al conjunto de entrenamiento
algo_funk_svd.fit(trainset)

# Realizar predicciones en el conjunto de prueba
predictions3 = algo_funk_svd.test(testset)

predictions3[:10]

rmse = accuracy.rmse(predictions3)
mse = accuracy.mse(predictions3)
mae = accuracy.mae(predictions3)

"""Este código utiliza la función `accuracy` de la biblioteca `surprise` para calcular diferentes métricas de evaluación del tercer modelo de recomendación construido y evaluado previamente, que es el modelo Funk Singular Value Decomposition (FunkSVD).

Métricas de Evaluación:
- **RMSE (Root Mean Squared Error):** Mide la raíz cuadrada de la media de los errores cuadrados entre las predicciones y los valores reales. En este caso, el valor obtenido es 0.7069.
- **MSE (Mean Squared Error):** Es la media de los errores cuadrados entre las predicciones y los valores reales. En este caso, el valor obtenido es 0.4998.
- **MAE (Mean Absolute Error):** Mide la media de las diferencias absolutas entre las predicciones y los valores reales. En este caso, el valor obtenido es 0.4998.

Interpretación de los Resultados:
- **RMSE:** Cuanto más cercano a cero, mejor. Indica la raíz cuadrada promedio de los errores.
- **MSE:** Cuanto más cercano a cero, mejor. Es el promedio de los errores cuadrados.
- **MAE:** Cuanto más cercano a cero, mejor. Representa la media de las diferencias absolutas.

**En comparación con los resultados de los modelos anteriores, estos resultados sugieren que el modelo FunkSVD tiene un rendimiento razonablemente bueno, con valores bajos de las métricas de evaluación. Estos resultados pueden indicar que el modelo es capaz de hacer predicciones precisas sobre las calificaciones de los usuarios en el conjunto de datos de prueba.**

# Obtener Recomendacion de libros

## Filtrado Colaborativo
"""

from IPython.display import display, HTML

def get_recommendations_with_images(user_id, n=10):
    # Encontrar los n usuarios más similares basados en sus revisiones textuales
    user_index = df[df['user_id'] == user_id].index[0]
    sim_scores = list(enumerate(cosine_sim[user_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    sim_users = [df['user_id'][i[0]] for i in sim_scores]

    # Encontrar los ítems que los usuarios similares han calificado positivamente
    top_items = {}
    recommended_titles = set()  # Conjunto para rastrear títulos ya recomendados

    for user in sim_users:
        items = df[df['user_id'] == user]['book_id']
        for item in items:
            title = df[df['book_id'] == item].iloc[0]['title']
            if title not in recommended_titles:
                if item not in top_items:
                    top_items[item] = 1
                else:
                    top_items[item] += 1
                recommended_titles.add(title)  # Agregar el título al conjunto de títulos recomendados

    # Ordenar los ítems por la cantidad de veces que han sido recomendados
    top_items = sorted(top_items.items(), key=lambda x: x[1], reverse=True)

    # Devolver los primeros n ítems como recomendaciones
    rec_books = []
    for i in top_items[:n]:
        book_id = i[0]
        book_name = df[df['book_id'] == book_id].iloc[0]['title']
        book_image = df[df['book_id'] == book_id].iloc[0]['image']
        rec_books.append({'title': book_name, 'image': book_image})

    return rec_books

""" Entrada de la Función:

- `user_id`: Identificador del usuario para el cual se generan las recomendaciones.
- `n`: Número de libros a recomendar (por defecto es 10).

 Cálculo de Usuarios Similares:

1. Se encuentra el índice del usuario en el DataFrame utilizando su `user_id`.
2. Se calcula la similitud coseno entre el usuario dado y todos los demás usuarios.
3. Los resultados se ordenan en orden descendente de similitud y se seleccionan los primeros `n` usuarios más similares.

Búsqueda de Libros Positivamente Calificados por Usuarios Similares:

1. Para cada usuario similar, se obtienen los libros que ha calificado positivamente.
2. Se evitan títulos duplicados utilizando un conjunto (`recommended_titles`).

Conteo de Recomendaciones por Libro:

- Se lleva un conteo de cuántas veces cada libro ha sido recomendado.

Ordenamiento y Devolución de las Recomendaciones:

1. Los libros se ordenan en función de la cantidad de recomendaciones recibidas.
2. Se devuelven las primeras `n` recomendaciones con sus títulos e imágenes correspondientes.

"""

df.head()

# Ejemplo de uso
user_id = 'A3NQU1649SH0Q4'
recommendations = get_recommendations_with_images(user_id)
print(f"Recomendaciones para el usuario '{user_id}':")
for book in recommendations:
    display(HTML(f"<h4>{book['title']}</h4><img src='{book['image']}' alt='{book['title']}' style='max-width:550px;'>"))

"""## Filtrado basado en contenido

Finalmente podemos obtener un modelo que genera recomendaciones a partir del género de los libros y los ordena según el rating otorgado por los usuarios.
"""

from IPython.display import display, HTML

def get_recommendations_with_images(title, cosine_sim=cosine_sim, books_df=books):
    # Restablece el índice para asegurarte de que sea consecutivo
    books_df = books_df.reset_index(drop=True)

    # Busca el índice del libro por título
    matching_titles = books_df[books_df['Title'] == title]

    if matching_titles.empty:
        print(f"No se encontró el libro con el título '{title}'.")
        return None

    idx = matching_titles.index[0]

    # Verifica si el índice está dentro de los límites
    if idx >= len(cosine_sim):
        print(f"Índice {idx} está fuera de los límites del DataFrame.")
        return None

    # Resto del código de tu función...
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    book_indices = [i[0] for i in sim_scores]

    # Obtén las recomendaciones ordenadas por ratingsCount
    recommendations_df = books_df.loc[book_indices].sort_values(by='ratingsCount', ascending=False)

    # Visualización de recomendaciones con imágenes
    for index, row in recommendations_df.iterrows():
        display(HTML(f"<h4>{row['Title']}, by {row['authors']}</h4><img src='{row['image']}' alt='{row['Title']}' style='max-width:550px;'>"))

    return recommendations_df['Title']

# Ejemplo de uso
book_title = 'Dr. Seuss: American Icon'
recommendations = get_recommendations_with_images(book_title)
print(f"Recomendaciones para '{book_title}':")
print(recommendations)