class Agent:
    def __init__(self, role, name):
        self.role=role
        self.name=name
    
    def run(self):
        print(f"{self.name} ({self.role}) is running")

a=Agent("Coder-1", "coder")
a.run()