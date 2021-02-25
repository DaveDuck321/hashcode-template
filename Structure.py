class Light:
    def __init__(self, simulation_length, street, cost, light_junction, destination_junction):
        self.street = street
        self.cost = cost
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

    def await_green(self, simulation_length, start_time):
        for current_time in range(time, simulation_length):
            if self.is_open[current_time] is None:
                self.set_open(current_time)
                self.open_used[current_time] = True
                return current_time - start_time

            if self.is_open[current_time] and not self.open_used[current_time]:
                self.open_used[current_time] = True
                return current_time - start_time

        return -1



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
        self.route_cost = 0

        # Get street classes
        for street in route:
            light = all_lights[street]
            self.route.append(light)
            self.route_cost += light.cost
