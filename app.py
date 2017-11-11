import base64
from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)
pokeapi_base_url = 'https://pokeapi.co/api/v2'

@app.route('/')
def view_pokedex_main():
	api_response = requests.get(pokeapi_base_url + '/pokemon').json()

	return render_template(
		'home.html',
		pokemon_results=api_response['results']
	)

@app.route('/pokemon/')
def view_pokedex_entry():
	name = request.args.get('name')

	data_dict = requests.get(pokeapi_base_url + '/pokemon-species/' + name).json()
	flavor_text = ''
	for data in data_dict['flavor_text_entries']:
		if data['language']['name'] == 'en':
			# replace is to make sure form feed character is replaced
			flavor_text = data['flavor_text'].replace('\x0C', ' ')
			# eh, just find the first english one
			break

	form_dict = requests.get(pokeapi_base_url + '/pokemon-form/' + name).json()
	return render_template(
		'pokemon.html',
		pokemon_data=data_dict,
		sprite_url=form_dict['sprites']['front_default'],
		description=flavor_text
	)

if __name__ == "__main__":
	app.run(host="0.0.0.0")
