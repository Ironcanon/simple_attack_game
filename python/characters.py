import random
import data


def attack_basic(char, target, check=False):
    if not check:
        target.health -= char.attack
        if target.health <= 0:
            target.health = 0
        return(f"\n{char.name} attacked {target.name} for {char.attack} damage!\n{target.name} has {target.health} health left.")
    else:
        #layout = ["attack_cost_sescription", mana_cost, ammo_cost]
        return [f"This attack will do {char.attack} dammage and is free", 0, 0]


def attack_archer_basic(char, target, check=False):
    if not check:
        if char.ammo > 0:
            target.health -= (char.attack + 5)
            char.ammo -= 1
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} shot {target.name} for {char.attack + 5} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of arrows so the attack failed!")
    else:
        #layout = ["attack_cost_sescription", mana_cost, ammo_cost]
        return [f"This attack will do {char.attack + 5} dammage and costs 1 ammo", 0, 1]


def attack_mage_basic(char, target, check=False):
    if not check:
        if char.mana >= 5:
            target.health -= (char.attack * 1.5)
            char.mana -= 5
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} blasted {target.name} for {char.attack * 1.5} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of mana so the attack failed!")
    else:
        #layout = ["attack_cost_sescription", mana_cost, ammo_cost]
        return [f"This attack will do {char.attack * 1.5} dammage and costs 5 mana", 5, 0]


def attack_dwarf_slam(char, target, check=False):
    if not check:
        if char.mana >= 10:
            target.health -= (char.attack * 2)
            char.mana -= 10
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} slammed {target.name} for {char.attack * 2} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of mana so the attack failed!")
    else:
        #layout = ["attack_cost_sescription", mana_cost, ammo_cost]
        return [f"This attack will do {char.attack * 2} dammage and costs 10 mana", 10, 0]


