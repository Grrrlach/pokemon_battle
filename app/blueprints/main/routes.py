from flask import render_template, request, redirect, url_for, flash
import requests
from .forms import *
from wtforms.validators import EqualTo, DataRequired, ValidationError
from flask_login import login_user, current_user, logout_user, login_required
from . import bp as main
from app import db
from app.models import Pokemon
from sqlalchemy import and_
import time
import random

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

@main.route('/battle', methods=['GET', 'POST'])
@login_required
def battle():
    form = BattleForm()
    my_pokemon = Pokemon.query.filter(Pokemon.user_id==current_user.id).all()
    # return str(my_pokemon)
    other_pokemon = Pokemon.query.filter(Pokemon.user_id != current_user.id).order_by(Pokemon.user_id.desc())
    
    if request.method == "POST":
        my_pokemon_id = request.form.get('my_pokemon_id')
        their_pokemon_id = request.form.get('their_pokemon_id')
        my_one_pokemon = Pokemon.query.filter(Pokemon.id == my_pokemon_id).first()
        their_one_pokemon = Pokemon.query.filter(Pokemon.id == their_pokemon_id).first()
        other_user = their_one_pokemon.user_id


        my_id_list = []
        for pokemon in my_pokemon:
            my_id_list.append(pokemon.id)
        other_id_list = []
        for pokemon in other_pokemon:
            other_id_list.append(pokemon.id)


        if my_pokemon_id not in my_id_list:
            flash ("That isn't one of your pokemon!", "danger")
            return redirect (url_for('main.battle', my_pokemon = my_pokemon, other_pokemon = other_pokemon))

        elif their_pokemon_id not in other_id_list:
            flash ("That isn't an available pokemon!", "danger")
            return redirect (url_for('main.battle'))

        else:
            flash (f'{my_pokemon.poke_name} uses {their_one_pokemon.move}: {my_pokemon.move_description}', 'warning')
            time.sleep(1)
            flash (f'{their_one_pokemon.poke_name} uses {my_pokemon.move}: {their_one_pokemon.move_description}', 'warning')
            time.sleep(1)
            flash ('.....')
            time.sleep(3)

        while True:
            my_hp = Pokemon.query.filter(Pokemon.user_id == my_pokemon_id).hit_points.all()[0] * random.randint(1,10)
            my_defense = Pokemon.query.filter(Pokemon.user_id == my_pokemon_id).defense.all()[0] * random.randint(1,10)
            my_attack = Pokemon.query.filter(Pokemon.user_id == my_pokemon_id).attack.all()[0] * random.randint(1,10)
            their_hp = Pokemon.query.filter(Pokemon.user_id == their_pokemon_id).hit_points.all()[0] * random.randint(1,10)
            their_defense = Pokemon.query.filter(Pokemon.user_id == their_pokemon_id).defense.all()[0] * random.randint(1,10)
            their_attack = Pokemon.query.filter(Pokemon.user_id == their_pokemon_id).attack.all()[0] * random.randint(1,10)

            if their_attack > my_defense:
                my_hp -= their_attack
                if my_hp <=0:
                    flash (f"{their_pokemon_id} wins!!!")
                    current_user.wins -=1
                    other_user.wins +=1
                    return redirect (url_for('main.battle'))
                else:
                    continue

            elif my_attack > their_defense:
                if their_hp <=0:
                    flash (f"{my_pokemon} wins!!!")
                    current_user.wins +=1
                    other_user.wins -=1
                    return redirect (url_for('main.battle'))
                else:
                    continue

            while True:
                my_hp = Pokemon.query.filter(Pokemon.user_id == my_pokemon_id).hit_points.all()[0] * random.randint(1,10)
                my_defense = Pokemon.query.filter(Pokemon.user_id == my_pokemon_id).defense.all()[0] * random.randint(1,10)
                my_attack = Pokemon.query.filter(Pokemon.user_id == my_pokemon_id).attack.all()[0] * random.randint(1,10)
                their_hp = Pokemon.query.filter(Pokemon.user_id == their_pokemon_id).hit_points.all()[0] * random.randint(1,10)
                their_defense = Pokemon.query.filter(Pokemon.user_id == their_pokemon_id).defense.all()[0] * random.randint(1,10)
                their_attack = Pokemon.query.filter(Pokemon.user_id == their_pokemon_id).attack.all()[0] * random.randint(1,10)
                
                if my_attack > their_defense and my_defense > their_attack:
                    flash (f"{my_pokemon} wins!!!")
                    current_user.wins +=1
                    other_user.wins -=1
                    return redirect (url_for('main.battle'))
                elif their_attack > my_defense and their_defense > my_attack:
                    flash (f"{their_one_pokemon} wins!!!")
                    current_user.wins -=1
                    other_user.wins +=1
                    return redirect (url_for('main.battle'))
                else:
                    continue
    else:

        return render_template('/battle.html.j2', form=form, my_pokemon = my_pokemon, other_pokemon = other_pokemon)


