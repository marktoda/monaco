ACCEL_FLOOR = 15
SHELL_FLOOR = 200
SUPER_SHELL_FLOOR = 300
SHIELD_FLOOR = 400

class Floor:
    def takeYourTurn(self, game, cars, bananas, idx):
        self.cars = cars
        self.idx = idx
        self.game = game
        self.bananas = bananas
        if game.getAccelerateCost(1) < ACCEL_FLOOR:
            self.accelerate(1)
        if game.getShellCost(1) < SHELL_FLOOR:
            self.shell(1)
        if idx == 2 and game.getSuperShellCost(1) < SUPER_SHELL_FLOOR:
            self.superShell(1)
        if idx != 2 and game.getShieldCost(1) < SHIELD_FLOOR:
            self.shield(1)


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


