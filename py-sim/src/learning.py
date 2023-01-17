WIN_REWARD = 1000000000000

# if win, bajillion points
# lots of points for being near to the finish in terms of time
# lose points for opponents being near to the finish in terms of time
# gain points for keeping balance
# lose points for opponents keeping balance
def reward_function(game, car_idx):
    (_, carData) = game.cars[car_idx]

    if carData.y >= 1000:
        return WIN_REWARD

    total = 0

    our_time_to_finish = (1000 - carData.y) / carData.speed
    their_time_to_finish = 10000000
    for i, car in enumerate(game.cars):
        if i != car_idx:
            ttf = 1000 - (car.y) / car.speed
            if ttf < their_time_to_finish:
                their_time_to_finish = ttf

            total -= car.balance

    # if we will finish in 10 turns, we get 1000 points.. if 100 turns we get 100 points
    total += 10000 / our_time_to_finish
    # if they will finish in 10 turns, subtract 1000 points.. if 100 turns subtract 100 points
    total -= 10000 / their_time_to_finish

    total += carData.balance