# if method is post:
    # import time
    # my_pokemon_hp = hp * random.randint(1,10)
    # their_pokemon_hp = hp*random.randint(1,10)

    # my_pokemon attack = attack * random.randint(1,10)
    # their_pokemon attack = attack * random.randint(1,10)
    # my_pokemon defense = defense * random.randint(1,10)
    # their_pokemon defense = defense * random.randint(1,10)

    # flash (f'my_pokemon.poke_name uses my_pokemon.move: my_pokemon.move_description', 'warning')
    # flash (f'{their_pokemon.poke_name} uses {their_pokemon.move}: {their_pokemon.move_description', 'warning'})

    # while True:
        # if my_pokemon_attack > their_pokemon_defense & my_pokemon_defense>their_pokemon_attack:
            # time.sleep(2)
            # flash (f'{my_pokemon.poke_name} wins!!!')
            # current_user.wins +=1
            # other user.wins -=1
            # return redirect(url_for('battle'))
        # elif my_pokemon_attack<their_pokemon_defense & my_pokemon_defense<their_pokemon_attack:
            # time.sleep(2)
            # flash (f'{their_pokemon.poke_name} wins!!!')
            # current_user.wins -=1
            # other user.wins +=1
            # return redirect(url_for('battle'))
        # elif my_pokemon_attack == their_pokemon_defense or my_pokemon_defense == their_pokemon_attack:
            # continue


# 
# create my_selected_pokemon

# if method is get:
# for user in users
# display table
# for pokemon in their pokemon
# display row

#for current user
# display table
# for pokemon in my_pokemon
# display row
# put form at bottom asking what pokemon of their you want to battle, and what pokemon of yours you want to battle
# display button to submit form


# if method is post:
    # import time
    # my_pokemon_hp = hp * random.randint(1,10)
    # their_pokemon_hp = hp*random.randint(1,10)

    # my_pokemon attack = attack * random.randint(1,10)
    # their_pokemon attack = attack * random.randint(1,10)
    # my_pokemon defense = defense * random.randint(1,10)
    # their_pokemon defense = defense * random.randint(1,10)

    # flash (f'my_pokemon.poke_name uses my_pokemon.move: my_pokemon.move_description', 'warning')
    # flash (f'{their_pokemon.poke_name} uses {their_pokemon.move}: {their_pokemon.move_description', 'warning'})

    # while True:
        # if my_pokemon_attack > their_pokemon_defense & my_pokemon_defense>their_pokemon_attack:
            # time.sleep(2)
            # flash (f'{my_pokemon.poke_name} wins!!!')
            # current_user.wins +=1
            # other user.wins -=1
            # return redirect(url_for('battle'))
        # elif my_pokemon_attack<their_pokemon_defense & my_pokemon_defense<their_pokemon_attack:
            # time.sleep(2)
            # flash (f'{their_pokemon.poke_name} wins!!!')
            # current_user.wins -=1
            # other user.wins +=1
            # return redirect(url_for('battle'))
        # elif my_pokemon_attack == their_pokemon_defense or my_pokemon_defense == their_pokemon_attack:
            # continue
