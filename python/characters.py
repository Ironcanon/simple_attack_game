import random
import data

name = ""
health = 0
dmg = 0.0
ammo = 0
mana = 0
attacks = []


def attack_basic(char, target, check=False):
    if not check:
        target.health -= char.dmg
        if target.health <= 0:
            target.health = 0
        return(f"\n{char.name} attacked {target.name} for {char.dmg} damage!\n{target.name} has {target.health} health left.")
    else:
        #layout = ["attack_cost_sescription", mana_cost, ammo_cost]
        return ["This attack is free", 0, 0]


def attack_archer_basic(char, target, check=False):
    if not check:
        if char.ammo > 0:
            target.health -= char.dmg + 5
            char.ammo -= 1
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} shot {target.name} for {char.dmg + 5} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of arrows so the attack failed!")
    else:
        #layout = ["attack_cost_sescription", mana_cost, ammo_cost]
        return ["This attack costs 1 ammo", 0, 1]


def attack_mage_basic(char, target, check=False):
    if not check:
        if char.mana >= 5:
            target.health -= (char.dmg * 1.5)
            char.mana -= 5
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} blasted {target.name} for {char.dmg * 1.5} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of mana so the attack failed!")
    else:
        #layout = ["attack_cost_sescription", mana_cost, ammo_cost]
        return ["This attack costs 5 mana", 5, 0]


def attack_dwarf_slam(char, target, check=False):
    if not check:
        if char.mana >= 10:
            target.health -= (char.dmg * 2)
            char.mana -= 10
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} slammed {target.name} for {char.dmg * 2} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of mana so the attack failed!")
    else:
        #layout = ["attack_cost_sescription", mana_cost, ammo_cost]
        return ["This attack costs 10 mana", 10, 0]


class Character():
    name = ""
    health = 0
    dmg = 0
    ammo = 0
    mana = 0
    attacks = []

    def __init__(self, atributes=[]):
        name = self.name
        health = self.health
        dmg = self.dmg
        ammo = self.ammo
        mana = self.mana
        attacks = self.attacks

        def apply_class_changes(self, changes=[]):
            nonlocal name
            nonlocal health
            nonlocal dmg
            nonlocal ammo
            nonlocal mana
            nonlocal attacks

            for change in changes:

                change_type = change[0]
                change_opperator = change[1]
                change_amount = change[2:]

                if change_type == 'h':
                    if change_opperator == '+':
                        health += float(change_amount)
                    elif change_opperator == '-':
                        health -= float(change_amount)
                    elif change_opperator == '*':
                        health *= float(change_amount)
                elif change_type == 'd':
                    if change_opperator == '+':
                        dmg += float(change_amount)
                    elif change_opperator == '-':
                        dmg -= float(change_amount)
                    elif change_opperator == '*':
                        dmg *= float(change_amount)
                elif change_type == 'a':
                    if change_opperator == '+':
                        ammo += float(change_amount)
                    elif change_opperator == '-':
                        ammo -= float(change_amount)
                    elif change_opperator == '*':
                        ammo *= float(change_amount)
                elif change_type == 'm':
                    if change_opperator == '+':
                        mana += float(change_amount)
                    elif change_opperator == '-':
                        mana -= float(change_amount)
                    elif change_opperator == '*':
                        mana *= float(change_amount)

        temp_race = data.get_all_races().get(atributes[0], 0)

        name = temp_race[0]
        health = temp_race[1]
        dmg = temp_race[2]
        ammo = temp_race[3]
        mana = temp_race[4]
        attacks = temp_race[5]

        temp_class = data.classes.get(atributes[1], 0)

        name = name + " " + temp_class[0]
        attacks += temp_class[1]
        attacks = list(set(attacks))
        apply_class_changes(self, temp_class[2])

        self.name = name
        self.health = health
        self.dmg = dmg
        self.ammo = ammo
        self.mana = mana
        self.attacks = attacks

    def __str__(self):
        return f"Character's name is {self.name}, they have {self.health} health and {self.dmg} dmg"


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
