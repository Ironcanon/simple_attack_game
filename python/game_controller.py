import characters
import data
import random
import saves

player_name = ""
player_char = None


def game():
    rounds = 0
    player_info = []

    print("\n\n\n\tWelcome to Dungoner!\n")

    welcome_str = "Would you like to start a new game"
    if saves.get_save_names():
        welcome_str += ", load an existing save"
    welcome_str += " or check the help? : "

    while True:
        choice = input(welcome_str)
        if choice.lower()[0] == 'n':
            player_info = new_game_setup()
            player_name, player_char = player_info[0], player_info[1]
            break
        elif saves.get_save_names() and choice.lower()[0] == 'l':
            print("The current saves are: ", end="")
            for i in saves.get_save_names():
                if i == saves.get_save_names()[-1]:
                    print(i, end=". ")
                elif i == saves.get_save_names()[-2]:
                    print(i, end=" and ")
                else:
                    print(i, end=", ")

            while True:
                save_choice = input(
                    "Which save would you like to load? : ").lower()
                if save_choice in saves.get_save_names():
                    break
                else:
                    print("That response was invalid, please try again")

            loaded_save = saves.load_save(save_choice)

            player_name = loaded_save[0]

            temp_char = characters.Character([0, 0])
            temp_char.health = loaded_save[1]
            temp_char.attack = loaded_save[2]
            temp_char.ammo = loaded_save[3]
            temp_char.mana = loaded_save[4]
            temp_char.attacks = loaded_save[5]
            temp_char.equiped_items = loaded_save[6]
            rounds = loaded_save[7]

            player_char = temp_char
            break

        elif choice.lower()[0] == 'h':
            with open("help.txt", mode="r") as help_file:
                for i in help_file.readlines:
                    print(i, end="")
        else:
            print("That response was invalid, please try again (valid responses are 'new game', 'load game' or 'help')")

    while player_char.health > 0:
        rounds = reg_round(player_char, player_name, rounds)
    else:
        return f"\n\tGAME OVER\n\tYou managed to pass {rounds} round(s)\n\tThanks for playing!\n\tCreated by Alexander Pezarro\n"


def new_game_setup():

    char_name = input("Please enter your characters name: ")

    print(f"Welcome {char_name}!")
    print("It's time to choose your character, first choose a race.\n")

    avalible_races = data.get_playable_races(True)

    print("The avalible races are: ", end="")

    for i in avalible_races:
        if i == avalible_races[-1]:
            print(i, end=". ")
        elif i == avalible_races[-2]:
            print(i, end=" and ")
        else:
            print(i, end=", ")

    race_choice = input("Which race would you like? : ").capitalize()

    while not race_choice or not data.is_race_valid(race_choice):
        race_choice = input(
            "That choice wasn't valid, please try again. Which race would you like? : ").capitalize()

    print(f"{race_choice}, a good choice! Now to choose a class.")
    print("The avalible classes are: ", end="")
    avalible_classes = data.get_assignable_classes(True)
    for i in avalible_classes:
        if i == avalible_classes[-2]:
            print(i[0].capitalize(), end=" and ")
        elif i == avalible_classes[-1]:
            print(i[0].capitalize(), end=". ")
        else:
            print(i[0].capitalize(), end=", ")

    class_choice = input("Which class would you like? : ").lower()

    while not class_choice or not data.is_class_valid(class_choice):
        class_choice = input(
            "That choice wasn't valid, please try again. Which class would you like? : ").lower()
    print(f"A {class_choice.capitalize()}, perfect!")

    player_char = characters.get_player(race_choice, class_choice)

    print(f"Well {char_name} the {player_char.name.lower()}, I wish you well on your adventure, bon voyage!\n")
    player_char.name = char_name
    return [char_name, player_char]


def player_turn(enemy, player, player_name):
    print(f"It is {player_name}'s turn")
    print("The available attacks are: ", end="")
    available_attacks = characters.get_available_attacks(player)
    for i in available_attacks:
        if i == available_attacks[-1]:
            print(i, end=". ")
        elif i == available_attacks[-2]:
            print(i, end=" and ")
        else:
            print(i, end=", ")

    while True:
        choice = input(
            "\nChoose an attack or enter '?' to check player stats: ")
        if choice in available_attacks:
            attack = characters.get_attack(choice)
            attack_check = input(
                f"Are you sure you want to use {choice}? Enter 'yes' or enter to attack or '?' to check attack details: ")
            if not attack_check or attack_check.lower()[0] == 'y':
                print(attack(player, enemy))
                break
            elif attack_check == '?':
                print(attack(player, enemy, True)[0])
            else:
                print(
                    "That choice wasn't valid (a valid response would be 'yes', enter or '?'), please try again.")
        elif choice == '?':
            print(player)
        else:
            print(
                "That choice wasn't valid (a valid response would be '?' or an attack name), please try again.")
    return f"{player_name}'s turn is finished\n"


def enemy_turn(enemy, player):
    print("It is the enemy's turn", end="")
    enemy.attacks.sort(reverse=True)
    for i in enemy.attacks:
        attack_check = data.attacks.get(i)[1]
        attack = characters.get_attack(attack_check)
        check_str = attack(enemy, player, True)
        if enemy.mana >= check_str[1] and enemy.ammo >= check_str[2]:
            print(attack(enemy, player))
            break
    return "Enemy's turn is finished\n"


def reg_round(player, player_name, round_number):
    enemy = characters.get_random_enemy()
    print("An enemy has appeared!")
    print(characters.get_random_greeting(enemy), end="\n\n")

    while True:
        print(player_turn(enemy, player, player_name))
        if enemy.health == 0:
            print(
                f"Congradulations {player_name} you defeated the {enemy.name}!\n")
            items = data.drop_items(enemy.item_drops, enemy.max_drops)
            player.equip_items(items)
            choice = input(
                "Would you like to save the game? (enter 'yes' to save or anything else to continue): ")
            if choice.lower()[0] == 'y':
                print(saves.save(player_name, player, round_number))
            return round_number + 1
        else:
            print(enemy_turn(enemy, player))
        if player.health == 0:
            print(f"{player_name} was defeated by the {enemy.name}\n")
            return round_number


print(game())
