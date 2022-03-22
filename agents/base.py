from mesa import Agent


class RandomWalker(Agent):
    def __init__(self, unique_id, pos, model, moore=True):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        cellmates = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(cellmates)

        self.model.grid.move_agent(self, next_move)
