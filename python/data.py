import random


attacks = {
    #layout = ["def_name", "ingame_name"]
    0: ["attack_basic", "basic attack"],
    1: ["attack_archer_basic", "archer attack"],
    2: ["attack_mage_basic", "mage attack"],
    3: ["attack_dwarf_slam", "slam"]
}
status_effects: {
    # layout = ["name", "description"]
    0: ["Stunned", "You will miss the next turn"]
}
races = {
    # layout = ["name" , health, dmg, ammo, mana, [ex_attacks], is_playable]
    0: ["Skeleton", 20, 5.0, 0, 0, [], False],
    1: ["Zombie", 35, 4.0, 0, 0, [], False],
    100: ["Human", 60, 10.0, 0, 0, [], True],
    101: ["Elf", 50, 10.0, 4, 20, [1, 2], True],
    102: ["Dwarf", 50, 10.0, 0, 20, [3], True]

}

classes = {
    # layout = ["name", [attacks], [changes]]
    0: ["soldier", [0], ["h+10", "d+2"]],
    1: ["mage", [0, 2], ["m+50"]],
    2: ["tank", [0], ["h*2", "d*0.7"]],
    3: ["archer", [0, 1], ["a+10"]],
    100: ["boss", [], ["h*1.5", "d*2", "a*2", "m*2"]],
    101: ["basic", [0], []]

}

fight_intro = {
    0: ["The ", " roars a challange."],
    1: ["Head down, the ", " prepares for a fight."],
    2: ["The ", " has been staring at you for some time, I think it wants a fight."],
    3: ["You caught the ", " unaware, make the most of it."],
    4: ["The ", " caught you by suprise, get ready to fight."]
}

items = {
    # key -1 stores the item types that can only have one equiped as a string list
    -1: ["helmet", "chestplate", "leggings", "boots", "weapon", "shield", "once_off_consumable"],
    # key -2 stores the item types that can have multiple equipped/ stored
    -2: {
        # layout = "name" : max_ammount
        "ring": 5,
        "consumable": 4
    },
    # layout = ["name", "description", "item_type", "stat_changes"]
    0: ["arrow", "It's an arrow, plain and simple, point sharp end towards enemy and shoot.", "once_off_consumable", "a+1"],
    1: ["old chestplate", "It's seen better days but it's better than nothing.", "chestplate", "h+5"],
    2: ["dented helmet", "Seems like it failed its last wearer, second time lucky.", "helmet", "h+3"],
    3: ["torn leggings", "Looks like it went through a wood chipper.", "leggings", "h+3"],
    4: ["holy boots", "Because they have lots of holes, get it.", "boots", "h+2"],
    5: ["chipped sword", "This sword has seen many battles but was never used for long, I wonder why.", "boots", "d+3"]
}


def get_all_classes(name_only=False):
    '''
    Gets all of the classes stored in classes.

    If name_only is true returns only the names
    '''
    all_classes = []
    if name_only:
        for i in classes.values():
            all_classes.append(i[0])
        return(all_classes)
    else:
        for i in classes.values():
            all_classes.append(i)
        return(all_classes)


def get_all_races(name_only=False):
    '''
    Gets all of the races stored in races.

    If name_only is true returns only the names
    '''
    all_races = []
    if name_only:
        for i in races.values():
            all_races.append(i[0])
        return(all_races)
    else:
        for i in races.values():
            all_races.append(i)
        return(all_races)


def get_enemy_races(name_only=False):
    '''
    Gets the enemy races stored in races.

    If name_only is true returns a list 
    otherwise a dict
    '''
    if name_only:
        enemy_races = []
        for i in races.values():
            if not i[-1]:
                enemy_races.append(i[0])
        return(enemy_races)
    else:
        enemy_races = {}
        for i in races.items():
            if not i[1][-1]:
                enemy_races[i[0]] = i[1]
        return(enemy_races)


def get_playable_races(name_only=False):
    '''
    Gets the playable races stored in races.

    If name_only is true returns a list 
    otherwise a dict
    '''
    if name_only:
        playable_races = []
        for i in races.values():
            if i[-1]:
                playable_races.append(i[0])
        return(playable_races)
    else:
        playable_races = {}
        for i in races.items():
            if i[1][-1]:
                playable_races[i[0]] = i[1]
        return(playable_races)


def get_assignable_classes(as_list=False):
    '''
    Gets all of the classes that can be either chosen or assigned.
    '''
    assignable_classes = classes.copy()
    assignable_classes.pop(100)
    assignable_classes.pop(101)

    if as_list:
        assignable_classes_li = []
        for i in assignable_classes.values():
            assignable_classes_li.append(i)
        return assignable_classes_li
    else:
        return assignable_classes
