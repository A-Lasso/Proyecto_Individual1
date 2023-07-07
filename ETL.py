# Se importan las librerias usadas en el código
import pandas as pd
import numpy as np
import ast

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

# Elimino los duplicados
# Filas que se detectan exactamente iguales.

data.drop_duplicates(inplace=True)

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

def desanidar_cast(row):
    cast_data = ast.literal_eval(row['cast'])
    desanidado = pd.json_normalize(cast_data)
    desanidado['id_pelicula'] = row['id_pelicula']
    return desanidado

# Agrego el "id_pelicula" 
# asi me aseguro que el mismo id tenga el mismo nombre en todos los df
df2["id_pelicula"]=df2["id"]
df2.drop(columns=["id"],inplace=True)

# Aplico la función y me quedo con una serie en la que cada dato es un dataframe (por cada fila un dataframe).

crew=df2.apply(desanidar_crew, axis=1).reset_index(drop=True)
cast=df2.apply(desanidar_cast, axis=1).reset_index(drop=True)

# Transformo la serie en lista para poder juntar todos los dataframes pertenecientes a esta.

crew=list(crew)
df_crew=pd.concat(crew, ignore_index=True)
cast=list(cast)
df_cast=pd.concat(cast, ignore_index=True)

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
# Es innecesario asi que no lo corro.
#des_spoken_languages=list(des_spoken_languages)
#df_spoken_languages=pd.concat(des_spoken_languages, ignore_index=True)

#production_countries
des_production_countries=list(des_production_countries)
df_production_countries=pd.concat(des_production_countries, ignore_index=True)

#production_companies
des_production_companies=list(des_production_companies)
df_production_companies=pd.concat(des_production_companies, ignore_index=True)

# Elimino las columnas anidadas del dataframe "data" ahora ya innecesarias.

data.drop(columns=["belongs_to_collection","genres","spoken_languages","production_countries","production_companies"],inplace=True)

# Ahora guardo los nuevos csv ya limpios 
# Usamos: data,df_belongs_to_collection,df_production_countries,df_production_companies,df_crew

# Ya se encuentran guardados en la carpeta "csv", si desea guardarlos en otra carpeta
# Solo saque el "#" delante de cada una y cambie la ruta donde guardar.
#data.to_csv(r"D:\Programacion\DataScience_Henry\Proyecto_Individual1\csv\data.csv",index=False)
#df_belongs_to_collection.to_csv(r"D:\Programacion\DataScience_Henry\Proyecto_Individual1\csv\collection.csv",index=False)
#df_production_countries.to_csv(r"D:\Programacion\DataScience_Henry\Proyecto_Individual1\csv\countries.csv",index=False)
#df_production_companies.to_csv(r"D:\Programacion\DataScience_Henry\Proyecto_Individual1\csv\companies.csv",index=False)
#df_crew.to_csv(r"D:\Programacion\DataScience_Henry\Proyecto_Individual1\csv\crew.csv",index=False)
#df_cast.to_csv(r"D:\Programacion\DataScience_Henry\Proyecto_Individual1\csv\cast.csv",index=False)