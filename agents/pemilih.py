from agents.base import RandomWalker


class Pemilih(RandomWalker):
    """
    Agen yang memiliki hak memilih wakil rakyat.
    Agen ini ada yang masih ragu-ragu untuk memilih dan sudah memiliki pilihan.
    """
    pemberian = 0

    def __init__(self, unique_id, pos, model, moore, keinginan=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.keinginan = keinginan
        self.threshold_max = 0.8
        self.threshold_min = 0.5
        self.peforma = model.peforma

        if self.pemberian <= 10:
            self.skor = 0.01
        elif 10 < self.pemberian < 25:
            self.skor = 0.2
        else:
            self.skor = 0.5

    def step(self):
        self.random_move()

        pemilih_sekitar = self.model.grid.get_neighbors(self.pos, self.moore, True, self.model.radius_pembanding)
        pemilih = [obj for obj in pemilih_sekitar if isinstance(obj, Pemilih)]
        jumlah_individu = sum(map(lambda individu: individu.keinginan >= self.threshold_max, pemilih))

        homogenkah = self.model.initial_tipe_pemilih == "Homogen"

        if homogenkah:
            noise = self.random.uniform(-0.1, 0.1)
        else:
            noise = self.random.gauss(0.0, 0.1)

        if len(pemilih) > 0:
            if jumlah_individu / len(pemilih) >= 0.7:
                self.keinginan += self.peforma + noise * self.skor

        if self.keinginan >= 1:
            self.keinginan = 1
        elif self.keinginan < 0:
            self.keinginan = 0
