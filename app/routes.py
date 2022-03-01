from re import search
from urllib import response
from flask import render_template, request
from app import app

import json
import urllib.request

api_url = "https://pokeapi.co/api/v2/pokemon/ditto"
headers={'User-Agent': 'Mozilla/5.0'}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def validate_results():
    pokemonName = request.args.get("name").lower()
    totalPokemonNumber = getPokemonNumbers()
    url = 'https://pokeapi.co/api/v2/pokemon/?limit=' + totalPokemonNumber
    data = loadJsonData(url)
    pokemonList = data['results']
    for i in range(len(data['results'])):
        if pokemonName == pokemonList[i]['name']:
            return search_results(pokemonName)
    return render_template('error.html')

def search_results(pokemonName):
    url = 'https://pokeapi.co/api/v2/pokemon/' + pokemonName
    data = loadJsonData(url)
    pokemonID = data['id']  
    imgURL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(pokemonID) + ".png"
    pokemonName = pokemonName.title()      
    pokemonHeight = data['height'] * 10
    pokemonWeight = data['weight'] / 10
    return render_template('results.html', image=imgURL, name=pokemonName, height=pokemonHeight, weight=pokemonWeight)

def getPokemonNumbers():
    url = 'https://pokeapi.co/api/v2/pokemon/'
    data = loadJsonData(url)
    return str(data['count'])

def loadJsonData(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'cheese'})
    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
    return data