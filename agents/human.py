from agents.base import RandomWalker
from agents.wolf import Wolf


class Human(RandomWalker):
    """
    Human that walks around and protect sheep.
    """

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        self.random_move()

        # If there are wolf present, take one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        wolves = [obj for obj in this_cell if isinstance(obj, Wolf)]
        if len(wolves) > 0:
            wolf_to_take = self.random.choice(wolves)

            # Take the wolf
            self.model.grid._remove_agent(self.pos, wolf_to_take)
            self.model.schedule.remove(wolf_to_take)
