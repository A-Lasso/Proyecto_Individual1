# Se importan las librerias usadas en el código
import pandas as pd
import numpy as np
import ast
from fastapi import FastAPI

# Transformaciones pedidas y necesarias
# comenzando con las más fáciles
data=pd.read_csv(r"D:\Programacion\DataScience_Henry\Proyecto_Individual1\Dataset\movies_dataset.csv")
df2=pd.read_csv(r"D:\Programacion\DataScience_Henry\Proyecto_Individual1\Dataset\credits.csv")

data.drop(columns=["video","imdb_id","adult","original_title","poster_path" , "homepage"],inplace=True)
data.loc[data["revenue"].isna(),"revenue"]=0
data.loc[data["budget"].isna(),"budget"]=0
data.dropna(subset=["release_date"],inplace=True)

# Creo la columna "return"
data["budget"]=pd.to_numeric(data["budget"],errors="coerce")
print(type(data["budget"][0]))

# Ahora la idea es hacer la división pero con un try and except
# en donde, si la división va a tirar un error porque budget es vacio (ya aclaramos que tiene que ser distinto de cero),
# se le deja el valor cero al nuevo valor de la lista.
# Y si budget es cero entra en else y también se le agregaría un valor cero.

columna=[]
for i, j in zip(data["revenue"], data["budget"]):
    if j!=0:
        try:
            columna.append(float(i)/(float(j)))
        except:
            columna.append(0)
    else:
        columna.append(0)

data["return"]=columna

# Creo la columna "release_year"
# Va a tener los años en los que salió la pelicula, esta información la sacamos de la columna "release_date", a la cual justamente paso anteriormente a tipo timestamp

data["release_date"] = pd.to_datetime(data["release_date"], format="%Y-%m-%d", errors="coerce")
data["release_year"]=data["release_date"].dt.year


# Estas tres filas estan llenas de valores nulos, y los pocos que tienen están mezclados (no se encuentran en su columna apropiada)
# al ser los tres inutilizables, tome la decisión de directamente quitarlos del dataframe

data.drop(labels=[19730,29503,35587],axis=0,inplace=True)

# Creo una columna "id_pelicula"(la cual es la misma que id pero le cambiamos el nombre) ya que me parece un nombre comodo para tratar más adelante.

data["id_pelicula"]=pd.to_numeric(data["id"],downcast="integer") # Me aseguro que quede en formato numerico para después poder comparar con este id

# La forma en la que yo quiero ordenadas las columnas

data=data[['id_pelicula', 'title','overview','status','runtime','popularity','belongs_to_collection','tagline','genres','original_language','spoken_languages','vote_average','vote_count','release_date','release_year','production_countries','production_companies','budget','revenue','return']]

# Desanidar los datos (como solo necesitamos los directores, desanidamos los datos de la columna "crew")


# Esta función esta mejor explicada en el readme
def desanidar_crew(row):
    '''
    Se  aplica de la forma:
    - nueva_serie=dataframe.apply(desanidar_crew, axis=1).reset_index(drop=True).
    - Devuelve una serie en la que cada dato es un dataframe perteneciente a cada fila.
    - Esta función solo funciona para desanidar columnas llamadas "crew".
    Para cambiar este valor se copia y pega la misma función y se cambia este nombre.
    Si la columna tiene vacios o valores no aceptables en las transformaciones tira errores.
    (más adelante se editó esto para columnas que tenían vacios).
    '''
    cast_data = ast.literal_eval(row['crew'])
    desanidado = pd.json_normalize(cast_data)
    desanidado['id_pelicula'] = row['id_pelicula']

    return desanidado

# Agrego el "id_pelicula" 
# asi me aseguro que el mismo id tenga el mismo nombre en todos los df
df2["id_pelicula"]=df2["id"]
df2.drop(columns=["id"],inplace=True)

# Aplico la función y me quedo con una serie en la que cada dato es un dataframe (por cada fila un dataframe).

crew=df2.apply(desanidar_crew, axis=1).reset_index(drop=True)

# Transformo la serie en lista para poder juntar todos los dataframes pertenecientes a esta.

