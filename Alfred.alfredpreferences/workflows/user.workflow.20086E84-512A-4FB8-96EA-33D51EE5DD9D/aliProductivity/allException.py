class FuncException(RuntimeError):
    def __init__(self, info, solution):
        self.info = info
        self.solution = solution
