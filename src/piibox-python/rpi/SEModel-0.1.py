# import environment
import pandas as pd
import numpy as np
import random
import math
from enum import Enum

import networkx as nx

# modelling
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid

# data collection
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

# visualisation window
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement

# notebook visualisation
import matplotlib.pyplot as plt
#% matplotlib
#inline

# clustering automation feature
import multilevel_mesa as mlm

# agent.py


class Agent(Agent):
    # a member of the general population
    def __init__(
            self,
            unique_id,
            model,
            engagement,  # network activity
            trustability,  # influence limitation
            influenceability,  # sensitivity to neighbors opinion
            recovery,  # capacity to recover its initial opinion
            experience,  # gain experience at each recovery
            initial_opinion,  # defined manually through interface
            # independent variable
            opinion  # y-axis to test
    ):
        super().__init__(unique_id, model)
        self.engagement = engagement
        self.trustability = trustability
        self.influenceability = influenceability
        self.recovery = recovery
        self.experience = experience
        self.initial_opinion = initial_opinion
        self.opinion = initial_opinion

    def step(self):
        print('Stepping agent {uid}'.format(uid=self.unique_id))
        # determine what agents do at each step:
        self.check_neighbors()
        self.try_to_influence()
        self.recover()

    def check_neighbors(self):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        self.neutral_neighbors = [agent for agent in
                             self.model.grid.get_cell_list_contents(neighbors_nodes)
                             if agent.opinion > -0.5 and agent.opinion < 0.5]
        self.positive_neighbors = [agent for agent in
                              self.model.grid.get_cell_list_contents(neighbors_nodes)
                              if agent.opinion > 0.5]
        self.negative_neighbors = [agent for agent in
                              self.model.grid.get_cell_list_contents(neighbors_nodes)
                              if agent.opinion < - 0.5]

    def try_to_influence(self):
        # if opinion positive or negative, try to influence neighbors
        # if neighbor neutral, influences
        # if neighbor agree, influences
        # if neighbor disagree, battle.
        # the strongest influences, the weakest loses trustability
        # if tie, nothing happens.
        # when influences, wins engagement depending on others' influenceability
        if self.opinion <= -0.5:  # negative
            for a in self.neutral_neighbors:
                a.opinion -= 0.1 * self.trustability * self.engagement
                self.engagement += 0.05 - (0.05 * a.influenceability)
            for a in self.negative_neighbors:
                a.opinion -= 0.1 * self.trustability * self.engagement
                self.engagement += 0.01 - (0.01 * a.influenceability)
                if a.opinion < -1:
                    a.opinion = -1
            for a in self.positive_neighbors:
                if abs(self.opinion) - abs(a.opinion) > 0:  # negative is stronger
                    a.opinion -= 0.1 * self.trustability * self.engagement
                    self.engagement += 0.1 - (0.1 * a.influenceability)
                if abs(self.opinion) - abs(a.opinion) < 0:  # positive is stronger
                    self.opinion += 0.1 * a.trustability * self.engagement
                    self.trustability -= 0.1
        if self.opinion >= 0.5:  # positive
            for a in self.neutral_neighbors:
                a.opinion += 0.1 * self.trustability * self.engagement
                self.engagement += 0.05 - (0.05 * a.influenceability)
            for a in self.positive_neighbors:
                a.opinion += 0.1 * self.trustability * self.engagement
                self.engagement += 0.01 - (0.01 * a.influenceability)
                if a.opinion > 1:
                    a.opinion = 1
            for a in self.negative_neighbors:
                if abs(self.opinion) - abs(a.opinion) > 0:  # positive is stronger
                    a.opinion += 0.1 * self.trustability * self.engagement
                    self.engagement += 0.1 - (0.1 * a.influenceability)
                if abs(self.opinion) - abs(a.opinion) < 0:  # negative is stronger
                    self.opinion -= 0.1 * a.trustability * self.engagement
                    self.trustability -= 0.1

    def recover(self):
        # if opinion != initial opinion, recover depending on experience
        # when recover, gain experience depending on influenceability
        # the more influenceable, the less experience win
        if self.opinion != self.initial_opinion:
            self.opinion = self.opinion * self.recovery * self.experience
            self.experience += 0.1 - (0.1 * self.influenceability)


# previous version

#class Opinion(Enum):
#    NEGATIVE < -0.5
#    NEUTRAL > -0.5 and < 0.5
#    POSITIVE > 0.5


# datacollector functions
def number_opinion(model, state):
    return sum([1 for a in model.grid.get_all_cell_contents() if a.opinion is opinion])


def num_negative(model):
    # return number of negative opinions
    return number_opinion(model, Opinion.NEGATIVE)


def num_neutral(model):
    # return number of neutral opinions
    return number_opinion(model, Opinion.NEUTRAL)


def num_positive(model):
    # return number of positive opinions
    return number_opinion(model, Opinion.POSITIVE)


# model.py

# datacollector functions
def num_negative(model):
    # return number of negative opinions
    num_negative = [a for a in model.schedule.agents if a.opinion < -0.5]
    return len(num_negative)


