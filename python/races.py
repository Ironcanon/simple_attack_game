enemy_races = {
    # layout = ["name" , health, attack, ammo, mana, [extra_attacks], [item_drops], max_drops]
    # cause I'm lazy 0: ["",0,0.0,0,0,[],[],0]
    0: ["Skeleton", 30, 4.5, 0, 0,  [],     [8],      4],
    1: ["Zombie",   35, 4.0, 0, 0,  [],     [9, 10],  4],
    2: ["Dark elf", 25, 5.5, 0, 15, [2],    [0, 12],  5],
    3: ["Orge",     40, 3.5, 0, 0,  [],     [10, 11], 4],
    4: ["Imp",      25, 4.0, 0, 10, [2, 4], [13, 14], 3]
}

player_races = {
    # layout = ["name" , health, attack, ammo, mana, [extra_attacks]]
    100: ["Human", 60, 10.0, 0, 0,  []],
    101: ["Elf",   50, 9.0,  0, 15, [2]],
    102: ["Dwarf", 45, 10.0, 0, 15, [3]],
    103: ["Gnome", 40, 10.0, 5, 0,  [1]]
}


def get_all_races(name_only=False):
    '''
    Gets all of the races stored in races.

    If name_only is true returns only the names as a list
    otherwise returns a dict with all values
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


def is_race_valid(race=""):
    return race.capitalize() in get_playable_races(True)
