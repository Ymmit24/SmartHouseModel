import random as ran

# modelling
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector

# visualisation window
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement

import networkx as nx


# Helper function
def more_than_half(model):
    return len([a for a in model.schedule.agents if a.preference > 0.5])


class MyAgent(Agent):
    def __init__(self, uid):
        self.preference = ran.random()
        self.unique_id = uid

    def step(self):
        self.preference = self.preference * ran.random()


class MyModel(Model):
    def __init__(self, num_nodes=100):
        self.num_nodes = num_nodes
        self.G = nx.erdos_renyi_graph(num_nodes, 0.02)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
        for i, node in enumerate(self.G.nodes):
            a = MyAgent(i)
            self.schedule.add(a)
            self.grid.place_agent(a, node)
        self.datacollector = DataCollector({"Greater": more_than_half})
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


def net_portrayal(G):
    def node_color(agent):
        if agent.preference > 0.5:
            return "FF0000"
        else:
            return "00FF00"

    def edge_color(a1, a2):
        return "0000FF"

    def edge_width(a1, a2):
        return 2

    return_portrayal = {}
    print(type(G))
    print(G.nodes[0])

    return_portrayal["nodes"] = [
        {
            "id": node_id,
            "size": 3,
            "color": node_color(G.nodes[node_id]['agent']),
            "label": None,
        }
        for (node_id, agents) in G.nodes.data("agent")
    ]

    return_portrayal["edges"] = [
        {"id": edge_id, "source": edge[0], "target": edge[1], "color": edge_color(edge[0], edge[1])}
        for edge_id, edge in enumerate(G.edges(data=True))
    ]

    return return_portrayal

if __name__ == '__main__':
    network_viz_element = NetworkModule(net_portrayal, 500, 500, library="d3")

    server = ModularServer(MyModel, [network_viz_element], "Test Network Model")
    server.launch(port=8765)
