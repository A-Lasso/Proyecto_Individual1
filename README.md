# Proyecto Individual 1
## Abril Lasso de la Vega
**Este readme esta escrito desde el punto de vista de los archivos de jupyter notebook, su paso a paso y orden.**<br>
**En el código de los archivos .py hay comentarios más simples y cambios de orden, la explicación es la misma**

- En el archivo ETL.py se encuentran todas las transformaciones que hice y luego guardé los .csv ya limpios, ordenados y de la forma que quería.

- En el archivo API.py se tienen las funciones para la API, se traen los csv limpios, y se trabaja toda la parte de API allí.

- Recuerde que para que el código ETL le funcione correctamente, debe cambiar la ruta del archivo en el pd.read_csv, a la ruta en la que se encuentre este en su pc (Luego para el resto de archivos los df creados son usando los csv limpios, que se encuentran en la carpeta "csv", por lo tanto no necesita cambiar nada).<br>

- En el archivo ETL.ipynb además de encontrarse cómo fui avanzando y cada cosa que hice respecto al ETL, también se encuentran las funciones de la API (es lo mismo a verlas en API.py, pero hay algunos codigo ejemplo y prueba).<br>

### ETL
Empecé por hacer las transformaciones pedidas y necesarias, comenzando con las más fáciles:<br>

* Empiezo por los datos del archivo "movies_dataset.csv".<br>
    * Eliminé las columnas pedidas ["video","imdb_id","adult","original_title","poster_path" , "homepage"], innecesarias que no van a ser utilizadas.<br>
    * Verifique los valores de budget y revenue para ver lo que me esperaba en el valor de la columna a crear "return". Al ver los valores de cada columna se nota como va a dominar el return 0, tanto por el lado de budget 0 (donde se deja return igual a 0) como por el de revenue igual 0.
    * Antes de crear la columna me aseguré de que los valores que fueran nulos se reemplazaran por 0, como nos pidieron (solamente la columna revenue contaba con vacios).
    * Elimino los vacios (filas) de la columna "release_date".
    * Solo por observación use el código "data.isna().sum()", asi veía los vacios que quedan y en qué columnas.
    * Ahora sí, cree la columna return, primero verificando el tipo de valores de cada columna, y luego asegurandome de pasar los valores de la columna budget de string a float. La columna return la cree realizando un ciclo (en el cual tuve que hacer zip para poder renombrar a los valores de cada columna como i y j) en el que si budget es distinto de cero se hace la división y se agrega el valor a la lista que en principio está vacía, y si budget es cero el valor que se agrega es cero a la lista. Luego esta lista es la contenedora de los valores de return y lo último por hacer es crear la nueva columna con estos valores.
    * Ahora paso a crear la siguiente columna pedida "release_year", para esto primero tuve que transformar la columna "release_date" a datetime y que en caso de que tire error (no es una fecha como tal o no esta en el formato correcto) me va a llenar con vacio. Luego cree la nueva columna de los años con <br>
    `"data["release_year"]=data["release_date"].dt.year"` 
    * Eliminé tres filas que eran completamente inusables, no solamente están llenas de vacios, sino que los pocos valores que tienen parecen estar intercambiados, y no sabría cómo sería el reordenamiento correcto. Justamente este desorden trajo mayores vacios, las fechas fueron imposibles de calcular.<br>
    `data.drop(labels=[19730,29503,35587],axis=0,inplace=True)`.<br>

**Terminé re acomodando las columnas del dataframe por simple gusto, el orden es a ojo y no cambia los valores ni los futuros resultados.**<br>
* **El nombre "id_pelicula" aclara mejor el tipo de id, asi que reemplacé todos los id que hagan referencia a la pelicula por este mismo nombre(va a verse los cambios en el código).**<br>

#### Desanidado
*Decidí un apartado para esto dentro de ETL ya que requiere mayor desarrollo que simplemente hacer una columna*<br>
**Empecé con el segundo csv provisto** de donde sacamos cast y crew(columna donde se encuentran los directores), como pueden apreciar también desanide una columna innecesariamente porque en el momento no me dí cuenta, pero tampoco quise eliminar ese proceso, fue la primer columna que desanide y de ella me base para el resto(para el archivo .py deje solamente las cosas utilizadas más adelante del codigo).<br>
Para desanidar utilicé la función:<br>
```python
def desanidar_cast(row):
    cast_data = ast.literal_eval(row['cast'])
    desanidado = pd.json_normalize(cast_data)
    desanidado['id'] = row['id']
    return desanidado
 
```
Para esta función obtuve ayuda principal de chatgpt y luego para entenderla bien pedí que me expliqué cada parte. La función se aplica a cada fila del DataFrame original utilizando df.apply(desanidar_cast, axis=1). Se utiliza `ast.literal_eval(row["cast"])` para evaluar de forma segura la expresión literal de la columna "cast" y convertirla en una estructura de datos legible por Python, esto *permite tratar el contenido de la columna como una lista de diccionarios*. Luego, se utiliza `pd.json_normalize` para desanidar los datos y convertirlos en un DataFrame, esto *crea nuevas columnas para cada clave en los diccionarios de la lista*. Se agrega una columna adicional llamada "id" al DataFrame desanidado, que contiene el valor de la columna "id" de la fila original, asegurando que *cada fila desanidada tenga su correspondiente "id"*. **La función se ejecuta una vez por cada fila y devuelve un DataFrame desanidando esa fila específica, agregando en cada uno la columna "id_pelicula" con el id correspondiente a la fila que se desanida del dataframe original**.<br>
* *Esta función se reutilizo para la columna crew (ver archivo ETL.py o ETL.ipynb)*.<br>
* Guardo el desanidado de la columna cast en la variable "cast" y el desanidado de la columna crew en la variable "crew".
* Hay que concatenar los dataframe que ahora se encuentran en una serie compuesta por los dataframes de cada fila como datos, para ello primero hay que pasar la serie a lista y luego aplicar pd.concat en la lista, ignorando los indices (reiniciando los indices del dataframe final). Entonces ahora me quedo con los dos dataframe, del cual solo me es útil crew para las primeras 6 funciones: 
```python
crew=list(crew)
df_crew=pd.concat(crew, ignore_index=True)
```
* Eliminé las columnas innecesarias: "credit_id" y "profile_path".<br>

