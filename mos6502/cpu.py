from copy import copy

from memory.memory import C64Membank
from mos6502.flags import Flags


class MOS6502:
    def __init__(self, memory: C64Membank, reset_vector: int = 0xFFFC) -> None:
        self._reset_vector = reset_vector
        self.PC = 0
        self._A = 0
        self._X = 0
        self._Y = 0
        self.flags = Flags()
        self.memory = memory
        self._cycle_counter = 0

        self.OPCODE_LOOKUP_TABLE = {
            0xEA: self._ins_nop,
            0xA9: self._ins_lda_imm,
            0xAD: self._ins_lda_abs,
            0xBD: self._ins_lda_xabs,
            0xB9: self._ins_lda_yabs,
            0xA5: self._ins_lda_abs_zp
        }

    @property
    def accumulator(self):
        return self._A

    @accumulator.setter
    def accumulator(self, value: int):
        if value > 0xFFFF:
            raise OverflowError("Only 8-bit unsigned integers (0-255) allowed.")
        self._A = value
        self.flags.set_by_value(value)

    @property
    def x_register(self):
        return self._X

    @x_register.setter
    def x_register(self, value: int):
        if value > 0xFFFF:
            raise OverflowError("Only 16-bit integers allowed.")
        self._X = value

    @property
    def y_register(self):
        return self._Y

    @y_register.setter
    def y_register(self, value: int):
        if value > 0xFFFF:
            raise OverflowError("Only 16-bit integers allowed.")
        self._Y = value

    @property
    def cycles_completed(self):
        return self._cycle_counter

    def cycle(self, count: int):
        # Here we could eventually add some
        # sort of delay to emulate real 6502 speed
        self._cycle_counter += count

    def reset(self):
        self.PC = self._reset_vector

    def _read_next_byte(self) -> int:
        value = self.memory[self.PC]
        self.PC += 1
        self.cycle(1)
        return value

    def _read_next_word(self) -> int:
        value = self.memory.read_word(self.PC)
        self.PC += 2
        self.cycle(2)
        return value

    def _read_from_address_with_offset(self, address: int, offset: int) -> int:
        # If absolute address crosses page boundary it costs an extra cycle
        if (address & 0xFF) + offset > 0x100:
            self.cycle(1)
        value = self.memory.read_word(address + offset)
        self.cycle(1)
        return value

    def execute(self, max_cycles: int = 0):
        resume = True
        while (self.cycles_completed < max_cycles) and resume:
            instruction = self._read_next_byte()
            resume = self._dispatch(instruction)
        return self.cycles_completed

    def _dispatch(self, instruction: int) -> bool:
        try:
            self.OPCODE_LOOKUP_TABLE[instruction]()
            return True
        except KeyError:
            print(f"Unrecognized opcode: 0x{instruction:X}")
            self._cycle_counter -= 1
            return False

    def _ins_nop(self):
        self.cycle(1)

    def _ins_lda_imm(self):
        value = self._read_next_byte()
        self.accumulator = value

    def _ins_lda_abs(self):
        address = self._read_next_word()
        value = self.memory.read_word(address)
        self.cycle(1)
        self.accumulator = value

    def _ins_lda_xabs(self):
        address = self._read_next_word()
        self.accumulator = self._read_from_address_with_offset(address, self.x_register)

    def _ins_lda_yabs(self):
        address = self._read_next_word()
        self.accumulator = self._read_from_address_with_offset(address, self.y_register)

    def _ins_lda_abs_zp(self):
        address = self._read_next_byte()
        value = self.memory.read_word(address)
        self.cycle(1)
        self.accumulator = value

