import json
from modules.combatant import Combatant
from modules.storyline import StoryLine
from modules.dialogueoption import DialogueOption
from modules.duel import Duel

def load_game_from_json(json_path: str):
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Create player from string
    player = Combatant.from_string(data["player"])

    # Dictionaries used as lookup tables
    story_by_id = {}
    duel_by_id = {}

    # Create empty placeholders
    for story in data["storylines"]:
        story_by_id[story["id"]] = StoryLine(id=story["id"], text=story["text"], options=[])

    for duel in data["duels"]:
        duel_by_id[duel["id"]] = None  # placeholder

    # Dictionary unpacking to merge two dictionaries into one
    elements_by_id = {**story_by_id, **duel_by_id}

    # Fill in options
    for story in data["storylines"]:
        story_by_id[story["id"]].options = [ DialogueOption(opt["text"], elements_by_id.get(opt["next_id"])) for opt in story["options"] ]
        # This is a list comprehension — a compact way to build a list.
        # The outer loop iterates over each story in the JSON.
        # The inner loop iterates over that story's options.
        # For each option, we instantiate a DialogueOption object:
        #   - The first argument is the option's display text.
        #   - The second argument is a lookup: we try to find the object
        #     (StoryLine or Duel) corresponding to opt["next_id"] in elements_by_id.
        # If opt["next_id"] doesn't exist as a key, elements_by_id.get(...) safely returns None,
        # so no KeyError is raised, and the option will just point to nothing (i.e., an endpoint).

    # Fill in duels
    for duel in data["duels"]:
        enemy = Combatant.from_string(duel["enemy"])
        duel_by_id[duel["id"]] = Duel(
            id=duel['id'], 
            win_story=story_by_id.get(duel["win_id"]),
            lose_story=story_by_id.get(duel["lose_id"]),
            enemy=enemy
        )

    return player, elements_by_id[data["storylines"][0]["id"]]
