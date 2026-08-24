def check_agent_status(agent_name, errors, role):
    # 1. If `errors` list is empty, print: "[agent_name] is healthy"
    #    Otherwise print: "[agent_name] has N error(s)"
    #    (use an f-string, and use truthy/falsy check, not len(errors) == 0)

    if not errors:
        print(f"[{agent_name}] is healthy")
    else:
        print(f"[{agent_name}] has {len(errors)} errro(s)")
    
    # 2. Then use `match` on `role` to print one of:
    #    "planner" -> "Planning next steps..."
    #    "coder"   -> "Generating code..."
    #    "tester"  -> "Running tests..."
    #    anything else -> "Unknown role, cannot proceed"

    match role:
        case "planner":
            print("Planning next steps...")
        case "coder":
            print("Generating code...")
        case "tester":
            print("Running tests...")
        case "orchestrator":
            print("Orchastrating...")
        case _:
            print("Unknown role, cannot proceed")
    
    pass  # replace this with your code

check_agent_status("Coder-1", [], "coder")
print("-" * 20)
check_agent_status("Tester-2", ["timeout", "assertion failed"], "tester")
print("-" * 20)
check_agent_status("Mystery-3", [], "orchestrator")