def num_neutral(model):
    # return number of neutral opinions
    num_neutral = [a for a in model.schedule.agents if a.opinion > 0.5 and a.opinion < -0.5]
    return len(num_neutral)


def num_positive(model):
    # return number of positive opinions
    num_positive = [a for a in model.schedule.agents if a.opinion > 0.5]
    return len(num_positive)


def total_engagement(model):
    # engagement level in the population
    agent_engagement = [a.engagement for a in model.schedule.agents]
    return sum(agent_engagement)


def total_trustability(model):
    # trustability level in the population
    agent_trustability = [a.trustability for a in model.schedule.agents]
    return sum(agent_trustability)


def total_recovery(model):
    # recovery level in the population
    agent_recovery = [a.recovery for a in model.schedule.agents]
    return sum(agent_recovery)


def total_experience(model):
    # experience level in the population
    agent_experience = [a.experience for a in model.schedule.agents]
    return sum(agent_experience)


def public_opinion(model):
    # orientation of the population
    agent_opinion = [a.opinion for a in model.schedule.agents]
    return sum(agent_opinion) / num_nodes


class SEmodel(Model):
    # manual model has parameters set by user interface
    def __init__(
            self,
            num_nodes=100,
            avg_node_degree=3,
            # taipei : 1.92
            # telaviv : 2.16
            # tallinn : 2.20,
            engagement=0.49,
            trustability=0.21,
            influenceability=0.53,
            recovery=0.63,
            experience=1,
            initial_opinion=0,
            opinion=0,
            public_sector_opinion=1,
            corpo_opinion=1,
            startup_opinion=1,
            academic_opinion=-1,
            civil_opinion=-1,
            media_opinion=-1
    ):
        # set network layout
        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        # set space and time of the model
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
        # set model parameters
        self.engagement = engagement
        self.trustability = trustability
        self.influenceability = influenceability
        self.recovery = recovery
        self.experience = experience
        self.initial_opinion = initial_opinion
        self.opinion = initial_opinion
        self.public_sector_opinion = public_sector_opinion
        self.corpo_opinion = corpo_opinion
        self.startup_opinion = startup_opinion
        self.academic_opinion = academic_opinion
        self.civil_opinion = civil_opinion
        self.media_opinion = media_opinion
        # set data collection
        self.datacollector = DataCollector(
            {
                "Negative": num_negative,
                "Neutral": num_neutral,
                "Positive": num_positive,
                "Total Engagement": total_engagement,
                "Total Trustability": total_trustability,
                "Total Recovery": total_recovery,
                "Total Experience": total_experience,
            }
        )

        # create agents with average parameters taken on #city tweets
        for i, node in enumerate(self.G.nodes()):
            a = Agent(i,
                      self,
                      self.engagement,
                      self.trustability,
                      self.influenceability,
                      self.recovery,
                      self.experience,
                      self.initial_opinion,  # fixed by interface
                      self.opinion
                      )
            self.schedule.add(a)
            # add the undetermined agents to the network
            self.grid.place_agent(a, node)

        # create 1 representative of each stakeholder category
        public_sector = self.random.sample(self.G.nodes(), 1)
        for a in self.grid.get_cell_list_contents(public_sector):
            a.engagement = 0.57
            a.trustability = 0.53
            a.influenceability = 0.59
            a.recovery = 0.70
            a.experience = 1
            a.initial_opinion = public_sector_opinion  # fixed by interface
            a.opinion = a.initial_opinion

        corporate = self.random.sample(self.G.nodes(), 1)
        for a in self.grid.get_cell_list_contents(corporate):
            a.engagement = 0.75
            a.trustability = 0.49
            a.influenceability = 0.68
            a.recovery = 0.73
            a.experience = 1
            a.initial_opinion = corpo_opinion  # fixed by interface
            a.opinion = a.initial_opinion

        startup = self.random.sample(self.G.nodes(), 1)
        for a in self.grid.get_cell_list_contents(startup):
            a.engagement = 0.69
            a.trustability = 0.29
            a.influenceability = 0.68
            a.recovery = 0.97
            a.experience = 1
            a.initial_opinion = startup_opinion  # fixed by interface
            a.opinion = a.initial_opinion

        academic = self.random.sample(self.G.nodes(), 1)
        for a in self.grid.get_cell_list_contents(academic):
            a.engagement = 0.49
            a.trustability = 0.20
            a.influenceability = 0.65
            a.recovery = 0.75
            a.experience = 1
            a.initial_opinion = academic_opinion  # fixed by interface
            a.opinion = a.initial_opinion

        civil = self.random.sample(self.G.nodes(), 1)
        for a in self.grid.get_cell_list_contents(civil):
            a.engagement = 0.43
            a.trustability = 0.21
            a.influenceability = 0.69
            a.recovery = 0.72
            a.experience = 1
            a.initial_opinion = civil_opinion  # fixed by interface
            a.opinion = a.initial_opinion

        media = self.random.sample(self.G.nodes(), 1)
        for a in self.grid.get_cell_list_contents(media):
            a.engagement = 0.50
            a.trustability = 0.23
            a.influenceability = 0.65
            a.recovery = 0.71
            a.experience = 1
            a.initial_opinion = media_opinion  # fixed by interface
            a.opinion = a.initial_opinion

        self.running = True
        self.datacollector.collect(self)
        print('Finished initialising model, network has %s nodes' % self.G.nodes)
        nx.draw_networkx(self.G)
        plt.show()

    def positive_negative_ratio(self):
        try:
            return num_positive(self) / num_negative(self)
        except ZeroDivisionError:
            return math.inf

    def step(self):
        # advance the model by one step and collect data
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        print(self.positive_negative_ratio())

    def run_model(self, n):
        for i in range(n):
            self.step()


