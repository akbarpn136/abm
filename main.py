from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from agents.grass import GrassPatch
from agents.human import Human
from agents.sheep import Sheep
from agents.wolf import Wolf
from models import AgenBayaran


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = dict()

    if type(agent) is Sheep:
        portrayal["Shape"] = "statics/sheep.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Wolf:
        portrayal["Shape"] = "statics/wolf.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is Human:
        portrayal["Shape"] = "statics/human.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3
        portrayal["text_color"] = "White"

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


if __name__ == "__main__":
    canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
    chart_element = ChartModule(
        [
            {"Label": "Wolves", "Color": "#AA0000"},
            {"Label": "Sheep", "Color": "#666666"},
            {"Label": "Human", "Color": "#CECECE"}
        ]
    )

    model_params = {
        "grass": UserSettableParameter("checkbox", "Grass Enabled", True),
        "grass_regrowth_time": UserSettableParameter(
            "slider", "Grass Regrowth Time", 20, 1, 50
        ),
        "initial_human": UserSettableParameter(
            "slider", "Initial Human Population", 8, 1, 10
        ),
        "initial_sheep": UserSettableParameter(
            "slider", "Initial Sheep Population", 100, 10, 300
        ),
        "sheep_reproduce": UserSettableParameter(
            "slider", "Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01
        ),
        "initial_wolves": UserSettableParameter(
            "slider", "Initial Wolf Population", 50, 10, 300
        ),
        "wolf_reproduce": UserSettableParameter(
            "slider",
            "Wolf Reproduction Rate",
            0.05,
            0.01,
            1.0,
            0.01,
            description="The rate at which wolf agents reproduce.",
        ),
        "wolf_gain_from_food": UserSettableParameter(
            "slider", "Wolf Gain From Food Rate", 20, 1, 50
        ),
        "sheep_gain_from_food": UserSettableParameter(
            "slider", "Sheep Gain From Food", 4, 1, 10
        ),
    }

    server = ModularServer(
        AgenBayaran, [canvas_element, chart_element], "Wolf Sheep Predation", model_params
    )
    server.port = 8080
    server.verbose = False
    server.launch()
