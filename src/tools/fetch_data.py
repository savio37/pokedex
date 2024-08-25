import aiopoke
import asyncio
from database import FacadeDB
        
        
async def get_species(ids:list[int]):
    client = aiopoke.AiopokeClient()
    db = FacadeDB()
    db.clear_species()
    
    for id in ids:
        pokemon = await client.get_pokemon(id)
        species = await client.get_pokemon_species(id)
        pokemon_dict = {}
        
        # sprite = pokemon.sprites.other.home_front_default
        # await sprite.save(client=client, path=f'./assets/images/pokemon')
        # os.rename(f'./assets/images/pokemon/home_{id}.png', f'./assets/images/pokemon/{id}.png')
        
        pokemon_dict['id'] = pokemon.id
        pokemon_dict['name'] = pokemon.name.title()
        pokemon_dict['img'] = f'assets/images/pokemon/{pokemon.id}.png'
        
        pokemon_dict['types'] = []
        for t in pokemon.types:
            type_dict = {'id': t.type.id, 'title':t.type.name.title(), 'img': f'assets/images/type/{t.type.id}.png'}
            pokemon_dict['types'].append(type_dict)
            
        pokemon_dict['height'] = round(pokemon.height / 10, 1)
        pokemon_dict['weight'] = round(pokemon.weight / 10, 1)
        
        pokemon_dict['stats'] = {}
        pokemon_dict['stats']['hp'] = pokemon.stats[0].base_stat
        pokemon_dict['stats']['atk'] = pokemon.stats[1].base_stat
        pokemon_dict['stats']['def'] = pokemon.stats[2].base_stat
        pokemon_dict['stats']['spatk'] = pokemon.stats[3].base_stat
        pokemon_dict['stats']['spdef'] = pokemon.stats[4].base_stat
        pokemon_dict['stats']['spd'] = pokemon.stats[5].base_stat
        
        desc = ""
        for entry in species.flavor_text_entries:
            if entry.language.name == 'en':
                desc = entry.flavor_text
                break
        pokemon_dict['description'] = desc.replace('\f', ' ') \
                                          .replace('\n', ' ') \
                                          .replace('\u00e9', 'é') \
                                          .replace('POKéMON', 'pokémon')
                                   
        
        chain = await species.evolution_chain.fetch()
        link = chain.chain
        if len(link.evolves_to) > 0:
            pokemon_dict['evo_chain'] = []
            if link.species.id <= 151 and link.species.id != pokemon.id:
                pokemon_dict['evo_chain'].append({'id': link.species.id, 'name': link.species.name.title(), 'img': f'assets/images/pokemon_{link.species.id}.png'})
            while True:
                link = link.evolves_to[0]
                if link.species.id <= 151 and link.species.id != pokemon.id:
                    pokemon_dict['evo_chain'].append({'id': link.species.id, 'name': link.species.name.title(), 'img': f'assets/images/pokemon_{link.species.id}.png'})
                if len(link.evolves_to) == 0:
                    break
    
        print(f'{pokemon_dict["id"]} - {pokemon_dict["name"]} - {pokemon_dict["description"]}')
        db.add_species(pokemon_dict)


async def get_types():
    client = aiopoke.AiopokeClient()
    db = FacadeDB()
    db.clear_types()
    
    for i in range(1, 19):
        type = await client.get_type(i)
        type_dict = {}
        
        type_dict['id'] = type.id
        type_dict['title'] = type.name.title()
        type_dict['img'] = f'assets/images/type/{type.id}.png'
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
            type_dict['defending']['immune'].append({'id': t.id, 'title':t.name.title(), 'img': f'assets/images/type/{t.id}.png'})
        for t in resistant:
            type_dict['defending']['resistant'].append({'id': t.id, 'title':t.name.title(), 'img': f'assets/images/type/{t.id}.png'})
        for t in vulnerable:
            type_dict['defending']['vulnerable'].append({'id': t.id, 'title':t.name.title(), 'img': f'assets/images/type/{t.id}.png'})
        
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
            type_dict['attacking']['immune'].append({'id': t.id, 'title':t.name.title(), 'img': f'assets/images/type/{t.id}.png'})
        for t in resistant:
            type_dict['attacking']['resistant'].append({'id': t.id, 'title':t.name.title(), 'img': f'assets/images/type/{t.id}.png'})
        for t in vulnerable:
            type_dict['attacking']['vulnerable'].append({'id': t.id, 'title':t.name.title(), 'img': f'assets/images/type/{t.id}.png'})
            
        db.add_type(type_dict)


# print("<<< TIPOS >>>") 
# asyncio.run(get_types())

# print("<<< ESPÉCIES >>>") 
# asyncio.run(get_species(range(1, 152)))