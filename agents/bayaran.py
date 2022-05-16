from agents.base import RandomWalker
from agents.pemilih import Pemilih


class Bayaran(RandomWalker):
    """
    Agen bayaran yang bergerak secara acak memberikan uang ke pemilih.
    """

    def __init__(self, unique_id, pos, model, moore, uang=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.uang = uang

    def step(self):
        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        pemilih = [obj for obj in this_cell if isinstance(obj, Pemilih)]

        if len(pemilih) > 0:
            pengaruhi_pemilih = self.random.choice(pemilih)

            if pengaruhi_pemilih.terima == False:
                pengaruhi_pemilih.pemberian = self.model.pengeluaran_uang

                self.uang -= self.model.pengeluaran_uang

        if self.uang <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
