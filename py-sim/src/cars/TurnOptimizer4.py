ACCEL_LOW_FLOOR = 5
FLOOR = 5

# The turn-based decay on prices seems v strong
# this car attempts to exploit that
class TurnOptimizer4:
    def __init__(self):
        self.prev_idx = 0
        self.turns_in_second = 0
        self.prev_speed = 0
        self.shelled_count = 0
        self.chilling = False

    def takeYourTurn(self, game, cars, bananas, idx):
        ourCar = cars[idx]
        self.cars = cars
        self.idx = idx
        self.game = game
        self.bananas = bananas

        if idx == 1 and self.prev_idx == 1:
            self.turns_in_second += 1
        elif idx == 1:
            self.turns_in_second = 1
        else:
            self.turns_in_second = 0

        if self.prev_speed > 1 and ourCar.speed == 1:
            self.shelled_count += 1

        turns_to_win = (1000 - ourCar.y) // ourCar.speed if ourCar.speed > 0 else 1000
        (turns_to_lose, best_opponent_idx) = self.turns_to_lose_optimistic()
        if turns_to_lose < 5:
            (turns_to_lose, best_opponent_idx) = self.turns_to_lose()

        # no need to accelerate, were about to win
        # just shell everyone
        if turns_to_win == 0:
            if not self.superShell(1):
                self.shell(self.max_shell(ourCar.balance))
            return

        # if we can buy enough acceleration to win right away, do it
        accel_to_win = (1000 - ourCar.y) - ourCar.speed
        if self.max_accel(ourCar.balance) >= accel_to_win:
            self.accelerate(accel_to_win)
            self.stop_opponent(best_opponent_idx)
            self.accelerate(self.max_accel(ourCar.balance))
            return

        # ACCEL DECISION MAKING
        # someone else is about to win
        if turns_to_lose < 1:
            self.stop_opponent(best_opponent_idx, 10000)
        elif turns_to_lose < 2:
            self.stop_opponent(best_opponent_idx, 5000)
        elif turns_to_lose < 3:
            self.stop_opponent(best_opponent_idx, 3000)
        elif turns_to_lose < 4:
            self.stop_opponent(best_opponent_idx, 2000)
        elif turns_to_lose < 6:
            self.stop_opponent(best_opponent_idx, int(1000 / turns_to_lose))
        elif turns_to_lose < 10:
            self.stop_opponent(best_opponent_idx, int(500 / turns_to_lose))

        # accel logic
        # - chill if were in front of a shelloor
        # - else optimize ttw
        if turns_to_lose > 10 and self.chilling:
            if idx == 2:
                # match speed
                target_speed = cars[1].speed
                max_accel = max(0, target_speed - ourCar.speed)
                if max_accel != 0:
                    self.accel_to_max(max_accel, int(4000 / turns_to_lose))
                pass
            else:
                # we need to sit and wait for the shelloorr to pass us
                pass
            return
        elif turns_to_lose > 10 and self.turns_in_second > 1 and self.shelled_count > 1 and not self.chilling:
            # no accelerate cuz its a waste
            # shell or super shell if cheap
            self.stop_opponent(best_opponent_idx, int(2000 / turns_to_lose))
            self.chilling = True
            return
        elif turns_to_lose > 3 and turns_to_lose < 10 and idx == 1:
            # sneak into close second
            target_speed = cars[0].speed
            max_accel = max(0, target_speed - ourCar.speed)
            if max_accel != 0:
                self.accel_to_max(max_accel, int(2000 / turns_to_lose))
        else:
            max_accel_cost = 100000 if turns_to_lose == 0 else int(5000 / turns_to_lose) if turns_to_lose < 6 else 10 + int(1000 / turns_to_lose)
            self.try_lower_turns_to_win(turns_to_win, max_accel_cost)

        # literally so cheap why not
        if game.getShellCost(1) < FLOOR:
            self.shell(1)
        if game.getSuperShellCost(1) < FLOOR:
            self.superShell(1)
        if game.getBananaCost() < FLOOR:
            self.banana()
        if game.getShieldCost(1) < FLOOR:
            self.shield(1)

        self.prev_idx = idx
        self.prev_speed = ourCar.speed

    def try_lower_turns_to_win(self, turns_to_win, max_accel_cost):
        our_car = self.cars[self.idx]
        max_accel_possible = self.max_accel(min(our_car.balance, max_accel_cost))
        if max_accel_possible == 0:
            return

        new_turns_to_win = (1000 - our_car.y) // (our_car.speed + max_accel_possible)
        # no amount of accel will help us
        if new_turns_to_win == turns_to_win:
            return turns_to_win

        # now iterate down and see the least speed that still gets the same accel possible
        least_accel = max_accel_possible
        for accel in range(max_accel_possible - 1, 0, -1):
            ttw = (1000 - our_car.y) // (our_car.speed + accel)
            if ttw > new_turns_to_win:
                least_accel = accel + 1
                break

        self.accelerate(least_accel)

    def accel_to_max(self, max_speed, max_cost):
        if self.game.getAccelerateCost(max_speed) < max_cost:
            return self.accelerate(max_speed)

        # else iterate until at max cost
        total_spent = self.game.getAccelerateCost(1)
        total_speed = 0
        while total_spent < max_cost and total_speed < max_speed:
            if not self.accelerate(1):
                return
            total_spent += self.game.getAccelerateCost(1)
            total_speed += 1

    def stop_opponent(self, opponent_idx, max_cost=10000):
        opponent_car = self.cars[opponent_idx]
        # if y equals, bananas and shells are pointless
        if opponent_car.y == self.cars[self.idx].y:
            return False

        if opponent_idx < self.idx:
            # no point shelling
            if opponent_car.speed == 1:
                return False

            super_cost = self.game.getSuperShellCost(1)

            if opponent_car.shield > 0 and super_cost < max_cost:
                return self.superShell(1)

            # enough shells to kill all bananas and stop them
            shell_amt = self.bananas_between(opponent_idx) + 1
            shell_cost = self.game.getShellCost(shell_amt)
            if super_cost > max_cost and shell_cost > max_cost:
                return False

            if super_cost <= shell_cost:
                return self.superShell(1)
            else:
                return self.shell(shell_amt)
        elif self.game.getBananaCost() < max_cost:
            return self.banana()
        return False

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


    # Instead of assuming all money goes to acceleration, assume 60% goes to acceleration, 40% to defense
    def turns_to_lose_optimistic(self):
        worst = 1000
        worst_idx = 0
        for i, car in enumerate(self.cars):
            if i is not self.idx:
                # end-game, assume oppo more likely to use full balance
                assumed_speed = car.speed + self.max_accel(0.6*car.balance)
                turns_to_win = (1000 - car.y) // assumed_speed if assumed_speed > 0 else 1000
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
        return best

    def max_shell(self, balance):
        best = 0
        for x in range(1, 1000):
            if self.game.getShellCost(x) > balance:
                return best
            best = x

    def accelerate(self, amount):
        if amount == 0:
            return

        car = self.cars[self.idx]
        if car.balance > self.game.getAccelerateCost(amount):
            car.balance -= self.game.buyAcceleration(amount)
            return True
        return False

    def shell(self, amount):
        if amount == 0:
            return

        car = self.cars[self.idx]
        if car.balance > self.game.getShellCost(amount):
            car.balance -= self.game.buyShell(amount)
            return True
        return False

    def superShell(self, amount):
        if amount == 0:
            return

        car = self.cars[self.idx]
        if car.balance > self.game.getSuperShellCost(amount):
            car.balance -= self.game.buySuperShell(amount)
            return True
        return False

    def shield(self, amount):
        if amount == 0:
            return

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


