from monaco import Game, State, ActionType
import json
from tabulate import tabulate
from enum import Enum
from cars.ExampleCar import ExampleCar
from cars.LearningCar import LearningCar
from cars.c000r import C000r
from cars.TurnOptimizer import TurnOptimizer
from cars.Lagger import Lagger
from cars.TurnOptimizer3 import TurnOptimizer3
from cars.TurnOptimizer4 import TurnOptimizer4
from cars.Decay import Decay
from cars.DecaySmart import DecaySmart
from cars.DecaySmart2 import DecaySmart2
from cars.DecaySmartBanana import DecaySmartBanana
from cars.Floor import Floor
from cars.Sauce import Sauce
from cars.Rando import Rando
import itertools


class CarType(Enum):
    EXAMPLE_CAR = "ExampleCar"
    LEARNING_CAR = "LearningCar"
    FLOOR = "Floor"
    SAUCE = "Sauce"
    TURN_OPTIMIZER = "TurnOptimizer"
    TURN_OPTIMIZER_3 = "TurnOptimizer3"
    TURN_OPTIMIZER_4 = "TurnOptimizer4"
    DECAY_SMART_2 = "DecaySmart2"
    C000r = "C000r"
    DECAY_SMART_B = "DecaySmartBanana"
    LAGGER = "Lagger"

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
    if type == CarType.TURN_OPTIMIZER:
        return TurnOptimizer()
    if type == CarType.TURN_OPTIMIZER_3:
        return TurnOptimizer3()
    if type == CarType.TURN_OPTIMIZER_4:
        return TurnOptimizer4()
    if type == CarType.C000r:
        return C000r()
    if type == CarType.LEARNING_CAR:
        return LearningCar(stored_inputs)
    if type == CarType.DECAY_SMART_2:
        return DecaySmart2()
    if type == CarType.DECAY_SMART_B:
        return DecaySmartBanana()
    if type == CarType.LAGGER:
        return Lagger()
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
                if CarType.TURN_OPTIMIZER_3 in p and p[j] is not CarType.TURN_OPTIMIZER_3:
                    print("WE LOSE!")
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
