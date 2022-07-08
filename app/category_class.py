
class Category:
    def __init__(self, name: str, planned: float, actual: float, goal: float):
        self.name = name
        self.planned = planned
        self.actual = actual
        self.goal = goal
        self.diff: float = planned - actual
        self.goal_met: bool = goal <= planned

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_planned(self,planned):
        self.planned = planned

    def get_planned(self):
        return self.planned

    def set_actual(self, actual):
        self.actual = actual

    def get_actual(self):
        return self.actual

    def set_goal(self, goal):
        self.goal = goal

    def get_goal(self):
        return self.goal

    def get_diff(self):
        return self.diff

    def get_goal_met(self):
        return self.goal_met