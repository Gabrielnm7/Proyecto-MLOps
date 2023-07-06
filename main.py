from fastapi import FastAPI
import pandas as pd

app = FastAPI()
#http://127.0.0.1:8000/

movies = pd.read_csv("./Dataset/movies_clean.csv")

@app.get("/peliculas_idioma/{idioma}")
def peliculas_idioma(Idioma: str):
    Idioma = Idioma.lower()
    movies["original_language"] = movies["original_language"].str.lower()
    idiomas = movies["original_language"].unique()
    if Idioma not in idiomas:
        return "No hay peliculas en ese idioma"
    else:
        cantidad = len(movies[movies["original_language"] == Idioma]["id"].unique())
        # Notemos que tomamos los valores unicos en id pues hay valores repetidos.
        return {"Idioma":Idioma,"Cantidad de peliculas":cantidad}
    
@app.get("/peliculas_duracion/{Pelicula}")
def peliculas_duracion(Pelicula: str):
    Pelicula = Pelicula.lower()
    movies["title"] = movies["title"].str.lower()
    peliculas = movies["title"].unique()
    if Pelicula not in peliculas:
        return "No hay peliculas con ese nombre"
    else:
        for i in range(movies.shape[0]):
            if movies["title"][i] == Pelicula:
                duracion = movies["runtime"][i]
                año      = int(movies["release_year"][i])
                return {"Pelicula":Pelicula,"Duracion":duracion,"Año":año}
    
@app.get("/franquicia/{Franquicia}")
def franquicia(Franquicia:str):
    Franquicia = Franquicia.lower()
    movies["belongs_to_collection"] = movies["belongs_to_collection"].str.lower()
    franquicias = movies["belongs_to_collection"].unique()
    if Franquicia not in franquicias:
        return "No hay ninguna franquicia con ese nombre"
    else:
        cant_peliculas = len(movies[movies["belongs_to_collection"]==Franquicia]["id"].unique())
        ganancia_total = movies[movies["belongs_to_collection"]==f"{Franquicia}"]["revenue"].sum()
        ganancia_prom = ganancia_total / cant_peliculas
    return {"Franquicia":Franquicia,
            "Cantidad de peliculas":cant_peliculas,
            "Ganancia Total": ganancia_total,
            "Ganancia Promedio":ganancia_prom}

@app.get("/peliculas_pais/{Pais}")
def peliculas_pais(Pais:str):
    # movies.drop_duplicates(subset=["id"],inplace=True) #!¿¿¿¿ Eliminamos las peliculas repetidas ???? CONSULTAR
    Pais = Pais.lower()
    cant_peliculas_prod = 0
    for i in movies["production_countries"].str.lower():
        if Pais in str(i):
            cant_peliculas_prod +=1
    return {"Pais":Pais,"Cantidad":cant_peliculas_prod}

@app.get("/productoras_exitosas/{productora}")
def productoras_exitosas(Productora:str):
    Productora = Productora.lower()
    revenue = [0]
    cantidad = 0
    for i in range(movies.shape[0]):
        if Productora in str(movies["production_companies"].str.lower()[i]):
            revenue.append(movies["revenue"][i])
            cantidad += 1
    return {"Productora":Productora,"Revenue":sum(revenue),"Cantidad de peliculas": cantidad}


@app.get("/get_director/{Director}")
def get_director(Director:str):
    Director = Director.lower()
    movies["crew"] = movies["crew"].str.lower()
    return_total = []
    peliculas = []
    for i in range(movies.shape[0]):
        if Director in str(movies["crew"][i]):
            return_total.append(movies["return"][i])
            peliculas.append({"Pelicula":movies["title"][i],
                            'anio':movies["release_year"][i],'retorno_pelicula':movies["return"][i], 
                            'budget_pelicula':movies["budget"][i], 'revenue_pelicula':movies["revenue"][i]})
    return {"Director":Director, "Return_total":sum(return_total),
            "Peliculas":peliculas}


















