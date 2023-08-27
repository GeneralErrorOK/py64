from memory.memory import C64Membank
from mos6502.cpu import MOS6502
from unittest import TestCase

# Note: setting the CPU flags after setting the accumulator
# is done through the same mechanics for every LOAD instruction.
# That's why we only test it once

class CPULoadTest(TestCase):
    def setUp(self) -> None:
        # Given a mos6502 CPU and memory
        self.memory = C64Membank(size=65536)
        self.cpu = MOS6502(memory=self.memory, reset_vector=0xFFFC)

    def test_cpu_ins_lda_immediate_loads_non_zero_value(self):
        # Given a mos6502 CPU and memory with
        # a LDA instruction with an immediate value loaded
        opcode = 0xA9
        operand = 0x10
        self.memory[0xFFFC] = opcode
        self.memory[0xFFFD] = operand
        self.cpu.reset()
        self.cpu.flags.negative = True
        self.cpu.flags.zero = True

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=2)

        # I expect 2 cycles spent
        self.assertEqual(2, spent_cycles)

        # I expect the value to be loaded into the accumulator
        self.assertEqual(operand, self.cpu.accumulator)

        # I expect the flags set accordingly
        self.assertFalse(self.cpu.flags.negative)
        self.assertFalse(self.cpu.flags.zero)

    def test_cpu_ins_lda_immediate_loads_negative_value(self):
        # Given a mos6502 CPU and memory with
        # a LDA instruction with an immediate value loaded
        opcode = 0xA9
        operand = 0x80
        self.memory[0xFFFC] = opcode
        self.memory[0xFFFD] = operand
        self.cpu.reset()
        self.cpu.flags.negative = False

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=2)

        # I expect 2 cycles spent
        self.assertEqual(2, spent_cycles)

        # I expect the flags set accordingly
        self.assertTrue(self.cpu.flags.negative)

    def test_cpu_ins_lda_immediate_loads_zero_value(self):
        # Given a mos6502 CPU and memory with
        # a LDA instruction with an immediate value loaded
        opcode = 0xA9
        operand = 0x0
        self.memory[0xFFFC] = opcode
        self.memory[0xFFFD] = operand
        self.cpu.reset()
        self.cpu.flags.zero = False

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=2)

        # I expect 2 cycles spent
        self.assertEqual(2, spent_cycles)

        # I expect the flags set accordingly
        self.assertTrue(self.cpu.flags.zero)

    def test_cpu_ins_lda_absolute_loads_value(self):
        # Given a mos6502 CPU and memory with
        # a LDA instruction with an absolute address and value loaded
        opcode = 0xAD
        operand = 0x4242
        value = 0xFFFF
        self.memory[0xFFFC] = opcode
        self.memory.store_word(0xFFFD, operand)
        self.memory.store_word(operand, value)
        self.cpu.reset()

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=4)

        # I expect 4 cycles spent
        self.assertEqual(4, spent_cycles)

        # I expect the value in the accumulator
        self.assertEqual(value, self.cpu.accumulator)

    def test_cpu_ins_lda_xabs_loads_value_same_page(self):
        # Given a mos6502 CPU and memory with
        # a LDA instruction with an absolute+x value loaded
        opcode = 0xBD
        operand = 0x4240
        self.cpu.x_register = 0x2
        value = 0xFFFF
        self.memory[0xFFFC] = opcode
        self.memory.store_word(0xFFFD, operand)
        self.memory.store_word(operand + self.cpu.x_register, value)
        self.cpu.reset()

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=4)

        # I expect 4 cycles spent
        self.assertEqual(4, spent_cycles)

        # I expect the value in the accumulator
        self.assertEqual(value, self.cpu.accumulator)

    def test_cpu_ins_lda_xabs_loads_value_page_crossed(self):
        # Given a mos6502 CPU and memory with
        # a LDA instruction with an absolute+x value loaded (x offset crosses page)
        opcode = 0xBD
        operand = 0x4240
        self.cpu.x_register = 0x100
        value = 0xFFFF
        self.memory[0xFFFC] = opcode
        self.memory.store_word(0xFFFD, operand)
        self.memory.store_word(operand + self.cpu.x_register, value)
        self.cpu.reset()

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=5)

        # I expect 5 cycles spent
        self.assertEqual(5, spent_cycles)

        # I expect the value in the accumulator
        self.assertEqual(value, self.cpu.accumulator)

    def test_cpu_ins_lda_yabs_loads_value_same_page(self):
        # Given a mos6502 CPU and memory with
        # a LDA instruction with an absolute+x value loaded
        opcode = 0xB9
        operand = 0x4240
        self.cpu.y_register = 0x2
        value = 0xFFFF
        self.memory[0xFFFC] = opcode
        self.memory.store_word(0xFFFD, operand)
        self.memory.store_word(operand + self.cpu.y_register, value)
        self.cpu.reset()

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=4)

        # I expect 4 cycles spent
        self.assertEqual(4, spent_cycles)

        # I expect the value in the accumulator
        self.assertEqual(value, self.cpu.accumulator)

    def test_cpu_ins_lda_yabs_loads_value_page_crossed(self):
        # Given a mos6502 CPU and memory with
        # a LDA instruction with an absolute+x value loaded (x offset crosses page)
        opcode = 0xB9
        operand = 0x4240
        self.cpu.y_register = 0x100
        value = 0xFFFF
        self.memory[0xFFFC] = opcode
        self.memory.store_word(0xFFFD, operand)
        self.memory.store_word(operand + self.cpu.y_register, value)
        self.cpu.reset()

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=5)

        # I expect 5 cycles spent
        self.assertEqual(5, spent_cycles)

        # I expect the value in the accumulator
        self.assertEqual(value, self.cpu.accumulator)

    def test_cpu_ins_lda_absolute_zp_loads_value(self):
        # Given a mos6502 CPU and memory with
        # a LDA instruction with an absolute address in zero page and value loaded
        opcode = 0xA5
        operand = 0x0042
        value = 0xFFFF
        self.memory[0xFFFC] = opcode
        self.memory.store_word(0xFFFD, operand)
        self.memory.store_word(operand, value)
        self.cpu.reset()

        # When I execute the instruction
        spent_cycles = self.cpu.execute(max_cycles=3)

        # I expect 3 cycles spent
        self.assertEqual(3, spent_cycles)

        # I expect the value in the accumulator
        self.assertEqual(value, self.cpu.accumulator)