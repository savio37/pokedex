import aiopoke
import asyncio
import json
import os
        
        
async def get_pokemon(ids:list[int]):
    
    client = aiopoke.AiopokeClient()
    
    pokemons = []
    
    for id in ids:
        pokemon = await client.get_pokemon(id)
        pokemon_dict = {}
        
        sprite = pokemon.sprites.front_default
        await sprite.save(client=client, path=f'./img/pokemon')
        
        pokemon_dict['id'] = pokemon.id
        pokemon_dict['species'] = pokemon.name.title()
        pokemon_dict['img'] = f'img/pokemon/pokemon_{pokemon.id}.png'
        print(f'{pokemon.id} - {pokemon.name.title()}')
        
        pokemon_dict['types'] = []
        for t in pokemon.types:
            type_dict = {'id': t.type.id, 'title':t.name.title(), 'img': f'img/type_{t.type.id}.png'}
            pokemon_dict['types'].append(type_dict)
            
        pokemon_dict['height'] = f'{pokemon.height / 10:.1f} m'
        pokemon_dict['weight'] = f'{pokemon.weight / 10:.1f} Kg'
        
        pokemon_dict['stats'] = {}
        pokemon_dict['stats']['hp'] = pokemon.stats[0].base_stat
        pokemon_dict['stats']['atk'] = pokemon.stats[1].base_stat
        pokemon_dict['stats']['def'] = pokemon.stats[2].base_stat
        pokemon_dict['stats']['spatk'] = pokemon.stats[3].base_stat
        pokemon_dict['stats']['spdef'] = pokemon.stats[4].base_stat
        pokemon_dict['stats']['spd'] = pokemon.stats[5].base_stat
        
        
        species = await client.get_pokemon_species(pokemon.id)
        chain = await species.evolution_chain.fetch()
        link = chain.chain
        if len(link.evolves_to) > 0:
            pokemon_dict['evo_chain'] = []
            if link.species.id <= 151 and link.species.id != pokemon.id:
                pokemon_dict['evo_chain'].append({'id': link.species.id, 'species': link.species.name.title(), 'img': f'img/pokemon_{link.species.id}.png'})
            while True:
                link = link.evolves_to[0]
                if link.species.id <= 151 and link.species.id != pokemon.id:
                    pokemon_dict['evo_chain'].append({'id': link.species.id, 'species': link.species.name.title(), 'img': f'img/pokemon_{link.species.id}.png'})
                if len(link.evolves_to) == 0:
                    break
        
        pokemons.append(pokemon_dict)
        
    with open("pokemon.json", "w") as file:
        json.dump(pokemons, file, indent=4, ensure_ascii=False)


async def get_types():
        
    client = aiopoke.AiopokeClient()
    
    types = []
    
    for i in range(1, 19):
        type = await client.get_type(i)
        type_dict = {}
        
        type_dict['id'] = type.id
        type_dict['title'] = type.name.title()
        type_dict['img'] = f'img/type/{type.id}.png'
        print(f'{type.id} - {type.name.title()}')
        
        type_dict['defending'] = {}
        immune = type.damage_relations.no_damage_from
        resistant = type.damage_relations.half_damage_from
        vulnerable = type.damage_relations.double_damage_from
        if len(immune) > 0:
            type_dict['defending']['immune'] = []
        if len(resistant) > 0:
            type_dict['defending']['resistant'] = []
        if len(vulnerable) > 0:
            type_dict['defending']['vulnerable'] = []
        for t in immune:
            type_dict['defending']['immune'].append({'id': t.id, 'title':t.name.title(), 'img': f'img/type/{t.id}.png'})
        for t in resistant:
            type_dict['defending']['resistant'].append({'id': t.id, 'title':t.name.title(), 'img': f'img/type/{t.id}.png'})
        for t in vulnerable:
            type_dict['defending']['vulnerable'].append({'id': t.id, 'title':t.name.title(), 'img': f'img/type/{t.id}.png'})
        
        type_dict['attacking'] = {}
        immune = type.damage_relations.no_damage_to
        resistant = type.damage_relations.half_damage_to
        vulnerable = type.damage_relations.double_damage_to
        if len(immune) > 0:
            type_dict['attacking']['immune'] = []
        if len(resistant) > 0:
            type_dict['attacking']['resistant'] = []
        if len(vulnerable) > 0:
            type_dict['attacking']['vulnerable'] = []
        for t in immune:
            type_dict['attacking']['immune'].append({'id': t.id, 'title':t.name.title(), 'img': f'img/type/{t.id}.png'})
        for t in resistant:
            type_dict['attacking']['resistant'].append({'id': t.id, 'title':t.name.title(), 'img': f'img/type/{t.id}.png'})
        for t in vulnerable:
            type_dict['attacking']['vulnerable'].append({'id': t.id, 'title':t.name.title(), 'img': f'img/type/{t.id}.png'})
            
        types.append(type_dict)
        
    with open("types.json", "w") as file:
        json.dump(types, file, indent=4, ensure_ascii=False)


for file in os.listdir('img'):
            path = os.path.join('img', file)
            if os.path.isfile(path):
                os.remove(path)

# rodar só uma função por vez!

print("<<< POKÉMON >>>") 
asyncio.run(get_pokemon(range(1, 152)))

# print("<<< TIPOS >>>") 
# asyncio.run(get_types())
