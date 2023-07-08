# Se importan las librerias usadas en el código
import pandas as pd
import numpy as np
from fastapi import FastAPI


# Usamos: data,df_belongs_to_collection,df_production_countries,df_production_companies,df_crew

data=pd.read_csv("csv/data.csv")
df_belongs_to_collection=pd.read_csv("csv/collection.csv")
df_production_countries=pd.read_csv("csv/countries.csv")
df_production_companies=pd.read_csv("csv/companies.csv")
df_crew=pd.read_csv("csv/crew.csv")
df_genres=pd.read_csv("csv/genres.csv")
df_cast=pd.read_csv("csv/cast.csv")

# Preparo el df para ML
data2=data.copy()
df_crew2=df_crew.copy()
df_cast2=df_cast.copy()
df_genres2=df_genres.copy()
df_belongs_to_collection2=df_belongs_to_collection.copy()

data2.drop(columns=['title','overview','runtime','tagline','original_language','release_date','status'],inplace=True)

df_genres2['genre_id']=df_genres2['id']
df_genres2.drop(columns=['id','name'],inplace=True)

df_crew2['crew_id']=df_crew2['id']
df_crew2.drop(columns=['gender','name','department','job','id'],inplace=True)

df_cast2['cast_id']=df_cast2['id']
df_cast2.drop(columns=['id','name','gender','order','character'],inplace=True)

df_belongs_to_collection2['collection_id']=df_belongs_to_collection2['id']
df_belongs_to_collection2.drop(columns=['name','id','revenue','budget'],inplace=True)


df_todo=pd.merge(data2,df_genres2,on='id_pelicula',how='left')
df_todo=pd.merge(df_todo,df_crew2,on='id_pelicula',how='left')
df_todo=pd.merge(df_todo,df_cast2,on='id_pelicula',how='left')
df_todo=pd.merge(df_todo,df_belongs_to_collection2,on='id_pelicula',how='left')

df_todo.loc[df_todo["collection_id"].isna(),"collection_id"]=0

# En EDA.ipynb ya analizamos los mejores hiperparametros con Random Search.
# Preferi un modelo de K vecinos ya que se basa en las semejanzas de los datos
# Para predecir.




# instanciamos FastAPI

app = FastAPI()

# Funciones para la API 

