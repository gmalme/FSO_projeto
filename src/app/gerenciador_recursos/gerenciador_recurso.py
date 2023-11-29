from enum import Enum, auto
from utils.singleton import Singleton
from utils.output import *
from utils.messages import *
from app.gerenciador_recursos.recursos_enum import Recurso


class GerenciadorRecurso(metaclass=Singleton):
    def __init__(self):
        self.out = Output()
        self.recursos = {
            Recurso.PRINTER: Recurso.PRINTER.value,
            Recurso.SCANNER: Recurso.SCANNER.value,
            Recurso.MODEM: Recurso.MODEM.value,
            Recurso.SATA: Recurso.SATA.value
        }
        self.allocated_recursos = {
            Recurso.PRINTER: 0,
            Recurso.SCANNER: 0,
            Recurso.MODEM: 0,
            Recurso.SATA: 0
        }
        self.recurso_processo = {
            Recurso.PRINTER: [],
            Recurso.SCANNER: [],
            Recurso.MODEM: [],
            Recurso.SATA: []
        }

    def __check_recurso_availability(self, processo):
        for recurso, max_quantity in self.recursos.items():
            proc_quantity = getattr(processo, recurso.name.lower())

            if proc_quantity > max_quantity:
                self.out.error(ERRO_SEM_RECURSOS, pid=processo.pid)
                return -1
            remaining_quantity = max_quantity - self.allocated_recursos[recurso]
            if proc_quantity > remaining_quantity:
                if processo.pid in self.recurso_processo[recurso]:
                    return 1
                self.out.error(ERRO_RECURSO_BLOQUEADO, pid=processo.pid, recurso=recurso, proc_quantity=proc_quantity, max_quantity=max_quantity, remaning=self.allocated_recursos[recurso], max_quantity_remaning=max_quantity - self.allocated_recursos[recurso])
                return 0
            
        return 1

    def request(self, processo):
        try:
            self.__check_recurso_availability(processo)
        except ValueError as e:
            self.out.error(ERRO_RECURSO_BLOQUEADO, pid=processo.pid, recurso=str(e))
            return 0

        for recurso in self.recursos:
            if processo.pid not in self.recurso_processo[recurso]:
                proc_quantity = getattr(processo, recurso.name.lower())
                self.allocated_recursos[recurso] += proc_quantity
                self.recurso_processo[recurso].append(processo.pid)

        return 1

    def deallocate(self, processo):
        for recurso in self.recursos:
            proc_quantity = getattr(processo, recurso.name.lower())
            if processo.pid in self.recurso_processo[recurso]:
                self.allocated_recursos[recurso] -= proc_quantity
                self.recurso_processo[recurso].remove(processo.pid)
