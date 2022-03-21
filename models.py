from mesa import Model
from mesa.space import MultiGrid, SingleGrid
from mesa.time import RandomActivationByType
from mesa.datacollection import DataCollector

from agents.human import Human
from agents.wolf import Wolf
from agents.sheep import Sheep
from agents.grass import GrassPatch


class AgenBayaran(Model):
    description = (
        "Model agen bayaran menerapkan konsep Standing Ovation Problem dalam hal pemilihan wakil rakyat"
        " yang disederhanakan."
    )

    def __init__(
            self,
            width=20,
            height=20,
            initial_sheep=100,
            initial_wolves=50,
            initial_human=8,
            sheep_reproduce=0.04,
            wolf_reproduce=0.05,
            wolf_gain_from_food=20,
            grass=False,
            grass_regrowth_time=30,
            sheep_gain_from_food=4,
    ):
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.initial_human = initial_human
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivationByType(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_type_count(Wolf),
                "Sheep": lambda m: m.schedule.get_type_count(Sheep),
                "Human": lambda m: m.schedule.get_type_count(Human),
            }
        )

        # Create sheep:
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.sheep_gain_from_food)
            sheep = Sheep(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create human
        for i in range(self.initial_human):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            human = Human(self.next_id(), (x, y), self, True)
            self.grid.place_agent(human, (x, y))
            self.schedule.add(human)

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():
                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
