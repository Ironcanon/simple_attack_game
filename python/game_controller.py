import characters
import data
import random

player_name = ""
player_char = None


def game():
    kill_count = 0
    player_info = game_setup()
    player_name, player_char = player_info[0], player_info[1]
    while player_char.health > 0:
        reg_round(player_char, player_name)
        kill_count += 1
    else:
        return f"\n\tGAME OVER\n\tYou managed to kill {kill_count} enemy(s)\n\tThanks for playing!\n\tCreated by Alexander Pezarro\n"


def game_setup():

    print("\n\n\n\tThe Game!\n")

    char_name = input("Please enter your characters name: ")

    print(f"Wellcome {char_name}!")
    print("It's time to choose your character, first choose a race.\n")

    avalible_races = data.get_playable_races(True)

    print("The avalible races are: ", end="")

    for i in avalible_races:
        if i == avalible_races[-2]:
            print(i, end=" and ")
        elif i == avalible_races[-1]:
            print(i, end=". ")
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
            "\nChoose an attack or enter '?' to check available ammo and/or mana: ")
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
            if player.ammo == 0 and player.mana == 0:
                print(f"{player_name} has no ammo nor mana.")
            elif player.ammo == 0:
                print(f"{player_name} has {player.mana} mana")
            elif player.mana == 0:
                print(f"{player_name} has {player.ammo} ammo")
            else:
                print(
                    f"{player_name} has {player.mana} mana and {player.ammo} ammo")
        else:
            print(
                "That choice wasn't valid (a valid response would be '?' or an attack name), please try again.")
    return f"{player_name}'s turn is finished\n"


def enemy_turn(enemy, player):
    print("It is the enemy's turn")
    enemy.attacks.sort(reverse=True)
    for i in enemy.attacks:
        attack_check = data.attacks.get(i)[1]
        attack = characters.get_attack(attack_check)
        check_str = attack(enemy, player, True)
        if enemy.mana >= check_str[1] and enemy.ammo >= check_str[2]:
            print(attack(enemy, player))
            break
    return "Enemy's turn is finished\n"


def reg_round(player, player_name):
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
            break
        else:
            print(enemy_turn(enemy, player))
        if player.health == 0:
            print(f"{player_name} was defeated by the {enemy.name}\n")
            break


print(game())