crew=list(crew)
df_crew=pd.concat(crew, ignore_index=True)

# Elimino las columnas que considero innecesarias
df_crew.drop(columns=["credit_id","profile_path"],inplace=True)

# traigo la función anteriormente usada
# Cambio en cada una la columna a desanidar
# Noté que me salia error y se me ocurrió que podía ser debido a que en este caso las columnas tienen valores vacios.
# Asi que ahora le agrego a las funciones que es caso de vacios regrese un dataframe vacio.

def desanidar_belongs(row):
    cast_data=row['belongs_to_collection']
    if np.all(pd.isna(cast_data)) or cast_data == '':
        return pd.DataFrame()  # Retorna un DataFrame vacío si la celda está vacía
    cast_data = ast.literal_eval(cast_data)
    desanidado = pd.json_normalize(cast_data)
    desanidado['id_pelicula'] = row['id_pelicula']
    desanidado['revenue']=row['revenue']
    desanidado['budget']=row['budget']
    # Agrego estas columnas porque más adelante para las funciones de API es mucho más útil y fácil
    return desanidado

def desanidar_genres(row):
    cast_data=row['genres']
    if np.all(pd.isna(cast_data)) or cast_data == '':
        return pd.DataFrame()  # Retorna un DataFrame vacío si la celda está vacía
    cast_data = ast.literal_eval(cast_data)
    desanidado = pd.json_normalize(cast_data)
    desanidado['id_pelicula'] = row['id_pelicula']
    return desanidado

def desanidar_spoken_languages(row):
    cast_data=row['spoken_languages']
    if np.all(pd.isna(cast_data))  or cast_data == '':
        return pd.DataFrame()  # Retorna un DataFrame vacío si la celda está vacía
    cast_data = ast.literal_eval(cast_data)
    desanidado = pd.json_normalize(cast_data)
    desanidado['id_pelicula'] = row['id_pelicula']
    return desanidado

def desanidar_production_countries(row):
    cast_data=row['production_countries']
    if np.all(pd.isna(cast_data)) or cast_data == '':
        return pd.DataFrame()  # Retorna un DataFrame vacío si la celda está vacía
    cast_data = ast.literal_eval(cast_data)
    desanidado = pd.json_normalize(cast_data)
    desanidado['id_pelicula'] = row['id_pelicula']
    return desanidado

def desanidar_production_companies(row):
    cast_data=row['production_companies']
    if np.all(pd.isna(cast_data))  or cast_data == '':
        return pd.DataFrame()  # Retorna un DataFrame vacío si la celda está vacía
    cast_data = ast.literal_eval(row['production_companies'])
    desanidado = pd.json_normalize(cast_data)
    desanidado['id_pelicula'] = row['id_pelicula']
    desanidado['revenue']=row['revenue']
    return desanidado

# se desanida cada columna
# personalmente prefiero quedarme con cada dato desanidado como dataframe aparte

des_belongs=data.apply(desanidar_belongs, axis=1).reset_index(drop=True)
des_genres=data.apply(desanidar_genres, axis=1).reset_index(drop=True)
des_spoken_languages=data.apply(desanidar_spoken_languages, axis=1).reset_index(drop=True)
des_production_countries=data.apply(desanidar_production_countries, axis=1).reset_index(drop=True)
des_production_companies=data.apply(desanidar_production_companies, axis=1).reset_index(drop=True)


#
# Hago lista a la serie para poder concatenar cada uno de los dataframes ahora enlistados

des_belongs=list(des_belongs)
df_belongs_to_collection=pd.concat(des_belongs, ignore_index=True)
# Tiro estas columnas que me parecen innecesarias.
df_belongs_to_collection.drop(columns=["poster_path","backdrop_path"],inplace=True)

# Ahora repetimos lo mismo en el resto de df

# genres
des_genres=list(des_genres)
df_genres=pd.concat(des_genres, ignore_index=True)

#spoken_languages
des_spoken_languages=list(des_spoken_languages)
df_spoken_languages=pd.concat(des_spoken_languages, ignore_index=True)

#production_countries
des_production_countries=list(des_production_countries)
df_production_countries=pd.concat(des_production_countries, ignore_index=True)

