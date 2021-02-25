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
    ns.streets = []
    for _ in range(ns.S):
        line = next(itr).split(' ')
        ns.streets.append({
            'start_junction': int(line[0]),
            'end_junction': int(line[1]),
            'name': line[2],
            'length': int(line[3])
        })

    # The next V lines describe the paths of each car
    ns.paths = []
    for _ in range(ns.V):
        line = next(itr).split(' ')
        ns.paths.append(line[1:])

    # Make Tom happy
    ns.all_lights = {}
    ns.destination_junctions = defaultdict(list)

    # Junctions
    for street in ns.streets:
        ns.destination_junctions[street.start_junction].append((street.name, street.end_junction))

    ns.junctions = []
    for i in ns.I:
        ns.junctions.append(Junction(ns.destination_junctions, ns.all_lights, ns.D, i))

    return ns


class FlexibleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, argparse.Namespace):
            return vars(obj)
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
