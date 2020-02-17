import random
import re
from items import items, drop_items
from races import player_races, enemy_races, get_all_races, get_enemy_races, get_playable_races, is_race_valid
from classes import classes, get_all_classes, get_assignable_classes, is_class_valid

fight_intro = {
    # The name of the enemy is placed between the two strings
    0: ["The ", " roars a challange."],
    1: ["Head down, the ", " prepares for a fight."],
    2: ["The ", " has been staring at you for some time, I think it wants a fight."],
    3: ["You caught the ", " unaware, make the most of it."],
    4: ["The ", " caught you by suprise, get ready to fight."],
    5: ["With a blood curling roar the ", " appears."],
    6: ["The ", " called your mom fat, mess it up."]
}
status_effects = {
    # layout = ["name", "description", effect, duration]
    0: ["stunned", "they will miss this ", "ds", 1],
    1: ["burnt", "they will take 5 damage at the beginning of their turn for the next ", "dH-5", 5],
    2: ["refreshed", "they will be cured of all status effects at the beginning of their next ", "bc", 1],
    3: ["strengthened", "their attack will be increased by 5 for the next ", "bd+5", 5]
}


class Character():
    def __init__(self, atributes=[]):

        item_drops = []
        max_drops = []

        temp_race = get_all_races().get(atributes[0], 0)

        name = temp_race[0]
        health = temp_race[1]
        attack = temp_race[2]
        ammo = temp_race[3]
        mana = temp_race[4]
        attacks = temp_race[5]
        speed = temp_race[6]
        try:
            item_drops = temp_race[7]
            max_drops = temp_race[8]
        except IndexError:
            pass
            # Character is a player

        temp_class = classes.get(atributes[1], 0)

        name = name + " " + temp_class[0]
        attacks += temp_class[1]
        attacks = list(set(attacks))

        item_drops += temp_class[2]
        item_drops = list(set(item_drops))

        self.name = name
        self.health, self.max_health = health, health
        self.attack = attack
        self.ammo, self.max_ammo = ammo, ammo
        self.mana, self.max_mana = mana, mana
        self.attacks = attacks
        self.speed = speed
        self.item_drops = item_drops
        self.equipped_items = [[]]
        self.max_drops = max_drops
        self.effects = []
        self.can_attack = True

        self.apply_stat_changes(temp_class[3])

    def apply_stat_changes(self, changes=[], check=False):
        if not check:
            for change in changes:
                change_type = change[0]
                if change_type != 'n':
                    change_opperator = change[1]
                    change_amount = change[2:]

                    if change_type.upper() == 'H':
                        if change_type == 'h':
                            if change_opperator == '+':
                                self.max_health += float(change_amount)
                            elif change_opperator == '-':
                                self.max_health -= float(change_amount)
                            elif change_opperator == '*':
                                self.max_health *= float(change_amount)
                        if change_opperator == '+':
                            self.health += float(change_amount)
                        elif change_opperator == '-':
                            self.health -= float(change_amount)
                        elif change_opperator == '*':
                            self.health *= float(change_amount)

                        if self.health > self.max_health:
                            self.health = self.max_health

                    elif change_type == 'd':
                        if change_opperator == '+':
                            self.attack += float(change_amount)
                        elif change_opperator == '-':
                            self.attack -= float(change_amount)
                        elif change_opperator == '*':
                            self.attack *= float(change_amount)

                    elif change_type.upper() == 'A':
                        if change_type == 'a':
                            if change_opperator == '+':
                                self.max_ammo += float(change_amount)
                            elif change_opperator == '-':
                                self.max_ammo -= float(change_amount)
                            elif change_opperator == '*':
                                self.max_ammo *= float(change_amount)
                        if change_opperator == '+':
                            self.ammo += float(change_amount)
                        elif change_opperator == '-':
                            self.ammo -= float(change_amount)
                        elif change_opperator == '*':
                            self.ammo *= float(change_amount)

                        if self.ammo > self.max_ammo:
                            self.ammo = self.max_ammo

                    elif change_type.upper() == 'M':
                        if change_type == 'm':
                            if change_opperator == '+':
                                self.max_mana += float(change_amount)
                            elif change_opperator == '-':
                                self.max_mana -= float(change_amount)
                            elif change_opperator == '*':
                                self.max_mana *= float(change_amount)
                        if change_opperator == '+':
                            self.mana += float(change_amount)
                        elif change_opperator == '-':
                            self.mana -= float(change_amount)
                        elif change_opperator == '*':
                            self.mana *= float(change_amount)

                        if self.mana > self.max_mana:
                            self.mana = self.max_mana
        else:
            length = len(changes)
            loop_num = 1
            print_str = ""
            for change in changes:

                change_type = change[0]
                change_opperator = change[1]
                change_amount = change[2:]

                if change_type == 'H':
                    if change_opperator == '+':
                        print_str += f"increases health by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases health by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases health by *{change_amount}"
                if change_type == 'h':
                    if change_opperator == '+':
                        print_str += f"increases max health by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases max health by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases max health by *{change_amount}"
                elif change_type == 'd':
                    if change_opperator == '+':
                        print_str += f"increases attack by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases attack by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases attack by *{change_amount}"
                elif change_type == 'A':
                    if change_opperator == '+':
                        print_str += f"increases ammo by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases ammo by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases ammo by *{change_amount}"
                elif change_type == 'a':
                    if change_opperator == '+':
                        print_str += f"increases max ammo by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases max ammo by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases max ammo by *{change_amount}"
                elif change_type == 'M':
                    if change_opperator == '+':
                        print_str += f"increases mana by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases mana by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases mana by *{change_amount}"
                elif change_type == 'm':
                    if change_opperator == '+':
                        print_str += f"increases max mana by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases max mana by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases max mana by *{change_amount}"

                if length - loop_num == 0:
                    print_str += ". "
                elif length - loop_num == 1:
                    print_str += " and "
                else:
                    print_str += ", "
            return print_str

    def equip_items(self, new_items=[]):
        if new_items[-1]:
            print("The item(s) that dropped were: " + new_items.pop() + "\n")
        else:
            print("No items dropped." + new_items.pop() + "\n")

        # Checks if there are any items to add
        if new_items:
            added_items = [[]]
            # Checks if there are any currently equipped items
            if len(self.equipped_items) > 1:
                equipped_item_types = []
                new_item_types = []
                # Itterates through the item id's of the currently equipped items,
                # gets their item type and adds it to a list
                for i in self.equipped_items[-1]:
                    temp_item = items.get(i)
                    equipped_item_types.append(temp_item[2])
                # Itterates through the item id's of the new items,
                # gets their item type and adds it to a list
                for i in new_items[-1]:
                    temp_item = items.get(i)
                    new_item_types.append(temp_item[2])
                # Itterates through the new_item_types_list
                index_nit = 0
                for i in new_item_types:
                    # Checks if each type is already present
                    if i in equipped_item_types:
                        # Checks whether that item type is unique
                        if i in items.get("unique_item_types"):
                            # Checks if the same item is already equipped
                            if self.equipped_items[-1][equipped_item_types.index(i)] == new_items[-1][index_nit]:
                                print(
                                    f"{self.name} already has a(n) {items.get(self.equipped_items[-1][equipped_item_types.index(i)])[0]}")
                            else:
                                #  Informs the user that an item of that type is already equipped
                                print(
                                    f"As {self.name} already has a(n) {i} you will have to pick which {i} to equip")
                                # Gets the str form of the stats of the new items
                                cur_item = items.get(
                                    self.equipped_items[-1][equipped_item_types.index(i)])
                                stat_of_cur_item = [cur_item[3]]

                                new_item = items.get(
                                    new_items[-1][index_nit])
                                stat_of_new_item = [new_item[3]]

                                stat_of_cur_item_str = self.apply_stat_changes(
                                    stat_of_cur_item, True)
                                stat_of_new_item_str = self.apply_stat_changes(
                                    stat_of_new_item, True)
                                #  Asks the user to choose which item they want
                                while True:
                                    choice = input(
                                        f"Would you like to keep your current {i} which {stat_of_cur_item_str} or equip the new item which {stat_of_new_item_str}? Enter 1 for current item or 2 for new item: ")
                                    if choice == 1:
                                        # Keeping the current item
                                        break
                                    elif choice == 2:
                                        # Choosing the new item
                                        self.equipped_items[-1].pop(
                                            equipped_item_types.index(i))
                                        self.equipped_items.pop(
                                            equipped_item_types.index(i))
                                        added_items.append(
                                            new_items[index_nit])
                                        added_items[-1].append(new_items[-1]
                                                               [index_nit])
                                    else:
                                        # Invalid choice
                                        print(
                                            "That choice wasn't valid, please try again.")
                        # Otherwise checks if the amount currently equipped
                        # is less than the max amount allowed
                        elif equipped_item_types.count(i) < items.get("regular_item_types").get(i):
                            added_items.insert(-1, new_items[index_nit])
                            added_items[-1].append(new_items[-1][index_nit])
                        else:
                            print(
                                f"{self.name} couldn't equip {new_items[index_nit]} because they already have the max amount they can hold of its type")
                    else:
                        # If item type isn't already equipped, adds it to items to be equipped
                        added_items.insert(-1, new_items[index_nit])
                        added_items[-1].append(new_items[-1][index_nit])
                    index_nit += 1
            else:
                added_items = new_items.copy()

            item_changes = []
            for i in added_items[-1]:
                # Gets the stat changes from the newly added items
                temp_item = items.get(i)
                if isinstance(temp_item[3], str):
                    item_changes.append(temp_item[3])
                else:
                    item_changes += temp_item[3]

            self.apply_stat_changes(item_changes)

            for i in added_items:
                if isinstance(i, list):
                    for j in i:
                        if items.get(j)[2] == "once_off_consumable":
                            added_items.remove(items.get(j)[0])
                        else:
                            self.equipped_items[-1].append(j)
                else:
                    self.equipped_items.insert(-1, i)

    def apply_status_effects(self):
        buffs = []
        debuffs = []
        clear_debuffs = False
        effects_str = ""
        # Itterates through the char's status effects stored in format [status_id,duration_left]
        for i in self.effects:
            effect = status_effects.get(i[0])
            # Checks if the effect is a buff
            if effect[2][0] == 'b':
                # Checks if it is refresh
                if effect[2][1] == 'c':
                    clear_debuffs = True
                else:
                    # Adds the effect's stat change, the dur left and the effect id
                    buffs.append([effect[2], i[1], i[0]])
            else:
                debuffs.append([effect[2], i[1], i[0]])
        # Empties the char's status effects and defaults the can_attack bool
        self.effects.clear()
        self.can_attack = True
        # If char had refresh removes any debuffs
        if clear_debuffs:
            debuffs.clear()
        # Itterates over debuffs applying effects and adding them to an output string
        for i in debuffs:
            effect = status_effects.get(i[2])
            dur_left = i[1]

            if dur_left > 1:
                dur_left = f"{dur_left} rounds"
            else:
                dur_left = "round"

            effects_str += f"{self.name} is {effect[0]} so {effect[1]}{dur_left}\n"
            if i[0][1:] == 's':
                self.can_attack = False
            else:
                self.apply_stat_changes([i[0][1:]])
            i[1] -= 1
            # If the remaining duration is 0 removes that effect
            if i[1] == 0:
                debuffs.remove(i)
        # Does the same for buffs
        for i in buffs:
            effect = status_effects.get(i[2])
            effects_str += f"You are {effect[0]} so {effect[1]}\n"

            self.apply_stat_changes([i[0][1:]])
            i[1] -= 1
            if i[1] == 0:
                buffs.remove(i)
        # Joins the remaining effects
        effects = buffs + debuffs
        for i in effects:
            # Re-enters the effects
            self.effects.append([i[2], i[1]])
        # Returns the output string
        return effects_str

    def get_random_greeting(self):
        greet_range = len(fight_intro)-1
        rand_greet = fight_intro[random.randint(0, greet_range)]
        greeting = rand_greet[0] + self.name + rand_greet[1]
        return greeting

    def output_save(self):
        return self.name, self.health, self.max_health, self.attack, self.ammo, self.max_ammo, self.mana, self.max_mana, self.attacks, self.equipped_items

    def __str__(self):
        item_str = ""
        if len(self.equipped_items) == 1:
            item_str = "no"
        else:
            if len(self.equipped_items[:-1]) == 1:
                item_str = self.equipped_items[:-1][0]
            else:
                for i in self.equipped_items[:-1]:
                    if i == self.equipped_items[:-1][-1]:
                        item_str = item_str + i
                    elif i == self.equipped_items[:-1][-2]:
                        item_str = item_str + i + " and "
                    else:
                        item_str = item_str + i + ", "

        return f"Character's name is {self.name}, they have {self.health} out of {self.max_health} health, {self.attack} attack, {self.mana} out of {self.max_mana} mana, {self.ammo} out of {self.max_ammo} ammo and has {item_str} item(s)"


