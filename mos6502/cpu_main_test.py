from memory.memory import C64Membank
from mos6502.cpu import MOS6502
from unittest import TestCase

class CPUMainTest(TestCase):
    def setUp(self) -> None:
        # Given a mos6502 CPU and memory
        self.memory = C64Membank(size=65536)
        self.cpu = MOS6502(memory=self.memory, reset_vector=0xFFFC)

    def test_cpu_will_have_program_counter_set_to_reset_vector_when_reset(self):
        # Given a mos6502 CPU and memory
        # When I reset
        self.cpu.reset()

        # I expect the program counter to be at the reset vector
        self.assertEqual(0xFFFC, self.cpu.PC)

    def test_cpu_will_have_empty_registers_and_status_flags_when_reset(self):
        # Given a mos6502 CPU  and memory
        # When I reset
        self.cpu.reset()

        # I expect the program counter to be at the reset vector
        self.assertEqual(0, self.cpu.accumulator)
        self.assertEqual(0, self.cpu.x_register)
        self.assertEqual(0, self.cpu.y_register)
        self.assertEqual(0, self.cpu.flags.all)

    def test_cpu_ins_nop_will_only_increment_pc(self):
        # Given a mos6502 CPU and memory with
        # a NOP instruction loaded
        self.memory[0xFFFC] = 0xEA
        self.cpu.reset()

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=2)

        # I expect the program counter to have incremented
        self.assertEqual(0xFFFD, self.cpu.PC)

        # I expect 2 cycles spent
        self.assertEqual(2, spent_cycles)
