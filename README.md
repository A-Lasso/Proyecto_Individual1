# **Machine Learning Operations (MLOps)**
<p align="center">
<img src=png\MLOPS.png >
</p><br>

# Proyecto Individual 1
## Rol a desarrollar
Empezaste recientemente como Data Scientist en una start-up que provee servicios de agregación de plataformas de streaming. El mundo es bello y vas a crear tu primer modelo de ML que soluciona un problema de negocio: un sistema de recomendación que aún no ha sido puesto en marcha!<br>

Vamos a sus datos y nos damos cuenta que la madurez de los mismos es poca (ok, es nula 😭): Datos anidados, sin transformar, no hay procesos automatizados para la actualización de nuevas películas o series, entre otras cosas…. haciendo el trabajo imposible.<br>

Debes empezar desde 0, haciendo un trabajo rápido de Data Engineer y tener un MVP (Minimum Viable Product) para el cierre del proyecto! Tu cabeza va a explotar 🤯, pero al menos sabes cual es, conceptualmente, el camino que debes de seguir ❗. Así que te espantas los miedos y te pones manos a la obra 💪.<br>

(Casi textualmente copiado de la propuesta de proyecto original para que entiendan la esencia de este)

## TECNOLOGÍAS

- Python. (pandas, numpy, seaborn, matplotlib, uvicorn y FastApi)
- Render

## Resumen
Se realizan las funciones pedidas y los cambios pedidos por el proyecto (Algunos extra que se mencionan en la explicación extensa). Luego con FastApi se va comprobando que estas funciones y sus cambios se apliquen, viendo que FastApi corre y las funciones realizan su trabajo (no al principio pero se fueron afilando antes de la fecha de entrega).<br>
Se utiliza el archivo con las funciones y FastApi para subir todo a Render y correrlo como una pagina con la capacidad de compartirse y que otras personas la utilicen.(el archivo subido a render fue "API.py" y además el "requirements.txt" para que descargara las librerias necesarias).<br>
Si bien la idea principal parecia rondear en los modelos ML yo y ellos no nos llevamos bien, ya que intente ferozmente y no logre generarlo como queria, por eso es que realice la función de recomendación basada en filtros que esta más abajo de todo, da resultados, es útil, cumple para recomendar, y se llego al MVP que se pide del proyecto.

<br>
<br>
## Analisis profundo
**La explicación esta escrita desde el punto de vista de los archivos de jupyter notebook, su paso a paso y orden.**<br>
**En el código de los archivos .py hay comentarios más simples y cambios de orden, la explicación es la misma**

- En el archivo ETL.py se encuentran todas las transformaciones que hice y luego guardé los .csv ya limpios, ordenados y de la forma que quería.

- En el archivo API.py se tienen las funciones para la API, se traen los csv limpios, y se trabaja toda la parte de API allí.

- Recuerde que para que el código ETL le funcione correctamente, debe cambiar la ruta del archivo en el pd.read_csv, a la ruta en la que se encuentre este en su pc (Luego para el resto de archivos son usados los csv limpios, que se encuentran en la carpeta "csv", por lo tanto no necesita cambiar nada).<br>

- En el archivo ETL.ipynb además de encontrarse cómo fui avanzando y cada cosa que hice respecto al ETL, también se encuentran las funciones de la API(conforme las fui desarrollando en este archivo y editando) -es lo mismo a verlas en API.py, pero hay algunos codigo ejemplo y prueba-.<br>

- Todo el EDA se encuentra en el archivo EDA.ipynb, también se encuentra allí el avance respecto a la función de recomendación. Por el EDA se genero un dataframe distinto para la recomendación, por lo tanto se encuentra otro ETL dentro del archivo EDA.ipynb (utilizando ya los csv tratados anteriormente).

## Explicación profunda de cada parte.
Esta parte es para quienes quieran entender el código en profundidad sino no es necesario leerla. Esta escrito en lo que yo considero un lenguaje coloquial con el objetivo de que sea entendible para la mayoría de personas. Por eso también es tan extenso, creo que hay veces que no explicamos ciertos detalles que consideramos básicos y por eso luego las personas a las que les explicamos no son capaces de seguirnos. Con eso dicho hasta esta parte el resumen del proyecto, lo siguiente es un poco tedioso.

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

* **Terminé re acomodando las columnas del dataframe por simple gusto, el orden es a ojo y no cambia los valores ni los futuros resultados.**<br>
* **El nombre "id_pelicula" aclara mejor el tipo de id, asi que reemplacé todos los id que hagan referencia a la pelicula por este mismo nombre(va a verse los cambios en el código).**<br>

