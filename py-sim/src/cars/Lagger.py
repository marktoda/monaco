

class Lagger:
    def takeYourTurn(self, game, cars, bananas, idx):
        ourCar = cars[idx]
        self.cars = cars
        self.idx = idx
        self.game = game
        self.bananas = bananas
        turns_to_win = (1000 - ourCar.y) // ourCar.speed if ourCar.speed > 0 else 1000
        # (turns_to_lose, best_opponent_idx) = self.turns_to_lose_optimistic()

        if self.idx == 0 or self.idx == 1 or self.game.turns < 5:
            # we're in front we need to slow down
            # beginning of the game or we are in first
            
            return
        
        # just try to match the car in front of us
        otherCar = self.cars[1]
        if ourCar.speed > otherCar.speed:
            # just shell
            self.shell(self.max_shell(1000))
        else:
            # calculate accel to max speed 
            max_cost = 1000
            # accel_in_one_turn = otherCar.y - ourCar.y
            turns_to_next_car = (otherCar.y - ourCar.y) // ourCar.speed if ourCar.speed > 0 else 1
            self.try_lower_turns_to_win(turns_to_next_car, max_cost, otherCar)
    
    def try_lower_turns_to_win(self, turns_to_win, max_accel_cost, otherCar):
        our_car = self.cars[self.idx]
        max_accel_possible = self.max_accel(min(our_car.balance, max_accel_cost))
        if max_accel_possible == 0:
            return

        new_turns_to_win = (otherCar.y - our_car.y) // (our_car.speed + max_accel_possible)
        # no amount of accel will help us
        if new_turns_to_win == turns_to_win:
            return turns_to_win

        # now iterate down and see the least speed that still gets the same accel possible
        least_accel = max_accel_possible
        for accel in range(max_accel_possible - 1, 0, -1):
            ttw = (otherCar.y - our_car.y) // (our_car.speed + accel)
            if ttw > new_turns_to_win:
                least_accel = accel + 1
                break

        self.accelerate(least_accel)

            
            
            
        
            



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
        
