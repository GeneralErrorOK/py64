class Flags:
    def __init__(self):
        self.negative = False
        self.overflow = False
        self.expansion = False
        self.break_command = False
        self.decimal = False
        self.interrupt = False
        self.zero = False
        self.carry = False

    def __int__(self):
        return ((int(self.negative) << 7) +
                 (int(self.overflow) << 6) +
                 (int(self.expansion) << 5) +
                 (int(self.break_command) << 4) +
                 (int(self.decimal) << 3) +
                (int(self.interrupt) << 2) +
                (int(self.zero) << 1) +
                (int(self.carry) << 0))

    @property
    def all(self):
        return self.__int__()