* Realice un drop_duplicates() aún si no fue parte de lo pedido.

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
* Para el caso de "df_cast" nos encontramos con "id" y "cast_id", como si no hubiera que hacer ningun cambio y solo tirar la columna id, pero analizando justamente el id representante que yo necesitaba se encontraba en la columna "id", y el que se encuentra en la columna "cast_id" en realidad es un id propio de cada pelicula, por lo que termina reiniciando y no perteneciendo a una persona en especifico, caso contrario con id que si pertenecia a solo una persona. Se cambio el "cast_id" y se eliminó la columna "id".
* Conforme se fue avanzando y analizando en el merge fui quitando dataframes que contenian los datos innecesarios, que generaban más vacios y no tenian correlaciones ni utilidad para futuras predicciones.
<p align="center">
<img src=png\Primer_correlación.png height="600">
</p>
Si bien parece que hay una conexión entre cast_id y las peliculas, esta termina siendo insignificante a comparación de no tener esta columna, con ella se llena de vacios y llegamos a 600k filas, mientras que sin ellas quedamos con 100k (mucho más optimizado, comodo y útil).<br>
<p align="center">
<img src=png\Segunda_correlación.png height="600">
</p>
<br>
La única razón que no saco el genero es que estas correlaciones se basan completamente en parecidos de la peliculas, por lo tanto es completamente logico que no se aprecie en sentido de los gustos de las personas, y creo que el genero es una de las cosas más importantes a la hora de recomendar.<br>
Además por pelicula tampoco se aprecia su cantidad de generos en estos analisis, siendo que por cada genero que tengan sus filas se multiplicaron cambiando el id.(más adelante se analizan peliculas por genero)<br>

* Entonces en cuanto a correlaciones el genero no tiene ya que no debería existir una relación lógica entre los generos de distintas peliculas. Pero no podemos quitarlos ya que para predecir/recomendar peliculas parecidas a una ingresada el genero es una de las primeras cosas a la que prestar atención.

Siguiendo:<br>

Decidi acortar Las filas del dataframe "df_todo" al poner un minimo a cumplir en las columnas 'vote_average','vote_count' y 'popularity'. 
* Antes se analizo cada una con un histograma para ver la densidad de los valores en cada columna, desde ahi decidir mas o menos dónde debería estar el filtro. <br>
* Analicé cuántas peliculas me sacadaba y si realmente era lo correcto poner x valor de filtro, si era mucho fui viendo cuántas peliculas me quedaban si iba aplicando otro filtro menor, y con esto analicé qué valores serian los mejores y decidí el que me convencia. 
* Resulto que por la columna "popularity" no me conviene filtrar, aun asi decidí hacerlo si tenian una popularidad menor a 1 ya que no quitaba tantas peliculas, y si está la popularidad para algo es. (Se entiende que si una pelicula no es popular por más buena que sea para la gente que la vió es muy probable que tenga un aspecto negativo, la razón por la que no se consume tanto)
* Analicé los nulos y resulto que no se perdían muchas peliculas ni quedaba información a medias, como mucho se pierde algún director de alguna pelicula que tenga más de uno(los quite para tener información completa).

`Antes de los cambios`<br>
<p align="center">
<img src=png\dist_cant_votos1.png height="400">
</p><br>

<p align="center">
<img src=png\dist_popularidad1.png height="400">
</p><br>

<p align="center">
<img src=png\dist_average1.png height="400">
</p><br>

`Después de los cambios`<br>

<p align="center">
<img src=png\dist_cant_votos2.png height="400">
</p><br>

<p align="center">
<img src=png\dist_popularidad2.png height="400">
</p><br>

<p align="center">
<img src=png\dist_average2.png height="400">
</p><br>

`Nube de palabras de los titulos`<br>
<p align="center">
<img src=png\Nube_Palabras.png >
</p><br>

`Histograma de generos desde df_generos (genres.csv sin editar)`<br>
<p align="center">
<img src=png\hist_genre.png >
</p><br>

`Histograma de generos desde el dataframe para recomendación`<br>
<p align="center">
<img src=png\hist_genre2.png >
</p><br>

## Función de recomendación
La idea era una función de aprendizaje que diera la mejor recomendación posible.<br>
No me fue posible, intente con varios modelos y de varias formas, termine con muchos errores o con la misma pelicula de devolución (no es la idea). Intente arreglar cada error, estuve con eso dias enteros, asi que llegue a realizar una función de filtro que recomiende en base a que tenga los mismos generos y además la 5ta recomendación (si se cumplen los requisitos) es la mejor pelicula del mismo director a la ingresada<br>
Esta función puede devolver otro resultado si es que la pelicula *no se encuentra en la base de datos*, para lo cual avisa justamente que no se tiene la pelicula y por lo tanto *no se puede usar su información para recomendar*.

