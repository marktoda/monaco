from monaco import Game, State, ActionType
import json
from tabulate import tabulate
from enum import Enum
from cars.ExampleCar import ExampleCar
from cars.PermaShield import PermaShield
from cars.LearningCar import LearningCar
from cars.c000r import C000r
from cars.Decay import Decay
from cars.Floor import Floor
from cars.Sauce import Sauce
from cars.Rando import Rando
import itertools


class CarType(Enum):
    EXAMPLE_CAR = "ExampleCar"
    PERMA_SHIELD = "PermaShield"
    LEARNING_CAR = "LearningCar"
    FLOOR = "Floor"
    SAUCE = "Sauce"
    RANDO = "Random"
    DECAY = "Decay"
    C000r = "C000r"

stored_inputs=\
[4.78139052,-0.1391743,0.21727997,3.77613546,0.55884698
,0.35326386,-6.9905554,-8.83087955,-1.7413438,-10.41282173
,-1.05400195,5.75539001,-0.62463737,7.29510429,-6.85702128
,5.97366861,9.10497974,7.57819866,-2.29658387,-6.69430074
,-9.59961646,3.37394756,-6.44425053,9.12231378,-5.85082534
,-4.58074154,-7.96478238,9.95435192,7.74248206,4.50762928
,1.29243496,4.91835437,3.37894947,5.66298941,2.61203381
,4.80642869,0.56512631,5.86199896,-7.62343023,3.72355512
,0.39033113,-3.77552723,-4.1571957,4.88497588,3.23678075
,6.0451521,-9.78536036,9.05616966,4.25112696,7.19999253
,8.32636116,-4.18956999,-5.73413664,-6.99218306,3.84583017
,4.46017274,-7.46040252,-2.51965368,-2.55063925,-2.20890019
,-9.88986485,-7.09627418,8.68718476,3.20234977,-0.91554427
,0.78042957,-1.35959228,4.21884968,-3.65148717,-4.62449277
,2.0565945,-4.43708599,-0.82112434,-6.17558266,4.98347881
,9.03451962,9.60008693,-10.20114179,-5.72514361,-4.06220477
,-3.87835974,-0.28426021,0.20845396,-4.01057075,-7.69414824
,6.63880459,6.60319511,4.96436417,0.24868948,6.08546379
,9.55083055,9.811822,7.23752012,2.47597193,-1.74390289]

def create_car(type):
    if type == CarType.EXAMPLE_CAR:
        return ExampleCar()
    if type == CarType.PERMA_SHIELD:
        return PermaShield()
    if type == CarType.FLOOR:
        return Floor()
    if type == CarType.SAUCE:
        return Sauce()
    if type == CarType.DECAY:
        return Decay()
    if type == CarType.RANDO:
        return Rando()
    if type == CarType.C000r:
        return C000r()
    if type == CarType.LEARNING_CAR:
        return LearningCar(stored_inputs)
    else:
        raise Exception("Unsupported car")

def create_cars_list(types):
    return map(lambda x: create_car(x), types)

def run_game(cars_list):
    g = Game()
    for c in cars_list:
        g.register(c)

    # each row is <balance, y, speed, shield>
    car_turns = [[], [], []]
    # each row is <accelerate, shell, superShell, shield, banana> prices
    prices = []
    actions_sold = []
    while g.state != State.DONE and g.turns < 1000:
        g.play(1)

        for i, (_, carData) in enumerate(g.cars):
            car_turns[i].append((carData.balance, carData.y, carData.speed, carData.shield))

        prices.append((g.getAccelerateCost(1), g.getShellCost(1), g.getSuperShellCost(1), g.getShieldCost(1), g.getBananaCost()))
        actions_sold.append((g.actionsSold[ActionType.ACCELERATE], g.actionsSold[ActionType.SHELL], g.actionsSold[ActionType.SUPER_SHELL], g.actionsSold[ActionType.SHIELD], g.actionsSold[ActionType.BANANA]))

    return (car_turns, prices, actions_sold)


def write_games(games):
    for i, g in enumerate(games):
        car_name_str = "-".join(g["cars"])
        with open(f"./data/games-{car_name_str}-{i}.json", 'w') as f:
            data = json.dumps(g)
            f.write(data)


def main():
    # double list to allow for multiple instances of same type
    # car_options = list(CarType) + list(CarType)
    car_options = list(CarType)
    permutations = list(itertools.permutations(car_options, 3))
    # permutations = list(itertools.combinations_with_replacement(car_options, 3))

    games = []
    stats = {}
    for opt in car_options:
        stats[opt] = {
            "wins": 0,
            "losses": 0,
        }

    for i, p in enumerate(permutations):
        (car_turns, prices, actions_sold) = run_game(create_cars_list(p))
        # pretty print prices
        # print(tabulate(prices, headers=["accelerate", "shell", "superShell", "shield", "banana"]))

        # print game
        for j, c in enumerate(car_turns):
            # print("Car", j, p[j])
            # print(tabulate(c, headers=['Balance', 'Y', 'Speed', 'Shield'], tablefmt='fancy_grid'))

            # update stats
            if c[len(c) - 1][1] >= 1000:
                print(f"Game {i} Winner: Car {j} {p[j]}, Turns: {len(c)}")
                stats[p[j]]["wins"] += 1
            else:
                stats[p[j]]["losses"] += 1

        all_turns = [val for tup in zip(*car_turns) for val in tup]
        games.append({
                         "cars": list(map(lambda x: x.value, p)),
                         "turns": all_turns,
                         "prices": prices,
                         "numTurns": len(all_turns),
                         "actionsSold": actions_sold,
                     })

    table = [['Car Type', 'Games Played', 'Wins', 'Losses', 'Ratio']]
    for car_type in stats:
        wins = stats[car_type]["wins"]
        losses = stats[car_type]["losses"]
        table.append([car_type, wins + losses, wins, losses, wins / (wins + losses)])
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    write_games(games)


if __name__ == '__main__':
    main()
