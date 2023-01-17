import pygad
from monaco import Game, State, ActionType
import json
from tabulate import tabulate
from enum import Enum
from cars.LearningCar import LearningCar
from cars.Decay import Decay
from cars.ExampleCar import ExampleCar
from cars.PermaShield import PermaShield
from cars.Rando import Rando
from cars.Floor import Floor
from cars.Sauce import Sauce
import itertools

WIN_REWARD = 100000

class CarType(Enum):
    EXAMPLE_CAR = "ExampleCar"
    PERMA_SHIELD = "PermaShield"
    FLOOR = "Floor"
    SAUCE = "Sauce"
    RANDO = "Random"
    LEARNING_CAR = "LearningCar"
    DECAY = "Decay"

stored_inputs=\
[-5.92403588,-2.09961041,5.10842475,-1.63619372,1.56596772
,7.78648556,6.40638994,-5.27050725,2.17560712,7.27581374
,8.25661028,-2.16783937,-8.73338452,5.16775773,4.43439213
,-10.08702292,5.32502721,3.34068275,-5.05668094,7.88928641
,7.04855914,11.40503862,-11.43984397,-6.01798165,-3.45369803
,-2.78160501,-9.50527209,4.94794348,1.73115421,-9.54193203
,4.56848694,-0.71558589,0.54187438,0.42186172,-9.20439745
,10.98993319,2.30649675,3.5517238,-0.49325797,4.06714769
,3.02003793,-0.84090557,-0.12617656,-5.65721236,5.00857652
,-1.12037216,-6.19347304,-0.48863355,-7.74925219,-5.83081974
,-2.00634125,8.55342369,8.21501223,-8.38177936,1.81574693
,-8.98401283,-3.76465674,9.90335496,-1.77966085,-0.53180865
,0.76155512,-0.89041625,1.71439182,9.80713344,-7.3089626
,-7.91987448,-2.57249113,-1.35536498,5.80312594,8.59604725
,2.73929098,4.91979225,-3.5076045,10.25572653,3.03228358
,1.57429602,-0.78500228,-1.41988512,-9.93841763,-3.56723041
,-4.57755683,-2.24552936,4.54141533,-4.12109438,-4.13473527
,-2.31165602,6.78085508,6.33976054,4.87972523,3.33017899
,8.0524662,5.96580217,1.70054952,0.47353315,6.02424368]

def create_car(type):
    if type == CarType.EXAMPLE_CAR:
        return ExampleCar()
    if type == CarType.PERMA_SHIELD:
        return PermaShield()
    if type == CarType.FLOOR:
        return Floor()
    if type == CarType.SAUCE:
        return Sauce()
    if type == CarType.RANDO:
        return Rando()
    if type == CarType.DECAY:
        return Decay()
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
                        num_parents_mating=7,
                        fitness_func=fitness_function,
                        sol_per_pop=20,
                        num_genes=19 * 5,
                        init_range_low=-10,
                        init_range_high=10,
                        on_generation=on_generation)
    instance.run()
    instance.plot_fitness()

if __name__ == "__main__":
    run()
