class Option():
    def __init__(self, default, values=[]):
        self.values = values
        self.choice = default

    def selected(self):
    	if self.values == []:
    		return None
    	return self.values[self.choice]

    def left(self):
        self.choice -= 1
        self.choice = max(self.choice, 0)

    def right(self):
        self.choice += 1
        self.choice = min(self.choice, len(self.values)-1)
