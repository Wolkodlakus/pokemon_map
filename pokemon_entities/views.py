import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    pokemons_django = Pokemon.objects.all()
    pokemons_entity = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            (request.build_absolute_uri(pokemon_entity.pokemon.image.url)
             if pokemon_entity.pokemon.image
             else None)
        )

    pokemons_on_page = []

    for pokemon in pokemons_django:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': (pokemon.image.url if pokemon.image else None),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_entity = PokemonEntity.objects.filter(pokemon=pokemon)

    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            (request.build_absolute_uri(pokemon.image.url)
             if pokemon.image
             else None)
        )
    description_of_pokemon = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": (request.build_absolute_uri(pokemon.image.url)
                    if pokemon.image
                    else None),
    }
    if pokemon.evolved_from:
        prev_pokemon = pokemon.evolved_from
        description_of_pokemon["previous_evolution"] = {
            "pokemon_id": prev_pokemon.id,
            "title_ru": prev_pokemon.title,
            "img_url": (request.build_absolute_uri(prev_pokemon.image.url)
                        if prev_pokemon.image
                        else None),
        }
    else:
        description_of_pokemon["previous_evolution"] = None

    next_pokemons = pokemon.evolves_into.all()
    if next_pokemons:
        next_pokemon = next_pokemons[0]
        description_of_pokemon["next_evolution"] = {
            "pokemon_id": next_pokemon.id,
            "title_ru": next_pokemon.title,
            "img_url": (request.build_absolute_uri(next_pokemon.image.url)
                        if next_pokemon.image
                        else None),
        }
    else:
        description_of_pokemon["next_evolution"] = None

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': description_of_pokemon
    })
