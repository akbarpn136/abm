from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from models import AgenBayaran
from agents.bayaran import Bayaran
from agents.pemilih import Pemilih


def bayaran_portrayal(agent):
    if agent is None:
        return

    portrayal = dict()

    if type(agent) is Bayaran:
        portrayal["Shape"] = "statics/bayaran.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3
        portrayal["text_color"] = "White"

    elif type(agent) is Pemilih:
        if agent.keinginan >= 0.8:
            portrayal["Color"] = "green"
            portrayal["Layer"] = 0
            portrayal["w"] = 1
            portrayal["h"] = 1
        elif 0.5 < agent.keinginan < 0.8:
            portrayal["Color"] = "gray"
            portrayal["Layer"] = 1
            portrayal["w"] = 0.7
            portrayal["h"] = 0.7
        else:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 2
            portrayal["w"] = 0.5
            portrayal["h"] = 0.5

        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"

    return portrayal


if __name__ == "__main__":
    canvas_element = CanvasGrid(bayaran_portrayal, 20, 20, 500, 500)
    chart_element = ChartModule(
        [
            {"Label": "Milih", "Color": "green"},
            {"Label": "Ragu_ragu", "Color": "gray"},
            {"Label": "Tidak_milih", "Color": "red"}
        ]
    )

    model_params = {
        "peforma": UserSettableParameter(
            "slider", "Peforma calon pemimpin", 0.5, 0.1, 1.0, 0.1
        ),
        "initial_agen_bayaran": UserSettableParameter(
            "slider", "Jumlah agen bayaran", 10, 1, 15
        ),
        "initial_pemilih": UserSettableParameter(
            "slider", "Jumlah pemilih", 100, 50, 350
        ),
        "initial_tipe_pemilih": UserSettableParameter(
            "choice", "Tipe Pemilih", value="Homogen", choices=("Homogen", "Heterogen")
        ),
        "initial_tipe_tetangga": UserSettableParameter(
            "choice", "Tipe Tetangga", value="Moore", choices=("Moore", "Von Neumann")
        ),
        "radius_pembanding": UserSettableParameter(
            "slider", "Radius pengamatan pemilih", 2, 1, 4
        ),
        "initial_uang": UserSettableParameter(
            "slider", "Jumlah uang", 500, 100, 1000
        ),
        "pengeluaran_uang": UserSettableParameter(
            "slider", "Jumlah uang yang dikeluarkan", 25, 10, 50
        )
    }

    server = ModularServer(
        AgenBayaran, [canvas_element, chart_element], "SOP Pemilihan Ketua", model_params
    )
    server.port = 8080
    server.verbose = False
    server.launch()
