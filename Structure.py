class Light:
    def __init__(self, simulation_length, street, light_junction, destination_junction):
        self.street = street
        self.light_junction = light_junction
        self.destination_junction = destination_junction
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
    def __init__(self, destination_junctions, all_lights, simulation_length, junction_id):
        self.junction_id = junction_id
        self.all_lights = []

        connected_streets = destination_junctions[junction_id]

        for street, end_id in connected_streets:
            light = Light(simulation_length, street, junction_id, end_id)
            all_lights[street] = light
            self.all_lights.append(light)


class Car:
    def __init__(self, all_lights, route):
        self.route = []

        # Get street classes
        for street in route:
            self.route.append(all_lights[street])
