import shelve
from characters import Character, Party


def load_save(save_name=""):
    save_file = shelve.open("saves/save")
    save_load = save_file[save_name]

    player_chars = []
    player_name = save_load[0][0]

    for char_li in save_load[:-1]:
        temp_char = Character([0, 0])

        temp_char.name = char_li[0]
        temp_char.health = char_li[1]
        temp_char.max_health = char_li[2]
        temp_char.attack = char_li[3]
        temp_char.ammo = char_li[4]
        temp_char.max_ammo = char_li[5]
        temp_char.mana = char_li[6]
        temp_char.max_mana = char_li[7]
        temp_char.attacks = char_li[8]
        temp_char.equipped_items = char_li[9]
        player_chars.append(temp_char)
    rounds = save_load[-1]

    player_party = Party(player_chars)

    save_file.close()
    return [player_name, player_party, rounds]


def get_save_names():
    save_file = shelve.open("saves/save")
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


def delete_save(save_name):
    save_file = shelve.open("python/saves/save")
    save_file.pop(save_name)
    save_file.close()


def save(player_name, player_party, rounds):
    while True:
        save_name = input("Please enter a name for this save: ")
        if check_save_name(save_name):
            break

    save_li = player_party.output_save().append(rounds)

    save_file = shelve.open("saves/save")
    save_file[save_name] = save_li
    save_file.close()
    return "Game saved!\n"
