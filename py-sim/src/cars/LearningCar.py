class LearningCar:
    def takeYourTurn(self, game, cars, bananas, idx):
        self.cars = cars
        self.idx = idx
        self.game = game
        self.bananas = bananas

    def evaluate(self):
        ourCar = self.cars[self.idx]
        our_pos = self.idx
        our_y = ourCar.y
        our_speed = ourCar.speed
        our_balance = ourCar.balance
        our_shield = ourCar.shield

        worst_opponent = self.cars[2] if self.idx != 2 else self.cars[1]
        best_opponent = self.cars[0] if self.idx != 0 else self.cars[1]

        worst_y = worst_opponent.y
        worst_speed = worst_opponent.speed
        worst_balance = worst_opponent.balance
        worst_shield = worst_opponent.shield

        best_y = best_opponent.y
        best_speed = best_opponent.speed
        best_balance = best_opponent.balance
        best_shield = best_opponent.shield

        distance_to_banana = 1000000000
        for banana in self.bananas:
            if banana > our_y:
                distance_to_banana = banana - our_y
                break

        acceleration_cost = self.game.getAccelerateCost(1)
        shell_cost = self.game.getShellCost(1)
        super_shell_cost = self.game.getSuperShellCost(1)
        shield_cost = self.game.getShieldCost(1)
        banana_cost = self.game.getBananaCost()

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

