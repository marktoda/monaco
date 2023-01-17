import random

class Rando:
    def takeYourTurn(self, game, cars, bananas, idx):
        self.cars = cars
        self.idx = idx
        self.game = game
        self.bananas = bananas
        self.accelerate(weighted_random(50))
        self.shield(weighted_random(20))
        if random.randrange(0, 100) < 25 and idx != 0:
            self.shell(1)
        if random.randrange(0, 100) < 25 and idx != 0:
            self.superShell(1)
        if random.randrange(0, 100) < 25 and idx != 2:
            self.banana()


    def accelerate(self, amount):
        car = self.cars[self.idx]
        if car.balance > self.game.getAccelerateCost(amount):
            car.balance -= self.game.buyAcceleration(amount)

    def shell(self, amount):
        car = self.cars[self.idx]
        if car.balance > self.game.getShellCost(amount):
            car.balance -= self.game.buyShell(amount)

    def superShell(self, amount):
        car = self.cars[self.idx]
        if car.balance > self.game.getSuperShellCost(amount):
            car.balance -= self.game.buySuperShell(amount)

    def shield(self, amount):
        car = self.cars[self.idx]
        if car.balance > self.game.getShieldCost(amount):
            car.balance -= self.game.buyShield(amount)

    def banana(self):
        car = self.cars[self.idx]
        if car.balance > self.game.getBananaCost():
            car.balance -= self.game.buyBanana()

def weighted_random(max):
    return min(random.randint(0, max), random.randint(0, max), random.randint(0, max))
