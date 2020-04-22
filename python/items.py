import random

items = {
    # Stores the item types that can only have one equiped as a string list
    "unique_item_types": ["helmet", "chestplate", "leggings", "boots", "weapon", "offhand", "once_off_consumable"],
    # key -2 stores the item types that can have multiple equipped/ stored
    "regular_item_types": {
        # layout = "name" : max_ammount
        "jewellery": 5,
        "consumable": 4,
        "rubish": 99
    },
    # layout = ["name", "description", "item_type", "stat_changes", drop_chance]
    # cause I'm lazy 0: ["","","","",0]
    0: ["arrow", "It's an arrow, plain and simple, point sharp end towards enemy and shoot.", "once_off_consumable", "A+1", 0.8],
    1: ["old chestplate", "It's seen better days but it's better than nothing.", "chestplate", "h+5", 0.3],
    2: ["dented helmet", "Seems like it failed its last wearer, second time lucky.", "helmet", "h+3", 0.4],
    3: ["torn leggings", "Looks like it went through a wood chipper.", "leggings", "h+3", 0.4],
    4: ["holy boots", "Because they have lots of holes, get it.", "boots", "h+2", 0.5],
    5: ["chipped sword", "This sword has seen many battles but was never used for long, I wonder why.", "weapon", "d+3", 0.4],
    6: ["worn shield", "Might actually be better off without it.", "offhand", "h+4", 0.3],
    7: ["blue ring", "Seems like an ordinary ring not going to lie", "jewellery", "m+5", 0.5],
    8: ["bone", "An old, flaky bone, just what I wanted for christmas", "rubish", "n", 0.9],
    9: ["rotten flesh", "Eww, just very eww", "rubish", "n", 0.9],
    10: ["bandage", "It won't do much but it's better than nothing", "once_off_consumable", "H+2", 0.7],
    11: ["health potion", "Not sure what's in here but it sure fixes up wounds", "consumable", "H+20", 0.4],
    12: ["elvish bow", "The elves are know for their archery and even more for their bows", "weapon", ["d+5", "a+5"], 0.2],
    13: ["imp charm", "A carved imp horn tied around your neck, it seems to give off an aura of energy", "jewellery", ["h+5", "m*1.5"], 0.3],
    14: ["wing", "An imp's wing, kinda leathery", "rubish", "n", 0.8]
}


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
        # if kill_chance is less than the drop chance of the object adds its name to the drop list
        elif kill_chance <= i[1]:
            dropped_items.append(i[0])
            # stores each dropped item's id in a secondary list
            item_ids.append(i[2])
    # adds the items ids
    dropped_items.append(item_ids)
    # Creates a str of the items dropped
    if len(dropped_items[:-1]):
        print_str = "The items dropped are: "
        for i in dropped_items[0:-1]:
            if i == dropped_items[0:-1][-1]:
                print_str = print_str + i + ". "
            elif i == dropped_items[0:-1][-2]:
                print_str = print_str + i + " and "
            else:
                print_str = print_str + i + ", "
    else:
        print_str=""
    # adds the str at the end
    print(print_str)
    return dropped_items


def get_consumables(char):
    char_items = char.equipped_items
    consumables = []
    for item_id in char_items[-1]:
        temp_item = items.get(item_id)
        item_type = temp_item[2]
        if item_type == 'consumable':
            consumables.append(temp_item[0])
    return consumables


def use_consumable(char, consumable, check=False):
    used_item = None
    for item in items.items():
        if isinstance(item[1], list):
            if item[1][0] == consumable:
                used_item = item
                break
    item_stat = []
    if isinstance(used_item[1][3], str):
        item_stat.append(used_item[1][3])
    else:
        item_stat += used_item[1][3]

    if check:
        stat_change = char.apply_stat_changes(item_stat, check)
        return f"The {used_item[1][0]} {stat_change}"
    else:
        char.apply_stat_changes(item_stat)

        char.equipped_items.remove(used_item[1][0])
        char.equipped_items[-1].remove(used_item[0])
        return f"{char.name} used the {used_item[1][0]}"

def check_item_stats(item_id, just_stats=False):
    item = items[item_id]
    if just_stats:
        print_str = ""
    else:
        print_str = f"Item's name is {item[0]}, {item[1]}, its item type is {item[2]} and it "

    changes = item[3] 
    if isinstance(changes, str):
        changes = [changes]
    length = len(changes)
    loop_num = 1
    
    for change in changes:

        change_type = change[0]
        change_opperator = change[1]
        change_amount = change[2:]

        if change_type == 'H':
            if change_opperator == '+':
                print_str += f"increases health by +{change_amount}"
            elif change_opperator == '-':
                print_str += f"decreases health by -{change_amount}"
            elif change_opperator == '*':
                print_str += f"increases health by *{change_amount}"
        if change_type == 'h':
            if change_opperator == '+':
                print_str += f"increases max health by +{change_amount}"
            elif change_opperator == '-':
                print_str += f"decreases max health by -{change_amount}"
            elif change_opperator == '*':
                print_str += f"increases max health by *{change_amount}"
        elif change_type == 'd':
            if change_opperator == '+':
                print_str += f"increases attack by +{change_amount}"
            elif change_opperator == '-':
                print_str += f"decreases attack by -{change_amount}"
            elif change_opperator == '*':
                print_str += f"increases attack by *{change_amount}"
        elif change_type == 'A':
            if change_opperator == '+':
                print_str += f"increases ammo by +{change_amount}"
            elif change_opperator == '-':
                print_str += f"decreases ammo by -{change_amount}"
            elif change_opperator == '*':
                print_str += f"increases ammo by *{change_amount}"
        elif change_type == 'a':
            if change_opperator == '+':
                print_str += f"increases max ammo by +{change_amount}"
            elif change_opperator == '-':
                print_str += f"decreases max ammo by -{change_amount}"
            elif change_opperator == '*':
                print_str += f"increases max ammo by *{change_amount}"
        elif change_type == 'M':
            if change_opperator == '+':
                print_str += f"increases mana by +{change_amount}"
            elif change_opperator == '-':
                print_str += f"decreases mana by -{change_amount}"
            elif change_opperator == '*':
                print_str += f"increases mana by *{change_amount}"
        elif change_type == 'm':
            if change_opperator == '+':
                print_str += f"increases max mana by +{change_amount}"
            elif change_opperator == '-':
                print_str += f"decreases max mana by -{change_amount}"
            elif change_opperator == '*':
                print_str += f"increases max mana by *{change_amount}"

        if length - loop_num == 0:
            print_str += ". "
        elif length - loop_num == 1:
            print_str += " and "
        else:
            print_str += ", "
    return print_str