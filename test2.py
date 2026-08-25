from dataclasses import dataclass, field

@dataclass
class AgentResult:
    agent_name: str
    role: str
    success: bool
    output: str = ""
    errors: list = field(default_factory=list)

# Your tasks:

# 1. Create three AgentResult instances representing one pipeline cycle:
#    - "Planner-1", role "planner", success=True, output="plan.json created"
#    - "Coder-1", role "coder", success=True, output="main.py generated"
#    - "Tester-1", role "tester", success=False, output="2 tests failed",
#         errors=["test_add failed", "test_sub failed"]
instance1=AgentResult(
    agent_name="Planner-1",
    role="planner",
    success=True,
    output="plan.json created"
)

instance2=AgentResult(
    agent_name="Coder-1",
    role="coder",
    success=True,
    output="main.py generated"
)

instance3=AgentResult(
    agent_name="Tester-1",
    role="tester",
    success=False,
    output="2 tests failed",
    errors=["test_add failed", "test_sub failed"]
)

# 2. Put all three into a list called `pipeline_run`
pipeline_run=[instance1, instance2, instance3]

# 3. Write a function `summarize_pipeline(results)` that:
#    - loops through the list
#    - prints "[agent_name] (role): OK" if success is True
#    - prints "[agent_name] (role): FAILED - N error(s)" if success is False
def summarize_pipeline(results):
    for agent in results:
        if agent.success:
            print(f"[{agent.agent_name}] ({agent.role}): OK")
        else:
            print(f"[{agent.agent_name}] ({agent.role}): Failed - {len(agent.errors)} errors(s)")

# 4. Call summarize_pipeline(pipeline_run)
r=summarize_pipeline(pipeline_run)
print(r)