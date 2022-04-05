from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from agents.bayaran import Bayaran
from agents.pemilih import Pemilih


class AgenBayaran(Model):
    description = (
        "Model agen bayaran menerapkan konsep Standing Ovation Problem dalam hal pemilihan wakil rakyat"
        " yang disederhanakan."
    )

    def __init__(
            self,
            width=20,
            height=20,
            peforma=0.5,
            radius_pembanding=2,
            initial_uang=500,
            pengeluaran_uang=50,
            initial_agen_bayaran=10,
            initial_pemilih=100,
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.peforma = peforma
        self.radius_pembanding = radius_pembanding
        self.pengeluaran_uang = pengeluaran_uang
        self.initial_uang = initial_uang
        self.initial_agen_bayaran = initial_agen_bayaran
        self.initial_pemilih = initial_pemilih

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.datacollector = DataCollector(
            {
                "Milih": self.agen_milih,
                "Ragu_ragu": self.agen_ragu,
                "Tidak_milih": self.agen_tidak_milih,
            }
        )

        # Agen bayaran:
        for i in range(self.initial_agen_bayaran):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            bayaran = Bayaran(self.next_id(), (x, y), self, True, self.initial_uang)
            self.grid.place_agent(bayaran, (x, y))
            self.schedule.add(bayaran)

        # Pemilih
        for i in range(self.initial_pemilih):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            keinginan = self.random.uniform(0, 1)
            pemilih = Pemilih(self.next_id(), (x, y), self, True, keinginan)
            self.grid.place_agent(pemilih, (x, y))
            self.schedule.add(pemilih)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def agen_milih(self) -> int:
        count = [1 for agent in self.schedule.agents if
                 isinstance(agent, Pemilih) and agent.keinginan >= agent.threshold_max]

        return sum(count)

    def agen_ragu(self) -> int:
        count = [1 for agent in self.schedule.agents if
                 isinstance(agent, Pemilih) and agent.threshold_min < agent.keinginan < agent.threshold_max]

        return sum(count)

    def agen_tidak_milih(self) -> int:
        count = [1 for agent in self.schedule.agents if
                 isinstance(agent, Pemilih) and agent.keinginan < agent.threshold_min]

        return sum(count)
