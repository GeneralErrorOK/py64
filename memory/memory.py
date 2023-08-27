class C64Membank:
    def __init__(self, size: int = 65536, initial_values: int = 0) -> None:
        self._mem = [initial_values for _ in range(size)]

    def __setitem__(self, key, value):
        if value > 0xFF:
            raise OverflowError("Only 8-bit unsigned integers (0-255) allowed.")
        self._mem[key] = value

    def __getitem__(self, item):
        return self._mem[item]

    def store_word(self, address: int, value: int):
        lsb, msb = value.to_bytes(length=2, byteorder="little")
        self._mem[address] = lsb
        self._mem[address+1] = msb

    def read_word(self, address: int) -> int:
        lsb = self._mem[address]
        msb = self._mem[address+1]
        return (msb << 8) + lsb

