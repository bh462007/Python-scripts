
# 3. Write a decorator `logged` that:
#    - prints "CALLING {function name}" before the function runs
#    - runs the function
#    - prints "DONE {function name}" after
#    - returns the function's result
def logged(fn):
    def wrapper(*args, **kwargs):
        print(f"CALLING {fn.__name__}")
        result=fn(*args, **kwargs)
        print(f"DONE {fn.__name__}")
        return result
    return wrapper;

# 1. Write a function `run_pipeline(*agents)` that:
#    - takes any number of agent name strings
#    - prints "Running pipeline: agent1 -> agent2 -> agent3" (joined with " -> ")
def run_pipeline(*agents):
    print("Running pipeline: " + " -> ".join(agents))


# 2. Write a function `configure_agent(name, **settings)` that:
#    - prints "Configuring {name}"
#    - then loops through settings and prints "  {key}: {value}" for each
@logged
def configure_agent(name, **settings):
    print(f"Configuring {name}")
    
    for key,value in settings.items():
        print(f"{key} : {value}")

# Apply @logged to configure_agent, then call it like:
run_pipeline("planner", "coder", "tester")
configure_agent("Coder-1", model="sonnet", temperature=0.3)