# server.py

# red
negative_color = "#FF0000"
# grey
neutral_color = "#808080"
# positive
positive_color = "#0400ff"


def network_portrayal(G):
    # the model ensures that there is always 1 agent per node

    def node_color(agent):
        if agent.opinion > 0.5:
            return positive_color
        if agent.opinion < -0.5:
            return negative_color
        return neutral_color

    def edge_color(agent1, agent2):
        if (agent1.opinion > 0.5 and agent2.opinion > 0.5):
            return positive_color
        if (agent1.opinion < -0.5 and agent2.opinion < -0.5):
            return negative_color
        return neutral_color

    def edge_width(agent1, agent2):
        if (agent1.opinion > 0.5 and agent2.opinion > 0.5):
            return 3
        if (agent1.opinion > 0.5 and agent2.opinion > 0.5):
            return 3
        return 2

    def get_edges(source, target):
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": "id: {}<br>opinion: {}".format(
                agents[0].unique_id, agents[0].opinion
            )
        }
        for (_, agents) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": edge_color(*get_edges(source, target)),
            "width": edge_width(*get_edges(source, target))
        }
        for (source, target) in G.edges
    ]

    return portrayal


# instantiate network module
network = NetworkModule(network_portrayal, 500, 500, library="d3")

# map data to chart in the ChartModule
chart = ChartModule(
    [
        {"Label": "Neutral", 'Color': neutral_color},
        {"Label": "Negative", 'Color': negative_color},
        {"Label": "Positive", 'Color': positive_color}
    ]
)


class MyTextElement(TextElement):
    def render(self, model):
        ratio = model.positive_negative_ratio()
        ratio_text = "&infin;" if ratio is math.inf else "{0:.2f}".format(ratio)
        positive_text = str(num_positive(model))
        negative_text = str(num_negative(model))

        return "Positive/Negative Ratio: {}<br>Positive Opinion: {}<br>Negative Opinion: {}".format(
            ratio_text, positive_text, negative_text
        )


# model parameters settable from interface
model_parameters = {
    "num_nodes": UserSettableParameter(
        "slider",
        "Number of nodes",
        100,
        10,
        1000,
        10,
        description="Number of nodes to include in the model"
    ),
    "avg_node_degree": UserSettableParameter(
        "slider",
        "Average node degree",
        2,
        1,
        5,
        0.1,
        description="Average number of links from each node"
    ),
    "initial_opinion": UserSettableParameter(
        "slider",
        "Initial opinion of undetermined nodes",
        0,
        -1,
        1,
        0.1,
        description="Opinion of the undetermined population."
    ),
    "public_sector_opinion": UserSettableParameter(
        "slider",
        "Public sector opinion",
        0,
        -1,
        1,
        1,
        description="Opinion of public sector stakeholder."
    ),
    "corpo_opinion": UserSettableParameter(
        "slider",
        "Corporate companies opinion",
        0,
        -1,
        1,
        1,
        description="Opinion of corporate companies stakeholder."
    ),
    "startup_opinion": UserSettableParameter(
        "slider",
        "Startup business opinion",
        0,
        -1,
        1,
        1,
        description="Opinion of startup business stakeholder."
    ),
    "academic_opinion": UserSettableParameter(
        "slider",
        "Academic sector opinion",
        0,
        -1,
        1,
        1,
        description="Opinion of academic sector stakeholder."
    ),
    "civil_opinion": UserSettableParameter(
        "slider",
        "Civil society opinion",
        0,
        -1,
        1,
        1,
        description="Opinion of civil society stakeholder."
    ),
    "media_opinion": UserSettableParameter(
        "slider",
        "Media industry opinion",
        0,
        -1,
        1,
        1,
        description="Opinion of media industry stakeholder."
    )
}


if __name__=='__main__':
    # create server
    server = ModularServer(
        SEmodel, [network, MyTextElement(), chart], "Stakeholder Engagement Model", model_parameters
    )
    server.port = 8765  # default port
    server.launch()

    # optional parameters to integrate to the interface to test more variables
    # "gain_engagement": UserSettableParameter(
    #     "checkbox",
    #     "Gain Engagement",
    #     value=True
    # ),
    # "gain_experience": UserSettableParameter(
    #     "checkbox",
    #     "Gain Experience",
    #     value=True
    # ),
    # "show_opinion": UserSettableParameter(
    #     "checkbox",
    #     "Show Opinion",
    #     value=True
    # ),

    # run.py

    # launch server
