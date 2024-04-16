import random

class Agent:
    def __init__(self, l):
        self.vertex = [random.randint(0, 1) for _ in range(l)]
        #self.vertex = [1] * l
        self.score = 0
    
    def vertex_by_set(self):
        s = set()
        for i, v in enumerate(self.vertex):
            if v == 1:
                s.add(i+1)
        return s
    
    def vertex_by_string_set(self):
        s = set()
        for i, v in enumerate(self.vertex):
            if v == 1:
                s.add(str(i+1))
        return s
    
    def update(self, new_agent):
        self.vertex = new_agent.vertex[:]
        self.score = new_agent.score

    def __repr__(self):
        return f"Agent(vertex={self.vertex_by_set()}, score={self.score})"