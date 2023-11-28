from enum import Enum, auto
from utils.singleton import Singleton
from utils.output import *
from utils.messages import *
from src.resources.resources_enum import Resource


class ResourceManager(metaclass=Singleton):
    def __init__(self):
        self.out = Output()
        self.resources = {
            Resource.PRINTER: Resource.PRINTER.value,
            Resource.SCANNER: Resource.SCANNER.value,
            Resource.MODEM: Resource.MODEM.value,
            Resource.SATA: Resource.SATA.value
        }
        self.allocated_resources = {
            Resource.PRINTER: 0,
            Resource.SCANNER: 0,
            Resource.MODEM: 0,
            Resource.SATA: 0
        }
        self.resource_process = {
            Resource.PRINTER: [],
            Resource.SCANNER: [],
            Resource.MODEM: [],
            Resource.SATA: []
        }

    def __check_resource_availability(self, process):
        for resource, max_quantity in self.resources.items():
            proc_quantity = getattr(process, resource.name.lower())

            if proc_quantity > max_quantity:
                self.out.error(EXCEEDED_RESOURCES, pid=process.pid)
                return -1
            remaining_quantity = max_quantity - self.allocated_resources[resource]
            if proc_quantity > remaining_quantity:
                if process.pid in self.resource_process[resource]:
                    return 1
                self.out.error(BLOCKED_DUE_RESOURCES, pid=process.pid, resource=resource, proc_quantity=proc_quantity, max_quantity=max_quantity, remaning=self.allocated_resources[resource], max_quantity_remaning=max_quantity - self.allocated_resources[resource])
                return 0
            
        return 1

    def request(self, process):
        try:
            self.__check_resource_availability(process)
        except ValueError as e:
            self.out.error(BLOCKED_DUE_RESOURCES, pid=process.pid, resource=str(e))
            return 0

        for resource in self.resources:
            if process.pid not in self.resource_process[resource]:
                proc_quantity = getattr(process, resource.name.lower())
                self.allocated_resources[resource] += proc_quantity
                self.resource_process[resource].append(process.pid)

        return 1

    def deallocate(self, process):
        for resource in self.resources:
            proc_quantity = getattr(process, resource.name.lower())
            if process.pid in self.resource_process[resource]:
                self.allocated_resources[resource] -= proc_quantity
                self.resource_process[resource].remove(process.pid)
