# Proyecto Individual 1
## Abril Lasso de la Vega
**Este readme esta escrito desde el punto de vista del archivo de jupyter notebook, su paso a paso y orden.**<br>
**En el código del archivo .py hay comentarios más simples y cambios de orden, la explicación sirve para ambos.**

- Recuerde que para que el código le funcione correctamente, debe cambiar la ruta del archivo en el pd.read_csv, a la ruta en la que se encuentre este en su pc.<br>

### ETL
Empecé por hacer las transformaciones pedidas y necesarias, comenzando con las más fáciles:<br>
* Empiezo por los datos del archivo "movies_dataset.csv".<br>
    * Eliminé las columnas pedidas ["video","imdb_id","adult","original_title","poster_path" , "homepage"], innecesarias que no van a ser utilizadas.<br>
    * Verifique los valores de budget y revenue para ver lo que me esperaba en el valor de la columna a crear "return". Al ver los valores de nada se ve como va a dominar el return 0, tanto por el lado de budget 0 (en donde decidí dejar return igual a 0)
    * Antes de crear la columna me aseguré de que los valores que fueran nulos se reemplazaran por 0, como nos pidieron (solamente la columna revenue contaba con vacios).
    * Elimino los vacios (filas) de la columna "release_date".
    * Solo por observación use el código "data.isna().sum()", asi veía los vacios que quedan y en qué columnas.
    * Ahora sí, cree la columna return, primero verificando el tipo de valores de cada columna, y luego asegurandome de pasar los valores de la columna budget de string a float. La columna return la cree realizando un ciclo (en el cual tuve que hacer zip para poder renombrar a los valores de cada columna como i y j) en el que si budget es distinto de cero se hace la división y se agrega el valor a la lista que en principio está vacía, y si budget es cero el valor que se agrega es cero a la lista. Luego esta lista es la contenedora de los valores de return y lo último por hacer es crear la nueva columna con estos valores.
    * Ahora paso a crear la siguiente columna pedida "release_year", para esto primero tuve que transformar la columna "release_date" a datetime y que en caso de que tire error (no es una fecha como tal o no esta en el formato correcto) me va a llenar con vacio. Luego cree la nueva columna de los años con `"data["release_year"]=data["release_date"].dt.year"` 
    * Eliminé tres filas que eran completamente inusables, no solamente están llenas de vacios, sino que los pocos valores que tienen parecen estar intercambiados, y no sabría cómo sería el reordenamiento correcto. Justamente este desorden trajo mayores vacios, las fechas fueron imposibles de calcular. `data.drop(labels=[19730,29503,35587],axis=0,inplace=True)`.<br>

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
Para esta función obtuve ayuda principal de chatgpt y luego para entenderla bien pedí que me expliqué cada parte. La función se aplica a cada fila del DataFrame original utilizando df.apply(desanidar_cast, axis=1). Se utiliza `ast.literal_eval(row["cast"])` para evaluar de forma segura la expresión literal de la columna "cast" y convertirla en una estructura de datos legible por Python, esto *permite tratar el contenido de la columna como una lista de diccionarios*. Luego, se utiliza `pd.json_normalize` para desanidar los datos y convertirlos en un DataFrame, esto *crea nuevas columnas para cada clave en los diccionarios de la lista*. Se agrega una columna adicional llamada "id" al DataFrame desanidado, que contiene el valor de la columna "id" de la fila original, asegurando que *cada fila desanidada tenga su correspondiente "id"*. **La función se ejecuta una vez por cada fila y devuelve un DataFrame desanidando esa fila específica, agregando en cada uno la columna id con el id correspondiente a la fila que se desanida del dataframe original**.<br>
* Esta función se reutilizo para la columna crew, donde se le cambió el nombre y también la columna a desanidar dentro de la función.<br>
* Guardo el desanidado de la columna cast en la variable "cast" y el desanidado de la columna crew en la variable "crew".
* Hay que concatenar los dataframe que ahora se encuentran en una serie compuesta por los dataframes como datos, para ello primero hay que pasar la serie a lista y luego aplicar pd.concat en la lista, ignorando los indices (reiniciando los indices del dataframe final). Entonces ahora me quedo con los dos dataframe, del cual solo me es útil crew: 
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
- En cada una de las funciones de desanidado agregue las columnas que necesitaba para estas funciones, y en la única que no podía (df_crew) comparé el id_pelicula dentro de la función y cree un dataframe dentro de esta que cumpliera el estar entre la lista generada de id's, también **realice un drop_duplicates()** de este dataframe creado asi no repetian filas, repitiendo valores de filas completas (exactamente mismas filas), generando returns, budget, etc, repetidos.

