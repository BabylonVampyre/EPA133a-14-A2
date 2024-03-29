from mesa import Agent
from enum import Enum
import numpy as np
import random


# ---------------------------------------------------------------
class Infra(Agent):
    """
    Base class for all infrastructure components

    Attributes
    __________
    vehicle_count : int
        the number of vehicles that are currently in/on (or totally generated/removed by)
        this infrastructure component

    length : float
        the length in meters
    ...

    """

    def __init__(self, unique_id, model, length=0,
                 name='Unknown', road_name='Unknown'):
        super().__init__(unique_id, model)
        self.length = length
        self.name = name
        self.road_name = road_name
        self.vehicle_count = 0

    def step(self):

        pass

    def __str__(self):
        return type(self).__name__ + str(self.unique_id)


# ---------------------------------------------------------------
class Bridge(Infra):
    """
    Creates delay time

    Attributes
    __________
    condition:
        condition of the bridge

    delay_time: int
        the delay (in ticks) caused by this bridge
    ...

    """

    def __init__(self, unique_id, model, length=0,
                 name='Unknown', road_name='Unknown', condition='Unknown', scenario=0, delay_time=0, seed=None):
        super().__init__(unique_id, model, length, name, road_name)

        self.condition = condition
        self.scenario = scenario
        self.delay_time = delay_time
        self.seed = seed
        extra_seed = unique_id
        seed = self.seed + extra_seed
        random.seed(seed)
        # this will be a random number from 1 to 100, it will help
        # determine if a bridge is broken
        broken_roll = random.randrange(1, 101)
        # this will be 0 or 1, meaning there will be a delay or not
        possible_delay_time = 1

        # Check the scenario, if the scenario is 0, there is no delay time
        if scenario == 0:
            self.delay_time = 0

        # If the scenario is 1, there is a possibility of a delay if the condition is D and the broken roll
        # is less than 5
        if scenario == 1:
            if condition == 'A' or condition == 'B' or condition == 'C':
                self.delay_time = 0
            elif condition == 'D' and broken_roll <= 5:
                self.delay_time = possible_delay_time
            else:
                self.delay_time = 0
        # If the scenario is 2, there is a possibility of a delay if the condition is D and the broken roll
        # is less than 10
        if scenario == 2:
            if condition == 'A' or condition == 'B' or condition == 'C':
                self.delay_time = 0
            elif condition == 'D' and broken_roll <= 10:
                self.delay_time = possible_delay_time
            else:
                self.delay_time = 0
        # If the scenario is 3, there is a possibility of a delay if the condition is C and the broken roll
        # is less than 5, or the condition is D and the broken roll is less than 10
        if scenario == 3:
            if condition == 'A' or condition == 'B':
                self.delay_time = 0
            elif condition == 'C' and broken_roll <= 5:
                self.delay_time = possible_delay_time
            elif condition == 'D' and broken_roll <= 10:
                self.delay_time = possible_delay_time
            else:
                self.delay_time = 0
        # If the scenario is 4, there is a possibility of a delay if the condition is C and the broken roll
        # is less than 10, or the condition is D and the broken_roll is 20
        if scenario == 4:
            if condition == 'A' or condition == 'B':
                self.delay_time = 0
            elif condition == 'C' and broken_roll <= 10:
                self.delay_time = possible_delay_time
            elif condition == 'D' and broken_roll <= 20:
                self.delay_time = possible_delay_time
            else:
                self.delay_time = 0

        # If the scenario is 5, the possibility of a delay if the condition is 5, there is a possibility of a delay
        # if the condition is B and the broken roll is less than 5, or, if the condition is C,
        if scenario == 5:
            if condition == 'A':
                self.delay_time = 0
            elif condition == 'B' and broken_roll <= 5:
                self.delay_time = possible_delay_time
            elif condition == 'C' and broken_roll <= 10:
                self.delay_time = possible_delay_time
            elif condition == 'D' and broken_roll <= 20:
                self.delay_time = possible_delay_time
            else:
                self.delay_time = 0

        # All the other scenarios are determined in a similar way.
        if scenario == 6:
            if condition == 'A':
                self.delay_time = 0
            elif condition == 'B' and broken_roll <= 10:
                self.delay_time = possible_delay_time
            elif condition == 'C' and broken_roll <= 20:
                self.delay_time = possible_delay_time
            elif condition == 'D' and broken_roll <= 40:
                self.delay_time = possible_delay_time
            else:
                self.delay_time = 0

        if scenario == 7:
            if condition == 'A' and broken_roll <= 5:
                self.delay_time = possible_delay_time
            elif condition == 'B' and broken_roll <= 10:
                self.delay_time = possible_delay_time
            elif condition == 'C' and broken_roll <= 20:
                self.delay_time = possible_delay_time
            elif condition == 'D' and broken_roll <= 40:
                self.delay_time = possible_delay_time
            else:
                self.delay_time = 0

        if scenario == 8:
            if condition == 'A' and broken_roll <= 10:
                self.delay_time = possible_delay_time
            elif condition == 'B' and broken_roll <= 20:
                self.delay_time = possible_delay_time
            elif condition == 'C' and broken_roll <= 40:
                self.delay_time = possible_delay_time
            elif condition == 'D' and broken_roll <= 80:
                self.delay_time = possible_delay_time
            else:
                self.delay_time = 0

    def get_delay_time(self):
        # import main seed for model_run and add the current step to it so the delay
        # each step is different, but deterministic
        extra_seed = self.model.schedule.steps
        # from model_run import seed
        seed = self.seed + extra_seed
        np.random.seed(seed)
        # Check length of the bridges and calculate the unique delay time at the bridge if it is broken
        if self.delay_time == 0:
            self.delay_time = 0
        elif self.length <= 10:
            self.delay_time = random.uniform(10, 20)
        elif self.length <= 50:
            self.delay_time = random.uniform(15, 60)
        elif self.length <= 200:
            self.delay_time = random.uniform(45, 90)
        else:
            self.delay_time = random.triangular(60, 240, 120)
        return self.delay_time


