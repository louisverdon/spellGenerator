import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class SpellGenerator:
    def __init__(self):
        self.essence_runes = {
            "Grak": {
                "ㄊ FÖL": "Essence de la vie",
                "ㄝ HAR": "Essence de l'eau",
                "ㄛ ZUN": "Essence du savoir/mental"
            },
            "Torgen": {
                "ㄋ POK": "Essence du feu",
                "ㄦ LOK": "Essence de la puissance",
                "ㄟ GUL": "Essence de la lumière"
            },
            "Myros": {
                "ㄚ KRA": "Essence de la terre",
                "ㄌ QUA": "Essence des animaux/hommes",
                "ㄜ CHA": "Essence de la magie"
            },
            "Malvan": {
                "ㄢ AO": "Essence du froid",
                "ㄞ XAL": "Essence des dragons",
                "ㄙ SHI": "Essence de l'air"
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
            "ㄑ EHR": "Faire un clin d'œil (+5%)",
            "ㄒ AI": "Taper dans ses mains (+5%)",
            "ㄓ EY": "Lever les mains aux cieux (+5%)",
            "ㄥ OU": "Sacrifice (bonus variable selon l'importance)",
            "ㄣ EN": "Guider de sa main (déplace le sort)",
            "ㄔ AN": "Faire un rond avec sa main (prolonge la durée)"
        }
        
        self.spells = []
        self.load_spells()
        
    def save_spells(self):
        with open("spells.json", "w", encoding="utf-8") as f:
            json.dump(self.spells, f, ensure_ascii=False, indent=2)
            
    def load_spells(self):
        if os.path.exists("spells.json"):
            try:
                with open("spells.json", "r", encoding="utf-8") as f:
                    self.spells = json.load(f)
            except:
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
        
        if not actual_essence:
             actual_essence = essence 
             print(f"Warning: Essence rune '{essence}' not found in ordered_runes, using provided essence.")

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

        if not actual_essence:
             actual_essence = essence 
             print(f"Warning: Essence rune '{essence}' not found in ordered_runes during update, using provided essence.")

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
        return rune_key
    
    def get_all_essence_runes(self):
        all_runes = []
        for deity, runes in self.essence_runes.items():
            for rune, desc in runes.items():
                all_runes.append(f"{rune} - {desc}")
        return all_runes
        
    def get_essence_runes_by_deity(self):
        return self.essence_runes
    
    def get_incantation_runes(self):
        return [f"{rune} - {desc}" for rune, desc in self.incantation_runes.items()]
    
    def get_somatic_runes(self):
        return [f"{rune} - {desc}" for rune, desc in self.somatic_runes.items()]

class SpellGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur de Sortilèges")
        self.root.geometry("1000x700")
        
        # Configure style for better appearance
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("Accent.TButton", font=("Helvetica", 10, "bold"), background="#4a90e2", foreground="white")
        
        self.generator = SpellGenerator()
        self.currently_editing = None
        self.selected_somatic_runes = [] # Gardé pour le transfert mais l'ordre final est la référence
        self.ordered_final_runes = [] # Nouvelle liste pour l'ordre final
        
        # Variables pour suivre l'essence et l'incantation sélectionnées
        self.selected_essence_rune = tk.StringVar()
        self.selected_incantation_rune = tk.StringVar()
        
        self.create_widgets()
        
        # Attacher les callbacks après la création des widgets
        self.selected_essence_rune.trace_add("write", self.update_final_rune_list)
        self.selected_incantation_rune.trace_add("write", self.update_final_rune_list)

    def create_widgets(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for spell creation
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right frame for spell list
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # ===== SPELL CREATION SECTION (LEFT FRAME) =====
        title_label = ttk.Label(left_frame, text="Création de Sortilège", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(0, 10), anchor="w", fill=tk.X)

        # --- Scrollable Area Start ---
        scrollable_canvas = tk.Canvas(left_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=scrollable_canvas.yview)
        scrollable_frame = ttk.Frame(scrollable_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: scrollable_canvas.configure(
                scrollregion=scrollable_canvas.bbox("all")
            )
        )

        scrollable_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        scrollable_canvas.pack(side="top", fill="both", expand=True)
        # --- Scrollable Area End ---
        
        # Widgets inside the scrollable frame
        inner_frame = ttk.Frame(scrollable_frame, padding=(0, 0, 15, 0))
        inner_frame.pack(fill=tk.BOTH, expand=True)

        # Spell name
        ttk.Label(inner_frame, text="Nom du sortilège:").pack(anchor="w", pady=(5, 2))
        self.name_entry = ttk.Entry(inner_frame, width=40)
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Spell description
        ttk.Label(inner_frame, text="Description:").pack(anchor="w", pady=(5, 2))
        self.description_text = tk.Text(inner_frame, height=4, width=40, wrap=tk.WORD)
        self.description_text.pack(fill=tk.X, pady=(0, 10))
        
        # ===== DEITY TABS =====
        ttk.Label(inner_frame, text="Rune d'Essence (obligatoire):").pack(anchor="w", pady=(5, 2))
        self.essence_notebook = ttk.Notebook(inner_frame)
        self.essence_notebook.pack(fill=tk.X, pady=(0, 10))
        
        # Create deity tabs
        self.essence_vars = {} # Toujours utilisé pour les radiobuttons
        essence_runes_by_deity = self.generator.get_essence_runes_by_deity()
        
        for deity, runes in essence_runes_by_deity.items():
            deity_frame = ttk.Frame(self.essence_notebook, padding=10)
            self.essence_notebook.add(deity_frame, text=deity)
            
            self.essence_vars[deity] = tk.StringVar() # Var pour ce groupe
            for i, (rune, desc) in enumerate(runes.items()):
                rune_text = f"{rune} - {desc}"
                rb = ttk.Radiobutton(
                    deity_frame, 
                    text=rune_text, 
                    value=rune, 
                    variable=self.essence_vars[deity],
                    command=lambda r=rune: self.selected_essence_rune.set(r) # Met à jour la variable globale
                )
                rb.pack(anchor="w", pady=2)
        
        # ===== INCANTATION SECTION =====
        ttk.Label(inner_frame, text="Rune d'Incantation (optionnelle):").pack(anchor="w", pady=(5, 2))
        self.incantation_var = tk.StringVar() # Gardé pour les radiobuttons
        self.incantation_var.set("None")
        self.selected_incantation_rune.set("") # Initialise la variable d'ordre
        
        incantation_frame = ttk.Frame(inner_frame)
        incantation_frame.pack(fill=tk.X, pady=(0, 10))
        
        rb_none = ttk.Radiobutton(
            incantation_frame,
            text="Aucune (silence)",
            value="None",
            variable=self.incantation_var,
            command=lambda: self.selected_incantation_rune.set("") # Met à jour la variable d'ordre
        )
        rb_none.pack(side=tk.LEFT, padx=(0, 15))
        
        for rune, desc in self.generator.incantation_runes.items():
            rune_text = f"{rune} - {desc}"
            rb = ttk.Radiobutton(
                incantation_frame,
                text=rune_text,
                value=rune,
                variable=self.incantation_var,
                command=lambda r=rune: self.selected_incantation_rune.set(r) # Met à jour la variable d'ordre
            )
            rb.pack(side=tk.LEFT, padx=(0, 15))
        
        # ===== SOMATIC RUNES SECTION =====
        self.create_somatic_section(inner_frame)

        # ===== FINAL RUNE ORDER SECTION =====
        self.create_final_order_section(inner_frame)

        # --- Elements below scrollable area ---
        # Button frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10, side=tk.TOP)
        
        # Create Button
        self.create_button = ttk.Button(
            button_frame, 
            text="Créer le Sortilège", 
            command=self.create_spell
        )
        self.create_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Edit Button
        self.edit_button = ttk.Button(
            button_frame,
            text="Modifier le Sortilège",
            command=self.edit_spell,
            state="disabled"
        )
        self.edit_button.pack(side=tk.LEFT)
        
        # Cancel Edit Button
        self.cancel_edit_button = ttk.Button(
            button_frame,
            text="Annuler la modification",
            command=self.cancel_edit,
            state="disabled"
        )
        self.cancel_edit_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # ===== SPELL DISPLAY SECTION =====
        spell_display_label = ttk.Label(left_frame, text="Détails du Sortilège:", font=("Helvetica", 12, "bold"))
        spell_display_label.pack(anchor="w", pady=(10, 5), side=tk.TOP)
        
        self.spell_display = tk.Text(left_frame, height=8, wrap=tk.WORD, state="disabled") # Reduced height slightly
        self.spell_display.pack(fill=tk.BOTH, expand=False, pady=(0, 10), side=tk.TOP) # Prevent expansion
        
        # ===== SPELL LIST SECTION (RIGHT FRAME) =====
        ttk.Label(right_frame, text="Grimoire des Sortilèges", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))
        
        # Spell listbox with scrollbar
        spell_list_frame = ttk.Frame(right_frame)
        spell_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        
        scrollbar_list = ttk.Scrollbar(spell_list_frame)
        scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.spell_listbox = tk.Listbox(
            spell_list_frame, 
            yscrollcommand=scrollbar_list.set,
            height=15,
            font=("Helvetica", 10)
        )
        self.spell_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_list.config(command=self.spell_listbox.yview)
        
        self.spell_listbox.bind('<<ListboxSelect>>', self.display_selected_spell)
        
        # Spell detail frame
        spell_detail_frame = ttk.LabelFrame(right_frame, text="Détails du Sortilège Sélectionné")
        spell_detail_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.spell_detail_text = tk.Text(spell_detail_frame, wrap=tk.WORD, height=15)
        self.spell_detail_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.spell_detail_text.config(state="disabled")
        
        # Load existing spells
        self.refresh_spell_list()
    
    def create_somatic_section(self, parent_frame):
        ttk.Label(parent_frame, text="Runes Somatiques (optionnelles):").pack(anchor="w", pady=(5, 2))
        
        somatic_main_frame = ttk.Frame(parent_frame)
        somatic_main_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        available_frame = ttk.LabelFrame(somatic_main_frame, text="Runes Somatiques Disponibles")
        available_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # On n'a plus besoin de la liste "sélectionnées" ici, juste le bouton Ajouter
        # Le retrait se fera depuis la liste d'ordre final
        available_list_frame = ttk.Frame(available_frame)
        available_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        available_scrollbar = ttk.Scrollbar(available_list_frame)
        available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.available_somatic_listbox = tk.Listbox(available_list_frame, selectmode=tk.SINGLE, yscrollcommand=available_scrollbar.set)
        self.available_somatic_listbox.pack(fill=tk.BOTH, expand=True)
        available_scrollbar.config(command=self.available_somatic_listbox.yview)

        # Bouton Ajouter (vertical)
        buttons_frame = ttk.Frame(somatic_main_frame)
        buttons_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y, anchor='n')
        ttk.Button(buttons_frame, text="Ajouter ↓", command=self.add_somatic_to_final_order, width=8).pack(pady=5)

        # Populate available somatic runes
        for rune, desc in self.generator.somatic_runes.items():
            self.available_somatic_listbox.insert(tk.END, f"{rune} - {desc}")

    def create_final_order_section(self, parent_frame):
        ttk.Label(parent_frame, text="Ordre Final des Runes:").pack(anchor="w", pady=(15, 2))

        final_order_main_frame = ttk.Frame(parent_frame)
        final_order_main_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        final_list_frame = ttk.LabelFrame(final_order_main_frame, text="Ordre Actuel")
        final_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        final_list_scrollbar = ttk.Scrollbar(final_list_frame)
        final_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.final_order_listbox = tk.Listbox(final_list_frame, selectmode=tk.SINGLE, yscrollcommand=final_list_scrollbar.set, height=6)
        self.final_order_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        final_list_scrollbar.config(command=self.final_order_listbox.yview)

        # Boutons de contrôle (vertical)
        control_buttons_frame = ttk.Frame(final_order_main_frame)
        control_buttons_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y, anchor='n')
        ttk.Button(control_buttons_frame, text="↑ Monter", command=self.move_final_rune_up, width=8).pack(pady=5)
        ttk.Button(control_buttons_frame, text="↓ Descendre", command=self.move_final_rune_down, width=8).pack(pady=5)
        ttk.Button(control_buttons_frame, text="Retirer", command=self.remove_rune_from_final_order, width=8).pack(pady=5)

    def add_somatic_to_final_order(self):
        selection = self.available_somatic_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        rune_full = self.available_somatic_listbox.get(index)
        rune_key = rune_full.split(" - ")[0]
        
        # Ajouter seulement si pas déjà présent (évite doublons de somatiques)
        if rune_key not in self.ordered_final_runes:
            self.ordered_final_runes.append(rune_key)
            self.final_order_listbox.insert(tk.END, rune_full)
            self.update_spell_preview() # Mettre à jour l'aperçu en bas

    def remove_rune_from_final_order(self):
        selection = self.final_order_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        rune_full = self.final_order_listbox.get(index)
        rune_key = rune_full.split(" - ")[0]
        
        # Si c'est l'essence, on ne peut pas la retirer (ou on la remet ? Pour l'instant, on interdit)
        if rune_key == self.selected_essence_rune.get():
             messagebox.showwarning("Action Interdite", "La rune d'essence est obligatoire et ne peut pas être retirée de l'ordre final.")
             return

        # Si c'est l'incantation, on la retire de l'ordre et on désélectionne le radiobutton
        if rune_key == self.selected_incantation_rune.get():
            self.selected_incantation_rune.set("") # Déclenche trace_add
            self.incantation_var.set("None") # Met à jour le radiobutton
        
        # Retirer de la liste interne et de l'affichage
        if rune_key in self.ordered_final_runes:
             self.ordered_final_runes.pop(index) # pop utilise l'index directement
        self.final_order_listbox.delete(index)
        self.update_spell_preview() # Mettre à jour l'aperçu

    def move_final_rune_up(self):
        selection = self.final_order_listbox.curselection()
        if not selection or selection[0] == 0:
            return
            
        index = selection[0]
        rune_full = self.final_order_listbox.get(index)
        
        self.final_order_listbox.delete(index)
        self.final_order_listbox.insert(index-1, rune_full)
        self.final_order_listbox.selection_set(index-1)
        
        # Mettre à jour la liste interne
        rune_key = self.ordered_final_runes.pop(index)
        self.ordered_final_runes.insert(index-1, rune_key)
        self.update_spell_preview()
        
    def move_final_rune_down(self):
        selection = self.final_order_listbox.curselection()
        if not selection or selection[0] == self.final_order_listbox.size()-1:
            return
            
        index = selection[0]
        rune_full = self.final_order_listbox.get(index)
        
        self.final_order_listbox.delete(index)
        self.final_order_listbox.insert(index+1, rune_full)
        self.final_order_listbox.selection_set(index+1)
        
        # Mettre à jour la liste interne
        rune_key = self.ordered_final_runes.pop(index)
        self.ordered_final_runes.insert(index+1, rune_key)
        self.update_spell_preview()

    # Callback pour mettre à jour la liste d'ordre final quand Essence/Incantation changent
    def update_final_rune_list(self, *args):
        essence = self.selected_essence_rune.get()
        incantation = self.selected_incantation_rune.get()
        
        # Conserver les somatiques actuelles
        current_somatics = [r for r in self.ordered_final_runes 
                            if r not in self.generator.essence_runes 
                            and r not in self.generator.incantation_runes]

        new_ordered_list = []
        # Ajouter l'incantation si sélectionnée
        if incantation:
             new_ordered_list.append(incantation)
        # Ajouter l'essence (toujours présente si sélectionnée)
        if essence:
            new_ordered_list.append(essence)
        # Ajouter les somatiques conservées
        new_ordered_list.extend(current_somatics)
        
        self.ordered_final_runes = new_ordered_list
        
        # Mettre à jour l'affichage de la liste d'ordre final
        self.final_order_listbox.delete(0, tk.END)
        for rune_key in self.ordered_final_runes:
            # Trouver la description complète pour l'affichage
            full_desc = f"{rune_key} - {self.generator.get_rune_description(rune_key, self.generator.essence_runes.get(self.find_deity_for_essence(rune_key), {})) or self.generator.get_rune_description(rune_key, self.generator.incantation_runes) or self.generator.get_rune_description(rune_key, self.generator.somatic_runes) or 'Rune inconnue'}"
            self.final_order_listbox.insert(tk.END, full_desc)
        
        self.update_spell_preview() # Mettre à jour l'aperçu

    def find_deity_for_essence(self, essence_key):
        """Trouve la déité associée à une rune d'essence."""
        for deity, runes in self.generator.essence_runes.items():
            if essence_key in runes:
                return deity
        return None

    # Mettre à jour l'aperçu du sort en bas à gauche
    def update_spell_preview(self):
        # Générer prononciation et gestes basés sur self.ordered_final_runes
        pronunciation_parts = []
        gestures = []
        for rune_key in self.ordered_final_runes:
            syllable = rune_key.split()[1] if " " in rune_key else rune_key
            pronunciation_parts.append(syllable)
            
            desc = ""
            if rune_key in self.generator.incantation_runes:
                desc = self.generator.incantation_runes[rune_key]
            elif rune_key in self.generator.somatic_runes:
                desc = self.generator.somatic_runes[rune_key]
            # Pas de geste visible pour l'essence dans l'aperçu des gestes
            
            if desc:
                gestures.append(desc)

        pronunciation = "-".join(pronunciation_parts)
        
        # Mettre à jour le widget d'affichage
        self.spell_display.config(state="normal")
        self.spell_display.delete("1.0", tk.END)
        
        # Afficher seulement si on a une essence (sort valide)
        if self.selected_essence_rune.get():
            self.spell_display.insert(tk.END, f"Prononciation: {pronunciation}\n\n")
            self.spell_display.insert(tk.END, "Gestes à réaliser (ordre important):\n")
            if not gestures:
                 self.spell_display.insert(tk.END, "(Aucun geste supplémentaire)\n")
            else:
                for i, gesture in enumerate(gestures):
                    self.spell_display.insert(tk.END, f"{i+1}. {gesture}\n")
        else:
            self.spell_display.insert(tk.END, "(Sélectionnez une rune d'essence pour voir l'aperçu)")
            
        self.spell_display.config(state="disabled")

    def create_spell(self):
        name = self.name_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not name or not description:
            messagebox.showerror("Erreur", "Le nom et la description sont requis.")
            return
            
        essence = self.selected_essence_rune.get()
        if not essence:
            messagebox.showerror("Erreur", "Une rune d'essence est obligatoire.")
            return
            
        # L'ordre final est maintenant la référence
        if not self.ordered_final_runes or essence not in self.ordered_final_runes:
             messagebox.showerror("Erreur", "La rune d'essence doit être présente dans l'ordre final.")
             return

        incantation = self.selected_incantation_rune.get() # Peut être ""
        # Les somatiques sont dérivés de ordered_final_runes dans le backend
        somatics = [r for r in self.ordered_final_runes if r in self.generator.somatic_runes]
        
        # Appeler create_spell avec la liste ordonnée
        spell = self.generator.create_spell(
            name,
            description,
            essence, # Passer l'essence sélectionnée pour référence
            incantation, # Passer l'incantation sélectionnée pour référence
            somatics, # Passer les somatiques dérivées pour référence
            self.ordered_final_runes # La liste ordonnée est la clé
        )
        
        # Afficher les détails complets du sort créé (pas juste l'aperçu)
        self.display_spell_details(spell, self.spell_display) # Met à jour la zone en bas à gauche
        self.refresh_spell_list()
        
        # Réinitialiser le formulaire
        self.clear_form()
            
        messagebox.showinfo("Succès", f"Le sortilège '{name}' a été créé et ajouté à votre grimoire.")

    def edit_spell(self):
        if self.currently_editing is None:
            # --- Entrer en mode édition --- 
            selection = self.spell_listbox.curselection()
            if not selection:
                messagebox.showerror("Erreur", "Veuillez sélectionner un sortilège à modifier.")
                return
            index = selection[0]
            # Les champs sont déjà remplis par display_selected_spell
            self.currently_editing = index
            self.create_button.config(state="disabled")
            self.edit_button.config(text="Sauvegarder")
            self.cancel_edit_button.config(state="normal")
        else:
            # --- Sauvegarder les modifications --- 
            name = self.name_entry.get().strip()
            description = self.description_text.get("1.0", tk.END).strip()
            
            if not name or not description:
                messagebox.showerror("Erreur", "Le nom et la description sont requis.")
                return
                
            essence = self.selected_essence_rune.get()
            if not essence or essence not in self.ordered_final_runes:
                messagebox.showerror("Erreur", "La rune d'essence est obligatoire et doit être dans l'ordre final.")
                return

            incantation = self.selected_incantation_rune.get()
            somatics = [r for r in self.ordered_final_runes if r in self.generator.somatic_runes]

            # Appeler update_spell avec l'ordre final
            spell = self.generator.update_spell(
                self.currently_editing,
                name,
                description,
                essence,
                incantation,
                somatics,
                self.ordered_final_runes
            )
            
            # Mettre à jour les affichages
            self.display_spell_details(spell, self.spell_display) # Bas gauche
            self.refresh_spell_list()
            self.spell_listbox.selection_set(self.currently_editing) # Resélectionner
            self.display_selected_spell(None) # Met à jour panneau droit ET regénère formulaire gauche
            
            # Sortir du mode édition
            current_index = self.currently_editing # Sauver l'index avant de reset
            self.currently_editing = None
            self.create_button.config(state="normal")
            self.edit_button.config(text="Modifier")
            # Garder actif car l'élément est sélectionné
            self.edit_button.config(state="normal") 
            self.cancel_edit_button.config(state="disabled")
            
            messagebox.showinfo("Succès", f"Le sortilège '{name}' a été modifié.")

    def cancel_edit(self):
        if self.currently_editing is not None:
            original_spell_index = self.currently_editing
            self.currently_editing = None # Sortir du mode édition
            
            # Resélectionner l'item original pour restaurer l'état du formulaire
            self.spell_listbox.selection_set(original_spell_index)
            self.display_selected_spell(None) # Recharge les données du sort sélectionné

            # Réinitialiser les boutons
            self.create_button.config(state="normal")
            self.edit_button.config(text="Modifier")
            self.edit_button.config(state="normal") # Actif car item sélectionné
            self.cancel_edit_button.config(state="disabled")
        else:
             # Cas improbable, juste clarifier
             self.clear_form()
             self.create_button.config(state="normal")
             self.edit_button.config(text="Modifier")
             self.edit_button.config(state="disabled")
             self.cancel_edit_button.config(state="disabled")

    # Doit maintenant aussi vider la liste d'ordre final et les variables associées
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
        
        # Désélectionner tous les radiobuttons Essence
        for deity, var in self.essence_vars.items():
            var.set("") # Ceci devrait idéalement désélectionner les radios
        self.selected_essence_rune.set("") # Vider la variable de suivi
        try: self.essence_notebook.select(0) 
        except: pass # Ignorer erreurs si pas possible

        # Désélectionner Incantation
        self.incantation_var.set("None")
        self.selected_incantation_rune.set("")

        # Vider la liste d'ordre final (interne et affichage)
        self.ordered_final_runes = []
        self.final_order_listbox.delete(0, tk.END)
        
        # Vider l'aperçu
        self.update_spell_preview()

        # Vider aussi la sélection des somatiques disponibles (bonne pratique)
        self.available_somatic_listbox.selection_clear(0, tk.END)

        # Vider l'affichage des détails du sort créé/modifié en bas à gauche
        # self.spell_display est géré par update_spell_preview maintenant

    # display_spell est renommé et généralisé
    def display_spell_details(self, spell, text_widget):
        """Affiche les détails complets d'un sort dans un widget Text donné."""
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        
        text_widget.insert(tk.END, f"Nom: {spell['name']}\n\n")
        text_widget.insert(tk.END, f"Description: {spell['description']}\n\n")
        text_widget.insert(tk.END, f"Essence: {spell.get('essence', 'N/A')}\n")
        text_widget.insert(tk.END, f"Incantation: {spell.get('incantation', 'Aucune') or 'Aucune'}\n")
        text_widget.insert(tk.END, f"Runes Somatiques: {', '.join(spell.get('somatic_runes', [])) or 'Aucune'}\n")
        text_widget.insert(tk.END, f"Ordre Final: {', '.join(spell.get('ordered_runes', []))}\n") # Afficher l'ordre sauvegardé
        
        text_widget.insert(tk.END, f"\nPrononciation: {spell['pronunciation']}\n\n")
        
        text_widget.insert(tk.END, "Gestes à réaliser:\n")
        if spell['gestures']:
            for gesture in spell['gestures']:
                text_widget.insert(tk.END, f"• {gesture}\n")
        else:
             text_widget.insert(tk.END, "(Aucun geste spécifique)\n")
            
        text_widget.config(state="disabled")
    
    def refresh_spell_list(self):
        self.spell_listbox.delete(0, tk.END)
        for spell in self.generator.spells:
            self.spell_listbox.insert(tk.END, spell['name'])
    
    # Modifié pour charger l'ordre final lors de la sélection
    def display_selected_spell(self, event):
        if not self.spell_listbox.curselection():
            self.clear_form() 
            self.edit_button.config(state="disabled")
            self.spell_detail_text.config(state="normal")
            self.spell_detail_text.delete("1.0", tk.END)
            self.spell_detail_text.config(state="disabled")
            return
            
        index = self.spell_listbox.curselection()[0]
        spell = self.generator.spells[index]
        
        # --- Afficher détails à droite --- 
        self.display_spell_details(spell, self.spell_detail_text)

        # --- Pré-remplir formulaire à gauche --- 
        if self.currently_editing is None or self.currently_editing == index:
            self.fill_form_with_spell_data(spell)
            if self.currently_editing is None:
                 self.edit_button.config(state="normal")
        else:
            self.edit_button.config(state="disabled")

    # Renommé depuis fill_form_with_spell et adapté pour charger ordered_runes
    def fill_form_with_spell_data(self, spell):
        """Remplit le formulaire de gauche avec les données d'un sort, y compris l'ordre final."""
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, spell['name'])
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", spell['description'])
        
        # Définir l'essence via la variable de suivi et sélectionner le radio/tab
        essence = spell.get('essence')
        if essence:
            self.selected_essence_rune.set(essence)
            # Trouver la deity et mettre à jour le radiobutton correspondant
            for deity, var in self.essence_vars.items():
                if essence in self.generator.essence_runes[deity]:
                    var.set(essence)
                    try: self.essence_notebook.select(list(self.essence_vars.keys()).index(deity))
                    except: pass
                    break
        else:
             self.selected_essence_rune.set("")
             for var in self.essence_vars.values(): var.set("")

        # Définir l'incantation via la variable de suivi et sélectionner le radio
        incantation = spell.get('incantation')
        self.selected_incantation_rune.set(incantation or "")
        self.incantation_var.set(incantation or "None")
        
        # Charger l'ordre final des runes
        self.ordered_final_runes = spell.get('ordered_runes', [])
        self.final_order_listbox.delete(0, tk.END)
        for rune_key in self.ordered_final_runes:
             full_desc = f"{rune_key} - {self.generator.get_rune_description(rune_key, self.generator.essence_runes.get(self.find_deity_for_essence(rune_key), {})) or self.generator.get_rune_description(rune_key, self.generator.incantation_runes) or self.generator.get_rune_description(rune_key, self.generator.somatic_runes) or 'Rune inconnue'}"
             self.final_order_listbox.insert(tk.END, full_desc)
        
        # Mettre à jour l'aperçu basé sur l'ordre chargé
        self.update_spell_preview()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellGeneratorApp(root)
    root.mainloop() 