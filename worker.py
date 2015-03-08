from calculator import FoodCalculator
from lifesum import LifesumAPI
import multiprocessing
import signal
import copy


class CalculatorProcess(multiprocessing.Process):
    def __init__(self, poison_event, result_queue,
        token_bucket, offset, offset_amount, epochs):
        super(CalculatorProcess, self).__init__()
        self.poison_event = poison_event
        self.result_queue = result_queue
        self.tk = token_bucket
        self.counter = FoodCalculator()
        self.offset = offset
        self.next_offset = offset
        self.offset_amount = offset_amount
        self.api = LifesumAPI()
        self.epochs = int(epochs)

    def send_partial_sums(self):
        food_partials = copy.copy(self.counter.food_counter)
        category_partials = copy.copy(self.counter.category_counter)

        self.result_queue.put({
            'payload': 'results',
            'food': food_partials,
            'category': category_partials,
        })

        self.counter.clear()

    def call_api(self):
        res = self.api.foodstats(limit=100, offset=self.next_offset)

        for item in res['response']:
            self.counter.update({item['food_id']: 1},
                {item['food__category_id']: 1})

        self.next_offset = res['meta']['next_offset']
        if self.next_offset is None:
            return False

        end_offset = self.offset + self.offset_amount
        if self.next_offset >= end_offset:
            return False

        return True

    def wait_queue(self):
        self.result_queue.put({
            'payload': 'quit',
        })
        self.result_queue.close()
        self.result_queue.join_thread()

    def run(self):
        print('[{0} Worker started.'.format(self.name))
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        iteration = 1
        while True:

            if self.poison_event.is_set():
                print('[{0}] Quitting...'.format(self.name))
                break


            if self.tk.can_consume():
                if not self.call_api():
                    break
            else:
                time.sleep(self.tk.expected_time())


            if iteration % self.epochs == 0:
                self.send_partial_sums()


            if iteration % 5 == 0:
                self.result_queue.put({
                    'payload': 'stats',
                    'offset_amount_done': self.next_offset - self.offset,
                    'worker': self.name,
                })

            iteration += 1

        self.wait_queue()

