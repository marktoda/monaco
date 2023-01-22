ACCEL_LOW_FLOOR = 5
FLOOR = 5

# The turn-based decay on prices seems v strong
# this car attempts to exploit that
class DecaySmartBanana:
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
        (turns_to_lose, best_opponent_idx) = self.turns_to_lose_optimistic()
        (banana_distance, banana_index) = self.get_closest_banana()

        # no need to accelerate, were about to win
        # just shell everyone
        if turns_to_win == 0:
            if not self.superShell(1):
                self.shell(self.max_shell(ourCar.balance))
            return

        # if we can buy enough acceleration to win right away, do it
        # ONLY IF THERE ARE NOT BANANAS IN THE WAY
        accel_to_win = (1000 - ourCar.y) - ourCar.speed
        if self.max_accel(ourCar.balance) >= accel_to_win:
            if banana_distance > 1000: # there are no bananas in the way
                self.accelerate(accel_to_win)
                self.stop_opponent(best_opponent_idx)
                self.accelerate(self.max_accel(ourCar.balance))
                return
            else:
                # there is a banana in the way but we are close to winning so lets get rid of the banana and try accelerating again
                # either accelerate right up until the banana or throw a shell
                cost_to_kill_banana = self.game.getShellCost(banana_distance)
                ratio = cost_to_kill_banana // ourCar.balance if ourCar.balance > 0 else 1
                if ratio < 1 // 2:
                    # if the cost of the banana is relatively low compared to overall balance lets nuke it
                    self.shell(banana_distance)
                    # technically there could be more bananas in the way... but lets just try this for now
                    self.accelerate(accel_to_win)
                else :
                    # cost to shell is too high lets just accelerate right up until the banana ? maybe someone will nuke it for us
                    self.accelerate(banana_distance - 1)

        

        # ACCEL DECISION MAKING
        # someone else is about to win
        if turns_to_lose == 0:
            self.stop_opponent(best_opponent_idx)
            self.accelerate(self.max_accel(ourCar.balance))
            # avoid div/0
            turns_to_lose = 1
        elif turns_to_lose < 5:
            self.stop_opponent(best_opponent_idx, 200)
            self.accelerate(20 // turns_to_lose)
        else:
            # always buy accel if cheap, ramp up later on in game
            self.accel_to_floor()


        # literally so cheap why not
        if game.getShellCost(1) < FLOOR:
            self.shell(1)
        if game.getSuperShellCost(1) < FLOOR:
            self.superShell(1)
        if game.getBananaCost() < FLOOR:
            self.banana()
        if game.getShieldCost(1) < FLOOR:
            self.shield(1)

    def accel_to_floor(self):
        (turns_to_lose, _) = self.turns_to_lose_optimistic()
        floor = ACCEL_LOW_FLOOR + (500 // turns_to_lose)
        while self.game.getAccelerateCost(1) < floor:
            if not self.accelerate(1):
                return

    def stop_opponent(self, opponent_idx, max_cost=10000):
        if opponent_idx < self.idx:
            # no point shelling
            if self.cars[opponent_idx].speed == 1:
                return

            super_cost = self.game.getSuperShellCost(1)
            # enough shells to kill all bananas and stop them
            shell_amt = self.bananas_between(opponent_idx) + 1
            shell_cost = self.game.getShellCost(shell_amt)
            if super_cost > max_cost and shell_cost > max_cost:
                return

            if super_cost <= shell_cost:
                self.superShell(1)
            else:
                self.shell(shell_amt)
        elif self.game.getBananaCost() < max_cost:
            self.banana()

    def bananas_between(self, opponent_idx):
        our_y = self.cars[self.idx].y
        their_y = self.cars[opponent_idx].y
        if our_y > their_y:
            return 0
        count = 0
        for b in self.bananas:
            if b >= our_y and b <= their_y:
                count += 1
        return count

    def calculate_banana_hit(self):
        (distance, index) = self.get_closest_banana()
    

    def turns_to_lose_optimistic(self):
        worst = 1000
        worst_idx = 0
        for i, car in enumerate(self.cars):
            if i is not self.idx:
                assumed_speed = car.speed + self.max_accel(0.6*car.balance)
                turns_to_win = (1000 - car.y) // assumed_speed if assumed_speed > 0 else 1000
                if turns_to_win < worst:
                    worst = turns_to_win
                    worst_idx = i
        return worst, worst_idx
        

    def get_closest_banana(self):
        closest = 1001
        index = 0
        for i in range(len(self.bananas)):
            distance = self.bananas[i] - self.cars[self.idx].y
            if distance > 0 and distance < closest:
                closest = distance
                index = i
        return closest, index

    # worst case turns to lose, if opponents spend all money on acceleration
    # potentially could use an avg case turns to lose as a heuristic somewhere?
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

    def max_shell(self, balance):
        best = 0
        for x in range(1, 1000):
            if self.game.getShellCost(x) > balance:
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