@app.get("/peliculas/idioma/{idioma}")
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
    'sq', 'qu', 'te', 'am', 'jv', 'tg', 'ml', 'hr', 'lo', 'ay',
    'kn', 'eu', 'ne', 'pa', 'ky', 'gl', 'uz', 'sm', 'mt', 'hy', 'iu',
    'lb', 'si']
    '''
    idioma=idioma.strip()
    count1= str(data["original_language"][data["original_language"]==idioma].count())

    return "{} cantidad de películas fueron estrenadas en '{}' ".format(count1,idioma)

@app.get("/peliculas/duracion/{Pelicula}")
def peliculas_duracion(Pelicula):
    '''
    Debe escribir el titulo correctamente, es decir, como esta escrito originalmente (buscar en internet), en inglés y con las mayúsculas correctas.
    Devuelve un diccionario.
    Si hay una sola pelicula con ese nombre, devuelve la duración y su año de estreno.
    De haber más de una con ese nombre, devuelve una lista de duración y otra de los años, en las que coinciden sus ordenes (primer indice de la duración es de la pelicula que salió en el primer indice de los años, asi sucesivamente).
    En caso de escribir un nombre que no se encuentre en la base de datos, devuelve: "No hay pelicula con ese titulo".
    '''
    Pelicula=Pelicula.strip()
    cant=int(data["runtime"][data["title"]==Pelicula].count())
    df=data
    # Cambio los datos del año a int asi se ve mejor
    df["release_year"]=pd.to_numeric(df["release_year"],downcast="integer")
    if cant>1:
        dur=list(df["runtime"][df["title"]==Pelicula].values)
        Anio=list(df["release_year"][df["title"]==Pelicula].values)

    elif cant==1:
        dur=str(df["runtime"][df["title"]==Pelicula].values[0])
        Anio=str(int(df["release_year"][df["title"]==Pelicula].values[0])) 
    else:
        return "No hay pelicula con ese titulo"
       
    return {'Pelicula ':Pelicula,'Duracion':dur,'Anio':Anio}

@app.get("/franquicia/{Franquicia}")
def franquicia(Franquicia:str):
    '''
    - Para esta función se debe escribir bien el nombre de la pelicula, exactamente al publicado oficial.
    - Luego del nombre de la pelicula se debe agregar la palabra "Collection", exactamente como esta escrita (sin las comillas).
    '''
    Franquicia=Franquicia.strip()
    df=df_belongs_to_collection[df_belongs_to_collection["name"]==Franquicia]
    
    # Me aseguro que esten en mismo tipo de dato.
    cant=float(df["name"].count())
    rev=float(df["revenue"].sum())
    if df['name'].count().sum()==0:
        return "No se encuentra la franquicia {}".format(Franquicia)
    else:
        if cant!=0:
            prom=str(rev/cant)
        else:
            prom='0'
    return "La franquicia "+ Franquicia + " posee "+ str(cant) +" peliculas, una ganancia total de "+ str(rev) +" y una ganancia promedio de "+ prom +""

@app.get("/peliculas/pais/{Pais}")
def peliculas_pais(Pais:str):
    '''
    - Recibe el Pais y devuelve la cantidad de peliculas producidas en este.
    - El idioma en el que se debe escribir el nombre del país es inglés, respetando los espacios y mayúsculas de cada nombre.
    - Si no le sale, verifique que esta escribiendo bien el país.
    '''
    Pais=Pais.strip()
    cant = df_production_countries["name"][df_production_countries["name"]==Pais].count()
    if cant==0:
        return "Este país no ha realizado peliculas o se encuentra mal escrito."
    
    return {"Pais": Pais,"Cantidad":cant}

@app.get("/productoras_exitosas/{Productora}")
def productoras_exitosas(Productora:str):
    '''
    - Recibe la productora y devuelve el revenue total que obtuvo y la cantidad de peliculas realizadas.
    '''
    Productora=Productora.strip()
    df=df_production_companies[df_production_companies['name']==Productora]
    if df['name'].count().sum()==0:
        return "No se encuentran datos de esta productora."

    suma=df['revenue'].sum()
    cant= df['name'].count()

    return {"Productora": Productora , "Revenue ": suma ,  "Cantidad": cant}

@app.get("/director/{nombre_director}")
def get_director(nombre_director:str):
    '''
    - Toma un solo nombre a la vez.

    Devuelve en un diccionario= el director con su exito (suma de return de todas sus peliculas), y luego el nombre de cada una de sus peliculas con su titulo,fecha de estreno,return(ganancia/costo),budget(costo) y revenue(ganancia).
    '''

    nombre_director=nombre_director.strip()
    df=df_crew[df_crew["job"]=='Director'][df_crew['name']==nombre_director]
    if df['name'].count().sum()==0:
        return "No se encuentra el director {} o no es un director.".format(nombre_director)
    id_pel=list(df['id_pelicula'].values)
    df2=data[data['id_pelicula'].isin(id_pel)]
    
    df2.drop_duplicates(inplace=True)
    df2=df2[['title','release_date','return','budget','revenue']]
    
    # Transformo la columna para que me de solamente la fecha
    # Ya que al querer listarla me deja valores donde da hora y además dice que es un tipo timestamp
    #df2['release_date']=df2['release_date'].dt.strftime('%Y-%m-%d') En este caso no es necesario ya que se importó como string.
    exito=df2["return"].sum()
    # Hacer la lista de lo pedido
    peliculas=df2['title'].tolist()
    fecha=df2['release_date'].tolist()
    retun=df2['return'].tolist()
    budget=df2['budget'].tolist()
    revenue=df2['revenue'].tolist()


    return {'director':nombre_director, 'retorno_total_director':exito, 
    'peliculas':peliculas, 'anio':fecha, 'retorno_pelicula':retun, 
    'budget_pelicula':budget, 'revenue_pelicula':revenue}

# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te devuelve una recomendación de 5 peliculas en una lista
       Esta recomendación esta ordenada de la mejor a la peor.
    '''

    return {'lista recomendada': titulo}