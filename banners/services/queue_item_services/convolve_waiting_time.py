from functools import cached_property


class ConvolveWaitingTime:
    def __init__(self, queue_item):
        self.banner = queue_item.banner
        self.queue_item = queue_item

    def call(self):
        if self.last_processed_item:
            return self.convolve_processing_time()

        return self.exact_processing_time()

    def exact_processing_time(self):
        return self.queue_item.processing_ended_at - \
               self.queue_item.processing_started_at

    def convolve_processing_time(self):
        return ((self.queue_item.processing_ended_at -
                 self.queue_item.processing_started_at) / 2) + \
               (self.last_processed_item.waiting_time_estimation / 2)

    @cached_property
    def last_processed_item(self):
        return self.banner.queue.processed().last()
