ACCEL_LOW_FLOOR = 5
ACCEL_HIGH_FLOOR = 20
FLOOR = 5

# The turn-based decay on prices seems v strong
# this car attempts to exploit that
class DecaySmart:
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
        (turns_to_lose, best_opponent_idx) = self.turns_to_lose()

        # no need to accelerate, were about to win
        # just shell everyone
        if turns_to_win == 0:
            if not self.superShell(1):
                self.shell(1)
            return

        # if we can buy enough acceleration to win right away, do it
        accel_to_win = (1000 - ourCar.y) - ourCar.speed
        self.accelerate(accel_to_win)

        # someone else is about to win
        if turns_to_lose == 0:
            if not self.superShell(1):
                self.shell(1)
            self.accelerate(10)
            # avoid div/0
            turns_to_lose = 1
        elif turns_to_lose < 3:
            # theyre behind us, banana
            if best_opponent_idx > idx:
                self.banana()
            else:
                if not self.superShell(1):
                    self.shell(1)
                self.accelerate(20 // turns_to_lose)


        # always buy accel if cheap, ramp up later on in game
        if game.getAccelerateCost(1) < ACCEL_LOW_FLOOR:
            self.accelerate(int(5 + self.turns / 5))

        # getting close to the end
        if turns_to_lose < 10:
            if game.getAccelerateCost(1) < ACCEL_HIGH_FLOOR:
                self.accelerate(5 + (10 // turns_to_lose))

        # literally so cheap why not
        if game.getShellCost(1) < FLOOR + (100 // turns_to_lose):
            self.shell(1)
        if game.getSuperShellCost(1) < FLOOR + (200 // turns_to_lose):
            self.superShell(1)
        if game.getBananaCost() < FLOOR + (20 // turns_to_lose):
            self.banana()
        if game.getShieldCost(1) < FLOOR + (20 // turns_to_lose):
            self.shield(1)

    # worst case turns to lose, if opponents spend all money on acceleration
    def turns_to_lose(self):
        worst = 1000
        worst_idx = 0
        for i, car in enumerate(self.cars):
            if i is not self.idx:
                max_speed = car.speed + self.max_accel(car.balance)
                turns_to_win = (1000 - car.y) // max_speed if max_speed > 0 else 1000
                if turns_to_win < worst:
                    worst = turns_to_win
                    worst_idx = i
        return worst, worst_idx


    def max_accel(self, balance):
        best = 0
        for x in range(1, 1000):
            if self.game.getAccelerateCost(x) > balance:
                return best
            best = x

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