```python
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te devuelve una recomendación de 5 peliculas en un diccionario
       Esta recomendación esta ordenada de la mejor a la peor.
    '''
    df_director2=df_director.copy()
    df_director2['director_id']=df_director2['id']
    df_director2['director_name']=df_director2['name']
    df_director2.drop(columns=['id','name','department','job','gender'],inplace=True)

    id_pel=list(data['id_pelicula'][data['title']==titulo])
    df=df_genres[df_genres['id_pelicula'].isin(id_pel)].drop(columns='id_pelicula').copy()
    df.drop_duplicates(inplace=True)

    # Hago un primer filtro para quedarme con las filas que tengan alguno
    # de los generos de la pelicula ingresada.
    genre=list(df['id'].unique())

    if len(genre)==0:
        return "La pelicula {} no se encuentra en la base de datos para recomendar a partir de ella".format(titulo)

    # En este primer filtro me fijo que las peliculas pertenezcan a los mismos generos
    primer_filtro=df_todo[df_todo['genre_id'].isin(genre)]
    primer_filtro=primer_filtro[~primer_filtro['id_pelicula'].isin(id_pel)]

    # Me deshago de las peliculas que tengan menos coincidencia de generos 
    # De forma tal que si no se repiten cantidad de generos menos 1 nos deshacemos de ellas
    # Esto significa que como minimo deben tener un genero menos que el de la pelicula.
    
    x=len(genre)-1
    filtro_1 = primer_filtro.groupby('id_pelicula')['id_pelicula'].transform('count') >= x
    primer_filtro = primer_filtro[filtro_1].copy()

    primer_filtro=primer_filtro.sort_values(by='vote_average',ascending=False).copy()
    primer_filtro.drop_duplicates(subset=['id_pelicula','release_year'],inplace=True,ignore_index=True)
    
    
    # Segundo filtro para devolver la mejor pelicula de alguno de los directores

    director=df_director2[df_director2['id_pelicula'].isin(id_pel)]
    director=list(director['director_id'].unique())
    segundo_filtro=df_todo[df_todo['director_id'].isin(director)]
    segundo_filtro=segundo_filtro[~segundo_filtro['id_pelicula'].isin(id_pel)]
    segundo_filtro=segundo_filtro.sort_values(by='vote_average',ascending=False,ignore_index=True).copy()
    
    # Dejo al dataframe de los directores solamente como un dataframe que 
    # contenga sus id y nombres.
    df_director2.drop(columns='id_pelicula',inplace=True)
    df_director2.drop_duplicates(inplace=True)

    # Mejores 5 peliculas desde el punto de vista de 
    primeros=primer_filtro.head(5)

    if segundo_filtro['id_pelicula'].count()!=0:

        primeros=primeros.append(segundo_filtro.head(1),ignore_index=True)
        primeros=pd.merge(primeros,df_director2,on='director_id',how='left')
        primeros.drop_duplicates(inplace=True)

        if primeros['title'].count()==6:
            primeros.drop(index=4,inplace=True)

        Nombre=list(primeros['title'])
        Anio=list(primeros['release_year'])
        Director=list(primeros['director_name'])

    else:
        primeros=pd.merge(primeros,df_director2,on='director_id',how='left')
        Nombre=list(primeros['title'])
        Anio=list(primeros['release_year'])
        Director=list(primeros['director_name'])

    

    return {'Nombre': Nombre,'Anio estreno':Anio,'Director':Director}
```

Se ve complicada pero no lo es. Se basa en quedarse con las mejores peliculas que cumplan el tener los mismos generos (como mucho les puede faltar uno de los generos de la pelicula ingresada).De antemano nos aseguramos de eliminar todas las peliculas duplicadas que tengan mismo id y año de estreno, son pocos los casos(17 si no estoy mal) y sus diferencias entre los valores de las columnas es muy poca, que nos quedemos con una o la otra no nos cambia, además esto elimina las filas repetidas por distintos generos id (ya no necesarios), optimizando la velocidad y ocupando menos espacio.<br>
Luego ordena por la columna de "vote_average" y nos quedamos con las 5 primeras peliculas recomendadas. A lo que, utilizando "segundo_filtro", le agregamos una pelicula que sea del mismo director, sin ser necesariamente de los mismos generos, y la dejamos como la 5ta pelicula a recomendar, siendo la mejor pelicula del director (basado en vote_average). Si es que el director no tiene otras peliculas además de la ingresada, y por lo tanto este dataframe quedaría vacio, se regresan solamente las 5 primeras peliculas basadas en los generos.
* El problema principal de esta función es que al basarse completamente en generos, las peliculas que no cuentan con esta información (por suerte bastante pocas) no van a poder usarse para recomendar.
* Siempre entre cada cambio de los dataframes que vamos creando (copiar,filtrar,eliminar columnas) hacemos un drop_duplicates() para asegurar que si alguno de esos cambios genero filas repetidas -ej: la diferencia entre las filas estaba en la columna eliminada- que deje una.
