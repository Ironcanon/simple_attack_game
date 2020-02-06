def is_save_file():
    try:
        open("save.txt", mode='x')
        return False
    except FileExistsError:
        return True


def load_save(save_name=""):
    modified_save_name = "#" + save_name + '\n'
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
            return 'o'
        else:
            print(
                "That response wasn't valid (a valid response would be 'yes' or 'no')")
            return ""
    else:
        return 'n'


def save(player_name, player_char, rounds):
    while True:
        save_name = input("Please enter a name for this save: ")
        save_type = check_save_name(save_name)
        if save_type:
            break

    with open("save.txt", mode='r') as save_file:
        lines = save_file.readlines()

    health = player_char.health
    attack = player_char.attack
    ammo = player_char.ammo
    mana = player_char.mana
    attacks = player_char.attacks
    equipped_items = player_char.equipped_items

    save_str = f"{player_name},{health},{attack},{ammo},{mana},{attacks},{equipped_items},{rounds}\n"

    if save_type == 'o':
        save_index = 0
        for i in lines:
            if i[1:] == save_name:
                save_index = lines.index(i) + 1
        lines[save_index] = save_str
        with open("save.txt", mode='w') as save_file:
            for i in lines:
                save_file.write(i)
    elif save_type == 'n':
        lines.append(
            f"#{save_name}\n{save_str}")
        with open("save.txt", mode='w') as save_file:
            for i in lines:
                save_file.write(i)
    else:
        return "Invalid save type, fix needed"
    return "game saved!"
