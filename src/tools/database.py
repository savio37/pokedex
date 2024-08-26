from tinydb import TinyDB, Query
import re

db = TinyDB('data/database.json')
pokemon_table = db.table('pokemons')

Pokemon = Query()

def in_types(entry, type):
    return any(t['title'] == type for t in entry['types'])

class FacadeDB:
    def __init__(self):
        self.db = TinyDB('data/database.json')
        self.table_species = self.db.table('species')
        self.table_types = self.db.table('types')
        self.entry = Query()
        
    def add_species(self, species:dict):
        self.table_species.insert(species)
        
    def get_species(self, id:int=None, name:str='', type1:str='Any', type2:str='Any', family:bool=False):
        result = self.table_species.search(
            (self.entry.id == id if id is not None else (self.entry.id.exists())) &
            (self.entry.name.matches(f'{name}[aZ]*', re.RegexFlag.IGNORECASE) if name != '' else self.entry.id.exists()) &
            (self.entry.types.any(lambda t: t['title'] == type1) if type1 != 'Any' else self.entry.id.exists()) &
            (self.entry.types.any(lambda t: t['title'] == type2) if type2 != 'Any' else self.entry.id.exists()))
        
        families = []
        if family == True:
            for species in result:
                if 'evo_chain' in species:
                    family = self.table_species.search(self.entry.id.one_of([evo['id'] for evo in species['evo_chain']]))
                    families.extend(family)
        
        result.extend(families)
        result = {s['id']: s for s in result}.values()
        result = sorted(result, key=lambda s: s['id'])
        
        return result
        
    
    def del_species(self, id:int):
        self.table_species.remove(self.entry['id'] == id)
        
    def add_type(self, type:dict):
        self.table_types.insert(type)
        
    def get_type(self, id:int|list[int]):
        if isinstance(id, list):
            return self.table_types.search(self.entry.id.one_of(id))
        else:
            return self.table_types.search(self.entry.id == id)
    
    def del_type(self, id:int):
            self.table_types.remove(self.entry['id'] == id)
        
    def clear_species(self):
        self.table_species.truncate()
        
    def clear_types(self):
        self.table_types.truncate()
        