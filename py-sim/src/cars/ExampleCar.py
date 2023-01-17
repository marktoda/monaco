class ExampleCar:
    def takeYourTurn(self, game, cars, bananas, idx):
        ourCar = cars[idx]
        # If we can afford to accelerate 3 times, let's do it.
        if ourCar.balance > game.getAccelerateCost(3):
            ourCar.balance -= game.buyAcceleration(3)

        if idx + 1 == len(cars) and ourCar.balance > game.getSuperShellCost(1):
            # If we are the last and we can afford it, shell everyone.
            game.buySuperShell(1) # This will instantly set every car in front of us' speed to 1.
        elif idx != 0 and cars[idx - 1].speed > ourCar.speed and ourCar.balance > game.getShellCost(1):
            # If we're not in the lead (index 0) + the car ahead of us is going faster + we can afford a shell, smoke em.
            game.buyShell(1) # This will instantly set the car in front of us' speed to 1.
        elif ourCar.shield == 0:
            # If we are in the lead, are not shielded and we can afford to shield ourselves, just do it.
            if idx == 0 and ourCar.balance > game.getShieldCost(2):
                game.buyShield(2)

