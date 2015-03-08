import time
import multiprocessing
import six.moves.queue as queue
import random

from mixin import KillableProcess
from calculator import FoodCalculator
from worker import CalculatorProcess
from kombu.utils import limits


class CalculatorApp(KillableProcess):
    LIFESUM_START_OFFSET = 658330693
    LIFESUM_MAX_OFFSET = 732158492
    LIFESUM_TOTAL = LIFESUM_MAX_OFFSET - LIFESUM_START_OFFSET
      
    def __init__(self, epochs=10, rate_limit=100,
        num_workers=None, stats_interval=5):
        super(CalculatorApp, self).__init__()
        if num_workers:
            self.num_workers = int(num_workers)
        else:
            self.num_workers = multiprocessing.cpu_count()
        
        self.stats_interval = stats_interval
        self.counter = FoodCalculator()
        self.epochs = epochs
        self.rate_limit = rate_limit
        self.finished_jobs = 0
        self.poison_event = multiprocessing.Event()
        self.result_queue = multiprocessing.Queue()
        self.workers = []
        self.statistics = {}

    def handle_results(self, payload):
        self.counter.update(payload['food'], payload['category'])
        return False

    def handle_quit(self, payload=None):
        self.finished_jobs += 1
        if self.finished_jobs >= self.num_workers:
            return True
        return False

    def handle_stats(self, payload):
        self.statistics[payload['worker']] = payload['offset_amount_done']
        return False

    def spawn_workers(self):
        rate_limit = int(self.rate_limit / self.num_workers)
        offset_amount = int(self.LIFESUM_TOTAL / self.num_workers)

        for worker_id in xrange(self.num_workers):
            offset = self.LIFESUM_START_OFFSET + (offset_amount * worker_id)

            worker = CalculatorProcess(self.poison_event, self.result_queue, 
                limits.TokenBucket(rate_limit),
                offset, offset_amount, self.epochs)

            self.workers.append(worker)

    def dump_statistics(self):
        phrases = ["We are working on it...", "Please wait...", 
        "We need more coffe here!", "Are we there yet?",
        "Keep calm, the numbers are coming.", 
        "Want to finish it? just Ctrl + C and Done!",
        "Always pass on what you have learned.",
        "Patience you must have my young padawan."
        ]
        print random.choice(phrases)

    def run(self):
        self.spawn_workers()

        for worker in self.workers:
            worker.start()

        self.start_time = time.time()
        self.stats_dump_time = time.time()

        while True:
            if self.interrupt and not self.poison_event.is_set():
                self.poison_event.set()

            try:
                queue_item = self.result_queue.get(True, 0.5)
                payload = queue_item['payload']
                handle_method = getattr(self, 'handle_{0}'.format(payload))
                ret = handle_method(queue_item)
                if ret:
                    break
            except queue.Empty:
                continue

            if (time.time() - self.stats_dump_time) >= self.stats_interval:
                self.dump_statistics()
                self.stats_dump_time = time.time()

        for worker in self.workers:
            worker.join()

        if len(self.counter):
            popular_food, popular_category = self.counter.most_popular()
            print(popular_food)
            print(popular_category)
        else:
            print('\nNo data received yet.')