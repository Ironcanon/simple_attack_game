classes = {
    # layout = ["name", [attacks],[item_drops], [changes]]
    0: ["soldier", [0], [2, 4, 5, 11], ["h+10", "d+2"]],
    1: ["mage", [0, 2], [3, 7], ["m+40"]],
    2: ["tank", [0], [1, 2, 6], ["h*2", "d*0.7"]],
    3: ["archer", [0, 1], [0, 3, 4], ["a+10"]],
    100: ["boss", [], [], ["h*1.3", "d*1.5", "a*2", "m*2"]],
    101: ["basic", [0], [], []]
}


def get_all_classes(name_only=False):
    '''
    Gets all of the classes stored in classes.

    If name_only is true returns only the names
    '''
    all_classes = []
    if name_only:
        for i in classes.values():
            all_classes.append(i[0])
        return(all_classes)
    else:
        for i in classes.values():
            all_classes.append(i)
        return(all_classes)


def get_assignable_classes(as_list=False):
    '''
    Gets all of the classes that can be either chosen or assigned.
    '''
    assignable_classes = classes.copy()
    assignable_classes.pop(100)
    assignable_classes.pop(101)

    if as_list:
        assignable_classes_li = []
        for i in assignable_classes.values():
            assignable_classes_li.append(i)
        return assignable_classes_li
    else:
        return assignable_classes


def is_class_valid(classe=""):
    for classes in get_assignable_classes(True):
        if classe.lower() in classes:
            return True
    return False
