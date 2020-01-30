import random


attacks = {
    # layout = ["def_name", "ingame_name"]
    0: ["attack_basic", "basic attack"],
    1: ["attack_archer_basic", "archer attack"],
    2: ["attack_mage_basic", "mage attack"],
    3: ["attack_dwarf_slam", "slam"]
}
status_effects: {
    # layout = ["name", "description"]
    0: ["Stunned", "You will miss the next turn"]
}
enemy_races = {
    # layout = ["name" , health, attack, ammo, mana, [ex_attacks], [item_drops], max_drops]
    0: ["Skeleton", 20, 5.0, 0, 0, [], [8], 3],
    1: ["Zombie", 35, 4.0, 0, 0, [], [9], 3]

}

player_races = {
    # layout = ["name" , health, attack, ammo, mana, [ex_attacks]]
    100: ["Human", 60, 10.0, 0, 0, []],
    101: ["Elf", 50, 10.0, 4, 20, [1, 2]],
    102: ["Dwarf", 50, 10.0, 0, 20, [3]]
}

classes = {
    # layout = ["name", [attacks],[item_drops], [changes]]
    0: ["soldier", [0], [2, 4, 5], ["h+10", "d+2"]],
    1: ["mage", [0, 2], [3, 7], ["m+50"]],
    2: ["tank", [0], [1, 6], ["h*2", "d*0.7"]],
    3: ["archer", [0, 1], [0, 3, 4], ["a+10"]],
    100: ["boss", [], [], ["h*1.5", "d*2", "a*2", "m*2"]],
    101: ["basic", [0], [], []]

}

fight_intro = {
    # The name of the enemy is placed between the two strings
    0: ["The ", " roars a challange."],
    1: ["Head down, the ", " prepares for a fight."],
    2: ["The ", " has been staring at you for some time, I think it wants a fight."],
    3: ["You caught the ", " unaware, make the most of it."],
    4: ["The ", " caught you by suprise, get ready to fight."]
}

items = {
    # key -1 stores the item types that can only have one equiped as a string list
    -1: ["helmet", "chestplate", "leggings", "boots", "weapon", "offhand", "once_off_consumable"],
    # key -2 stores the item types that can have multiple equipped/ stored
    -2: {
        # layout = "name" : max_ammount
        "ring": 5,
        "consumable": 4,
        "rubish": 99
    },
    # layout = ["name", "description", "item_type", "stat_changes", drop_chance]
    # cause I'm lazy 0: ["","","","",0]
    0: ["arrow", "It's an arrow, plain and simple, point sharp end towards enemy and shoot.", "once_off_consumable", "a+1", 0.8],
    1: ["old chestplate", "It's seen better days but it's better than nothing.", "chestplate", "h+5", 0.2],
    2: ["dented helmet", "Seems like it failed its last wearer, second time lucky.", "helmet", "h+3", 0.3],
    3: ["torn leggings", "Looks like it went through a wood chipper.", "leggings", "h+3", 0.3],
    4: ["holy boots", "Because they have lots of holes, get it.", "boots", "h+2", 0.4],
    5: ["chipped sword", "This sword has seen many battles but was never used for long, I wonder why.", "boots", "d+3", 0.2],
    6: ["worn shield", "Might actually be better off without it.", "offhand", "h+4", 0.25],
    7: ["blue ring", "Seems like an ordinary ring not going to lie", "ring", "m+5", 0.5],
    8: ["bone", "An old, flaky bone, just what I wanted for christmas", "rubish", "n", 0.9],
    9: ["rotten flesh", "Eww, just very eww", "rubish", "n", 0.9]


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
    otherwise returns a dict
    '''
    if name_only:
        all_races = []
        for i in enemy_races.values():
            all_races.append(i[0])
        for i in player_races.values():
            all_races.append(i[0])
        return(all_races)
    else:
        all_races = {}
        for i in enemy_races.items():
            all_races[i[0]] = i[1]
        for i in player_races.items():
            all_races[i[0]] = i[1]
        return(all_races)


def get_enemy_races(name_only=False):
    '''
    Gets the enemy races stored in races.

    If name_only is true returns a list 
    otherwise a dict
    '''
    if name_only:
        enemy_races_temp = []
        for i in enemy_races.values():
            enemy_races_temp.append(i[0])
        return(enemy_races_temp)
    else:
        enemy_races_temp = {}
        for i in enemy_races.items():
            enemy_races_temp[i[0]] = i[1]
        return(enemy_races_temp)


def get_playable_races(name_only=False):
    '''
    Gets the playable races stored in races.

    If name_only is true returns a list 
    otherwise a dict
    '''
    if name_only:
        playable_races = []
        for i in player_races.values():
            playable_races.append(i[0])
        return(playable_races)
    else:
        playable_races = {}
        for i in player_races.items():
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


def is_race_valid(race=""):
    return race.capitalize() in get_playable_races(True)


def is_class_valid(classe=""):
    for classes in get_assignable_classes(True):
        if classe.lower() in classes:
            return True
    return False


def drop_items(possible_drops=[], max_drops=0):
    dropped_items = []
    items_sim = []
    item_ids = []
    # iterates through dict to grab item_name, drop_chance and item_id
    for i in items.items():
        if i[0] in possible_drops:
            items_sim.append([i[1][0], i[1][4], i[0]])
    # sorts list by drop_chance so rarest will be first
    items_sim.sort(key=lambda x: x[1])
    for i in items_sim:
        # get a random float (0,1] to test against drop_chance
        kill_chance = round(random.random(), 3)
        if len(dropped_items) == max_drops:
            break
        # if kill_chance is less than the drop chance of the object adds it to the drop list
        elif kill_chance <= i[1]:
            dropped_items.append(i[0])
            # stores each dropped item's id in a secondary list
            item_ids.append(i[2])
    # adds the items id's at the end
    dropped_items.append(item_ids)
    return dropped_items
