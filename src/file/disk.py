from utils.ascii_table import create_table
from src.file.bit_enum import Bit


class Disk:
    def __init__(self, size) -> None:
        """Initialize a disk with the given size."""
        self.size = int(size.strip())
        self.bit_map = [Bit.FREE.value] * self.size

    def __repr__(self):
        return create_table(self.bit_map)

    def __str__(self):
        return self.__repr__()

    def __first_fit(self, block_size):
        """Find the first fit for a block of the given size."""
        assert 0 < block_size <= self.size, "Invalid block size"

        for index in range(self.size - block_size + 1):
            space = self.bit_map[index:index + block_size]
            if space.count(Bit.FREE.value) == block_size:
                return index

        return -1

    def alloc(self, block_size, filename):
        """Allocate a block of the given size for the specified filename."""
        start_addr = self.__first_fit(block_size)

        if start_addr < 0:
            return -1

        self.fill(start_addr, block_size, filename)
        return start_addr

    def fill(self, start_addr, block_size, filename):
        """Fill the specified block with the given filename."""
        for i in range(start_addr, start_addr + block_size):
            self.bit_map[i] = filename

    def free(self, start_addr, block_size):
        """Free the specified block."""
        for i in range(start_addr, start_addr + block_size):
            self.bit_map[i] = Bit.FREE.value
