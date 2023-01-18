import pygad
from monaco import Game, State, ActionType
import json
from tabulate import tabulate
from enum import Enum
from cars.LearningCar import LearningCar
from cars.Decay import Decay
from cars.DecaySmart import DecaySmart
from cars.ExampleCar import ExampleCar
from cars.PermaShield import PermaShield
from cars.Rando import Rando
from cars.Floor import Floor
from cars.Sauce import Sauce
import itertools

WIN_REWARD = 100000

class CarType(Enum):
    EXAMPLE_CAR = "ExampleCar"
    FLOOR = "Floor"
    SAUCE = "Sauce"
    RANDO = "Random"
    LEARNING_CAR = "LearningCar"
    DECAY = "Decay"
    DECAY_SMART = "DecaySmart"

stored_inputs=\
[2.99302436,-6.19551457,-0.11540604,-4.14079942,-5.35729832
,6.48971592,0.29768569,-5.55742078,8.27697242,-7.33978811
,-3.49586414,1.83227145,2.16207882,6.63560981,9.80326107
,-6.44319262,-11.53943194,-6.57644056,-5.21567502,-2.69141625
,-2.12670384,-4.07877791,1.51844994,10.21591255,1.65164766
,6.7663602,-4.82408691,-5.76694436,1.71358054,3.29748226
,-5.67139143,7.15869216,0.82773653,8.72834422,-8.52870869
,-1.72756936,-4.30678628,1.90593757,-7.08955911,9.91463553
,0.78065199,4.69869098,8.64854318,-4.54894983,9.81309803
,-9.05025379,-1.45768145,1.09783283,3.2562936,-1.85234482
,8.61872962,-5.33924522,-2.88039735,0.98027364,4.35905046
,-9.6940585,-5.06415052,5.52582478,5.80240312,2.56638262
,2.96683599,-1.38233493,-9.67811484,6.53571968,0.53500973
,5.21159194,3.77145427,-5.77044425,-5.20427398,-6.2304048
,2.05862304,9.48859946,8.9910895,-3.76712959,-3.54332658
,7.11525021,-7.59271744,-5.28420976,-2.5630888,2.32392894
,3.60032748,3.4897744,-9.04027625,5.97410179,-4.16340694
,-5.36954669,-7.97617734,5.97042207,-3.85266185,9.49915254
,-6.99725626,5.3294815,2.4626933,-9.04294683,-2.78212203]

def create_car(type):
    if type == CarType.EXAMPLE_CAR:
        return ExampleCar()
    if type == CarType.FLOOR:
        return Floor()
    if type == CarType.SAUCE:
        return Sauce()
    if type == CarType.RANDO:
        return Rando()
    if type == CarType.DECAY:
        return Decay()
    if type == CarType.DECAY_SMART:
        return DecaySmart()
    if type == CarType.LEARNING_CAR:
        return LearningCar(stored_inputs)
    else:
        raise Exception("Unsupported car")

def on_generation(instance):
    (solution, fitness, _) = instance.best_solution()
    print(f"Best fitness: {fitness} -- solution: {solution}")
    stored_inputs = solution

def create_cars_list(types, inputs):
    result = [LearningCar(list(map(lambda x: x.item(), inputs)))]
    result += list(map(lambda x: create_car(x), types))
    return result

def reward_function(game, car_idx):
    (_, carData) = game.cars[car_idx]

    if carData.y >= 1000:
        return WIN_REWARD

    return 0

    # total = 0
    #
    # our_time_to_finish = (1000 - carData.y) / carData.speed if carData.speed > 0 else -1
    #
    # # if we will finish in 10 turns, we get 100 points.. if 100 turns we get 10 points
    # total += 1000 / our_time_to_finish
    # return total


def fitness_function(solution, solution_idx):
    car_options = list(CarType)
    permutations = list(itertools.combinations(car_options, 2)) + ([[CarType.RANDO, CarType.RANDO], [CarType.RANDO, CarType.RANDO]])
    fitness = 0
    for i, p in enumerate(permutations):
        cars_list = create_cars_list(p, solution)
        g = Game()
        for c in cars_list:
            g.register(c)
        g.play(400)
        fitness += reward_function(g, 0)
    print(fitness)
    return fitness



def run():
    instance = pygad.GA(num_generations=500,
                        num_parents_mating=8,
                        fitness_func=fitness_function,
                        sol_per_pop=50,
                        num_genes=19 * 5,
                        init_range_low=-20,
                        init_range_high=20,
                        on_generation=on_generation)
    instance.run()
    instance.plot_fitness()

if __name__ == "__main__":
    run()
