from time import perf_counter

from memory.memory import C64Membank
from mos6502.cpu import MOS6502

if __name__ == '__main__':
    print('Placeholder for the py64 Commodore64 emulator main entrypoint.')
    memory = C64Membank(initial_values=0xA9)
    cpu = MOS6502(memory=memory, reset_vector=0)

    start_time = perf_counter()
    cycles = cpu.execute(max_cycles=65000)
    stop_time = perf_counter()
    print(f"Ran {cycles} cycles in {stop_time - start_time} seconds.")
    print(f"That is {cycles // (stop_time - start_time)} cycles per second.")
