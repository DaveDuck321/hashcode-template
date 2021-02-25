class Light:
    def __init__(self, simulation_length, street, junction):
        self.street = street
        self.junction = junction
        self.is_open = [None] * simulation_length
        self.open_used = [False] * simulation_length


    def set_open(self, time):
        assert self.is_open[time] is None

        self.is_open[time] = True
        for light in self.junction:
            if light.street == self.street:
                continue

            light.self.is_open[time] = False

class Junction:
    def __init__(self, simulation_length, junction_id, connected_streets):
        self.junction_id = junction_id
        self.all_lights = []

        for street in connected_streets:
            self.all_lights.append(Light(simulation_length, street, junction_id))