class Success:
    def __init__(self, result=None):
        self.result = result
        self.succeed = True
        self.failed = not self.succeed


class Failure:
    def __init__(self, error):
        self.error = error
        self.succeed = False
        self.failed = not self.succeed
