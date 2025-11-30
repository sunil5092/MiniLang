import re
from .errors import MiniLangError, LazyValue

class Evaluator:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def eval(self, expr, env):
        expr = expr.strip()

        # lazy
        if expr.startswith("lazy "):
            inner = expr[5:].strip()
            if inner.startswith("(") and inner.endswith(")"):
                inner_expr = inner[1:-1]
                return LazyValue(lambda: self.eval(inner_expr, env))

        # string methods
        if "." in expr and "(" in expr and expr.endswith(")"):
            try:
                left, right = expr.split(".", 1)
                method, args_str = right.split("(", 1)
                args_str = args_str[:-1]
                try:
                    value = eval(left, {}, env)
                except:
                    value = env.get(left, None)

                if isinstance(value, str):
                    args = [self.eval(a.strip(), env) for a in args_str.split(",")] \
                           if args_str.strip() else []
                    if hasattr(value, method):
                        return getattr(value, method)(*args)
            except:
                pass

        # function call
        if "(" in expr and expr.endswith(")"):
            fname, args_str = expr.split("(", 1)
            fname = fname.strip()
            args_str = args_str[:-1]

            if fname == "force":
                v = self.eval(args_str, env)
                return v.force() if isinstance(v, LazyValue) else v

            if fname == "len":
                return len(self.eval(args_str, env))

            if fname == "str":
                return str(self.eval(args_str, env))

            if fname in self.interpreter.funcs:
                args = [self.eval(a.strip(), env) for a in args_str.split(",")] \
                        if args_str.strip() else []
                return self.interpreter.call_function(fname, args, env)

        # list indexing
        if "[" in expr and expr.endswith("]"):
            left, idx = expr.split("[", 1)
            left = left.strip()
            if left.isidentifier():
                idx = idx[:-1]
                return env[left][self.eval(idx, env)]

        # variable lookup
        if expr.isidentifier() and expr in env:
            return env[expr]

        # identifier replacement (except functions)
        tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr)
        for t in tokens:
            if t in self.interpreter.funcs:
                continue
            if t in env:
                expr = expr.replace(t, f"({repr(env[t])})")

        # ENABLE RECURSION — inject function names into env
        for fname in self.interpreter.funcs.keys():
            env[fname] = lambda *args, f=fname: self.interpreter.call_function(f, list(args), env)

        try:
            return eval(expr, {}, env)
        except Exception as e:
            raise MiniLangError(str(e))
