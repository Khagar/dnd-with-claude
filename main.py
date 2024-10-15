import ai_campaign_func as aidnd
import characters as char
import re
import streamlit as st


st.title("Claude Sonnet AI generated Dungeons and Dragons campaing")

st.markdown("""
            Embark on an epic journey crafted by artificial intelligence!
            Prepare yourself for a unique adventure where every twist and turn is shaped by the creative prowess of Claude Sonnet, an advanced AI Dungeon Master
            """)



#message array to keep conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

    #Prompt to Anthropic to start the campaign
    campaign_start_message = aidnd.ai_message_format("user",
        """Act as a Dungeon Master for Dungeons and Dragons. 
        Come up with a fantasy campaign and describe its beginning. 
        Do not introduce any monsters in first response (at start of the campaign).
        In Later responses, If you introduce any monsters, please provide their stats in the following format:
        {"monster": [Name], "race": [Race], "class": [Class], "level": [Level], "hp": [Hit Points], "initiative": [Initiative]}
        All numeric values in monster format need to be an integer
        Do not include + in initiative values
        Exclude acknowledgement of receiving the prompt from the output"""
    )

    #append init prompt to message array as user role
    st.session_state.messages.append(campaign_start_message)
    #get response from Anthropic for initial prompt
    campaign_start_response = aidnd.ai_response(st.session_state.messages)
    #append response for starting the campaing into message array as assistant role
    st.session_state.messages.append(aidnd.ai_message_format("assistant", campaign_start_response))

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Create player characters
player_characters = [
    char.Character("Eldrin", "Tiefling", "Knight", 1, 10, 1),
    char.Character("Thorne", "Human", "Fighter", 1, 12, 2),
    char.Character("Conan", "Orc", "Barbarian", 1, 8, 3)
]


if user_input := st.chat_input("You: "):
#if user input it not empty proceed, if exit strings are in input, exit app
    if len(user_input) > 0:
        #prompt for inputs, append user inputs into message array as user role
        # with st.chat_message("user"):
        #     st.markdown(user_input)

        with st.chat_message("user"):
            st.markdown(user_input)
            st.session_state.messages.append(aidnd.ai_message_format("user", user_input))
        with st.chat_message("assistant"):
            #get response from Anthropic considering all conversation history (st.session_state.messages), print response and add into message array as assistant role
            response = aidnd.ai_response(st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append(aidnd.ai_message_format("assistant", response))

            # Check for new monsters in the response
            monsters = []
            monster_matches = re.findall(r"\{.*\}", response)
            for match in monster_matches:
                #if there are monsters in response, create them as Character class and add to monsters list
                monster = aidnd.parse_monster_info(match)
                if monster:
                    monsters.append(monster)
            
            #if there are monsters, simulate the combat
            # if monsters:
            #     combat_result = aidnd.simulate_combat(player_characters, monsters, st.session_state.messages)
            #     st.markdown("Combat results: " + response)