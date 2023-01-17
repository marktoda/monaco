ACCEL_LOW_FLOOR = 5
ACCEL_HIGH_FLOOR = 5
FLOOR = 5

# The turn-based decay on prices seems v strong
# this car attempts to exploit that
class C000r:

    def takeYourTurn(self, game, cars, bananas, idx):
        self.game = game
        self.cars = cars
        self.bananas = bananas
        self.idx = idx

        ourCar = cars[idx]
        if ourCar.y > 850 and ourCar.balance >= game.getAccelerateCost(1000 - (ourCar.y + ourCar.speed)):
            self.accelerate(1000 - (ourCar.y - ourCar.speed))

        shellCost = game.getShellCost(1)
        if shellCost < 400 and idx != 0 and cars[0].y > 8 and cars[1].y == 0 and cars[2].y == 0:
            self.shell(1)
            shellCost = 15001
        elif shellCost == 0:
            self.shell(1)
        elif idx == 1 and ourCar.balance >= shellCost and cars[0].y + cars[0].speed >= 1000:
            ourCar.balance -= game.buyShell(1)
            shellCost = 15001

        if idx != 0 and cars[0].y < 200:
            if ourCar.speed < 3 and shellCost < 15000:
                self.accelerate(2)


        if cars[0].y > 850:
            if (idx == 0 and cars[1].speed > ourCar.speed) or cars[2].speed > ourCar.speed:
                largerSpeed = cars[1].speed if cars[1].speed > cars[2].speed else cars[2].speed
                self.accelerate(largerSpeed - ourCar.speed)
            else:
                self.accelerate(5)
            return

        if idx != 0:
            frontCarSpeed = cars[idx - 1].speed
            if ourCar.balance >= shellCost and shellCost < 2000 and ((frontCarSpeed > ourCar.speed and frontCarSpeed > 4) or frontCarSpeed > 8):
                ourCar.balance -= game.buyShell(1)
                shellCost = 15001
            bigMove = game.getAccelerateCost(7)
            if ourCar.balance >= bigMove and bigMove < 1000:
                self.accelerate(7)
                ourCar.speed += 7


        costToCatchUp = 0
        if idx == 2:
            if cars[1].balance < 200 or (cars[0].y > 825 and cars[1].y < 750):
                costToCatchUp = game.getAccelerateCost(1 + cars[1].speed + cars[1].y - (ourCar.speed + ourCar.y))
            elif cars[1].speed > ourCar.speed:
                    costToCatchUp = game.getAccelerateCost(cars[1].speed - ourCar.speed)

        nextCarSpeed = cars[0].speed
        if idx == 1 and nextCarSpeed > 3 and ourCar.balance >= shellCost:
            if shellCost < 300 and (nextCarSpeed > (ourCar.speed + 6) or nextCarSpeed > 24):
                self.shell(1)
            elif shellCost < 1000 and (nextCarSpeed > 35 or cars[0].y - ourCar.y > 50 or cars[0].y > 950 or ourCar.balance > 1000):
                self.shell(1)

        if ourCar.balance > (2000 if cars[0].y < 800 else 500) and ourCar.speed < 6:
            game.accelerate(2 if idx == 0 else 4)





    def accelerate(self, amount):
        car = self.cars[self.idx]
        if car.balance > self.game.getAccelerateCost(amount):
            car.balance -= self.game.buyAcceleration(amount)
            return True
        return False

    def shell(self, amount):
        car = self.cars[self.idx]
        if car.balance > self.game.getShellCost(amount):
            car.balance -= self.game.buyShell(amount)
            return True
        return False

    def superShell(self, amount):
        car = self.cars[self.idx]
        if car.balance > self.game.getSuperShellCost(amount):
            car.balance -= self.game.buySuperShell(amount)
            return True
        return False

    def shield(self, amount):
        car = self.cars[self.idx]
        if car.balance > self.game.getShieldCost(amount):
            car.balance -= self.game.buyShield(amount)
            return True
        return False

    def banana(self):
        car = self.cars[self.idx]
        if car.balance > self.game.getBananaCost():
            car.balance -= self.game.buyBanana()
            return True
        return False


