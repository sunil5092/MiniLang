# functions.py
from .errors import ReturnValue

class FunctionSystem:
    """
    Stores function definitions and performs function calls.
    Works with dynamic scoping.
    """
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.funcs = interpreter.funcs   # shared with core

    def call(self, name, args, caller_env):
        if name not in self.funcs:
            raise Exception(f"Function '{name}' not defined")

        params, body = self.funcs[name]

        # Dynamic scoping:
        # Function inherits caller's environment
        dyn_env = {}
        if caller_env:
            dyn_env.update(caller_env)

        # Bind arguments
        for p, v in zip(params, args):
            dyn_env[p] = v

        try:
            # Execute function body in dynamic environment
            self.interpreter.run_block(body, 0, len(body), dyn_env)
        except ReturnValue as r:
            return r.value

        return None
