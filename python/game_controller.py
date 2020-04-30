from saves import check_save_name, get_save_names, load_save, save, delete_save
from classes import get_assignable_classes, is_class_valid
from races import is_race_valid, get_playable_races
from characters import Character, get_player, get_random_enemy, get_random_boss, Party, get_enemy_party, get_random_player, chance_to_get_new_player
from attacks import get_attack, attacks, get_available_attacks
from items import drop_items, get_consumables, use_consumable

player_name = ""
player_char = None


def game():
    rounds = 0
    player_info = []

    print("\n\n\n\tWelcome to Dungoner!\n")

    welcome_str = "Would you like to start a new game"
    if get_save_names():
        welcome_str += ", load an existing save"
    welcome_str += " or check the help? : "
    repeat = True
    while repeat:
        choice = input(welcome_str)
        if choice.lower()[0] == 'n':
            player_info = new_game_setup()
            player_name, player_party = player_info[0], player_info[1]
            repeat = False
            break
        elif get_save_names() and choice.lower()[0] == 'l':
            if get_save_names():
                print("The current saves are: ", end="")
                for i in get_save_names():
                    if i == get_save_names()[-1]:
                        print(i, end=". ")
                    elif i == get_save_names()[-2]:
                        print(i, end=" and ")
                    else:
                        print(i, end=", ")
                while repeat:
                    save_choice = input(
                        "\nWhich save would you like to select? (Type 'back' to go back) : ")
                    if save_choice in get_save_names():
                        while repeat:
                            choice = input(
                                "\nWould you like to load or delete this save? (Type 'back' to go back) : ")
                            if choice.lower() == 'load':
                                loaded_save = load_save(save_choice)

                                player_name = loaded_save[0]
                                player_party = loaded_save[1]
                                rounds = loaded_save[2]

                                print(
                                    f"Save {save_choice} loaded!", end='\n\n')
                                repeat = False
                                break
                            elif choice.lower() == 'delete':
                                delete_save(save_choice)
                                print(
                                    f"Save {save_choice} deleted!", end='\n\n')
                                break
                            elif choice.lower() == 'back':
                                break
                            else:
                                print("That response was invalid, please try again")

                    elif save_choice.lower() == 'back':
                        break
                    else:
                        print("That response was invalid, please try again")

            else:
                print("There are no longer any saves.")

        elif choice.lower()[0] == 'h':
            with open("help.txt", mode="r") as help_file:
                for i in help_file.readlines:
                    print(i, end="")
        else:
            print("That response was invalid, please try again (valid responses are 'new game', 'load game' or 'help')")

    while player_party.get_party_health() > 0:
        rounds = reg_round(player_party, player_name, rounds)
    else:
        return f"\n\tGAME OVER\n\tYou managed to pass {rounds} round(s)\n\tThanks for playing!\n\tCreated by Alexander Pezarro\n"


def new_game_setup():

    char_name = input("Please enter your characters name: ")

    print(f"Welcome {char_name}!")
    print("It's time to choose your character, first choose a race.\n")

    avalible_races = get_playable_races(True)

    print("The avalible races are: ", end="")

    for i in avalible_races:
        if i == avalible_races[-1]:
            print(i, end=". ")
        elif i == avalible_races[-2]:
            print(i, end=" and ")
        else:
            print(i, end=", ")

    race_choice = input("Which race would you like? : ").capitalize()

    while not race_choice or not is_race_valid(race_choice):
        race_choice = input(
            "That choice wasn't valid, please try again. Which race would you like? : ").capitalize()

    print(f"{race_choice}, a good choice! Now to choose a class.\n")
    print("The avalible classes are: ", end="")
    avalible_classes = get_assignable_classes(True)
    for i in avalible_classes:
        if i == avalible_classes[-2]:
            print(i[0].capitalize(), end=" and ")
        elif i == avalible_classes[-1]:
            print(i[0].capitalize(), end=". ")
        else:
            print(i[0].capitalize(), end=", ")

    class_choice = input("Which class would you like? : ").lower()

    while not class_choice or not is_class_valid(class_choice):
        class_choice = input(
            "That choice wasn't valid, please try again. Which class would you like? : ").lower()
    print(f"A(n) {class_choice.capitalize()}, perfect!")

    player_char = get_player(race_choice, class_choice)

    print(f"Well {char_name} the {player_char.name.lower()}, I wish you well on your adventure, bon voyage!\n")

    player_char.name = char_name
    player_party = Party(player_char)

    return [char_name, player_party]


