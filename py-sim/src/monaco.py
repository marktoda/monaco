import random
import copy
from enum import Enum
import wad
import math

PLAYERS_REQUIRED = 3
POST_SHELL_SPEED = 1
STARTING_BALANCE = 17500
FINISH_DISTANCE = 1000
BANANA_SPEED_MODIFIER = 0.5 * (10**18)
WAD = 10**18

SHELL_TARGET_PRICE = 200
SHELL_PER_TURN_DECREASE = 0.33
SHELL_SELL_PER_TURN = 0.2

ACCELERATE_TARGET_PRICE = 10
ACCELERATE_PER_TURN_DECREASE = 0.33
ACCELERATE_SELL_PER_TURN = 2

SUPER_SHELL_TARGET_PRICE = 300
SUPER_SHELL_PER_TURN_DECREASE = 0.35
SUPER_SHELL_SELL_PER_TURN = 0.2

BANANA_TARGET_PRICE = 200
BANANA_PER_TURN_DECREASE = 0.33
BANANA_SELL_PER_TURN = 0.2

SHIELD_TARGET_PRICE = 150
SHIELD_PER_TURN_DECREASE = 0.33
SHIELD_SELL_PER_TURN = 0.2

class ActionType(Enum):
    ACCELERATE = 1
    SHELL = 2
    SUPER_SHELL = 3
    BANANA = 4
    SHIELD = 5

class State(Enum):
    WAITING = 1
    ACTIVE = 2
    DONE = 3

class CarData:
    balance = 0
    speed = 0
    y = 0
    shield = 0

    def __init__(self, idx):
        self.balance = STARTING_BALANCE
        self.idx = idx