#production_companies
des_production_companies=list(des_production_companies)
df_production_companies=pd.concat(des_production_companies, ignore_index=True)

# Elimino las columnas anidadas del dataframe "data" ahora ya innecesarias.

data.drop(columns=["belongs_to_collection","genres","spoken_languages","production_countries","production_companies"],inplace=True)

# Funciones para la API 

def peliculas_idioma(idioma):
    '''
    - Ingresa el idioma, sale la cantidad de peliculas estrenadas en ese idioma.

    - Debe ingresar el abreviado del idioma a buscar, las opciones son las de la siguiente lista:
    ['en', 'fr', 'zh', 'it', 'fa', 'nl', 'de', 'cn', 'ar', 'es', 'ru',
    'sv', 'ja', 'ko', 'sr', 'bn', 'he', 'pt', 'wo', 'ro', 'hu', 'cy',
    'vi', 'cs', 'da', 'no', 'nb', 'pl', 'el', 'sh', 'xx', 'mk', 'bo',
    'ca', 'fi', 'th', 'sk', 'bs', 'hi', 'tr', 'is', 'ps', 'ab', 'eo',
    'ka', 'mn', 'bm', 'zu', 'uk', 'af', 'la', 'et', 'ku', 'fy', 'lv',
    'ta', 'sl', 'tl', 'ur', 'rw', 'id', 'bg', 'mr', 'lt', 'kk', 'ms',
    'sq', nan, 'qu', 'te', 'am', 'jv', 'tg', 'ml', 'hr', 'lo', 'ay',
    'kn', 'eu', 'ne', 'pa', 'ky', 'gl', 'uz', 'sm', 'mt', 'hy', 'iu',
    'lb', 'si']
    '''
    idioma=idioma.strip()
    count1= str(data["original_language"][data["original_language"]==idioma].count())

    return count1 + ' cantidad de películas fueron estrenadas en '+'"' + idioma+ '"'

def peliculas_duracion(Pelicula):
    '''
    Debe escribir el titulo correctamente, es decir, como esta escrito originalmente (buscar en internet), en inglés y con las mayúsculas correctas.
    '''
    Pelicula=Pelicula.strip()
    dur=data["runtime"][data["title"]==Pelicula].values[0]
    Anio=int(data["release_year"][data["title"]==Pelicula].values[0])
    
    return Pelicula + ". Duración:"+ str(dur) + " min."+" Año:"+ str(Anio)

def franquicia(Franquicia):
    '''
    - Para esta función se debe escribir bien el nombre de la pelicula, exactamente al publicado oficial.
    - Luego del nombre de la pelicula se debe agregar la palabra "Collection", exactamente como esta escrita entre las comillas.
    '''
    Franquicia=Franquicia.strip()
    df=df_belongs_to_collection[df_belongs_to_collection["name"]==Franquicia]
    
    # Me aseguro que esten en mismo tipo de dato.
    cant=float(df["name"].count())
    rev=float(df["revenue"].sum())
    
    return "La franquicia "+ Franquicia + " posee "+ str(cant) +" peliculas, una ganancia total de "+ str(rev) +" y una ganancia promedio de "+ str(rev/cant) +""

def peliculas_pais(Pais):
    '''
    - Recibe el Pais y devuelve la cantidad de peliculas producidas en este.
    - El idioma en el que se debe escribir el nombre del país es inglés, respetando los espacios y mayúsculas de cada nombre.
    - Si no le sale, verifique que esta escribiendo bien el país.
    '''
    Pais=Pais.strip()
    cant = df_production_countries["name"][df_production_countries["name"]==Pais].count()
    
    return "Se produjeron " + str(cant) + " películas en el país" + Pais

def productoras_exitosas(Productora):
    '''
    - Recibe la productora y devuelve el revenue total que obtuvo y la cantidad de peliculas realizadas.
    '''
    Productora=Productora.strip()
    df=df_production_companies[df_production_companies['name']==Productora]
    

    suma=df['revenue'].sum()
    cant= df['name'].count()

    return "La productora "+ Productora + " ha tenido un revenue de " + str(suma) + " y realizó " + str(cant) + " peliculas."

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

