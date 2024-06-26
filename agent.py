import random

class Agent:
    def __init__(self, l):
        self.vertex = self.gen(l)
        self.score = 0
        
    def gen(self, l):
        while True:
            g = [random.randint(0, 1) for _ in range(l)]
            if 1 in g:
                break 
        return g
    
    def vertex_by_set(self):
        return {i + 1 for i, v in enumerate(self.vertex) if v == 1}
    
    def vertex_by_string_set(self):
        return {str(i + 1) for i, v in enumerate(self.vertex) if v == 1}
    
    def update(self, new_agent):
        self.vertex = new_agent.vertex[:]
        self.score = new_agent.score

    def __repr__(self):
        return f"Agent(vertex={self.vertex_by_set()}, score={self.score})"