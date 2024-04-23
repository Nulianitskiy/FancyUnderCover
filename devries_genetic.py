import random

from agent import Agent

class Devries:
    def __init__(self, graph, agent_count, stop_point):
        self.G = graph
        self.agent_count = agent_count
        self.stop_point = stop_point
        self.n_nodes = graph.number_of_nodes()
        self.agents = self.generate(agent_count)
        
        self.doom_count = 0
    
    def generate(self, n):
        agents = []
        for _ in range(n):
            agents.append(Agent(self.n_nodes))
        return agents
    
    def mutate(self, agent):
        while True:
            i = random.randint(0, self.n_nodes - 1)
            
            if agent.vertex[i] == 0:
                agent.vertex[i] = 1
            else:
                agent.vertex[i] = 0
            
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
        for u, v in self.G.edges():
            if u not in nodes and v not in nodes:
                return False
        return True

    def fitness_function(self, agent):
        if not self.is_edge_cover(agent.vertex_by_set()):
            return -1
        return 1 - (len(agent.vertex_by_set())/self.n_nodes)
        
    def get_best(self):
        return max(self.agents, key=lambda agent: agent.score)
    
    def take_score(self):
        for agent in self.agents:
            agent.score = self.fitness_function(agent)
            
            
    def doom_mutation(self, agent):
        for _ in range(random.randint(0, self.n_nodes - 1)):
            
            while True:
                i = random.randint(0, self.n_nodes - 1)
                
                if agent.vertex[i] == 0:
                    agent.vertex[i] = 1
                else:
                    agent.vertex[i] = 0
                
                if 1 in agent.vertex:
                    break
                
        return agent
    
    def doom(self):
        self.doom_count += 1
        
        new_pop = self.agents.copy()
        
        for i in range(self.agent_count):
            new_pop[i] = self.doom_mutation(new_pop[i])
        
        self.agents = new_pop
        self.take_score()
    
    def iteration(self):
        i = random.random()
        
        if i <= 0.05:
            self.doom()
        else:    
            #select
            a = sorted(self.agents, key=lambda agent: agent.score, reverse=True)
            new_pop = a[:int(self.agent_count * 0.4)]
            
            # mutate
            n = int(self.agent_count * 0.4)
            p = int(self.agent_count * 0.2)
            
            for i in range(p):
                a, b = self.crossingover(new_pop[i], new_pop[random.randint(0,n-1)])
                new_pop.append(a)
                new_pop.append(b)
                
            for agent in new_pop:
                i = random.random()
                if i <= 0.2:
                    agent = self.mutate(agent)
            
            #new
            for _ in range(p):
                new_pop.append(Agent(self.n_nodes))
            
            self.agents = new_pop
            self.take_score()