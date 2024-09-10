import dotenv
import os
import anthropic
import characters as char
import re
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

#Create monster using Character class
def create_monster(name, race, _class, level, base_hit_points, initiative):
    return char.Character(name, race, _class, level, base_hit_points, initiative)

#Convert string to JSON and create monster
def parse_monster_info(monster_description):
    monster_json = json.loads(monster_description)
    print(monster_json)
    return create_monster(
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


############## MAIN ######################

#message array to keep conversation history
message_array = []
#Prompt to Anthropic to start the campaign
campaign_start_message = ai_message_format("user",
    """Act as a Dungeon Master for Dungeons and Dragons. 
    Come up with a fantasy campaign and describe its beginning. 
    Do not introduce any monsters in first response (at start of the campaign).
    In Later responses, If you introduce any monsters, please provide their stats in the following format:
    {"monster": [Name], "race": [Race], "class": [Class], "level": [Level], "hp": [Hit Points], "initiative": [Initiative]}
    Do not include + in initiative values
    Exclude acknowledgement of receiving the prompt from the output"""
)

#append init prompt to message array as user role
message_array.append(campaign_start_message)
#get response from Anthropic for initial prompt
campaign_start_response = ai_response(message_array)
#append response for starting the campaing into message array as assistant role
message_array.append(ai_message_format("assistant", campaign_start_response))

print(campaign_start_response)

# Create player characters
player_characters = [
    char.Character("Eldrin", "Tiefling", "Knight", 1, 10, 1),
    char.Character("Thorne", "Human", "Fighter", 1, 12, 2),
    char.Character("Conan", "Orc", "Barbarian", 1, 8, 3)
]

while True:
    user_input = input("\nYou: ").strip()
    
    #if user input it not empty proceed, if exit strings are in input, exit app
    if len(user_input) > 0:
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Game over")
            break
        
        #prompt for inputs, append user inputs into message array as user role
        prompt = ai_message_format("user", user_input)
        message_array.append(prompt)
        #get response from Anthropic considering all conversation history (message_array), print response and add into message array as assistant role
        response = ai_response(message_array)
        print(response)
        message_array.append(ai_message_format("assistant", response))
        
        # Check for new monsters in the response
        monsters = []
        monster_matches = re.findall(r"\{.*\}", response)
        for match in monster_matches:
            #if there are monsters in response, create them as Character class and add to monsters list
            monster = parse_monster_info(match)
            if monster:
                monsters.append(monster)
        
        #if there are monsters, simulate the combat
        if monsters:
            combat_result = simulate_combat(player_characters, monsters, message_array)
            print("\nCombat Result:")
            print(combat_result)