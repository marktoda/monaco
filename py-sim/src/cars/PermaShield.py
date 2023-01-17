class PermaShield:
    def takeYourTurn(self, game, cars, bananas, idx):
        if game.getShieldCost(1) < 500:
            game.buyShield(1)
        if game.getAccelerateCost(1) < 800:
            game.buyAcceleration(1)
        if cars[idx].speed == 0:
            game.buyAcceleration(1)

