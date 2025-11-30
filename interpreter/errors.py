class MiniLangError(Exception):
    def __init__(self, value):
        self.value = value


class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value


class LazyValue:
    def __init__(self, thunk):
        self.thunk = thunk
        self.done = False
        self.value = None

    def force(self):
        if not self.done:
            self.value = self.thunk()
            self.done = True
        return self.value
