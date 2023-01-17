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
[6.25616069,0.34617134,0.20539233,2.30440248,0.47615718
,0.29839338,-6.9905554,-8.4201641,-2.48767545,-10.87419651
,-1.6296828,6.68196947,-0.60733494,7.29510429,-6.85702128
,6.4764934,7.75706498,8.80532851,-1.87573158,-6.29895791
,-9.12011099,3.39717519,-5.49493637,9.08472542,-5.85082534
,-3.66396477,-6.58278385,10.40888958,7.74248206,5.30411392
,1.53993363,4.91835437,2.12892923,5.05786736,2.61203381
,4.06035902,0.86179447,5.86199896,-6.54614553,2.93256219
,1.28300484,-3.97531001,-4.1571957,5.45253427,4.01821376
,6.0451521,-8.98020278,10.30690584,4.25112696,7.19999253
,8.83093589,-3.60062026,-4.55570416,-6.97378383,3.84583017
,3.88072449,-7.46040252,-2.51965368,-3.10010234,-2.36393111
,-9.00511366,-7.53894949,7.9975175,2.50624332,-1.28890229
,0.0123683,-1.1869503,5.32495831,-2.79101895,-3.86254411
,1.17851641,-4.32175498,-1.67005766,-6.33803347,4.02279297
,9.03451962,10.37625447,-9.7747155,-5.41769541,-5.06048761
,-3.82370268,-0.34790768,0.20845396,-4.87040012,-7.69414824
,5.99666748,6.68961179,4.66792175,0.24868948,6.3806802
,9.46643214,9.67651943,6.24603897,2.47597193,-0.79639154]

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
