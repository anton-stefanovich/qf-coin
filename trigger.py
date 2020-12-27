class Trigger:
    __delta = float()
    __silence = float()
    __sensitivity = float()
    __aspect_ratio = float()
    __is_muted = False
    __history = list()

    def __init__(self, sensitivity: float, silence: float = 0):
        self.reset(sensitivity, silence)

    def mute(self):
        self.__is_muted = True

    def reset(self, sensitivity: float = None, silence: float = None):
        sensitivity, silence = sensitivity or 0, silence or 0
        self.__silence = self.__silence if not silence else \
            silence if silence < 1 else 100 / silence

        self.__sensitivity = self.__sensitivity if not sensitivity else \
            sensitivity if sensitivity < 1 else 100 / sensitivity

        assert (self.__sensitivity >= 0)
        assert (self.__sensitivity <= 1)

        self.__is_muted = False
        self.__aspect_ratio = float()
        self.__history = list()
        self.__delta = float()

    def feed(self, value1: float, value2: float) -> bool:

        def __add_history_record():
            from time import asctime
            from data.picker import pick_last

            history_record = (value1, value2, self.__delta)
            if pick_last(self.__history) != history_record:
                self.__history.append(history_record)
                print(asctime(), history_record)

        if not self.__history:
            self.__aspect_ratio = value1 / value2
            __add_history_record()
            return False

        delta = value1 - self.__aspect_ratio * value2
        self.__delta = max(self.__delta, delta) \
            if self.__delta or delta > 0 else min(self.__delta, delta)

        __add_history_record()  # adding new history record
        self.__is_muted = self.__is_muted and abs(delta) <= abs(self.__delta)

        return not self.__is_muted and abs(delta / value1) > self.__silence and \
            abs(delta) < (1 - self.__sensitivity) * abs(self.__delta)

    def trade_first(self):
        return self.__delta > 0

    def trade_second(self):
        return self.__delta < 0
