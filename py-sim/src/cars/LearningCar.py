
NUM_VALS = 19 * 5
ACCEL_OFFSET = 0
SHELL_OFFSET = 19
SUPER_OFFSET = 19 * 2
SHIELD_OFFSET = 19 * 3
BANANA_OFFSET = 19 * 4

MAX_ACCELERATE = 20
MAX_SHIELD = 20
MAX_SHELL = 1

class LearningCar:
    def __init__(self, inputs):
        self.inputs = inputs

    def takeYourTurn(self, game, cars, bananas, idx):
        self.cars = cars
        self.idx = idx
        self.game = game
        self.bananas = bananas

        self.accelerate(max(1, min(MAX_ACCELERATE, self.evaluate(ACCEL_OFFSET))))
        self.shell(max(1, min(MAX_SHELL, self.evaluate(SHELL_OFFSET))))
        self.superShell(max(1, min(MAX_SHELL, self.evaluate(SUPER_OFFSET))))
        if self.evaluate(BANANA_OFFSET) > 0:
            self.banana()
        self.shield(max(1, min(MAX_SHIELD, self.evaluate(SHIELD_OFFSET))))

    def evaluate(self, start_val):
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
        return int(our_pos * self.inputs[start_val + 0] \
            + our_y * self.inputs[start_val + 1] \
            + our_speed * self.inputs[start_val + 2] \
            + our_balance * self.inputs[start_val + 3] \
            + our_shield * self.inputs[start_val + 4] \
            + worst_y * self.inputs[start_val + 5] \
            + worst_speed * self.inputs[start_val + 6] \
            + worst_balance * self.inputs[start_val + 7] \
            + worst_shield * self.inputs[start_val + 8] \
            + best_y * self.inputs[start_val + 9] \
            + best_speed * self.inputs[start_val + 10] \
            + best_balance * self.inputs[start_val + 11] \
            + best_shield * self.inputs[start_val + 12] \
            + distance_to_banana * self.inputs[start_val + 13] \
            + acceleration_cost * self.inputs[start_val + 14] \
            + shell_cost * self.inputs[start_val + 15] \
            + super_shell_cost * self.inputs[start_val + 16] \
            + shield_cost * self.inputs[start_val + 17] \
            + banana_cost * self.inputs[start_val + 18])

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

