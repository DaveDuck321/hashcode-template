import argparse
import random
import sys
sys.path.extend(['..', '.'])
from collections import *
from dataparser import parse
from util import get_in_file_content

# inp is an input file as a single string
# return your output as a string
def solve(inp, args):
    # TODO: Solve the problem
    random.seed(args['seed'])
    car_routes, junctions, simulation_time = parse(inp)

    #car_order = sorted(car_routes, key=lambda route: route.route_cost)
    for car in car_routes:
        time = 0
        car_position = 0

        while time < simulation_time:
            wait_time = car.route[car_position].await_green()
            if wait_time == -1:
                break

            car_position += 1
            if car_position == len(car.route[car_position].route):
                break

            time += wait_time
            time += car.route[car_position].cost

    to_output()
    return '0'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))
