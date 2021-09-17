from functools import cached_property
from datetime import timedelta


class EstimateWaitingTime:
    def __init__(self, banner, queue_item=None):
        self.banner = banner
        self.queue_item = queue_item

    def call(self):
        # can be processed immediately, if there is no queue
        if self.actual_count == 0:
            return timedelta(0)

        # no processing history
        if not self.last_processed_item:
            return None

        if self.queue_item:
            return self.last_processed_item.waiting_time_estimation * \
                   self.queue_item.position

        return self.last_processed_item.waiting_time_estimation * \
            self.actual_count

    @cached_property
    def last_processed_item(self):
        return self.banner.queue.processed().last()

    @cached_property
    def actual_count(self):
        return self.banner.queue.actual().count()