class Party():
    def __init__(self, *characters):
        self.party = []
        self.items = [[]]
        for char in characters:
            self.party.append(char)

    def get_party_members_names(self):
        names = []
        for char in self.party:
            names.append(char.name)
        return names

    def get_member_from_name(self, char_name):
        for char in self.party:
            if char_name == char.name:
                return char

    def add_items(self, item_li=[]):
        self.items.extend(item_li[:-1])
        self.items[-1].extend(item_li[-1])

    def get_party_health(self):
        health = 0
        for char in self.party:
            health += char.health
        return health

    def get_random_greeting(self):
        greetings = ''
        for char in self.party:
            if char != self.party[-1]:
                greetings += char.get_random_greeting() + '\n'
            else:
                greetings += char.get_random_greeting()
        return greetings

    def get_dead_party_members(self):
        dead_party_members = []
        for char in self.party:
            if char.health == 0:
                dead_party_members.append(char)
        return dead_party_members

    def add_party_member(self, char):
        self.party.append(char)

    def output_save(self):
        save_output = []
        for char in self.party:
            save_output.append(char.output_save)
        return save_output

    def __str__(self):
        print_str = 'This party contains the folowing charcters:'
        for char in self.party:
            print_str += " " + char.name
        return print_str


def get_random_enemy():
    enemy_atributes = []

    num_possible_races = len(get_enemy_races())
    enemy_atributes.append(random.randint(0, num_possible_races-1))

    possible_classes = get_assignable_classes()
    num_possible_classes = len(possible_classes)
    enemy_atributes.append(random.randint(0, num_possible_classes-1))

    temp_enemy = Character(enemy_atributes)
    return temp_enemy


def get_enemy_party(round_num, is_boss_round=False):
    enemy_party = None
    if is_boss_round:
        boss = get_random_boss()
        enemy_party = Party(boss)
    else:
        extra_enemies = round_num // 10
        enemies = []
        for _ in range(0, 1 + extra_enemies):
            temp_enemy = get_random_enemy()
            enemies.append(temp_enemy)
        enemy_party = Party(enemies)
    return enemy_party


def get_random_boss():
    temp_boss = get_random_enemy()
    boss_class = classes.get(100)
    temp_boss.name += " " + boss_class[0]
    temp_boss.apply_stat_changes(boss_class[3])
    temp_boss.max_drops = 5
    return temp_boss


def get_player(race="", classe=""):
    if is_race_valid(race) and is_class_valid(classe):
        player_race = 0
        player_class = 0

        for i in player_races.items():
            if i[1][0] == race:
                player_race = i[0]
                break
        for i in get_assignable_classes().items():
            if i[1][0] == classe:
                player_class = i[0]
                break
        player_attributes = [player_race, player_class]

        temp_char = Character(player_attributes)
        return temp_char