class Character():
    name = ""
    health = 0
    attack = 0
    ammo = 0
    mana = 0
    attacks = []
    item_drops = []
    equipped_items = []
    max_drops = 0

    def apply_stat_changes(self, changes=[], check=False):
        if not check:
            for change in changes:

                change_type = change[0]
                change_opperator = change[1]
                change_amount = change[2:]

                if change_type == 'h':
                    if change_opperator == '+':
                        self.health += float(change_amount)
                    elif change_opperator == '-':
                        self.health -= float(change_amount)
                    elif change_opperator == '*':
                        self.health *= float(change_amount)
                elif change_type == 'd':
                    if change_opperator == '+':
                        self.attack += float(change_amount)
                    elif change_opperator == '-':
                        self.attack -= float(change_amount)
                    elif change_opperator == '*':
                        self.attack *= float(change_amount)
                elif change_type == 'a':
                    if change_opperator == '+':
                        self.ammo += float(change_amount)
                    elif change_opperator == '-':
                        self.ammo -= float(change_amount)
                    elif change_opperator == '*':
                        self.ammo *= float(change_amount)
                elif change_type == 'm':
                    if change_opperator == '+':
                        self.mana += float(change_amount)
                    elif change_opperator == '-':
                        self.mana -= float(change_amount)
                    elif change_opperator == '*':
                        self.mana *= float(change_amount)
        else:
            length = len(changes)
            loop_num = 1
            print_str = ""
            for change in changes:

                change_type = change[0]
                change_opperator = change[1]
                change_amount = change[2:]

                if change_type == 'h':
                    if change_opperator == '+':
                        print_str += f"increases health by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases health by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases health by *{change_amount}"
                elif change_type == 'd':
                    if change_opperator == '+':
                        print_str += f"increases attack by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases attack by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases attack by *{change_amount}"
                elif change_type == 'a':
                    if change_opperator == '+':
                        print_str += f"increases ammo by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases ammo by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases ammo by *{change_amount}"
                elif change_type == 'm':
                    if change_opperator == '+':
                        print_str += f"increases mana by +{change_amount}"
                    elif change_opperator == '-':
                        print_str += f"decreases mana by -{change_amount}"
                    elif change_opperator == '*':
                        print_str += f"increases mana by *{change_amount}"

                if length - loop_num == 0:
                    print_str += ". "
                elif length - loop_num == 1:
                    print_str += " and "
                else:
                    print_str += ", "
            return print_str

    def equip_items(self, new_items=[]):
        if new_items[-1]:
            print("The item(s) that dropped were: " + new_items.pop())
        else:
            print("No items dropped." + new_items.pop())

        # Checks if there are any items to add
        if new_items:
            added_items = []
            # Checks if there are any currently equipped items
            if len(self.equipped_items) > 1:
                equipped_item_types = []
                new_item_types = []
                # Itterates through the item id's of the currently equipped items,
                # gets their item type and adds it to a list
                for i in self.equipped_items[-1]:
                    temp_item = data.items.get(i)
                    equipped_item_types.append(temp_item[2])
                # Itterates through the item id's of the new items,
                # gets their item type and adds it to a list
                for i in new_items[-1]:
                    temp_item = data.items.get(i)
                    new_item_types.append(temp_item[2])
                # Itterates through the new_item_types_list
                index_nit = 0
                for i in new_item_types:
                    # Checks if each type is already present
                    if i in equipped_item_types:
                        # Checks whether that item type is unique
                        if i in data.items.get("unique_item_types"):
                            #  Informs the user that an item of that type is already equipped
                            print(
                                f"As {self.name} already has a(n) {i} you will have to pick which {i} to equip")
                            # Gets the str form of the stats of the new items
                            stat_of_cur_item = self.apply_stat_changes(data.items.get(
                                self.equipped_items[-1])[equipped_item_types.index(i)], True)
                            stat_of_new_item = self.apply_stat_changes(
                                data.items.get(new_items[-1][index_nit])[3], True)
                            #  Asks the user to choose which item they want
                            while True:
                                choice = input(
                                    f"Would you like to keep your current {i} which {stat_of_cur_item} or equip the new item which {stat_of_new_item}? Enter 1 for current item or 2 for new item: ")
                                if choice == 1:
                                    # Keeping the current item
                                    break
                                elif choice == 2:
                                    # Choosing the new item
                                    self.equipped_items[-1].pop(
                                        equipped_item_types.index(i))
                                    self.equipped_items.pop(
                                        equipped_item_types.index(i))
                                    added_items.append(new_items[index_nit])
                                    added_items[-1].append(new_items[-1]
                                                           [index_nit])
                                else:
                                    # Invalid choice
                                    print(
                                        "That choice wasn't valid, please try again.")
                        # Otherwise checks if the amount currently equipped
                        # is less than the max amount allowed
                        elif equipped_item_types.count(i) < data.items.get("regular_item_types").get(i):
                            added_items.append(new_items[index_nit])
                            added_items[-1].append(new_items[-1][index_nit])
                        else:
                            print(
                                f"{self.name} couldn't equip {new_items[index_nit]} because they already have the max amount they can hold of its type")
                    else:
                        added_items.append(new_items[index_nit])
                        added_items[-1].append(new_items[-1][index_nit])
                    index_nit += 1
            else:
                for i in new_items:
                    if isinstance(i, list):
                        added_items.insert(-1, i)
                    else:
                        added_items.append(i)

            item_changes = []
            for i in added_items[-1]:
                temp_item = data.items.get(i)
                item_changes.append(temp_item[3])

            self.apply_stat_changes(item_changes)

            for i in added_items:
                if isinstance(i, list):
                    self.equipped_items[-1].append(i)
                else:
                    self.equipped_items.insert(-1, i)

    def __init__(self, atributes=[]):

        item_drops = []
        max_drops = []

        temp_race = data.get_all_races().get(atributes[0], 0)

        name = temp_race[0]
        health = temp_race[1]
        attack = temp_race[2]
        ammo = temp_race[3]
        mana = temp_race[4]
        attacks = temp_race[5]

        if len(temp_race) > 6:
            item_drops = temp_race[6]
            max_drops = temp_race[7]

        temp_class = data.classes.get(atributes[1], 0)

        name = name + " " + temp_class[0]
        attacks += temp_class[1]
        attacks = list(set(attacks))

        item_drops += temp_class[2]
        item_drops = list(set(item_drops))

        self.apply_stat_changes(temp_class[3])

        self.name = name
        self.health = health
        self.attack = attack
        self.ammo = ammo
        self.mana = mana
        self.attacks = attacks
        self.item_drops = item_drops
        self.equipped_items = [[]]
        self.max_drops = max_drops

    def __str__(self):
        return f"Character's name is {self.name}, they have {self.health} health and {self.attack} attack"


def get_random_enemy():
    enemy_atributes = []

    num_possible_races = len(data.get_enemy_races())
    enemy_atributes.append(random.randint(0, num_possible_races-1))

    possible_classes = data.get_assignable_classes()
    num_possible_classes = len(possible_classes)
    enemy_atributes.append(random.randint(0, num_possible_classes-1))

    temp_enemy = Character(enemy_atributes)
    return temp_enemy


def get_player(race="", classe=""):
    if data.is_race_valid(race) and data.is_class_valid(classe):
        player_race = 0
        player_class = 0

        for i in data.player_races.items():
            if i[1][0] == race:
                player_race = i[0]
                break
        for i in data.get_assignable_classes().items():
            if i[1][0] == classe:
                player_class = i[0]
                break
        player_attributes = [player_race, player_class]

        temp_char = Character(player_attributes)
        return temp_char


def get_available_attacks(char):
    possible_attacks = []
    attacks = char.attacks
    for i in attacks:
        possible_attacks.append(data.attacks.get(i, "")[1])
    return possible_attacks


def get_attack(attack=""):
    for i in data.attacks.items():
        if i[1][1] == attack:
            attack_id = i[0]
            break
    if attack_id == 0:
        return attack_basic
    elif attack_id == 1:
        return attack_archer_basic
    elif attack_id == 2:
        return attack_mage_basic
    elif attack_id == 3:
        return attack_dwarf_slam


def get_random_greeting(char):
    greet_range = len(data.fight_intro)-1
    rand_greet = data.fight_intro[random.randint(0, greet_range)]
    greeting = rand_greet[0] + char.name + rand_greet[1]
    return greeting


# test_li = 1
# print(isinstance(test_li, list))
