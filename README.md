# D&D Game Simulator

This Python script simulates a Dungeons & Dragons (D&D) game, acting as an automated Dungeon Master. It uses the Anthropic API to generate campaign narratives and manage combat encounters.

The game will start with an initial campaign description. You can then interact with the game by typing your actions or questions. The AI will respond and manage the game accordingly.

To exit the game, type "quit", "exit", or "q".

## Features

- Generates a fantasy campaign using the Anthropic AI
- Creates and manages player characters
- Dynamically generates monsters with stats
- Simulates combat encounters
- Maintains conversation history for context

## Prerequisites

- Python 3.x
- `dotenv` library
- `anthropic` library

## Setup

1. Clone this repository or download the script.
2. Install required libraries:
   ```
   pip install python-dotenv 
   pip install anthropic
   ```
3. Create a `.env` file in the same directory as the script and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Code Structure

### main.py

- `ai_message_format()`: Formats messages for the Anthropic API
- `ai_response()`: Sends prompts to the Anthropic API and returns responses
- `create_monster()`: Creates a monster using the Character class
- `parse_monster_info()`: Parses monster information from JSON strings
- `simulate_combat()`: Simulates combat between players and monsters

### characters.py

This file contains the `Character` class, which is used to create both player characters and monsters. The class has the following features:

- Attributes: name, race, class, level, hit points, initiative, experience, and equipment
- Methods for managing health, taking damage, healing, leveling up, and equipping items
- Customizable damage and armor multipliers based on level and equipment

This is very simplistic version that only covers meele combat. Proper DnD statistics (saving throws and skills) and spells will be implemented at later stage

Key methods include:

- `take_damage()`: Reduces hit points based on incoming damage and armor
- `heal_damage()`: Increases hit points
- `level_up()`: Increases level and adjusts attributes when experience threshold is reached
- `equip_weapon()`: Updates damage calculations based on equipped weapon
- `equip_armor()`: Updates armor multiplier based on equipped armor