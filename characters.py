import random


#simplistic version of character class (no saving throws, skills) - to be expanded later
class Character:
    def __init__(self, name, race, _class, level, base_hit_points, initiative):
        self.name = name
        self.race = race
        self._base_hit_points = base_hit_points
        self.hit_points = self._base_hit_points
        self._class = _class
        self.level = level
        self.exp = 0
        self.exp_threshold = 100 + 1.6 * level
        self.initiative = initiative
        self.dmg_multiplier = 1.2 * self.level
        self.armor_multiplier = 1
        self.meele_dmg = 1 + self.dmg_multiplier
        self.equipment = {
            "weapon":"unarmed",
            "armor":"naked"
        }
    
    def get_health(self):
        return self.hit_points

    def take_damage(self, dmg):
        self.hit_points -= dmg * self.armor_multiplier
        return self.hit_points

    def heal_damage(self, heal):
        self.hit_points += heal
        return self.hit_points

    def level_up(self):
        if self.exp >= self.exp_threshold:
            self.exp = self.exp - self.exp_threshold
            self.level += 1
            self.hit_points = self._base_hit_points + 2 * self.level
            self.dmg_multiplier = self.dmg_multiplier + 1.2 * self.level 

    def get_exp(self, exp_points):
        self.exp += exp_points
        self.level_up()


    def equip_weapon(self, name, w_dmg):
        self.meele_dmg = w_dmg + self.dmg_multiplier
        self.equipment["weapon"] = name

    def equip_armor(self, name, armor_value):
        self.armor_multiplier = 0.1 * armor_value
        self.equipment["armor"] = name

    def __str__(self):
        return f"{self.name}, Level {self.level} {self.race} {self.__class__.__name__}"

# Example usage:
# knight = Character("Eldrin", "Tiefling", "Knight", 1, 10, 1)
# fighter = Character("Thorne", "Human", "Fighter", 1, 12, 2)
# barbarian = Character("Conan", "Orc", "Barbarian", 1, 8, 3)

# print(knight)
# print(f"Knight HP: {knight.hit_points}")
# print(f"Knight Weapon: {knight.equipment['weapon']}")
# print(f"Knight Dmg: {knight.meele_dmg}")

# print("\n" + str(fighter))
# print(f"Fighter HP: {fighter.hit_points}")
# fighter.equip_weapon("Pig Sticker", 3)
# print(f"Fighter Weapon: {fighter.equipment['weapon']}")
# print(f"Fighter Dmg: {fighter.meele_dmg}")

# print("\n" + str(barbarian))
# print(f"Barbarian HP: {barbarian.hit_points}")
# fighter.equip_armor("Boobplate", 20)
# print(f"Fighter Armor: {fighter.equipment['armor']}")
# print(f"Fighter Armor multi: {fighter.armor_multiplier}")