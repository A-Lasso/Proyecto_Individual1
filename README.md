# Proyecto Individual 1
## Abril Lasso de la Vega

### ETL
Empece por hacer las transformaciones pedidas y necesarias, comenzando con las más fáciles.:<br>
* Empiezo por los datos del archivo "movies_dataset.csv".<br>
    * Eliminé las columnas pedidas ["video","imdb_id","adult","original_title","poster_path" , "homepage"], innecesarias que no van a ser utilizadas.<br>
    * Verifique los valores de budget y revenue para ver lo que me esperaba en el valor de la columna a crear "return". Al ver los valores de nada se ve como va a dominar el return 0, tanto por el lado de budget 0 (en donde decidí dejar return igual a 0)
    * Antes de crear la columna me aseguré de que los valores que fueran nulos se reemplazaran por 0, como nos pidieron (solamente la columna revenue contaba con vacios).
    * Elimino los vacios (filas) de la columna "release_date".
    * Solo por observación use el código "data.isna().sum()", asi veía los vacios que quedan y en qué columnas.
    * Ahora sí, cree la columna return, primero verificando el tipo de valores de cada columna, y luego asegurandome de pasar los valores de la columna budget de string a float. La columna return la cree realizando un ciclo (en el cual tuve que hacer zip para poder renombrar a los valores de cada columna como i y j) en el que si budget es distinto de cero se hace la división y se agrega el valor a la lista que en principio está vacía, y si budget es cero el valor que se agrega es cero a la lista. Luego esta lista es la contenedora de los valores de return y lo último por hacer es crear la nueva columna con estos valores.
    * Ahora paso a crear la siguiente columna pedida "release_year", para esto primero tuve que transformar la columna "release_date" a datetime y que en caso de que tire error (no es una fecha como tal o no esta en el formato correcto) me va a llenar con vacio. Luego cree la nueva columna de los años con `"data["release_year"]=data["release_date"].dt.year"` 
    * Decidi eliminar tres filas que eran completamente inusables, no solamente están llenas de vacios, sino que los pocos valores que tienen parecen estar intercambiados, y no sabría cómo sería el reordenamiento correcto. Justamente este desorden trajo mayores vacios, las fechas fueron imposibles de calcular. `data.drop(labels=[19730,29503,35587],axis=0,inplace=True)`
**Termine re acomodando las columnas del dataframe por simple gusto, el orden es a ojo y no cambia los valores ni los futuros resultados.**

#### Desanidado
*Decidi un apartado para esto dentro de ETL ya que requiere mayor desarrollo que simplemente hacer una columna*<br>

La función desanidar_cast se aplica a cada fila del DataFrame original utilizando df.apply(desanidar_cast, axis=1). Esto significa que la función se ejecuta una vez por cada fila y devuelve un DataFrame desanidado para esa fila específica