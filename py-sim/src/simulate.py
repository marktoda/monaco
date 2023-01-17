from monaco import Game, State
import json
from tabulate import tabulate
from enum import Enum
from cars.ExampleCar import ExampleCar
from cars.PermaShield import PermaShield
from cars.Floor import Floor
from cars.Sauce import Sauce
import itertools


class CarType(Enum):
    EXAMPLE_CAR = "ExampleCar"
    PERMA_SHIELD = "PermaShield"
    FLOOR = "Floor"
    SAUCE = "Sauce"

def create_car(type):
    if type == CarType.EXAMPLE_CAR:
        return ExampleCar()
    if type == CarType.PERMA_SHIELD:
        return PermaShield()
    if type == CarType.FLOOR:
        return Floor()
    if type == CarType.SAUCE:
        return Sauce()
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
    while g.state != State.DONE and g.turns < 1000:
        g.play(1)

        for i, (_, carData) in enumerate(g.cars):
            car_turns[i].append((carData.balance, carData.y, carData.speed, carData.shield))
            prices.append((g.getAccelerateCost(1), g.getShellCost(1), g.getSuperShellCost(1), g.getShieldCost(1), g.getBananaCost()))


    return (car_turns, prices)


def write_games(games):
    for i, g in enumerate(games):
        with open(f"./data/games-{i}.json", 'w') as f:
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
        (car_turns, prices) = run_game(create_cars_list(p))
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
                         "numTurns": len(all_turns)
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
