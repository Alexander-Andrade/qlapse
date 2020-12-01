from shared.services.result import Success, Failure


class SkipItem:

    def __init__(self, banner):
        self.banner = banner

    def skip(self, ):
        if not self.banner:
            return Failure('banner is not found')

        item = self.banner.queue.first()
        if item:
            item.delete()

        return Success()
