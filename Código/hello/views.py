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


def home_t1(request):
    response = requests.get("https://swapi.co/api/films/")
    films1 = response.content
    f = json.loads(films1)
    return render(request, "t1/home.html", {"films": f["results"]})

def busqueda(request):
    ''' This could be your actual view or a new one// extraido de https://stackoverflow.com/questions/27112729/search-field-in-django-template'''
    # Your code
    if request.method == 'GET': # If the form is submitted
        texto = request.GET.get('q', None).lower()
        print(texto)
        dic = {"personajes": [], "planetas": [], "naves": [], "peliculas": [], "error": ""}
        #peliculas
        for p in (json.loads(requests.get("https://swapi.co/api/films/").content))["results"]:
            if texto in p["title"].lower():
                dic["peliculas"].append({"id": p["url"].split("/")[5], "nombre": p["title"]})
        # personajes
        for p in aux_busq("https://swapi.co/api/people/", []):
            if texto in p["name"].lower():
                dic["personajes"].append({"id": p["url"].split("/")[5], "nombre": p["name"]})
        # planetas
        for p in aux_busq("https://swapi.co/api/planets/", []):
            if texto in p["name"].lower():
                dic["planetas"].append({"id": p["url"].split("/")[5], "nombre": p["name"]})
        # naves
        for p in aux_busq("https://swapi.co/api/starships/", []):
            if texto in p["name"].lower():
                dic["naves"].append({"id": p["url"].split("/")[5], "nombre": p["name"]})
        #error
        if len(dic["peliculas"]) + len(dic["naves"]) + len(dic["personajes"]) + len(dic["planetas"]) == 0:
            dic["error"] = "No se encontraron coincidencias"
        return render(request, "t1/busqueda.html", dic)
        # Do whatever you need with the word the user looked for

def aux_busq(url, list):
    base = (json.loads(requests.get(url).content))
    ini = base["results"]
    list += ini
    if base["next"]:
        return aux_busq(base["next"], list)
    else:
        return list





def pelicula(request, url):
    f = json.loads(requests.get("https://swapi.co/api/films/"+url).content)
    info = {"title": f["title"], "release_date": f["release_date"], "director": f["director"], "producer": f["producer"],"episode_id": f["episode_id"],
            "personas": [], "naves": [], "planetas": []}
    for pers in f["characters"]:
        info["personas"].append({"id": pers.split("/")[5], "nombre": json.loads(requests.get(pers).content)["name"]})
    for nave in f["starships"]:
        info["naves"].append({"id": nave.split("/")[5], "nombre": json.loads(requests.get(nave).content)["name"]})
    for planeta in f["starships"]:
        info["planetas"].append({"id": planeta.split("/")[5], "nombre": json.loads(requests.get(planeta).content)["name"]})
    return render(request, "t1/pelicula.html", {"film": info})

def personaje(request, url):
    p = json.loads(requests.get("https://swapi.co/api/people/" + url).content)
    dic = {"p": p,  "planeta_id": p["homeworld"].split("/")[5], "planeta_nombre": json.loads(requests.get(p["homeworld"]).content)["name"], "naves": [], "peliculas":[] }
    for nave in p["starships"]:
        dic["naves"].append({"id": nave.split("/")[5], "nombre": json.loads(requests.get(nave).content)["name"]})
    for pelicula in p["films"]:
        dic["peliculas"].append({"id": pelicula.split("/")[5], "nombre": json.loads(requests.get(pelicula).content)["title"]})
    return render(request, "t1/personaje.html", dic)

def nave(request, url):
    p = json.loads(requests.get("https://swapi.co/api/starships/" + url).content)
    dic = {"p": p, "pilotos":[], "peliculas":[]}
    for pelicula in p["films"]:
        dic["peliculas"].append({"id": pelicula.split("/")[5], "nombre": json.loads(requests.get(pelicula).content)["title"]})
    for piloto in p["pilots"]:
        dic["pilotos"].append({"id": piloto.split("/")[5], "nombre": json.loads(requests.get(piloto).content)["name"]})
    return render(request, "t1/nave.html", dic)


def planeta(request, url):
    p = json.loads(requests.get("https://swapi.co/api/planets/" + url).content)
    dic = {"p": p,  "peliculas": [], "residentes":[]}
    for pelicula in p["films"]:
        dic["peliculas"].append({"id": pelicula.split("/")[5], "nombre": json.loads(requests.get(pelicula).content)["title"]})
    for res in p["residents"]:
        dic["residentes"].append({"id": res.split("/")[5], "nombre": json.loads(requests.get(res).content)["name"]})
    return render(request, "t1/planeta.html", dic)






def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
