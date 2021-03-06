class Picker:

    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences
        self.next_preference = self.next_preference()
        self.current_preference = preferences[0]

    def next_preference(self):
        for i in range(len(self.preferences)):
            yield self.preferences[i]

    def set_next_preference(self):
        self.current_preference = next(self.next_preference)


class Choice:

    def __init__(self, name, preferences, capacity=None):
        self.name = name
        self.preferences = preferences
        self.capacity = capacity

    def current_pickers_number(self, pickers):
        n = 0
        for picker_name in pickers:
            if pickers[picker_name].current_preference == self.name:
                n += 1
        return n

    def good_to_go(self, pickers):
        return self.current_pickers_number(pickers) <= self.capacity

    def current_pickers(self, pickers):
        current_pickers = []
        for picker_name in pickers:
            if pickers[picker_name].current_preference == self.name:
                current_pickers.append(picker_name)
        return current_pickers


class StableMatch:

    def __init__(self, dic_pickers, dic_choices):
        self.dic_pickers = dic_pickers
        self.dic_choices = dic_choices
        self.pickers = None
        self.choices = None
        self.matches = None
        self.create_pickers()
        self.create_choices()

    def create_pickers(self):
        self.pickers = {}
        for picker_name in self.dic_pickers:
            preferences = []
            for i in range(len(self.dic_pickers[picker_name])):
                for preference in self.dic_pickers[picker_name]:
                    if int(preference['rating']) == i + 1:
                        preferences.append(preference['username'])
                        self.dic_pickers[picker_name].remove(preference)
            self.pickers[picker_name] = Picker(name=picker_name, preferences=preferences)

    def create_choices(self):
        self.choices = {}
        a = len(self.pickers)
        b = len(self.dic_choices)
        capacity = int(a/b if a%b == 0 else a//b + 1)
        for choice_name in self.dic_choices:
            preferences = []
            for i in range(len(self.dic_choices[choice_name])):
                for preference in self.dic_choices[choice_name]:
                    if int(preference['rating']) == i + 1:
                        preferences.append(preference['username'])
                        self.dic_choices[choice_name].remove(preference)
            self.choices[choice_name] = Choice(name=choice_name, preferences=preferences, capacity=capacity)

    def solved(self):
        for choice_name in self.choices:
            if not self.choices[choice_name].good_to_go(self.pickers):
                return False, self.choices[choice_name]
        return True, None

    def solve(self):
        solved, problem_choice = self.solved()
        while not solved:
            if not solved:
                bottom_preferences = problem_choice.preferences[problem_choice.capacity:]
                bottom_preferences.reverse()
                for picker_name in bottom_preferences:
                    if self.pickers[picker_name].current_preference == problem_choice.name:
                        self.pickers[picker_name].set_next_preference()
                        break
            solved, problem_choice = self.solved()
        return {name: self.choices[name].current_pickers(self.pickers) for name in self.choices}

if __name__ == '__main__':
    dic_pickers = {'Thomas Muñoz': [{'rating': '1', 'username': 'Polo D. Vargas'}],
                   'Rodolfo Palma Otero': [{'rating': '1', 'username': 'Polo D. Vargas'}]}
    dic_choices = {'Polo D. Vargas': [{'rating': '1', 'username': 'Rodolfo Palma Otero'},
                                      {'rating': '2', 'username': 'Thomas Muñoz'}]}
    problem = StableMatch(dic_pickers=dic_pickers, dic_choices=dic_choices)
    print(problem.solve())
