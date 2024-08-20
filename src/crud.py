from tinydb import TinyDB, Query

db = TinyDB('pokemons.json')
pokemon_table = db.table('pokemons')

Pokemon = Query()

def create_pokemon(name, type, level):
    pokemon_table.insert({'name': name, 'type': type, 'level': level})
    print(f"Pokémon {name} cadastrado com sucesso!")

def read_pokemon(name):
    result = pokemon_table.search(Pokemon.name == name)
    if result:
        for p in result:
            print(f"Nome: {p['name']}, Tipo: {p['type']}, Nível: {p['level']}")
    else:
        print(f"Pokémon {name} não encontrado.")

def update_pokemon(name, new_name=None, new_type=None, new_level=None):
    updates = {}
    if new_name:
        updates['name'] = new_name
    if new_type:
        updates['type'] = new_type
    if new_level:
        updates['level'] = new_level

    if updates:
        pokemon_table.update(updates, Pokemon.name == name)
        print(f"Pokémon {name} atualizado com sucesso!")
    else:
        print("Nenhum dado para atualizar.")

def delete_pokemon(name):
    pokemon_table.remove(Pokemon.name == name)
    print(f"Pokémon {name} deletado com sucesso!")

if __name__ == "__main__":
    create_pokemon("Pikachu", "Electric", 35)
    create_pokemon("Charmander", "Fire", 12)
    create_pokemon("Bulbasaur", "Grass/Poison", 8)

    print("\n--- Listando Pokémons ---")
    read_pokemon("Pikachu")
    read_pokemon("Charmander")

    update_pokemon("Pikachu", new_level=36)

    delete_pokemon("Bulbasaur")