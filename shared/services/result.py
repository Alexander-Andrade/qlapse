class Success:
    def __init__(self, result=None):
        self.result = result
        self.succeed = True
        self.failed = False


class Failure:
    def __init__(self, error):
        self.error = error
        self.succeed = False
        self.failed = True