# ---------------------------------------------------------------
class Link(Infra):
    pass


# ---------------------------------------------------------------
class Sink(Infra):
    """
    Sink removes vehicles

    Attributes
    __________
    vehicle_removed_toggle: bool
        toggles each time when a vehicle is removed
    self.vehicle_removed_driving_time: array int
        difference between vehicle's tick of sink and tick of source

    """
    vehicle_removed_toggle = False

    vehicle_removed_driving_time = []
    tick_removing = 0

    def step(self):
        if self.tick_removing < self.model.schedule.steps:
            self.vehicle_removed_driving_time = []

    def remove(self, vehicle):
        # update the tick we are removing at
        self.tick_removing = self.model.schedule.steps

        # append the truck to the list of vehicles this sink removes at this tick
        self.vehicle_removed_driving_time.append([vehicle.unique_id, vehicle.removed_at_step-vehicle.generated_at_step])

        self.model.schedule.remove(vehicle)
        self.vehicle_removed_toggle = not self.vehicle_removed_toggle


# ---------------------------------------------------------------

class Source(Infra):
    """
    Source generates vehicles

    Class Attributes:
    -----------------
    truck_counter : int
        the number of trucks generated by ALL sources. Used as Truck ID!

    Attributes
    __________
    generation_frequency: int
        the frequency (the number of ticks) by which a truck is generated

    vehicle_generated_flag: bool
        True when a Truck is generated in this tick; False otherwise
    ...

    """

    truck_counter = 0
    generation_frequency = 5
    vehicle_generated_flag = False
    print(truck_counter)

    def step(self):
        if self.model.schedule.steps % self.generation_frequency == 0:
            self.generate_truck()
        else:
            self.vehicle_generated_flag = False

    def generate_truck(self):
        """
        Generates a truck, sets its path, increases the global and local counters
        """

        try:
            agent = Vehicle('Truck' + str(Source.truck_counter), self.model, self)
            if agent:
                self.model.schedule.add(agent)
                agent.set_path()
                Source.truck_counter += 1
                self.vehicle_count += 1
                self.vehicle_generated_flag = True
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")


# ---------------------------------------------------------------
class SourceSink(Source, Sink):
    """
    Generates and removes trucks
    """
    # combined step function because multiple inheritance is weird?
    def step(self):
        # source step
        if self.model.schedule.steps % self.generation_frequency == 0:
            self.generate_truck()
        else:
            self.vehicle_generated_flag = False

        # sink step
        if self.tick_removing < self.model.schedule.steps:
            self.vehicle_removed_driving_time = []


