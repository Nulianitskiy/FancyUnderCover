import random

from agent import Agent

class Darwin:
    def __init__(self, graph, agent_count, stop_point):
        self.G = graph
        self.agent_count = agent_count
        self.stop_point = stop_point
        self.n_nodes = graph.number_of_nodes()
        self.agents = self.generate(agent_count)
    
    def generate(self, n):
        agents = []
        for _ in range(n):
            agents.append(Agent(self.n_nodes))
        return agents
    
    def mutate(self, agent):
        i = random.randint(0, len(agent.vertex) - 1)
        if agent.vertex[i] == 0:
            agent.vertex[i] = 1
        else:
            agent.vertex[i] = 0
        return agent
    
    def crossingover(self, first, second):
        i = random.randint(0, self.n_nodes - 1)
        new_agent1 = first.vertex[:i] + second.vertex[i:]
        new_agent2 = second.vertex[:i] + first.vertex[i:]
        
        return new_agent1, new_agent2
    
    def is_coverage(self, vertex_cover):
        subgraph = self.G.subgraph(vertex_cover)
        covered_edges = subgraph.number_of_edges()
        total_edges = self.G.number_of_edges()
        
        return covered_edges == total_edges
    
    def coverage_ratio(self, vertex_cover):
        subgraph = self.G.subgraph(vertex_cover)
        covered_edges = subgraph.number_of_edges()
        total_edges = self.G.number_of_edges()
        coverage_ratio = covered_edges / total_edges

        return coverage_ratio
    
    def fitness_function(self, agent):
        if not self.is_coverage(agent.vertex_by_set()):
            return 0
        if len(agent.vertex_by_set()) == 0:
            return 0
        return  1 - (len(agent.vertex_by_set())/self.n_nodes)
    
    def select(self):
        a = sorted(self.agents, key=lambda agent: agent.score, reverse=True)
        return a[:self.n_nodes//2].copy()
        
    def get_best(self):
        return max(self.agents, key=lambda agent: agent.score)
    
    def take_score(self):
        for agent in self.agents:
            agent.score = self.fitness_function(agent)
    
    def iteration(self):
        #select
        a = sorted(self.agents, key=lambda agent: agent.score, reverse=True)
        new_pop = a[:self.n_nodes//2]
        
        # mutate
        for agent in new_pop:
            i = random.random()
            # if i <= 0.2:
            #     agent = self.mutate(agent)
            if i > 0.2 and i <= 0.3:
                j = random.randint(0, len(new_pop) - 1)
                agent.vertex, new_pop[j].vertex = self.crossingover(agent, new_pop[j])
                
        #new
        for _ in range(int(self.agent_count//2)):
            new_pop.append(Agent(self.n_nodes))
        
        self.agents = new_pop
        self.take_score()