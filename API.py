# Se importan las librerias usadas en el código
import pandas as pd
import numpy as np
import ast
from fastapi import FastAPI


# Usamos: data,df_belongs_to_collection,df_production_countries,df_production_companies,df_crew

data=pd.read_csv("csv_limpios/data.csv")
df_belongs_to_collection=pd.read_csv("csv_limpios/collection.csv")
df_production_countries=pd.read_csv("csv_limpios/countries.csv")
df_production_companies=pd.read_csv("csv_limpios/companies.csv")
df_crew=pd.read_csv("csv_limpios/crew.csv")

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
    'sq', nan, 'qu', 'te', 'am', 'jv', 'tg', 'ml', 'hr', 'lo', 'ay',
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
       
    return "{} . Duración: {} minutos. Año:{}. ".format(Pelicula,dur,Anio)

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
            prom=0
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
    
    return "Se produjeron " + str(cant) + " películas en el país " + Pais

@app.get("/productoras_exitosas/{Productora}")
def productoras_exitosas(Productora:str):
    '''
    - Recibe la productora y devuelve el revenue total que obtuvo y la cantidad de peliculas realizadas.
    '''
    Productora=Productora.strip()
    df=df_production_companies[df_production_companies['name']==Productora]
    

    suma=df['revenue'].sum()
    cant= df['name'].count()

    return "La productora "+ Productora + " ha tenido un revenue de " + str(suma) + " y realizó " + str(cant) + " peliculas."

@app.get("/director/{nombre_director}")
def get_director(nombre_director:str):
    '''
    - Toma un solo nombre a la vez
    Devuelve el director con su exito (suma de return de todas sus peliculas), y luego una lista de listas.
    Cada lista dentro es una pelicula del director, los valores dentro de esas listas son : 
    [NombrePelicula,FechaLanzamiento,retorno,costo,ganacia] siendo estos sacados de las columnas (en mismo orden)= ['title','release_date','return','budget','revenue']
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
    lista_de_listas=df2.values.tolist()

    return "El director {} tiene un éxito de {}. Y sus peliculas son {}.".format(nombre_director, exito,lista_de_listas)