# ---------------------------------------------------------------
class Vehicle(Agent):
    """

    Attributes
    __________
    speed: float
        speed in meter per minute (m/min)

    step_time: int
        the number of minutes (or seconds) a tick represents
        Used as a base to change unites

    state: Enum (DRIVE | WAIT)
        state of the vehicle

    location: Infra
        reference to the Infra where the vehicle is located

    location_offset: float
        the location offset in meters relative to the starting point of
        the Infra, which has a certain length
        i.e. location_offset < length

    path_ids: Series
        the whole path (origin and destination) where the vehicle shall drive
        It consists the Infras' uniques IDs in a sequential order

    location_index: int
        a pointer to the current Infra in "path_ids" (above)
        i.e. the id of self.location is self.path_ids[self.location_index]

    waiting_time: int
        the time the vehicle needs to wait

    generated_at_step: int
        the timestamp (number of ticks) that the vehicle is generated

    removed_at_step: int
        the timestamp (number of ticks) that the vehicle is removed
    ...

    """

    # 50 km/h translated into meter per min
    speed = 50 * 1000 / 60
    # One tick represents 1 minute
    step_time = 1

    class State(Enum):
        DRIVE = 1
        WAIT = 2

    def __init__(self, unique_id, model, generated_by,
                 location_offset=0, path_ids=None):
        super().__init__(unique_id, model)
        self.generated_by = generated_by
        self.generated_at_step = model.schedule.steps
        self.location = generated_by
        self.location_offset = location_offset
        self.pos = generated_by.pos
        self.path_ids = path_ids
        # default values
        self.state = Vehicle.State.DRIVE
        self.location_index = 0
        self.waiting_time = 0
        self.waited_at = None
        self.removed_at_step = None

    def __str__(self):
        return "Vehicle" + str(self.unique_id) + \
               " +" + str(self.generated_at_step) + " -" + str(self.removed_at_step) + \
               " " + str(self.state) + '(' + str(self.waiting_time) + ') ' + \
               str(self.location) + '(' + str(self.location.vehicle_count) + ') ' + str(self.location_offset)

    def set_path(self):
        """
        Set the origin destination path of the vehicle
        """
        self.path_ids = self.model.get_random_route(self.generated_by.unique_id)

    def step(self):
        """
        Vehicle waits or drives at each step
        """
        if self.state == Vehicle.State.WAIT:
            self.waiting_time = max(self.waiting_time - 1, 0)
            if self.waiting_time == 0:
                self.waited_at = self.location
                self.state = Vehicle.State.DRIVE

        if self.state == Vehicle.State.DRIVE:
            self.drive()

        """
        To print the vehicle trajectory at each step
        """

    def drive(self):

        # the distance that vehicle drives in a tick
        # speed is global now: can change to instance object when individual speed is needed
        distance = Vehicle.speed * Vehicle.step_time
        distance_rest = self.location_offset + distance - self.location.length

        if distance_rest > 0:
            # go to the next object
            self.drive_to_next(distance_rest)
        else:
            # remain on the same object
            self.location_offset += distance

    def drive_to_next(self, distance):
        """
        vehicle shall move to the next object with the given distance
        """

        self.location_index += 1
        next_id = self.path_ids[self.location_index]
        next_infra = self.model.schedule._agents[next_id]  # Access to protected member _agents

        if isinstance(next_infra, Sink):
            # arrive at the sink
            self.arrive_at_next(next_infra, 0)
            self.removed_at_step = self.model.schedule.steps
            self.location.remove(self)
            return
        elif isinstance(next_infra, Bridge):
            self.waiting_time = next_infra.get_delay_time()
            if self.waiting_time > 0:
                # arrive at the bridge and wait
                self.arrive_at_next(next_infra, 0)
                self.state = Vehicle.State.WAIT
                return
            # else, continue driving

        if next_infra.length > distance:
            # stay on this object:
            self.arrive_at_next(next_infra, distance)
        else:
            # drive to next object:
            self.drive_to_next(distance - next_infra.length)

    def arrive_at_next(self, next_infra, location_offset):
        """
        Arrive at next_infra with the given location_offset
        """
        self.location.vehicle_count -= 1
        self.location = next_infra
        self.location_offset = location_offset
        self.location.vehicle_count += 1

# EOF -----------------------------------------------------------
