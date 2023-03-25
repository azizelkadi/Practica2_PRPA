"""
SOLUCIÓN SEGURA
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 20
NPED = 10
TIME_CAR_NORTH = 0.5  # a new car enters each 0.5s
TIME_CAR_SOUTH = 0.5  # a new car enters each 0.5s
TIME_PED = 5 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CAR = (1, 0.5) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRIAN = (30, 10) # normal 30s, 10s

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.count = Value('i', 0)

        #Numero de coches y peatones
        self.ncar_north = Value('i', 0)
        self.ncar_south = Value('i', 0)
        self.nped = Value('i', 0)

        #Condiciones
        self.can_car_north = Condition(self.mutex)
        self.can_car_south = Condition(self.mutex)
        self.can_ped = Condition(self.mutex)

    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        self.count.value += 1
        #### Código añadido
        if direction == NORTH:
            self.can_car_north.wait_for(self.can_pass_car_north)
            self.ncar_north.value += 1
        else:
            self.can_car_south.wait_for(self.can_pass_car_south)
            self.ncar_south.value += 1
        self.mutex.release()

    def leaves_car(self, direction: int) -> None:
        self.mutex.acquire() 
        self.count.value += 1
        #### Código añadido
        if direction == NORTH:
            self.ncar_north.value -= 1
            if self.ncar_north.value == 0:
                self.can_car_south.notify_all()
                self.can_ped.notify_all()
        else:
            self.ncar_south.value -= 1
            if self.ncar_south.value == 0:
                self.can_car_north.notify_all()
                self.can_ped.notify_all()
        self.mutex.release()

    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.count.value += 1
        #### Código añadido
        self.can_ped.wait_for(self.can_pass_ped)
        self.nped.value += 1
        self.mutex.release()

    def leaves_pedestrian(self) -> None:
        self.mutex.acquire()
        self.count.value += 1
        #### Código añadido
        self.nped.value -= 1
        if self.nped.value == 0:
            self.can_car_north.notify_all()
            self.can_car_south.notify_all()
        self.mutex.release()

    def can_pass_car_south(self) -> bool:
        return self.ncar_north.value == 0 and self.nped.value == 0
    
    def can_pass_car_north(self) -> bool:
        return self.ncar_south.value == 0 and self.nped.value == 0
    
    def can_pass_ped(self) -> bool:
        return self.ncar_north.value == 0 and self.ncar_south.value == 0

    def __repr__(self) -> str:
        return f'Monitor: {self.count.value}'


# Delay

def delay_car_north(factor = 1) -> None:
    delay = random.gauss(*TIME_IN_BRIDGE_CAR)
    time.sleep(abs(delay * factor))

def delay_car_south(factor = 1) -> None:
    delay = random.gauss(*TIME_IN_BRIDGE_CAR)
    time.sleep(abs(delay * factor))

def delay_pedestrian(factor = 1/30) -> None:
    delay = random.gauss(*TIME_IN_BRIDGE_PEDESTRIAN)
    time.sleep(abs(delay * factor))


# Procesos

def car(cid: int, direction: int, monitor: Monitor) -> None:
    # Quiere entrar al puente
    print(f"car {cid} heading {direction} wants to enter. {monitor}")
    monitor.wants_enter_car(direction)

    # Entra al puente
    print(f"car {cid} heading {direction} enters the bridge. {monitor}")
    if direction == NORTH:
        delay_car_north()
    else:
        delay_car_south()

    # Sale del puente
    print(f"car {cid} heading {direction} leaving the bridge. {monitor}")
    monitor.leaves_car(direction)
    print(f"car {cid} heading {direction} out of the bridge. {monitor}")

def pedestrian(pid: int, monitor: Monitor) -> None:
    # Quiere entrar al puente
    print(f"pedestrian {pid} wants to enter. {monitor}")
    monitor.wants_enter_pedestrian()

    # Entra al puente
    print(f"pedestrian {pid} enters the bridge. {monitor}")
    delay_pedestrian()

    # Sale del puente
    print(f"pedestrian {pid} leaving the bridge. {monitor}")
    monitor.leaves_pedestrian()
    print(f"pedestrian {pid} out of the bridge. {monitor}")


# Generadores

def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_PED))

    for p in plst:
        p.join()

def gen_cars(direction: int, time_cars, monitor: Monitor) -> None:
    cid = 0
    plst = []
    for _ in range(NCARS):
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/time_cars))

    for p in plst:
        p.join()

def main():
    # Inicializamos el monitor
    monitor = Monitor()

    # Creamos los generadores de coches y peatones
    gcar_north = Process(target=gen_cars, args=(NORTH, TIME_CAR_NORTH, monitor))
    gcar_south = Process(target=gen_cars, args=(SOUTH, TIME_CAR_SOUTH, monitor))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    
    # Inicializamos los procesos
    gcar_north.start()
    gcar_south.start()
    gped.start()

    gcar_north.join()
    gcar_south.join()
    gped.join()
    
    # Han finalizado todos los procesos
    print("FIN")

if __name__ == '__main__':
    main()
