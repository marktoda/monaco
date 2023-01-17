ACCEL_FLOOR = 5
FLOOR = 2

# The turn-based decay on prices seems v strong
# this car attempts to exploit that
class Decay:
    def __init__(self):
        self.turns = 0


    def takeYourTurn(self, game, cars, bananas, idx):
        ourCar = cars[idx]
        self.turns += 1
        self.cars = cars
        self.idx = idx
        self.game = game
        self.bananas = bananas
        turns_to_win = (1000 - ourCar.y) // ourCar.speed if ourCar.speed > 0 else 1000
        overall_turns_to_win = (1000 - cars[0].y) // cars[0].speed if cars[0].speed > 0 else 1000

        # no need to accelerate, were about to win
        # just shell everyone
        if turns_to_win == 0:
            if not self.superShell(1):
                self.shell(1)
            return

        # someone else is about to win
        if overall_turns_to_win == 0:
            if not self.superShell(1):
                self.shell(1)

        # try to make it 0 :)
        if turns_to_win == 1:
            speed_needed = (1000 - ourCar.y) - ourCar.speed
            if self.accelerate(speed_needed):
                if not self.superShell(1):
                    self.shell(1)
                return

        # always buy accel if cheap, ramp up later on in game
        if game.getAccelerateCost(1) < ACCEL_FLOOR:
            self.accelerate(int(5 + self.turns / 5))

        # literally so cheap why not
        if game.getShellCost(1) < FLOOR:
            self.shell(1)
        if game.getSuperShellCost(1) < FLOOR:
            self.superShell(1)
        if game.getBananaCost() < FLOOR:
            self.banana()
        if game.getShieldCost(1) < FLOOR:
            self.shield(1)


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


