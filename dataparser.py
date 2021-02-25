import argparse
import json
from collections import *
from pathlib import Path
from Structure import *
from collections import defaultdict


def ni(itr):
    return int(next(itr))


def nl(itr):
    # parses the next string of itr as a list of integers
    return [int(v) for v in next(itr).split()]


def dump_to_output(file_name, junctions, simulation_time):
    junctions_timings = []  # junction_id, [(Street, time)]
    for junction in junctions:
        junction_id = junction.junction_id

        current_on = -1
        time_on = 0

        timings = []  # (Street, time)
        for time in range(junction.last_used):
            now_on = -1
            time_on += 1
            for light in junction.all_lights:
                if light.is_open[time]:
                    now_on = light.street
            
            if now_on == -1:
                continue  # Keep it on

            if now_on == current_on:
                continue

            timings.append((now_on, time_on))
            current_on = now_on
            time_on = 0

        if len(timings) != 0:
            junctions_timings.append((junction_id, timings))

    # Print to file
    buffer = []
    buffer.append(f"{len(junctions_timings)}")

    for junction_id, lights in junctions_timings:
        buffer.append(f"{junction_id}")
        buffer.append(f"{len(lights)}")

        for light in lights:
            buffer.append(f"{light[0]} {light[1]}")

    return '\n'.join(buffer)

def parse(inp):
    itr = (line for line in inp.split('\n'))
    ns = argparse.Namespace()

    # Parse first line
    ns.D, ns.I, ns.S, ns.V, ns.F = nl(itr)
    assert 1 <= ns.D <= 10**4
    assert 2 <= ns.I <= 10**5
    assert 2 <= ns.S <= 10**5
    assert 1 <= ns.V <= 10**3
    assert 1 <= ns.F <= 10**3

    # The next S lines contain descriptions of streets
    streets = []
    for _ in range(ns.S):
        line = next(itr).split(' ')
        streets.append({
            'start_junction': int(line[0]),
            'end_junction': int(line[1]),
            'name': line[2],
            'length': int(line[3])
        })

    # The next V lines describe the paths of each car
    paths = []
    for _ in range(ns.V):
        line = next(itr).split(' ')
        paths.append(line[1:])

    # Make Tom happy
    ns.all_lights = {}
    destination_junctions = defaultdict(list)

    # Junctions
    for street in streets:
        destination_junctions[street['start_junction']].append((street['name'], street['end_junction'], street['length']))

    ns.junctions = []
    for i in range(ns.I):
        ns.junctions.append(Junction(destination_junctions, ns.all_lights, ns.D, i))

    # Routes -> Cars
    ns.cars = list(map(lambda path: Car(ns.all_lights, path), paths))

    return ns


class FlexibleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, argparse.Namespace):
            return vars(obj)
        if isinstance(obj, Light):
            return obj.__dict__
        if isinstance(obj, Junction):
            return obj.__dict__
        if isinstance(obj, Car):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def parse2json(inp):
    ns = parse(inp)
    return json.dumps(ns, cls=FlexibleEncoder)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inp', nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.inp:
        file_list = [args.inp]
    else:
        file_list = Path('in').glob('*.in')

    for inp in file_list:
        data = parse2json(inp.read_text())
        with inp.with_suffix('.json').open('w') as f:
            f.write(data)
