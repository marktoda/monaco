from monaco import Game, State, ActionType
import json
from tabulate import tabulate
from enum import Enum
from cars.ExampleCar import ExampleCar
from cars.LearningCar import LearningCar
from cars.c000r import C000r
from cars.Decay import Decay
from cars.DecaySmart import DecaySmart
from cars.Floor import Floor
from cars.Sauce import Sauce
from cars.Rando import Rando
import itertools


class CarType(Enum):
    EXAMPLE_CAR = "ExampleCar"
    LEARNING_CAR = "LearningCar"
    FLOOR = "Floor"
    SAUCE = "Sauce"
    RANDO = "Random"
    DECAY = "Decay"
    DECAY_SMART = "DecaySmart"
    C000r = "C000r"

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
    if type == CarType.DECAY:
        return Decay()
    if type == CarType.DECAY_SMART:
        return DecaySmart()
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
                if CarType.DECAY_SMART in p and p[j] is not CarType.DECAY_SMART:
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
