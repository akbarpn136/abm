from agents.base import RandomWalker
from agents.grass import GrassPatch


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.
    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        living = True

        if self.model.grass:
            # Reduce energy
            self.energy -= 1

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.sheep_gain_from_food
                grass_patch.fully_grown = False

            # Death
            if self.energy < 0:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                living = False

        if living and self.random.random() < self.model.sheep_reproduce:
            # Create a new sheep:
            if self.model.grass:
                self.energy /= 2
            lamb = Sheep(
                self.model.next_id(), self.pos, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)