def player_turn(enemy_party, player_party, player_name):
    print(f"It is {player_name}'s party's turn")
    for player in player_party.party:
        print(f"It's {player.name}'s chance")
        print(player.apply_status_effects(), end="")
        if player.can_attack:
            repeat = True
            while repeat:
                choice = input(
                    "\nDo you want to attack, use an item, wait or enter '?' to check player stats? : ")
                if choice.lower() == 'attack':
                    print("The available attacks are: ", end="")

                    available_attacks = get_available_attacks(player)
                    for i in available_attacks:
                        if i == available_attacks[-1]:
                            print(i, end=". ")
                        elif i == available_attacks[-2]:
                            print(i, end=" and ")
                        else:
                            print(i, end=", ")
                    while repeat:
                        choice = input(
                            "\nChoose an attack or enter 'back' to return to the previous choice: ").lower()
                        if choice in available_attacks:
                            attack = get_attack(choice)
                            attack_name = choice
                            while repeat:
                                choice = input(
                                    f"Are you sure you want to use {attack_name}? Enter 'yes' or enter to attack, '?' to check attack details or 'back' to return to the previous choice: ")
                                if not choice or choice.lower()[0] == 'y':
                                    if len(enemy_party.party) > 1:
                                        print(
                                            "The available enemies are: ", end="")
                                        for enemy in enemy_party.party:
                                            if enemy == enemy_party.party[-1]:
                                                print(enemy.name, end=". ")
                                            elif enemy == enemy_party.party[-2]:
                                                print(enemy.name, end=" and ")
                                            else:
                                                print(enemy.name, end=", ")
                                        while repeat:
                                            choice = input(
                                                "\nChoose an enemy or enter 'back' to return to the previous choice: ")
                                            if choice in enemy_party.get_party_members_names():
                                                chosen_enemy = enemy_party.get_member_from_name(
                                                    choice)
                                                print(
                                                    "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~", end="")
                                                print(
                                                    attack(player, chosen_enemy))
                                                print(
                                                    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                                repeat = False
                                                break
                                            elif choice.lower() == 'back':
                                                break
                                            else:
                                                print(
                                                    "That choice wasn't valid (a valid response would be a valid enemy name or 'back'), please try again.")
                                    else:
                                        chosen_enemy = enemy_party.party[0]
                                        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~", end="")
                                        print(attack(player, chosen_enemy))
                                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                        repeat = False
                                        break
                                elif choice == '?':
                                    print(attack(player, None, True)[0])
                                elif choice.lower() == 'back':
                                    break
                                else:
                                    print(
                                        "That choice wasn't valid (a valid response would be 'yes', enter,'?' or 'back'), please try again.")
                        elif choice.lower() == 'back':
                            break
                        else:
                            print(
                                "That choice wasn't valid (a valid response would be a valid attack name or 'back'), please try again.")
                elif choice.lower() == 'item':
                    available_consumables = get_consumables(player)
                    if available_consumables:
                        print("The available consumables are: ", end="")

                        for i in available_consumables:
                            if i == available_consumables[-1]:
                                print(i, end=". ")
                            elif i == available_consumables[-2]:
                                print(i, end=" and ")
                            else:
                                print(i, end=", ")
                        while repeat:
                            choice = input(
                                "\nChoose a consumable or enter 'back' to return to the previous choice: ")
                            if choice in available_consumables:
                                consumable = choice
                                while repeat:
                                    choice = input(
                                        f"Are you sure you want to use {consumable}? Enter 'yes' or enter to use it, '?' to check consumable details or 'back' to return to the previous choice: ")
                                    if not choice or choice.lower()[0] == 'y':
                                        print(use_consumable(
                                            player, consumable))
                                        repeat = False
                                        break
                                    elif choice == '?':
                                        print(use_consumable(
                                            player, consumable, True))
                                    elif choice.lower() == 'back':
                                        break
                                    else:
                                        print(
                                            "That choice wasn't valid (a valid response would be 'yes', enter or '?'), please try again.")
                            elif choice.lower() == 'back':
                                break
                            else:
                                print(
                                    "That choice wasn't valid (a valid response would be 'yes', enter or '?'), please try again.")
                    else:
                        print("There are no consumables available.")
                elif choice.lower() == 'wait':
                    while repeat:
                        choice = input(
                            "Are you sure you want to skip your turn? Enter 'yes' or enter to wait or 'back' to return to the previous choice: ")
                        if not choice or choice.lower()[0] == 'y':
                            print(f"{player.name} chose to skip their turn")
                            repeat = False
                            break
                        elif choice.lower() == 'back':
                            break
                        else:
                            print(
                                "That choice wasn't valid (a valid response would be attack, item, wait or ?). Please try again.")
                elif choice.lower() == '?':
                    print(player)
                else:
                    print(
                        "That choice wasn't valid (a valid response would be attack, item, wait or ?). Please try again.")

    return f"{player_name}'s party's turn is finished"


def enemy_turn(enemy_party, player_party):
    print("It is the enemy party's turn")
    for enemy in enemy_party.party:
        print(f"It's the {enemy.name}'s chance")
        print(enemy.apply_status_effects(), end="")
        if enemy.can_attack:
            enemy.attacks.sort(reverse=True)
            current_target = None
            for player_char in sorted(player_party.party,key=lambda char: char.health):
                if player_char.health > 0:
                    current_target = player_char
                    break
            for i in enemy.attacks:
                attack_check = attacks.get(i)[1]
                attack = get_attack(attack_check)
                check_str = attack(enemy, current_target, True)
                if enemy.mana >= check_str[1] and enemy.ammo >= check_str[2]:
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print(attack(enemy, current_target))
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    break
    return "Enemy party's turn is finished"


def reg_round(player_party, player_name, round_number):
    boss_round = False
    print("###########################")
    if (round_number + 1) % 5 == 0:
        boss_round = True
        print("A boss has appeared!")
    else:
        print("An enemy party has appeared!")
    enemy_party = get_enemy_party(round_number, boss_round)

    print(enemy_party.get_random_greeting(), end="\n\n")

    while enemy_party.get_party_health() > 0:
        print("----------------------------")
        print(player_turn(enemy_party, player_party, player_name))
        print("----------------------------", end="\n\n")
        killed_enemies = enemy_party.get_dead_party_members()
        if killed_enemies:
            for enemy in killed_enemies:
                print(
                    f"The {enemy.name} was defeated!\n")
                items = drop_items(enemy.item_drops, enemy.max_drops)
                player_party.add_items(items)
        else:
            print("----------------------------")
            print(enemy_turn(enemy_party, player_party))
            print("----------------------------",end="\n\n")
            killed_players = player_party.get_dead_party_members()
            if killed_players:
                for player in killed_players:
                    print(
                        f"{player.name} was defeated!\n")

        if not player_party.get_party_health() > 0:
            print(f"{player_name}'s party was defeated by the enemy party\n")
            return round_number

    print(f"Congradulations {player_name} you defeated the enemy party!")
    round_number += 1
    print("###########################")

    if chance_to_get_new_player(round_number, len(player_party.party)):
        new_player = get_random_player()
        player_party.add_party_member(new_player)
        print(f"\nCongradulations, {new_player.name} has decided to join your party!")

    if boss_round:
        while True:
            choice = input(
                "Would you like to save, quit, save and quit or continue? (enter 's' to save, 'q' to quit, 'sq' to save and quit or anything else to continue): ")
            if choice.lower() == 's':
                print(save(player_name, player_party, round_number))
                return round_number
            elif choice.lower() == 'q':
                print("Thank you for playing, hope to see you again!")
                exit()
            elif choice.lower() == 'sq':
                print(save(player_name, player_party, round_number))
                print("Thank you for playing, hope to see you again!")
                exit()
            else:
                return round_number
    print("")
    player_party.equip_items()
    return round_number
    


print(game())
