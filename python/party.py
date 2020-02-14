class Party():
    def __init__(self, character):
        party = []
        self.party = party.append(character)

    def get_party_members_names(self):
        names = []
        for char in self.party:
            names.append(char.name)
        return names

    def __str__(self):
        print_str = 'This party contains the folowing charcters:'
        for char in self.party:
            print_str += " " + char.name
        return print_str
