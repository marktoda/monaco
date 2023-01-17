from monaco import Game, State, ActionType
import json
from tabulate import tabulate
from enum import Enum
from cars.ExampleCar import ExampleCar
from cars.PermaShield import PermaShield
from cars.LearningCar import LearningCar
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

stored_inputs=\
[-2.7046551,6.94741019,6.10476945,5.6395508,-7.53900326,-1.08904729
,-0.99514503,6.3237883,-8.62433431,-1.97309807,2.52204135,-0.51315463
,-3.09736826,6.85114008,-8.58434561,-3.41484134,3.23493316,6.44884636
,-7.12272333,8.87162932,9.40337156,-5.90352307,3.63664252,-5.75996806
,-4.307686,7.04949271,4.58026302,6.54558715,3.54630172,2.77591739
,-7.49281875,-8.19607915,-3.05859765,5.1975602,-8.33971651,-4.72013972
,8.47452424,5.42439454,5.73994874,-7.8605622,4.51318849,7.44091687
,5.0793094,-2.25349789,-7.75735791,10.18759679,3.34424062,7.79191926
,-2.23284485,0.59059822,-2.16797511,1.15890225,0.0434501,7.96885386
,1.4031039,8.21912073,3.29576103,9.25741014,-3.34521455,6.80719635
,-7.38115853,2.24730318,-9.55095525,-6.69424668,-8.12659548,8.25252468
,-5.4838856,0.07892217,-8.94000962,-1.17669348,4.64469551,-1.30045923
,4.84755159,0.03666665,-6.84552499,-1.24395144,1.68361141,-9.47602401
,-7.37959524,-2.23272819,-3.90299131,-7.06668352,-8.4654235,2.65436268
,-0.88534725,9.20766865,2.82228612,6.04644962,0.35059258,7.5305539
,-3.29517605,-5.04323316,2.93998764,-9.39562733,7.44755506]

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
