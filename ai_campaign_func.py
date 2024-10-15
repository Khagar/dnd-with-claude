import dotenv
import os
import anthropic
import characters as char
import json

dotenv.load_dotenv()
#Access Anthropic
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

#Format message for Anthropic with role
def ai_message_format(role, message_text):
    return {
        "role": role,
        "content": message_text
    }

#Prompt to Anthropic and return text of response
def ai_response(ai_messages):
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=ai_messages
    )
    return response.content[0].text

#Convert string to JSON and create monster
def parse_monster_info(monster_description):
    monster_json = json.loads(monster_description)
    print(monster_json)
    return char.Character(
        monster_json["monster"],
        monster_json["race"],
        monster_json["class"] if monster_json["class"] != 'N/A' else '',
        monster_json["level"],
        monster_json["hp"],
        monster_json["initiative"]
        )

#[PH] Simulate combat between players and monsters
def simulate_combat(player_characters, monsters, ai_messages):
    combat_prompt = ai_message_format("user", f"""
    Manage a combat encounter between the player characters and the monsters.
    Player Characters: {', '.join(str(pc) for pc in player_characters)}
    Monsters: {', '.join(str(monster) for monster in monsters)}
    
    For each round of combat:
    1. Determine initiative order.
    2. For each character or monster's turn, describe their action and calculate damage or healing.
    3. Update health points using the take_damage() or heal_damage() methods.
    4. Check if any character or monster is defeated (HP <= 0).
    5. Continue until all monsters are defeated or all player characters are defeated.

    Present the combat narrative and results in a clear, engaging manner.
    """)
    
    ai_messages.append(combat_prompt)
    combat_result = ai_response(ai_messages)
    ai_messages.append(ai_message_format("assistant", combat_result))
    
    return combat_result