**Ahora desanido los datos de movies_dataset.csv**<br>
Utilizando la misma función que antes y los mismos pasos, solo que esta vez renombro a la columna a agregar de id como "id_pelicula", ya que dentro de cada dato anidado parece haber propios id's pero no puedo editar los nombres de estos hasta que haya desanidado y hecho los nuevos dataframes. Ademas como en este caso hay vacios hago que verifique si el array es vacio entonces que devuelva un dataframe vacio.<br>
También hay funciones en las que agregue más columnas de los datos originales, para que más adelante a la hora de hacer las funciones para la API se utilicen los datos dentro de un mismo df, en lugar de andar comparando y llamando datos de dos df distintos.<br>

**En el archivo .py hice una limpieza de datos innecesarios que trabajé en el .ipynb, asi corre más rápido y no ocupa espacio con df no utilizados, por eso en el archivo .ipynb van a ver que hay más df mientras que en el .py solo están los usados para todo el código.**

### Funciones API
- Para hacerlas utilice los dataframe que dividí desanidando (en mi caso en lugar de unirlos deje cada uno aparte).
- En cada una de las funciones de desanidado anteriores, agregue las columnas que necesitaba para estas funciones pedidas(ej agregue "revenue" al df que informa las colecciones por id de peliculas), y en la única que no podía (df_director) comparé el id_pelicula de este y de "data" dentro de la función, creando un dataframe dentro de esta que cumpliera el estar entre la lista generada de id's, también **realice un drop_duplicates()** de este dataframe creado asi no repetian filas generando returns, budget, etc, repetidos.
- La forma esencial de funcionamiento de estas funciones es agarrar los dataframe y a partir de estos crear sub dataframes dentro de la función en los que se filtró el df original. Luego de ello ya aplicado el filtro (ej: un df que contenga solo las peliculas que salieron en el año *x* del df "data" `data[data['release_year']==int(x)]`) generalmente con esto es suficiente y saco los calculos necesarios a una nueva variable, o los datos de las columnas que quiero en otra variable (pasandolos a listas).
- Para el caso de `get_director()` tuve que comparar las columnas del df_director para que tuvieran el nombre del director guardandolo en una nueva variable, siendo un nuevo df -vamos a nombrarlo 'a' para la explicación-. Se verifica que hayan filas del director, sino simplemente se devuelve que este no existe, o no es el nombre de un director.

## EDA
- El EDA se realizó en el archivo "EDA.ipynb", no hice un archivo .py porque lo consideré innecesario y en el jupyter notebook van a tener vista previa de todos los graficos y demas. De ser necesario también pueden correr el código sin problemas , no hay necesidad de cambiar ninguna ruta (los csv llamados son los pasados por etl que se encuentran guardados en la carpeta "csv").<br>
- Para el EDA se utilizaron todos los df aún si no eran utilizados para las primeras funciones hechas de la API (hay que analizar cada parametro y ver si para el sistema de recomendación es importante).

Lo primero que se me ocurrio fue juntar todos los df en uno solo, utilizando merge teniendo en cuenta la columna "id_pelicula" (que ya todos los df tienen con el mismo nombre). Pero para hacerlo habia que verificar que ciertos nombres de columnas no se pisen y que fueran todas necesarias.<br>
* Varios df tenian una columna de nombre "id" asi que lo primero que hice fue renombrar este a "nombredf_id" siendo "nombredf" no solamente parte de su nombre, sino que también la caracteristica más importante del df. Luego de este cambio se elimina la columna "id", ya innecesaria.
* Para el caso de "df_cast" nos encontramos con "id" y "cast_id", como si no hubiera que hacer ningun cambio y solo tirar la columna id, pero analizando justamente el id representante que yo necesitaba se encontraba en la columna "id" y el que se encuentra en la columna "cast_id" en realidad es un id propio de cada pelicula, por lo que termina reiniciando y no perteneciendo a una persona en especifico, caso contrario con id que si pertenecia a solo una persona. Se cambio el "cast_id" y se eliminó la columna "id".
* Para el caso de "df_belongs_collection"