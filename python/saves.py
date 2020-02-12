import shelve


def load_save(save_name=""):
    save_file = shelve.open("save")
    save_load = save_file[save_name]
    save_file.close()
    return save_load


def get_save_names():
    save_file = shelve.open("save")
    save_names = list(save_file.keys())
    save_file.close()
    return save_names


def check_save_name(save_name):
    if save_name in get_save_names():
        choice = input(
            "That save name already exists, would you like to override the save? : ")
        if choice != '' and choice.lower()[0] == 'y':
            return True
        else:
            print(
                "That response wasn't valid (a valid response would be 'yes' or 'no')")
            return False
    else:
        return True


def save(player_name, player_char, rounds):
    while True:
        save_name = input("Please enter a name for this save: ")
        if check_save_name(save_name):
            break

    health = player_char.health
    attack = player_char.attack
    ammo = player_char.ammo
    mana = player_char.mana
    attacks = player_char.attacks
    equipped_items = player_char.equipped_items

    save_li = [player_name, health, attack,
               ammo, mana, attacks, equipped_items, rounds]

    save_file = shelve.open("save")
    save_file[save_name] = save_li
    save_file.close()
    return "game saved!\n"
