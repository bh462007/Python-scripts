# 1. Write a base class `Agent` with:
#    - __init__(self, name) that sets self.name and self.errors = []
#    - a method log(self, message) that prints "[{name}] {message}"
#    - a method execute(self) that raises NotImplementedError
class Agent:
    def __init__(self, name):
        self.name=name
        self.errors=[]
    def log(self, message):
        print(f"[{self.name}] {message}")
    def execute(self):
        raise NotImplementedError("not implemented error raised")

# 2. Write a subclass `PlannerAgent(Agent)` that:
#    - overrides execute(self, goal)
#    - calls self.log("Planning...") 
#    - returns f"plan for {goal}"
class PlannerAgent(Agent):
    def execute(self, goal):
        self.log("Planning...")
        return f"plan for {goal}"

# 3. Write a subclass `ReviewerAgent(Agent)` that:
#    - has its own __init__(self, name, strictness="normal") 
#      -> calls super().__init__(name), then sets self.strictness = strictness
#    - overrides execute(self, code)
#    - calls self.log(f"Reviewing with {self.strictness} strictness...")
#    - returns f"review of {code}"
class ReviewerAgent(Agent):
    def __init__(self, name, strictness="normal"):
        super().__init__(name)
        self.strictness=strictness
    def execute(self,code):
        self.log(f"Reviewing with {self.strictness} strictness...")
        return f"review of {code}"

# Test it like:
p = PlannerAgent("Planner-1")
print(p.execute("build a todo app"))

r = ReviewerAgent("Reviewer-1", strictness="high")
print(r.execute("main.py"))