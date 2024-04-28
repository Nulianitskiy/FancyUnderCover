import random

from agent import Agent

class Devries:
    def __init__(self, graph, agent_count, stop_point):
        self.G = graph
        self.agent_count = agent_count
        self.stop_point = stop_point
        self.n_nodes = graph.number_of_nodes()
        self.agents = self.generate(agent_count)
        self.res_stash = []
        self.doom_count = 0
    
    def generate(self, n):
        return [Agent(self.n_nodes) for _ in range(n)]
    
    def mutate(self, agent):
        while True:
            i = random.randint(0, self.n_nodes - 1)
            agent.vertex[i] = 1 - agent.vertex[i]
            if 1 in agent.vertex:
                break
        return agent
    
    def crossingover(self, first, second):
        while True:
            i = random.randint(0, self.n_nodes - 1)
            a1 = Agent(self.n_nodes)
            a2 = Agent(self.n_nodes)
            a1.vertex = first.vertex[:i] + second.vertex[i:]
            a2.vertex = second.vertex[:i] + first.vertex[i:]
            if 1 in a1.vertex and 1 in a2.vertex: 
                break
        return a1, a2
    
    def is_edge_cover(self, nodes):
        return all((u in nodes or v in nodes) for u, v in self.G.edges())


    def fitness_function(self, agent):
        if not self.is_edge_cover(agent.vertex_by_set()):
            return 0
        return 1 - (len(agent.vertex_by_set()) / self.n_nodes)
        
    def get_best(self):
        return max(self.agents, key=lambda agent: agent.score)
    
    def take_score(self):
        for agent in self.agents:
            agent.score = self.fitness_function(agent)
            
            
    def doom_mutation(self, agent):
        for _ in range(random.randint(0, self.n_nodes - 1)):
            i = random.randint(0, self.n_nodes - 1)
            agent.vertex[i] = 1 - agent.vertex[i]
        return agent
    
    def doom(self):
        self.doom_count += 1
        new_pop = [self.doom_mutation(agent) for agent in self.agents]
        self.agents = new_pop
        self.take_score()
    
    def iteration(self):
        if random.random() <= 0.05:
            self.doom()
        else:    
            # Select
            sorted_agents = sorted(self.agents, key=lambda agent: agent.score, reverse=True)
            new_pop = sorted_agents[:int(self.agent_count * 0.4)]
            
            # Operations
            n = int(self.agent_count * 0.4)
            p = int(self.agent_count * 0.2)
            
            for i in range(p):
                a, b = self.crossingover(new_pop[random.randint(0, p - 1)], new_pop[random.randint(0, n - 1)])
                new_pop.extend([a, b])
                
            for agent in new_pop:
                if random.random() <= 0.2:
                    agent = self.mutate(agent)
            
            # Generate new agents
            new_pop.extend(Agent(self.n_nodes) for _ in range(p))
            
            self.agents = new_pop
            self.take_score()
            
        best_agent = self.get_best()
        self.res_stash.append(best_agent.score)