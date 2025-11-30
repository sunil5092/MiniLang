from .errors import MiniLangError, ReturnValue

class MiniLang:
    def __init__(self):
        self.env = {}
        self.funcs = {}
        from .evaluator import Evaluator
        from .functions import FunctionSystem
        self.evaluator = Evaluator(self)
        self.functions = FunctionSystem(self)

    ########################
    # Run full program
    ########################
    def run(self, src):
        lines = src.splitlines()
        self.run_block(lines, 0, len(lines), None)

    ########################
    # Match pattern system
    ########################
    def match_pattern(self, value, pattern, env):
        pattern = pattern.strip()

        if pattern == "_":
            return True, {}

        # literal match
        try:
            if eval(pattern, {}, env) == value:
                return True, {}
        except:
            pass

        # variable binding
        if pattern.isidentifier():
            return True, {pattern: value}

        # tuple match
        if pattern.startswith("(") and pattern.endswith(")"):
            if not isinstance(value, tuple):
                return False, {}
            inner = pattern[1:-1].strip()
            parts = [p.strip() for p in inner.split(",")]
            if len(parts) != len(value):
                return False, {}
            out = {}
            for p, v in zip(parts, value):
                ok, bind = self.match_pattern(v, p, env)
                if not ok: return False, {}
                out.update(bind)
            return True, out

        # list match
        if pattern.startswith("[") and pattern.endswith("]"):
            if not isinstance(value, list):
                return False, {}
            inner = pattern[1:-1].strip()
            parts = [p.strip() for p in inner.split(",")] if inner else []
            if len(parts) != len(value):
                return False, {}
            out = {}
            for p, v in zip(parts, value):
                ok, bind = self.match_pattern(v, p, env)
                if not ok: return False, {}
                out.update(bind)
            return True, out

        return False, {}

    ########################
    # Run a block of code
    ########################
    def run_block(self, lines, start, end, local_env):
        i = start

        while i < end:
            raw = lines[i]
            line = raw.rstrip()
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                i += 1
                continue

            env = local_env if local_env else self.env

            ###############################
            # Function Definition
            ###############################
            if stripped.startswith("def ") and stripped.endswith(":"):
                header = stripped[4:-1]
                fname, args = header.split("(", 1)
                fname = fname.strip()
                args = args.replace(")", "")
                params = [p.strip() for p in args.split(",")] if args.strip() else []

                i += 1
                b_start = i
                while i < end and lines[i].startswith("    "):
                    i += 1
                b_end = i

                body = [l[4:] for l in lines[b_start:b_end]]
                self.funcs[fname] = (params, body)
                continue

            ###############################
            # MATCH ... CASE
            ###############################
            if stripped.startswith("match ") and stripped.endswith(":"):
                expr = stripped[6:-1].strip()
                match_val = self.evaluator.eval(expr, env)

                i += 1
                cases = []

                while i < end and lines[i].startswith("    case "):
                    head = lines[i].strip()[5:]
                    pat, _ = head.split(":", 1)
                    pat = pat.strip()

                    i += 1
                    cb_start = i
                    while i < end and lines[i].startswith("        "):
                        i += 1
                    cb_end = i
                    block = [l[8:] for l in lines[cb_start:cb_end]]

                    cases.append((pat, block))

                for pat, block in cases:
                    ok, bind = self.match_pattern(match_val, pat, env)
                    if ok:
                        local = env.copy()
                        local.update(bind)
                        self.run_block(block, 0, len(block), local)
                        break

                continue

            ###############################
            # TRY / EXCEPT
            ###############################
            if stripped == "try:":
                i += 1
                ts = i
                while i < end and lines[i].startswith("    "):
                    i += 1
                te = i

                if not (i < end and lines[i].startswith("except:")):
                    raise MiniLangError("try without except")

                i += 1
                es = i
                while i < end and lines[i].startswith("    "):
                    i += 1
                ee = i

                try:
                    self.run_block([l[4:] for l in lines[ts:te]], 0, te-ts, env)
                except MiniLangError:
                    self.run_block([l[4:] for l in lines[es:ee]], 0, ee-es, env)

                continue

            ###############################
            # IF STATEMENT
            ###############################
            if stripped.startswith("if ") and stripped.endswith(":"):
                cond = stripped[3:-1].strip()
                cond_val = self.evaluator.eval(cond, env)

                i += 1
                ts = i
                while i < end and lines[i].startswith("    "):
                    i += 1
                te = i

                if i < end and lines[i].startswith("else:"):
                    i += 1
                    es = i
                    while i < end and lines[i].startswith("    "):
                        i += 1
                    ee = i
                else:
                    es = ee = None

                if cond_val:
                    self.run_block([l[4:] for l in lines[ts:te]], 0, te-ts, env)
                elif es is not None:
                    self.run_block([l[4:] for l in lines[es:ee]], 0, ee-es, env)

                continue

            ###############################
            # WHILE LOOP
            ###############################
            if stripped.startswith("while ") and stripped.endswith(":"):
                cond = stripped[6:-1].strip()

                i += 1
                ts = i
                while i < end and lines[i].startswith("    "):
                    i += 1
                te = i
                block = [l[4:] for l in lines[ts:te]]

                while self.evaluator.eval(cond, env):
                    self.run_block(block, 0, len(block), env)

                continue

            ###############################
            # RETURN
            ###############################
            if stripped.startswith("return "):
                val = stripped[7:].strip()
                raise ReturnValue(self.evaluator.eval(val, env))

            ###############################
            # LIST INDEX ASSIGNMENT (FIXED)
            ###############################
            if "=" in stripped and "[" in stripped and "]" in stripped:
                left, right = stripped.split("=", 1)
                left = left.strip()
                right = right.strip()

                if "[" in left and left.endswith("]"):
                    name, idx = left.split("[", 1)
                    name = name.strip()
                    idx = idx[:-1].strip()

                    if name.isidentifier():
                        env[name][self.evaluator.eval(idx, env)] = self.evaluator.eval(right, env)
                        i += 1
                        continue

            ###############################
            # LET
            ###############################
            if stripped.startswith("let "):
                var, expr = stripped[4:].split("=", 1)
                env[var.strip()] = self.evaluator.eval(expr.strip(), env)
                i += 1
                continue

            ###############################
            # PRINT
            ###############################
            if stripped.startswith("print(") and stripped.endswith(")"):
                inner = stripped[6:-1]
                print(self.evaluator.eval(inner, env))
                i += 1
                continue

            ###############################
            # RAISE
            ###############################
            if stripped.startswith("raise "):
                val = stripped[6:].strip()
                raise MiniLangError(self.evaluator.eval(val, env))

            ###############################
            # Expression fallback
            ###############################
            self.evaluator.eval(stripped, env)
            i += 1

    ###############################
    # Call function
    ###############################
    def call_function(self, name, args, caller_env):
        params, body = self.funcs[name]

        dyn_env = {}
        if caller_env:
            dyn_env.update(caller_env)

        for p, v in zip(params, args):
            dyn_env[p] = v

        try:
            self.run_block(body, 0, len(body), dyn_env)
        except ReturnValue as r:
            return r.value

        return None
