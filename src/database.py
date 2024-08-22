from tinydb import TinyDB, Query
import re

db = TinyDB('data/database.json')
pokemon_table = db.table('pokemons')

Pokemon = Query()

class FacadeDB:
    def __init__(self):
        self.db = TinyDB('data/database.json')
        self.table_species = self.db.table('species')
        self.table_types = self.db.table('types')
        self.entry = Query()
        
    def add_species(self, species:dict):
        self.table_species.insert(species)
        
    def get_species(self, value:int|str|list[int]|list[str], key:str='id'):
        if isinstance(value, list):
            return self.table_species.search(self.entry[key] in value)
        elif isinstance(value, str):
            return self.table_species.search(self.entry[key].matches(f"{value}[aZ]*", flags=re.IGNORECASE))
        else:
            return self.table_species.search(self.entry[key] == value)
    
    def del_species(self, id:int):
        self.table_species.remove(self.entry['id'] == id)
        
    def add_type(self, type:dict):
        self.table_types.insert(type)
        
    def get_type(self, value:int|list[int], key:str='id'):
        if isinstance(value, list):
            return self.table_types.search(self.entry[key] in value)
        else:
            return self.table_types.search(self.entry[key] == value)
    
    def del_type(self, id:int):
            self.table_types.remove(self.entry['id'] == id)
        
    def clear_species(self):
        self.table_species.truncate()
        
    def clear_types(self):
        self.table_types.truncate()
        