def is_save_file():
    try:
        open("save.txt", mode='r')
        return True
    except FileNotFoundError:
        open("save.txt", mode='w')
        return False


def load_save(save_name=""):
    modified_save_name = "#" + save_name
    with open("save.txt", mode='r') as save_file:
        save_lines = save_file.readlines()
        for i in range(len(save_lines)-1):
            if save_lines[i] == modified_save_name:
                return save_lines[i+1].split(',')


def get_save_names():
    with open("save.txt", mode='r') as save_file:
        saves = []
        save_lines = save_file.readlines()
        for i in save_lines:
            if '#' in i:
                saves.append(i[1:])
        return saves


def check_save_name(save_name):
    if save_name in get_save_names():
        choice = input(
            "That save name already exists, would you like to override the save? : ")
        if choice.lower()[0] == 'y':
            return 'w'
        else:
            print(
                "That response wasn't valid (a valid response would be 'yes' or 'no')")
    else:
        return 'a'


def save(player_name, player_char, rounds):
    while True:
        save_name = input("Please enter a name for this save: ")
        if check_save_name(save_name):
            break
    save_type = check_save_name(save_name)

    health = player_char.health
    attack = player_char.attack
    ammo = player_char.ammo
    mana = player_char.mana
    attacks = player_char.attacks
    equipped_items = player_char.equipped_items

    with open("save.txt", mode=save_type) as save_file:
        save_file.write(
            f"#{save_name}\n{player_name},{health},{attack},{ammo},{mana},{attacks},{equipped_items},{rounds}\n")
    return "game saved!"
