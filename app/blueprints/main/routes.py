from flask import render_template, request, redirect, url_for, flash
import requests
from .forms import PokemonForm
from wtforms.validators import EqualTo, DataRequired, ValidationError
from flask_login import login_user, current_user, logout_user, login_required
from . import bp as main
from app import db
from app.models import Pokemon
from sqlalchemy import and_

@main.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
# @app.route('/pokemon', methods=['GET', 'POST'])
# def pokemon():
    form = PokemonForm()
    my_pokemon = Pokemon.query.filter(Pokemon.user_id==current_user.id).all()

    if request.method == 'POST' and form.validate_on_submit():
        poke_id = request.form.get('poke_id')
        url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
        response = requests.get (url)
        
        if response.ok:
            #the request worked
            if not response.json():
                return "We had an error loading your data. It's likely the Pokemon is not in the database"
            data = response.json()
            move_url = data['moves'][0]['move']['url']
            move_data = requests.get(move_url).json()
                
            poke_dict={
                'poke_name': data ['forms'][0] ['name'],
                'hit_points': data['stats'][0]['base_stat'],
                'hp_base': data ['stats'][0] ['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense': data['stats'][2]['base_stat'],
                'move': data['moves'][0]['move']['name'],
                'move_description': move_data['flavor_text_entries'][3]['flavor_text'],
                'front_shiny_sprite': data ['sprites']['front_shiny']
            }
            # print(poke_dict)
            return render_template('pokemon.html.j2', pokemon_stats = poke_dict, form=form, my_pokemon = my_pokemon)
        else:
            return "Ain't gonna catch that 'un! That's no pokemon. Go back to search again!"
            #the request failed
                #format is: name inside of my html = name in python
    return render_template('pokemon.html.j2', my_pokemon=my_pokemon, form=form)
    

# !!!Catch a pokemon
@main.route('/catch/<poke_id>', methods=['GET', 'POST'])
@login_required
def catch(poke_id):
    # establish data sources
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    response = requests.get(url)
    data = response.json()
    move_url = data['moves'][0]['move']['url']
    move_data = requests.get(move_url).json()

    # create poke dictionary
    poke_dict ={
        'poke_name': data['name'],
        'hit_points': data['stats'][0]['base_stat'],
        'attack': data['stats'][1]['base_stat'],
        'defense': data['stats'][2]['base_stat'],
        'image': data['sprites']['other']['official-artwork']['front_default'],
        'move': data['moves'][0]['move']['name'],
        'move_description': move_data['flavor_text_entries'][3]['flavor_text']
    }
    # # !!!!!!!!!!DELETE THIS!!!!!!!!!!!!!!!!!
    # this_pokemon = Pokemon (user_id = current_user.id, poke_name = poke_dict['poke_name'], hit_points = poke_dict['hit_points'], attack = poke_dict['attack'], defense = poke_dict['defense'], image = poke_dict['image'], move = poke_dict['move'], move_description = move_data['flavor_text_entries'][3]['flavor_text'])
    # this_pokemon.capture()

    # check if specific pokemon is already owned, check if 5 already owned.
    pokemon = Pokemon.query.filter(and_(Pokemon.poke_name==poke_id, Pokemon.user_id==current_user.id)).all()
    pokemon_count = Pokemon.query.filter(Pokemon.user_id == current_user.id).count()

    if pokemon_count == 5:
        flash ("You already have 5 pokemon. Let one go to catch another.", 'danger')
        return redirect (url_for('main.pokemon'))

    elif pokemon:
        flash (f"You've already caught one of those! Try to catch a different one.", 'danger')
        return redirect (url_for('main.pokemon'))
    
    else:
        this_pokemon = Pokemon (user_id = current_user.id, poke_name = poke_dict['poke_name'], hit_points = poke_dict['hit_points'], attack = poke_dict['attack'], defense = poke_dict['defense'], image = poke_dict['image'], move = poke_dict['move'], move_description = poke_dict['move_description'])
        this_pokemon.capture()
        vowels = ['a', 'e', 'i', 'o', 'u']
        if poke_id[0] in vowels:
            flash (f'You caught an {poke_id}!', 'success')
        else:
            flash (f'You caught a {poke_id}!', 'success')
        return redirect (url_for('main.pokemon'))


# !!!Release a pokemon
@main.route('/release/<poke_name>', methods=['GET', 'POST'])
@login_required
def release(poke_name):
    this_pokemon = Pokemon.query.filter(and_(Pokemon.poke_name==poke_name, Pokemon.user_id==current_user.id)).all()
    pokemon_name = this_pokemon[0].poke_name
    this_pokemon[0].release()
    flash (f'You have released your {pokemon_name}.', 'warning')
    return redirect(url_for('main.pokemon'))

# @main.route('/battle', methods=['GET', 'POST'])
# @login_required
# def battle()
# 
# create my_selected_pokemon

# if method is get:
# for user in users
# display table
# for pokemon in their pokemon
# display row
# change let it go button to select for battle button
# button creates their_pokemon

#for current user
# display table
# for pokemon in my_pokemon
# display row
# change let it go button to select for battle button

# display button to submit


# if method is post:
# 