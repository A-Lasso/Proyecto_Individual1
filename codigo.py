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
print(data["budget"].values)
print(type(data["budget"][0]))

# Ahora la idea es hacer la división pero con un try and except
# en donde, si la división va a tirar un error sea porque budget es cero o vacio,
# se le deja el valor cero a la nueva columna.
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

# Usar el otro archivo csv provisto

# Desanidar los datos (como solo necesitamos los directores, desanidamos los datos de la columna "crew")

# Esta función esta mejor explicada en el readme

def desanidar_crew(row):
    cast_data = ast.literal_eval(row['crew'])
    desanidado = pd.json_normalize(cast_data)
    desanidado['id'] = row['id']
    return desanidado

