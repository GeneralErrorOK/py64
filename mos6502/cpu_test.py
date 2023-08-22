from mos6502.cpu import MOS6502
from unittest import TestCase

class CPUTest(TestCase):
    def test_cpu_will_have_program_counter_set_to_reset_vector_when_reset(self):
        # Given a mos6502 CPU
        cpu = MOS6502(reset_vector=0xFFFC)

        # When I reset
        cpu.reset()

        # I expect the program counter to be at the reset vector
        self.assertEqual(0xFFFC, cpu.PC)

    def test_cpu_will_have_empty_registers_and_status_flags_when_reset(self):
        # Given a mos6502 CPU
        cpu = MOS6502(reset_vector=0xFFFC)

        # When I reset
        cpu.reset()

        # I expect the program counter to be at the reset vector
        self.assertEqual(0, cpu.A)
        self.assertEqual(0, cpu.X)
        self.assertEqual(0, cpu.Y)
        self.assertEqual(0, cpu.flags.all)