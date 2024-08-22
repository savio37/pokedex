from tinydb import TinyDB, Query
from tinydb.table import Table

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
        
    def get_species(self, key:str, value):
        return self.table_species.search(self.entry[key] == value)
    
    def del_species(self, key:str, value):
        self.table_species.remove(self.entry[key] == value)
        
    def add_type(self, type:dict):
        self.table_types.insert(type)
        
    def get_type(self, key:str, value):
        return self.table_types.search(self.entry[key] == value)
    
    def del_type(self, key:str, value):
        self.table_types.remove(self.entry[key] == value)
        
    def clear_species(self):
        self.table_species.truncate()
        
    def clear_types(self):
        self.table_types.truncate()
        