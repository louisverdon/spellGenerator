from flask import Flask, render_template, request, jsonify, abort
import os
from .spell_generator_logic import SpellGenerator

app = Flask(__name__)

# Adjust the path to spells.json relative to this app.py file
# It should be in the parent directory of web_app
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SpellGenerator.spells_file_path = os.path.join(project_root, "spells.json")

generator = SpellGenerator() # Instance is created after path is set

@app.route('/')
def index():
    # Ensure spells are loaded on first request or if data is stale
    # generator.load_spells() # load_spells is called in __init__ now
    return render_template('index.html', 
                           essence_runes=generator.get_essence_runes_by_deity(), 
                           incantation_runes=generator.get_incantation_runes(), 
                           somatic_runes=generator.get_somatic_runes(),
                           spells=generator.spells)

# API to get all spells
@app.route('/api/spells', methods=['GET'])
def get_all_spells_api():
    return jsonify(generator.spells)

# API to get essence runes
@app.route('/api/runes/essence', methods=['GET'])
def get_essence_runes_api():
    return jsonify(generator.get_essence_runes_by_deity())

# API to get incantation runes
@app.route('/api/runes/incantation', methods=['GET'])
def get_incantation_runes_api():
    return jsonify(generator.get_incantation_runes())

# API to get somatic runes
@app.route('/api/runes/somatic', methods=['GET'])
def get_somatic_runes_api():
    return jsonify(generator.get_somatic_runes())

# API to get a specific spell by index
@app.route('/api/spell/<int:index>', methods=['GET'])
def get_spell_details_api(index):
    try:
        spell = generator.spells[index]
        return jsonify(spell)
    except IndexError:
        abort(404, description="Spell not found")

# API to create a new spell
@app.route('/api/spell', methods=['POST'])
def create_spell_api():
    data = request.json
    if not data:
        abort(400, description="Request body must be JSON")
    try:
        # Ensure ordered_runes is present and is a list
        if 'ordered_runes' not in data or not isinstance(data['ordered_runes'], list):
             abort(400, description="'ordered_runes' is required and must be a list.")
        if not data.get('essence') and not any(r in generator.get_all_essence_runes() for r in data['ordered_runes']):
            abort(400, description="An essence rune must be selected or included in ordered_runes.")

        spell = generator.create_spell(
            name=data.get('name'),
            description=data.get('description'),
            essence=data.get('essence'), # Selected essence from form
            incantation=data.get('incantation'), # Selected incantation
            somatic_runes=data.get('somatic_runes', []), # Somatic runes derived in JS, passed here
            ordered_runes=data['ordered_runes'] # The final, crucial order
        )
        return jsonify(spell), 201
    except KeyError as e:
        abort(400, description=f'Missing data: {e}')
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        app.logger.error(f"Error creating spell: {e}")
        abort(500, description="Internal server error creating spell")


# API to update an existing spell
@app.route('/api/spell/<int:index>', methods=['PUT'])
def update_spell_api(index):
    if not (0 <= index < len(generator.spells)):
        abort(404, description="Spell not found for update")
    data = request.json
    if not data:
        abort(400, description="Request body must be JSON for update")
    try:
        if 'ordered_runes' not in data or not isinstance(data['ordered_runes'], list):
             abort(400, description="'ordered_runes' is required and must be a list for update.")
        if not data.get('essence') and not any(r in generator.get_all_essence_runes() for r in data['ordered_runes']):
            abort(400, description="An essence rune must be selected or included in ordered_runes for update.")

        spell = generator.update_spell(
            index=index,
            name=data.get('name'),
            description=data.get('description'),
            essence=data.get('essence'),
            incantation=data.get('incantation'),
            somatic_runes=data.get('somatic_runes', []),
            ordered_runes=data['ordered_runes']
        )
        return jsonify(spell)
    except KeyError as e:
        abort(400, description=f'Missing data for update: {e}')
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        app.logger.error(f"Error updating spell: {e}")
        abort(500, description="Internal server error updating spell")

# API to delete a spell
@app.route('/api/spell/<int:index>', methods=['DELETE'])
def delete_spell_api(index):
    try:
        del generator.spells[index]
        generator.save_spells()
        return jsonify({'message': 'Spell deleted successfully'}), 200
    except IndexError:
        abort(404, description="Spell not found for deletion")
    except Exception as e:
        app.logger.error(f"Error deleting spell: {e}")
        abort(500, description="Internal server error deleting spell")


if __name__ == '__main__':
    app.run(debug=True) 