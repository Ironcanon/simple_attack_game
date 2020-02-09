import random

items = {
    # Stores the item types that can only have one equiped as a string list
    "unique_item_types": ["helmet", "chestplate", "leggings", "boots", "weapon", "offhand", "once_off_consumable"],
    # key -2 stores the item types that can have multiple equipped/ stored
    "regular_item_types": {
        # layout = "name" : max_ammount
        "ring": 5,
        "consumable": 4,
        "rubish": 99
    },
    # layout = ["name", "description", "item_type", "stat_changes", drop_chance]
    # cause I'm lazy 0: ["","","","",0]
    0: ["arrow", "It's an arrow, plain and simple, point sharp end towards enemy and shoot.", "once_off_consumable", "a+1", 0.8],
    1: ["old chestplate", "It's seen better days but it's better than nothing.", "chestplate", "h+5", 0.3],
    2: ["dented helmet", "Seems like it failed its last wearer, second time lucky.", "helmet", "h+3", 0.4],
    3: ["torn leggings", "Looks like it went through a wood chipper.", "leggings", "h+3", 0.4],
    4: ["holy boots", "Because they have lots of holes, get it.", "boots", "h+2", 0.5],
    5: ["chipped sword", "This sword has seen many battles but was never used for long, I wonder why.", "weapon", "d+3", 0.4],
    6: ["worn shield", "Might actually be better off without it.", "offhand", "h+4", 0.3],
    7: ["blue ring", "Seems like an ordinary ring not going to lie", "ring", "m+5", 0.5],
    8: ["bone", "An old, flaky bone, just what I wanted for christmas", "rubish", "n", 0.9],
    9: ["rotten flesh", "Eww, just very eww", "rubish", "n", 0.9],
    10: ["bandage", "It won't do much but it's better than nothing", "once_off_consumable", "h+2", 0.7],
    11: ["health potion", "Not sure what's in here but it sure fixes up wounds", "consumable", "n", 0.2],
    12: ["elvish bow", "The elves are know for their archery and even more for their bows", "weapon", ["d+5", "a+5"], 0.2]
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
    print_str = ""
    for i in dropped_items[0:-1]:
        if i == dropped_items[0:-1][-1]:
            print_str = print_str + i + ". "
        elif i == dropped_items[0:-1][-2]:
            print_str = print_str + i + " and "
        else:
            print_str = print_str + i + ", "
    # adds the str at the end
    dropped_items.append(print_str)
    return dropped_items
