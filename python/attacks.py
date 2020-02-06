import random
attacks = {
    # layout = ["def_name", "ingame_name"]
    0: ["attack_basic", "basic attack"],
    1: ["attack_archer_basic", "archer attack"],
    2: ["attack_mage_basic", "mage attack"],
    3: ["attack_dwarf_slam", "slam"]
}


def attack_basic(char, target, check=False):
    if not check:
        target.health -= char.attack
        target.health = round(target.health, 1)
        if target.health <= 0:
            target.health = 0
        return(f"\n{char.name} attacked {target.name} for {char.attack} damage!\n{target.name} has {target.health} health left.")
    else:
        # layout = ["attack_cost_description", mana_cost, ammo_cost]
        return [f"This attack will do {char.attack} dammage and is free", 0, 0]


def attack_archer_basic(char, target, check=False):
    if not check:
        if char.ammo > 0:
            target.health -= (char.attack + 5)
            target.health = round(target.health, 1)
            char.ammo -= 1
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} shot {target.name} for {char.attack + 5} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of arrows so the attack failed!")
    else:
        # layout = ["attack_cost_description", mana_cost, ammo_cost]
        return [f"This attack will do {char.attack + 5} dammage and costs 1 ammo", 0, 1]


def attack_mage_basic(char, target, check=False):
    if not check:
        if char.mana >= 5:
            target.health -= (char.attack * 1.5)
            target.health = round(target.health, 1)
            char.mana -= 5
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} blasted {target.name} for {char.attack * 1.5} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of mana so the attack failed!")
    else:
        # layout = ["attack_cost_description", mana_cost, ammo_cost]
        return [f"This attack will do {char.attack * 1.5} dammage and costs 5 mana", 5, 0]


def attack_dwarf_slam(char, target, check=False):
    stunned_chance = 0.5
    if not check:
        if char.mana >= 10:
            target.health -= (char.attack * 2)
            target.health = round(target.health, 1)
            char.mana -= 10
            effect_chance = random.random()
            if effect_chance < stunned_chance:
                target.status_effects.append(0)
            if target.health <= 0:
                target.health = 0
            return(f"\n{char.name} slammed {target.name} for {char.attack * 2} damage!\n{target.name} has {target.health} health left.")
        else:
            return(f"\n{char.name} is out of mana so the attack failed!")
    else:
        # layout = ["attack_cost_description", mana_cost, ammo_cost]
        return [f"This attack will do {char.attack * 2} dammage and costs 10 mana", 10, 0]


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
