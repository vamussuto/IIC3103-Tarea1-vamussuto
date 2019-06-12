from django.shortcuts import render
from django.http import HttpResponse
from .models import Greeting
import requests
import json

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

#def index(request):
#    r = requests.get('http://httpbin.org/status/418')
#    print(r.text)
#    return HttpResponse('<pre>' + r.text + '</pre>')


def home_t3(request):
    response = requests.get("https://swapi-graphql-integracion-t3.herokuapp.com/?query={ allFilms { edges { node { id title releaseDate director producers episodeID } } } }")
    films1 = response.content
    f = json.loads(films1)
    return render(request, "t3/home.html", {"films": f["data"]["allFilms"]["edges"]})






def pelicula(request, url):
    f = json.loads(requests.get(
        'https://swapi-graphql-integracion-t3.herokuapp.com/?query= {film(id:"' + url + '"){title openingCrawl director producers episodeID releaseDate planetConnection { edges { node { id name } } } characterConnection { edges { node { id name } } } starshipConnection { edges { node { id name } } } } }').content)[
        "data"]["film"]
    info = {"title": f["title"], "release_date": f["releaseDate"], "director": f["director"], "opening" : f["openingCrawl"],
            "producer": f["producers"], "episode_id": f["episodeID"], "personas": [], "naves": [], "planetas": []}


    for personaje in f["characterConnection"]["edges"]:
        info["personas"].append({"id": personaje["node"]["id"], "nombre": personaje["node"]["name"]})

    for nave in f["starshipConnection"]["edges"]:
        info["naves"].append({"id": nave["node"]["id"], "nombre": nave["node"]["name"]})

    for planeta in f["planetConnection"]["edges"]:
        info["planetas"].append({"id": planeta["node"]["id"], "nombre": planeta["node"]["name"]})
    return render(request, "t3/pelicula.html", {"film": info})

def personaje(request, url):
    p = json.loads(requests.get('https://swapi-graphql-integracion-t3.herokuapp.com/?query={ person(id:"'+url+'") { name hairColor id eyeColor birthYear mass height gender skinColor filmConnection { edges { node { id title} } } homeworld { id name} starshipConnection { edges { node { id name } } } } }').content)["data"]["person"]
    dic = {"p": p, "homeworld":[], "naves": [], "peliculas":[] }
    for nave in p['starshipConnection']['edges']:
        dic["naves"].append({"id": nave["node"]["id"], "nombre": nave["node"]["name"] })

    for pelicula in p["filmConnection"]["edges"]:
        dic["peliculas"].append({"id": pelicula["node"]["id"], "nombre": pelicula["node"]["title"]})
    return render(request, "t3/personaje.html", dic)

def nave(request, url):
    p = json.loads(requests.get('https://swapi-graphql-integracion-t3.herokuapp.com/?query={ starship(id: "'+url+'") { name model manufacturers costInCredits length maxAtmospheringSpeed crew passengers cargoCapacity consumables hyperdriveRating MGLT starshipClass pilotConnection { edges { node { id name } } } filmConnection { edges { node { id title} } } } }').content)["data"]["starship"]
    dic = {"p": p, "pilotos":[], "peliculas":[]}
    for pelicula in p["filmConnection"]["edges"]:
        dic["peliculas"].append({"id": pelicula["node"]["id"], "nombre":pelicula["node"]["title"]})

    for piloto in p["pilotConnection"]["edges"]:
        dic["pilotos"].append({"id": piloto["node"]["id"], "nombre": piloto["node"]["name"] })
    return render(request, "t3/nave.html", dic)


def planeta(request, url):
    p = json.loads(requests.get('https://swapi-graphql-integracion-t3.herokuapp.com/?query={ planet(id: "'+url+'") { name rotationPeriod residentConnection { edges { node { id name} } } orbitalPeriod diameter climates gravity terrains surfaceWater population filmConnection { edges { node { id title} } } } }').content)["data"]["planet"]
    dic = {"p": p,  "peliculas": [], "residentes":[]}
    for pelicula in p["filmConnection"]["edges"]:
        dic["peliculas"].append({"id": pelicula["node"]["id"], "nombre": pelicula["node"]["title"]})
    for r in p["residentConnection"]["edges"]:
        dic["residentes"].append({"id": r["node"]["id"], "nombre":r["node"]["name"] })

    return render(request, "t3/planeta.html", dic)






def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
