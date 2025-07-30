import json
from combatant import Combatant
from storyline import StoryLine
from dialogueoption import DialogueOption
from duel import Duel

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
        story_by_id[story["id"]].options = [
            DialogueOption(opt["text"], elements_by_id[opt["next_id"]])
            for opt in story["options"]
        ]

    # Fill in duels
    for duel in data["duels"]:
        enemy = Combatant.from_string(duel["enemy"])
        duel_by_id[duel["id"]] = Duel(
            id=duel['id'], 
            win_story=story_by_id[duel["win_id"]],
            lose_story=story_by_id[duel["lose_id"]],
            enemy=enemy
        )

    return player, elements_by_id[data["storylines"][0]["id"]]
