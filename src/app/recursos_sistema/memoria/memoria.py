from utils.singleton import Singleton
from utils.output import *
from utils.messages import *


def create_table(row_data):
    header = [str(x) for x in range(len(row_data))]
    cols = len(row_data)
    divider = '+'
    lines = ['|', '|']
    for i in range(cols):
        pivot = len(header[i]) if len(header[i]) > len(row_data[i]) else len(row_data[i])
        pivot += 2
        divider += '-'*pivot + '+'
        if(len(header[i]) > len(row_data[i])):
            lines[0] += ' '+ header[i] + ' |'
            lines[1] += ' '*(pivot-len(row_data[i])-1)  + row_data[i] + ' ' + '|'
        else:
            lines[0] += ' '*(pivot-len(header[i])-1) + header[i] + ' ' + '|'
            lines[1] += ' ' + row_data[i] + ' |'

    return '''{0}\n{1}\n{0}\n{2}\n{0}'''.format(divider, lines[0], lines[1])



class Memory(metaclass=Singleton):
    def __init__(self, real_time_size, user_size) -> None:
        self.real_time_size = real_time_size
        self.user_size = user_size
        self.size = self.real_time_size + self.user_size
        self.bit_map = ['0']*self.size
        self.out = Output()

    def __repr__(self):
        return create_table(self.bit_map) 
    
    def __str__(self):
        return self.__repr__()

    def __can_alloc(self, pid, priority, size):
        if(priority > 0):
            if(size > self.user_size):
                self.out.error(ERRO_SEM_MEMORIA, pid=pid)
                return -2
        else:
            if(size > self.real_time_size):
                self.out.error(ERRO_SEM_MEMORIA, pid=pid)
                return -2
            
        return 1
    

    def __first_fit(self, pid, priority, size):
        result = self.__can_alloc(pid, priority, size)
        if(result < 0): return result

        start_index = 64 if priority > 0 else 0
        max_index = 1024 if priority > 0 else 64

        for index in range(start_index, max_index):
            if(self.bit_map[index] == '0'):
                space = self.bit_map[index:index+size]
                if(space.count('0') == size):
                    return index

        self.out.error(ERRO_PROCESSO_BLOQUEADO, pid=pid)
        return -1    

    def malloc(self, priority, mem_block_size, pid):
        start_addr = self.__first_fit(pid, priority, mem_block_size)

        if(start_addr < 0): return start_addr

        for i in range(start_addr, start_addr+mem_block_size):
            self.bit_map[i] = '1'

        return start_addr

    def free(self, start_addr, block_size):
        for i in range(start_addr, start_addr+block_size):
            self.bit_map[i] = '0'
