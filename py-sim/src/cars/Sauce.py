MID_GAME = 400
LATE_GAME = 600
FLAT_OUT = 800
ACCEL_FLOOR = 10


def hasEnoughBalance(car, cost):
    return car.balance > cost

def updateBalance(car, cost):
    car.balance -= cost

class CarData:
    balance = 0
    speed = 0
    y = 0
    shield = 0

class Sauce:
    def buyAsMuchAccelerationAsSensible(self, game, car, idx):
        baseCost = 25
        speed = car.speed
        y = car.y
        speedBoost = 5 if speed < 5 else 3 if speed < 10 else 2 if speed < 15 else 1
        yBoost = 1 if y < 100 else 2 if y < 250 else 3 if y < 500 else 4 if y < 750 else 5 if y < 950 else 10
        costCurve = baseCost * speedBoost * yBoost
        speedCurve = 8 * ((y + 500) // 300)
        while hasEnoughBalance(car, game.getAccelerateCost(1)) and game.getAccelerateCost(1) < costCurve and car.speed < speedCurve:
            updateBalance(car, game.buyAcceleration(1))

    def buyAsMuchAccelerationAsPossible(self, game, car, idx):
        while hasEnoughBalance(car, game.getAccelerateCost(1)):
            updateBalance(car, game.buyAcceleration(1))

    def buy1ShellIfPriceIsGood(self, game, car, idx):
        if game.getShellCost(1) < 1500 and hasEnoughBalance(car, game.getShellCost(1) + 500):
            updateBalance(car, game.buyShell(1))

    def buy1ShellIfSensible(self, game, car, idx, speedOfNextCarAhead):
        if speedOfNextCarAhead < 5:
            return
        costCurve = 500 * ((car.y + 1000) // 500) * ((speedOfNextCarAhead + 5) // 5)
        if game.getShellCost(1) < costCurve and hasEnoughBalance(car, game.getShellCost(1)):
            updateBalance(car, game.buyShell(1))

    def buy1ShellWhateverThePrice(self, game, car, idx):
        if hasEnoughBalance(car, game.getShellCost(1)):
            updateBalance(car, game.buyShell(1))

    def takeYourTurn(self, game, cars, bananas, idx):
        ourCar = cars[idx]
        leadCar = CarData()
        lagCar = CarData()
        if idx == 0:
            lagCar = cars[1]
        elif idx == 1:
            leadCar = cars[0]
            lagCar = cars[2]
        else:
            leadCar = cars[1]

        speedDelta = leadCar.speed - ourCar.speed if ourCar.speed < leadCar.speed else ourCar.speed - leadCar.speed
        leadDistance = leadCar.y - ourCar.y if ourCar.y < leadCar.y else ourCar.y - leadCar.y

        action = {
            "accelerate": 0,
            "shell": 0,
            "superShell": 0,
            "shield": 0,
        }

        if game.getAccelerateCost(1) < ACCEL_FLOOR:
            action["accelerate"] += 1

        point = (cars[0].y + cars[1].y) // 2
        if point < MID_GAME:
            if ourCar.speed == 0:
                action["accelerate"] += 1
            if idx != 0 and speedDelta > 5:
                action["accelerate"] += 1
            # if idx == 2 and cars[0].speed < 5:
            #     action["superShell"] += 1
        elif MID_GAME <= point and point < LATE_GAME:
            if idx == 2:
                action["accelerate"] += 1
                if 100 < leadDistance:
                    action["shell"] += 1
                # if cars[0].speed < 5:
                #     action["superShell"] += 1
        elif LATE_GAME <= point and point < FLAT_OUT:
            action["shell"] += 1
        else:
            action["shield"] += 1
            self.buyAsMuchAccelerationAsSensible(game, ourCar, idx)

        if action["accelerate"] != 0 and hasEnoughBalance(ourCar, game.getAccelerateCost(action["accelerate"])):
            updateBalance(ourCar, game.buyAcceleration(action["accelerate"]))
        if action["shell"] != 0:
            if idx != 0 and 0 < leadCar.shield:
                action["shell"] += 1
            if hasEnoughBalance(ourCar, game.getShellCost(action["shell"])):
                updateBalance(ourCar, game.buyShell(action["shell"]))
        if action["shield"] != 0:
            if hasEnoughBalance(ourCar, game.getShieldCost(action["shield"])):
                updateBalance(ourCar, game.buyShield(action["shield"]))
        if action["superShell"] != 0:
            if hasEnoughBalance(ourCar, game.getSuperShellCost(action["superShell"])):
                updateBalance(ourCar, game.buySuperShell(action["superShell"]))


