ACCEL_LOW_FLOOR = 5
FLOOR = 5

# The turn-based decay on prices seems v strong
# this car attempts to exploit that
class TurnOptimizer3:
    def takeYourTurn(self, game, cars, bananas, idx):
        ourCar = cars[idx]
        self.cars = cars
        self.idx = idx
        self.game = game
        self.bananas = bananas
        turns_to_win = (1000 - ourCar.y) // ourCar.speed if ourCar.speed > 0 else 1000
        (turns_to_lose, best_opponent_idx) = self.turns_to_lose_optimistic()

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
        elif turns_to_lose < 6:
            self.stop_opponent(best_opponent_idx, int(1000 / turns_to_lose))

        # if idx == 0:
        #     max_accel_cost = 100000 if turns_to_lose == 0 else int(5000 / turns_to_lose) if turns_to_lose < 6 else 10 + int(1000 / turns_to_lose)
        #     self.try_lower_turns_to_win(turns_to_win, max_accel_cost)
        # else:
        #     if turns_to_lose == 0:
        #         # div/0
        #         turns_to_lose = 1
        #
        #     distance_from_opponent = cars[best_opponent_idx].y - ourCar.y
        #     # turns_to_lose 30
        #     # distance_from_opponent 300
        #
        #     # super fucked
        #     if turns_to_lose < 3 and distance_from_opponent > turns_to_lose * 20:
        #         # accel more
        #         self.try_lower_turns_to_win(turns_to_win, 10000)
        #     # kinda fucked
        #     elif turns_to_lose < 6 and distance_from_opponent > turns_to_lose * 10:
        #         self.try_lower_turns_to_win(turns_to_win, int(7000 / turns_to_lose))
        #     # kinda fucked, midgame
        #     elif turns_to_lose < 20 and distance_from_opponent > turns_to_lose * 10:
        #         self.try_lower_turns_to_win(turns_to_win, int(distance_from_opponent * 10 / turns_to_lose))
        #     # fine
        #     else:
        #         # accel less
        #         self.try_lower_turns_to_win(turns_to_win, 10 + int(1000 / turns_to_lose))
        #
        max_accel_cost = 100000 if turns_to_lose == 0 else int(5000 / turns_to_lose) if turns_to_lose < 6 else 10 + int(1000 / turns_to_lose)
        self.try_lower_turns_to_win(turns_to_win, max_accel_cost)


        # kill bananas in our way
        # were in front, theres no nanners
        # TODO: if theres bananas and too spendy to kill maybe dont accel
        if idx != 0 and turns_to_lose > 0:
            # cost of n shells to cost of super
            # get the bananas b/t us and next car
            # compare our accel and not kill ones too far ahead (like we wont even hit them)
            opponent_y = cars[best_opponent_idx].y
            our_y_in_3 = ourCar.y + (ourCar.speed * 3)
            max_dist = min(opponent_y, our_y_in_3)
            bananas_to_kill = self.bananas_between_max_dist(max_dist)
            super_cost = game.getSuperShellCost(1)
            shell_cost = game.getShellCost(bananas_to_kill + 1)
            max_cost = 20 if turns_to_lose > 10 else 500 // turns_to_lose
            if super_cost < shell_cost and super_cost < max_cost:
                self.superShell(1)
            elif shell_cost < super_cost and shell_cost < max_cost:
                self.shell(bananas_to_kill)

        # literally so cheap why not
        if game.getShellCost(1) < FLOOR:
            self.shell(1)
        if game.getSuperShellCost(1) < FLOOR:
            self.superShell(1)
        if game.getBananaCost() < FLOOR:
            self.banana()
        if game.getShieldCost(1) < FLOOR:
            self.shield(1)

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

    def accel_to_floor(self):
        (turns_to_lose, _) = self.turns_to_lose()
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

            if self.cars[opponent_idx].shield > 0 and super_cost < max_cost:
                self.superShell(1)
                return

            # enough shells to kill all bananas and stop them
            shell_amt = self.bananas_between(opponent_idx) + 1
            shell_cost = self.game.getShellCost(shell_amt)
            if super_cost > max_cost and shell_cost > max_cost:
                return

            if super_cost <= shell_cost:
                self.superShell(1)
            else:
                self.shell(shell_amt)
            self.bananas = []
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

    def bananas_between_max_dist(self, max_dist=1000):
        our_y = self.cars[self.idx].y
        count = 0
        for b in self.bananas:
            if b >= our_y and b <= max_dist:
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
            car.speed += amount
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


