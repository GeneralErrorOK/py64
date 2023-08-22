from mos6502.flags import Flags


class MOS6502:
    def __init__(self, reset_vector: int = 0xFFFC) -> None:
        self._reset_vector = reset_vector
        self.PC = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.flags = Flags()

    def reset(self):
        self.PC = self._reset_vector