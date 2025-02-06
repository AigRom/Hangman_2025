import time


class Stopwatch:
    def __init__(self,lbl_time):
        self.__lbl_time = lbl_time
        self.__seconds = 0
        self.__running = False

    def start(self):
        self.__running = True
        self.update()

    def update(self):
        if self.__running:
            if self.__seconds == 0:
                display = '00:00:00'
            else:
                display = time.strftime('%H:%M:%S', time.gmtime(self.__seconds))

            self.__lbl_time['text'] = display
            self.__lbl_time.after(1000, self.update)
            self.__seconds += 1

    def stop(self):

        self.__running = False

    def reset(self):
        self.__seconds = 0
        self.__lbl_time['text'] = '00:00:00'

    @property
    def seconds(self):
        return self.__seconds




