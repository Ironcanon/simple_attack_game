import random
from characters import status_effects
attacks = {
    # layout = ["def_name", "ingame_name"]
    0: ["attack_basic", "basic attack"],
    1: ["attack_archer_basic", "archer attack"],
    2: ["attack_mage_basic", "mage attack"],
    3: ["attack_dwarf_slam", "slam"],
    4: ["attack_imp_blaze", "blaze"]
}


def attack_basic(char, target, check=False):
    if not check:
        attack_dmg = round(char.attack, 1)
        target.health -= attack_dmg
        target.health = round(target.health, 1)
        if target.health <= 0:
            target.health = 0
        return(f"\n{char.name} attacked {target.name} for {attack_dmg} damage!\n{target.name} has {target.health} health left.")
    else:
        # layout = ["attack_cost_description", mana_cost, ammo_cost]
        return [f"This attack will do {attack_dmg} dammage and is free", 0, 0]


def attack_archer_basic(char, target, check=False):
    if not check:
        if char.ammo > 0:
            attack_dmg = round(char.attack + 5, 1)
            target.health -= attack_dmg
            target.health = round(target.health, 1)
            char.ammo -= 1
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} shot {target.name} for {attack_dmg} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of arrows so the attack failed!")
    else:
        # layout = ["attack_cost_description", mana_cost, ammo_cost]
        return [f"This attack will do {attack_dmg} dammage and costs 1 ammo", 0, 1]


def attack_mage_basic(char, target, check=False):
    if not check:
        if char.mana >= 5:
            attack_dmg = round(char.attack * 1.5, 1)
            target.health -= attack_dmg
            target.health = round(target.health, 1)
            char.mana -= 5
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} blasted {target.name} for {attack_dmg} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of mana so the attack failed!")
    else:
        # layout = ["attack_cost_description", mana_cost, ammo_cost]
        return [f"This attack will do {attack_dmg} dammage and costs 5 mana", 5, 0]


def attack_dwarf_slam(char, target, check=False):
    effect_id = 0
    effect_chance = 0.5
    if not check:
        if char.mana >= 10:
            attack_dmg = round(char.attack * 2, 1)
            target.health -= attack_dmg
            target.health = round(target.health, 1)
            char.mana -= 10
            effect_chance_roll = random.random()
            if effect_chance_roll < effect_chance:
                target.effects.append(
                    [effect_id, status_effects[effect_id][3]])
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} slammed {target.name} for {attack_dmg} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of mana so the attack failed!")
    else:
        # layout = ["attack_cost_description", mana_cost, ammo_cost]
        return [f"This attack will do {attack_dmg} dammage, have a 50% chance to stun the target and costs 10 mana", 10, 0]


def attack_imp_blaze(char, target, check=False):
    effect_id = 1
    effect_chance = 0.8
    if not check:
        if char.mana >= 10:
            attack_dmg = round((char.attack * 0.8), 1)
            target.health -= attack_dmg
            target.health = round(target.health, 1)
            char.mana -= 10
            effect_chance_roll = random.random()
            if effect_chance_roll < effect_chance:
                target.effects.append(
                    [effect_id, status_effects[effect_id][3]])
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} burnt {target.name} for {attack_dmg} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of mana so the attack failed!")
    else:
        # layout = ["attack_cost_description", mana_cost, ammo_cost]
        return [f"This attack will do {attack_dmg} dammage, have an 80% chance to burn the target and costs 10 mana", 10, 0]


def get_attack(attack=""):
    for i in attacks.items():
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


def get_available_attacks(char):
    possible_attacks = []
    pos_attacks = char.attacks
    for i in pos_attacks:
        possible_attacks.append(attacks.get(i, "")[1])
    return possible_attacks
