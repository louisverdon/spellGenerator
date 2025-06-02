import json
import os

class SpellGenerator:
    def __init__(self):
        self.essence_runes = {
            "Grak": {
                "ㄊ FÖL": "Essence de la vie",
                "ㄝ HAR": "Essence de l\'eau",
                "ㄛ ZUN": "Essence du savoir/mental"
            },
            "Torgen": {
                "ㄋ POK": "Essence du feu",
                "ㄦ LOK": "Essence de la puissance",
                "ㄟ GUL": "Essence de la lumière"
            },
            "Myros": {
                "ㄚ KRA": "Essence de la terre",
                "ㄌ CHA": "Essence des animaux/hommes",
                "ㄜ QUA": "Essence de la magie"
            },
            "Malvan": {
                "ㄢ AO": "Essence du froid",
                "ㄞ XAL": "Essence des dragons",
                "ㄙ SHI": "Essence de l\'air"
            },
            "Roi démon": {
                "ㄠ XI": "Essence démoniaque"
            }
        }
        
        self.incantation_runes = {
            "ㄍ TOU": "En chuchotant",
            "ㄎ ZI": "En parlant normalement",
            "ㄏ RA": "En criant"
        }
        
        self.somatic_runes = {
            "ㄕ SU": "Toucher la cible (+5%)",
            "ㄖ SEN": "Ouvrir le grimoire (+5%)",
            "ㄗ YA": "Regarder sa cible (+5%)",
            "ㄤ UNG": "Cibler avec sa main (+5%)",
            "ㄘ OZ": "Fermer les yeux (+5%)",
            "ㄐ EK": "Fermer son poing (+5%)",
            "ㄑ EHR": "Faire un clin d\'œil (+5%)",
            "ㄒ AI": "Taper dans ses mains (+5%)",
            "ㄓ EY": "Lever les mains aux cieux (+5%)",
            "ㄥ OU": "Sacrifice (bonus variable selon l\'importance)",
            "ㄣ EN": "Guider de sa main (déplace le sort)",
            "ㄔ AN": "Faire un rond avec sa main (prolonge la durée)"
        }
        
        self.spells = []
        self.load_spells()
        
    def save_spells(self):
        with open("spells.json", "w", encoding="utf-8") as f:
            json.dump(self.spells, f, ensure_ascii=False, indent=2)
            
    def load_spells(self):
        # Ensure spells.json is in the same directory as this logic file
        # or use an absolute path if it's elsewhere.
        # For simplicity, assuming it's in the project root, relative to app.py's location
        spells_file_path = os.path.join(os.path.dirname(__file__), "..", "spells.json") 
        if not os.path.exists(spells_file_path):
             # If not in parent, check current directory (if web_app is project root)
            spells_file_path = "spells.json"

        if os.path.exists(spells_file_path):
            try:
                with open(spells_file_path, "r", encoding="utf-8") as f:
                    self.spells = json.load(f)
            except json.JSONDecodeError:
                print(f"Error decoding spells.json. Initializing with empty list.")
                self.spells = []
            except Exception as e:
                print(f"An unexpected error occurred loading spells: {e}")
                self.spells = []
        else:
            self.spells = []
                
    def create_spell(self, name, description, essence, incantation, somatic_runes, ordered_runes):
        pronunciation_parts = []
        gestures = []
        
        actual_essence = None
        actual_incantation = None
        actual_somatics = []

        for rune_key in ordered_runes:
            syllable = rune_key.split()[1] if " " in rune_key else rune_key
            pronunciation_parts.append(syllable)
            
            if rune_key in self.incantation_runes:
                gestures.append(self.incantation_runes[rune_key])
                actual_incantation = rune_key
            elif rune_key in self.somatic_runes:
                gestures.append(self.somatic_runes[rune_key])
                actual_somatics.append(rune_key)
            else:
                for deity_runes in self.essence_runes.values():
                    if rune_key in deity_runes:
                        actual_essence = rune_key
                        break

        pronunciation = "-".join(pronunciation_parts)
        
        if not actual_essence and essence:
             actual_essence = essence 
             # print(f"Warning: Essence rune '{essence}' was provided but not found in ordered_runes. Using provided essence.")
        elif not actual_essence and not essence:
            raise ValueError("Essence rune is required but not found or provided.")


        spell = {
            "name": name,
            "description": description,
            "essence": actual_essence,
            "incantation": actual_incantation,
            "somatic_runes": actual_somatics,
            "ordered_runes": ordered_runes,
            "pronunciation": pronunciation,
            "gestures": gestures
        }
        
        self.spells.append(spell)
        self.save_spells()
        return spell
    
    def update_spell(self, index, name, description, essence, incantation, somatic_runes, ordered_runes):
        pronunciation_parts = []
        gestures = []
        actual_essence = None
        actual_incantation = None
        actual_somatics = []

        for rune_key in ordered_runes:
            syllable = rune_key.split()[1] if " " in rune_key else rune_key
            pronunciation_parts.append(syllable)
            
            if rune_key in self.incantation_runes:
                gestures.append(self.incantation_runes[rune_key])
                actual_incantation = rune_key
            elif rune_key in self.somatic_runes:
                gestures.append(self.somatic_runes[rune_key])
                actual_somatics.append(rune_key)
            else:
                for deity_runes in self.essence_runes.values():
                    if rune_key in deity_runes:
                        actual_essence = rune_key
                        break
        
        pronunciation = "-".join(pronunciation_parts)

        if not actual_essence and essence:
             actual_essence = essence 
             # print(f"Warning: Essence rune '{essence}' was provided but not found in ordered_runes during update. Using provided essence.")
        elif not actual_essence and not essence:
            raise ValueError("Essence rune is required but not found or provided for update.")

        self.spells[index] = {
            "name": name,
            "description": description,
            "essence": actual_essence,
            "incantation": actual_incantation,
            "somatic_runes": actual_somatics, 
            "ordered_runes": ordered_runes,
            "pronunciation": pronunciation,
            "gestures": gestures
        }
        
        self.save_spells()
        return self.spells[index]
    
    def get_rune_description(self, rune_key, rune_dict):
        if rune_key in rune_dict:
            return rune_dict[rune_key]
        # Check across all essence deities if not found in provided dict (e.g. when dict is specific deity)
        for deity_runes in self.essence_runes.values():
            if rune_key in deity_runes:
                return deity_runes[rune_key]
        return rune_key # return key itself if no description found
    
    def get_all_essence_runes(self):
        all_runes = {}
        for deity, runes in self.essence_runes.items():
            for rune, desc in runes.items():
                all_runes[rune] = desc # Store as key-value for easier lookup
        return all_runes
        
    def get_essence_runes_by_deity(self):
        return self.essence_runes
    
    def get_incantation_runes(self):
        return self.incantation_runes # Return the dict itself
    
    def get_somatic_runes(self):
        return self.somatic_runes # Return the dict itself 