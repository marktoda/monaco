ACCEL_FLOOR = 15
SHELL_FLOOR = 200
SUPER_SHELL_FLOOR = 300
SHIELD_FLOOR = 400

class Floor:
    def takeYourTurn(self, game, cars, bananas, idx):
        if game.getAccelerateCost(1) < ACCEL_FLOOR:
            game.buyAcceleration(1)
        if game.getShellCost(1) < SHELL_FLOOR:
            game.buyShell(1)
        if idx == 2 and game.getSuperShellCost(1) < SUPER_SHELL_FLOOR:
            game.buySuperShell(1)
        if idx != 2 and game.getShieldCost(1) < SHIELD_FLOOR:
            game.buyShield(1)

