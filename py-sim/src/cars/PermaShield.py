class PermaShield:
    def takeYourTurn(self, game, cars, bananas, idx):
        self.cars = cars
        self.idx = idx
        self.game = game
        self.bananas = bananas
        if game.getShieldCost(1) < 500:
            self.shell(1)
        if game.getAccelerateCost(1) < 800:
            self.accelerate(1)
        if cars[idx].speed == 0:
            self.accelerate(1)


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

