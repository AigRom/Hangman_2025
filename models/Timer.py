class Timer:
    def __init__(self, scheduled_callback, cancel_callback, interval, callback):
        """

        :param scheduled_callback: ajasti mis käivitab funktsiooni teatud intervali tagant
        :param cancel_callback: funktsioon mis planeerib uue ajastuse
        :param interval: Funktsioon mis tühistab ajastuse
        :param callback:
        """
        self.scheduled_callback = scheduled_callback
        self.cancel_callback = cancel_callback
        self.interval = interval
        self.callback = callback
        self.timer_id= None

    def start(self):
        self.stop()
        self.timer_id = self.scheduled_callback(self.interval, self._run)

    def stop(self):
        if self.timer_id:
            self.cancel_callback(self.timer_id)
            self.timer_id = None

    def _run(self):
        self.callback()
        self.start()



