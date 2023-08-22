from memory.memory import C64Membank
from unittest import TestCase

class MemoryTest(TestCase):
    def setUp(self) -> None:
        self.SIZE = 65536
        self.memorybank = C64Membank(size=self.SIZE)

    def test_will_init_memorybank_with_all_zeroes(self):
        # Given I initiate a new memory bank
        # When I check all addresses
        # I expect to get all zeroes
        for address in range(self.SIZE):
            self.assertEqual(0, self.memorybank._mem[address])

    def test_will_store_and_retrieve_bytes_by_index(self):
        # Given an empty memory bank
        # When I store a 1-byte value at a certain "address"
        address = 0x4000
        value = 0x42
        self.memorybank[address] = value

        # I expect to be able to retrieve it from the same "address"
        self.assertEqual(value, self.memorybank[address])

    def test_will_throw_exception_if_value_is_too_large(self):
        # Given an empty memory bank
        # When I store a bigger-than-8-bit-value at a certain "address"
        address = 0x4000
        value = 0x100
        # I expect it to throw an exception
        with self.assertRaises(OverflowError):
            self.memorybank[address] = value

        # I expect to NOT have the value stored
        self.assertNotEqual(value, self.memorybank[address])

    def test_will_store_16bit_word_as_little_endian(self):
        # Given an empty memory bank
        # When I store a 16-bit value
        address = 0x1000
        value = 0x1234
        self.memorybank.store_word(address, value)

        # I expect it to be represented in memory as little endian
        self.assertEqual(0x34, self.memorybank[address])
        self.assertEqual(0x12, self.memorybank[address+1])

    def test_will_not_store_word_if_address_out_of_bounds(self):
        # Given an empty memory bank
        # When I store a 16-bit value at the last address
        address = 0xFFFF
        value = 0x1234
        # I expect to get an IndexError
        with self.assertRaises(IndexError):
            self.memorybank.store_word(address, value)

    def test_will_retrieve_16bit_word(self):
        # Given I have a memorybank with a 16bit value stored in little endian format
        expected = 0x1234
        self.memorybank[0x1000] = 0x34
        self.memorybank[0x1001] = 0x12

        # When I read the value from memory
        value = self.memorybank.read_word(0x1000)

        # I expect it to be valid
        self.assertEqual(expected, value)