class Game:
    turns = 1
    entropy = random.randint(0, 2**72)
    # bananas in play, tracked by y position
    bananas = []
    actionsSold = {
        ActionType.ACCELERATE: 0,
        ActionType.SHELL: 0,
        ActionType.SUPER_SHELL: 0,
        ActionType.BANANA: 0,
        ActionType.SHIELD: 0,
    }
    # (car, carData)
    cars = []
    state = State.WAITING

    def __init__(self):
        self.cars = []
        self.bananas = []
        self.turns = 1
        self.actionsSold = {
            ActionType.ACCELERATE: 0,
            ActionType.SHELL: 0,
            ActionType.SUPER_SHELL: 0,
            ActionType.BANANA: 0,
            ActionType.SHIELD: 0,
        }
        self.state = State.WAITING

    def register(self, car):
        if len(self.cars) + 1 > PLAYERS_REQUIRED:
            raise Exception("Max players")

        self.cars.append((car, CarData(len(self.cars))))
        if len(self.cars) == PLAYERS_REQUIRED:
            self.state = State.ACTIVE

    def play(self, turnsToPlay):
        self.assertActive()

        for _ in range(turnsToPlay):
            (currentCar, currentCarData) = self.cars[self.turns % PLAYERS_REQUIRED]
            sorted_cars = self.getCarsSortedByY()
            self.currentCarIndex = self.turns % PLAYERS_REQUIRED
            yourCarIndex = 0
            for i, car in enumerate(sorted_cars):
                if car.idx == currentCarData.idx:
                    yourCarIndex = i
                    break

            carDataBefore = copy.deepcopy(currentCarData)
            actionsSoldBefore = copy.deepcopy(self.actionsSold)
            try:
                currentCar.takeYourTurn(self, sorted_cars, self.bananas, yourCarIndex)
            except:
                # ignore raise in turn
                self.cars[self.currentCarIndex] = (currentCar, carDataBefore)
                self.actionsSold = actionsSoldBefore
                print(f"Turn failed {self.currentCarIndex}")
                pass

            self.bananas = sorted(self.bananas)
            for i in range(PLAYERS_REQUIRED):
                (_, carData) = self.cars[i]
                # decrement shield if its active
                if carData.shield > 0:
                    carData.shield -= 1

                carTargetPosition = carData.y + carData.speed

                # check for banana collisions
                for bananaIdx in range(len(self.bananas)):
                    bananaPosition = self.bananas[bananaIdx]
                    if carData.y >= bananaPosition:
                        continue
                    # we will pass over the banana
                    if carTargetPosition >= bananaPosition:
                        # stop at banana
                        carTargetPosition = bananaPosition
                        # apply banana speed modifier
                        carData.speed = carData.speed // 2

                        # remove banana
                        self.bananas.pop(bananaIdx)
                        # resort
                        self.bananas = sorted(self.bananas)

                    # skip the rest as they are too far
                    break

                # update y and check if winner
                carData.y = carTargetPosition
                if carData.y >= FINISH_DISTANCE:
                    self.state = State.DONE
                    return

            self.turns += 1

    def buyAcceleration(self, amount):
        self.assertActive()
        cost = self.getAccelerateCost(amount)

        (_, carData) = self.cars[self.currentCarIndex]
        self.purchase(self.currentCarIndex, cost)
        carData.speed += amount
        self.actionsSold[ActionType.ACCELERATE] += amount
        return cost

    def buyShell(self, amount):
        self.assertActive()
        if amount == 0:
            raise Exception("Cannot buy 0 shells")
        cost = self.getShellCost(amount)

        (_, carData) = self.cars[self.currentCarIndex]
        self.purchase(self.currentCarIndex, cost)
        self.actionsSold[ActionType.SHELL] += amount

        closestCar = None
        distanceFromClosestCar = FINISH_DISTANCE + 1
        for i in range(PLAYERS_REQUIRED):
            (_, nextCar) = self.cars[i]
            if nextCar.y <= carData.y:
                continue
            distanceFromNextCar = nextCar.y - carData.y
            if distanceFromNextCar < distanceFromClosestCar:
                closestCar = nextCar
                distanceFromClosestCar = distanceFromNextCar

        self.bananas = sorted(self.bananas)
        for i in range(len(self.bananas)):
            if self.bananas[i] <= carData.y:
                continue
            if self.bananas[i] > carData.y + distanceFromClosestCar:
                break
            # TODO: Check this doesnt break anything, modifying array while iterating
            self.bananas.pop(i)
            closestCar = None
            break
        self.bananas = sorted(self.bananas)

        if closestCar is not None:
            # shell em
            if closestCar.shield == 0 and closestCar.speed > POST_SHELL_SPEED:
                closestCar.speed = POST_SHELL_SPEED
        return cost

    def buySuperShell(self, amount):
        self.assertActive()
        if amount == 0:
            raise Exception("Cannot buy 0 shells")
        cost = self.getSuperShellCost(amount)
        (_, carData) = self.cars[self.currentCarIndex]
        self.purchase(self.currentCarIndex, cost)
        self.actionsSold[ActionType.SUPER_SHELL] += amount

        for i in range(PLAYERS_REQUIRED):
            (_, nextCar) = self.cars[i]
            if nextCar.y <= carData.y:
                continue
            if nextCar.speed > POST_SHELL_SPEED:
                nextCar.speed = POST_SHELL_SPEED

        # check for banana collisions
        self.bananas = sorted(self.bananas)
        banana_len = len(self.bananas)
        num_to_pop = 0
        for i in range(banana_len):
            # banana is behind or under us, skip
            if self.bananas[i] <= carData.y:
                continue

            # otherwise pop
            num_to_pop += 1
        for _ in range(num_to_pop):
            self.bananas.pop()
        self.bananas = sorted(self.bananas)
        return cost

    def buyBanana(self):
        self.assertActive()
        cost = self.getBananaCost()
        (_, carData) = self.cars[self.currentCarIndex]
        self.purchase(self.currentCarIndex, cost)
        self.actionsSold[ActionType.BANANA] += 1
        self.bananas.append(carData.y)
        self.bananas = sorted(self.bananas)
        return cost

    def buyShield(self, amount):
        self.assertActive()
        cost = self.getShieldCost(amount)
        (_, carData) = self.cars[self.currentCarIndex]
        self.purchase(self.currentCarIndex, cost)
        self.actionsSold[ActionType.SHIELD] += amount
        carData.shield += 1 + amount
        return cost


    def purchase(self, carIdx, cost):
        (_, carData) = self.cars[carIdx]
        # sim quirk: in solidity if failure during turn we revert the turn
        # revert not as easy here so we just stop the turn but keep whatever was already done
        # TODO: could journal purchases and only execute if no revert
        if carData.balance < cost:
            raise Exception("Can't afford")
        carData.balance -= cost


    def getAccelerateCost(self, amount):
        sum = 0
        for i in range(amount):
            sum += computeActionPrice(
                ACCELERATE_TARGET_PRICE,
                ACCELERATE_PER_TURN_DECREASE,
                self.turns,
                self.actionsSold[ActionType.ACCELERATE] + i,
                ACCELERATE_SELL_PER_TURN)
        return sum

    def getShellCost(self, amount):
        sum = 0
        for i in range(amount):
            sum += computeActionPrice(
                SHELL_TARGET_PRICE,
                SHELL_PER_TURN_DECREASE,
                self.turns,
                self.actionsSold[ActionType.SHELL] + i,
                SHELL_SELL_PER_TURN)
        return sum

    def getSuperShellCost(self, amount):
        sum = 0
        for i in range(amount):
            sum += computeActionPrice(
                SUPER_SHELL_TARGET_PRICE,
                SUPER_SHELL_PER_TURN_DECREASE,
                self.turns,
                self.actionsSold[ActionType.SUPER_SHELL] + i,
                SUPER_SHELL_SELL_PER_TURN)
        return sum

    def getBananaCost(self):
        return computeActionPrice(
            BANANA_TARGET_PRICE,
            BANANA_PER_TURN_DECREASE,
            self.turns,
            self.actionsSold[ActionType.BANANA],
            BANANA_SELL_PER_TURN)

    def getShieldCost(self, amount):
        sum = 0
        for i in range(amount):
            sum += computeActionPrice(
                SHIELD_TARGET_PRICE,
                SHIELD_PER_TURN_DECREASE,
                self.turns,
                self.actionsSold[ActionType.SHIELD] + i,
                SHIELD_SELL_PER_TURN)
        return sum


    def assertActive(self):
        if self.state != State.ACTIVE:
            raise Exception("Not active")


    def getCarsSortedByY(self):
        sortedCars = list(map(lambda x: x[1], copy.deepcopy(self.cars)))
        for i in range(PLAYERS_REQUIRED):
            for j in range(i + 1, PLAYERS_REQUIRED):
                if sortedCars[j].y > sortedCars[i].y:
                    temp = sortedCars[i]
                    sortedCars[i] = sortedCars[j]
                    sortedCars[j] = temp
        return sortedCars


def computeActionPrice(targetPrice, perTurnPriceDecrease, turnsSinceStart, sold, sellPerTurnWad):
    perTurn = (sold + 1) / sellPerTurnWad
    turnStuff = (turnsSinceStart - 1) - perTurn
    decrease = math.log(1 - perTurnPriceDecrease)
    multiplier = math.exp(decrease * turnStuff)
    return int(targetPrice * multiplier)



class MockCar:
    buy = 0

    def takeYourTurn(self, game, cars, bananas, idx):
        if self.buy > 0:
            game.buyAcceleration(self.buy)

    def buyAcceleration(self, amt):
        self.buy = amt



if __name__ == '__main__':
    game = Game()
    game.register(MockCar())
    game.register(MockCar())
    game.register(MockCar())
    game.play(10)

