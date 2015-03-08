import signal


class KillableProcess(object):
    def __init__(self):
        self.interrupt = False
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, sign, frame):
        self.interrupt = True