def logged(fn):
    def wrapper(*args, **kwargs):
        print(f"CALLING {fn.__name__}")
        result = fn(*args, **kwargs)
        print(f"DONE {fn.__name__}")
        return result
    return wrapper

@logged
def tester_agent(code, timeout=30, verbose=True):
    return f"testing {code} with timeout={timeout}, verbose={verbose}"

tester_agent("main.py", verbose=False)