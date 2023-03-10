import unittest
import monaco

class OverflowBalanceTest:
    overflow = False

    def setOverflow(self, set):
        self.overflow = set

    def takeYourTurn(self, game, cars, bananas, idx):
        game.buyShell(1)
        if self.overflow:
            game.buyAcceleration(10000000000)

class ActionsTest(unittest.TestCase):
    def testShell(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.cars[0][1].balance = 15000
        game.cars[0][1].speed = 100
        game.cars[0][1].shield = 0
        game.cars[0][1].y = 200

        game.currentCarIndex = 1
        game.buyShell(1)
        self.assertEqual(game.cars[0][1].speed, 1)
        self.assertEqual(game.cars[0][1].y, 200)
        self.assertEqual(game.cars[1][1].balance, 16019)

    def testBalanceUnderflow(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.cars[0][1].balance = 15000
        game.cars[0][1].speed = 100
        game.cars[0][1].shield = 0
        game.cars[0][1].y = 200

        game.currentCarIndex = 1
        with self.assertRaises(Exception):
            game.buyShell(10)

    def testAccelerate(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.currentCarIndex = 0
        game.buyAcceleration(1)
        game.currentCarIndex = 1
        game.buyAcceleration(5)
        game.currentCarIndex = 2
        game.buyAcceleration(15)

        self.assertEqual(game.cars[0][1].speed, 1)
        self.assertEqual(game.cars[0][1].y, 0)
        self.assertEqual(game.cars[0][1].balance, 17488)
        self.assertEqual(game.cars[1][1].speed, 5)
        self.assertEqual(game.cars[1][1].y, 0)
        self.assertEqual(game.cars[2][1].speed, 15)
        self.assertEqual(game.cars[2][1].y, 0)

        game.play(1)
        self.assertEqual(game.cars[0][1].y, 1)
        self.assertEqual(game.cars[1][1].y, 5)
        self.assertEqual(game.cars[2][1].y, 15)

    def testShield(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        # set car 0 ahead of car 1
        game.cars[0][1].y = 200
        game.cars[0][1].speed = 100
        game.cars[1][1].y = 0
        game.cars[1][1].speed = 100

        # the front car buys a shield
        game.currentCarIndex = 0
        game.buyShield(1)
        # the behind car buys a shell
        game.currentCarIndex = 1
        game.buyShell(1)
        self.assertEqual(game.cars[0][1].speed, 100)

    def testShieldDuration(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.play(18)

        game.currentCarIndex = 0
        game.buyShield(3)
        for i in range(4):
            game.play(1)
            self.assertEqual(game.cars[0][1].shield, 3 - i)
        self.assertEqual(game.cars[0][1].shield, 0)

    def testSuperShell(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        # position 2 cars ahead
        game.cars[1][1].speed = 100
        game.cars[1][1].y = 200
        game.cars[2][1].speed = 200
        game.cars[2][1].y = 500
        game.cars[0][1].speed = 200
        game.cars[0][1].y = 0

        game.currentCarIndex = 0
        game.buySuperShell(1)
        self.assertEqual(game.cars[0][1].speed, 200)
        self.assertEqual(game.cars[1][1].speed, 1)
        self.assertEqual(game.cars[2][1].speed, 1)

    def testSuperShellIgnoresShield(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        # position 2 cars ahead
        game.cars[1][1].speed = 100
        game.cars[1][1].y = 200
        game.cars[2][1].speed = 200
        game.cars[2][1].y = 500
        game.cars[0][1].speed = 200
        game.cars[0][1].y = 0

        game.currentCarIndex = 1
        game.buyShield(1)
        game.currentCarIndex = 0
        game.buySuperShell(1)
        self.assertEqual(game.cars[0][1].speed, 200)
        self.assertEqual(game.cars[1][1].speed, 1)
        self.assertEqual(game.cars[2][1].speed, 1)

    def testBanana(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        # position 1 cars ahead
        game.cars[1][1].speed = 200
        game.cars[1][1].y = 100

        game.currentCarIndex = 1
        game.buyBanana()
        self.assertEqual(len(game.bananas), 1)
        self.assertEqual(game.bananas[0], 100)

    def testBananaCollision(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        bananaPos = 100

        game.cars[1][1].speed = 0
        game.cars[1][1].y = bananaPos
        game.cars[2][1].speed = 60
        game.cars[2][1].y = 0
        game.currentCarIndex = 1
        game.buyBanana()

        game.play(1)
        self.assertEqual(game.bananas[0], bananaPos)
        self.assertEqual(len(game.bananas), 1)
        game.play(1)
        # banana collision for car 2
        self.assertEqual(game.cars[2][1].speed, 30)
        self.assertEqual(game.cars[2][1].y, bananaPos)
        # banana is now gone
        self.assertEqual(len(game.bananas), 0)

    def testBananaMultipleCollision(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        banana1Pos = 100
        banana2Pos = 110
        banana3Pos = 120
        game.bananas.append(banana1Pos)
        game.bananas.append(banana2Pos)
        game.bananas.append(banana3Pos)

        game.cars[1][1].speed = 100
        game.cars[1][1].y = 50

        game.play(1)
        self.assertEqual(game.cars[1][1].y, banana1Pos)
        game.play(1)
        self.assertEqual(game.cars[1][1].y, banana2Pos)
        game.play(1)
        self.assertEqual(game.cars[1][1].y, banana3Pos)
        self.assertEqual(len(game.bananas), 0)
        self.assertEqual(game.cars[1][1].speed, 12)

    def testShellBanana(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        car1Position = 100
        game.bananas.append(car1Position)
        game.cars[0][1].speed = 100
        game.cars[0][1].y = car1Position
        car2Position = 50
        game.cars[1][1].speed = 100
        game.cars[1][1].y = car2Position

        # behind car buys shell which should kill the banana
        game.currentCarIndex = 1
        game.buyShell(1)
        game.play(1)

        # no more banana
        self.assertEqual(len(game.bananas), 0)
        # car 1 unaffected by the shell
        self.assertEqual(game.cars[0][1].speed, 100)
        self.assertEqual(game.cars[0][1].y, car1Position + 100)
        # car 2 unaffected by the banana
        self.assertEqual(game.cars[1][1].speed, 100)
        self.assertEqual(game.cars[1][1].y, car2Position + 100)

    def testShellMultipleBananas(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        car1Position = 100
        game.bananas.append(car1Position)
        game.bananas.append(car1Position - 1)
        game.bananas.append(car1Position - 2)
        game.cars[0][1].speed = 100
        game.cars[0][1].y = car1Position
        car2Position = 0
        game.cars[1][1].speed = 50
        game.cars[1][1].y = car2Position

        # behind car buys shell which should kill the banana
        self.assertEqual(len(game.bananas), 3)
        game.currentCarIndex = 1
        game.buyShell(1)
        game.play(1)

        # no more banana
        self.assertEqual(len(game.bananas), 2)
        # car 1 unaffected by the shell
        self.assertEqual(game.cars[0][1].speed, 100)
        self.assertEqual(game.cars[0][1].y, car1Position + 100)
        # car 2 unaffected by the banana
        self.assertEqual(game.cars[1][1].speed, 50)
        self.assertEqual(game.cars[1][1].y, car2Position + 50)


    def testSuperShellBanana(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.bananas.append(15)
        game.bananas.append(14)
        game.bananas.append(13)
        game.bananas.append(12)
        game.bananas.append(11)
        game.bananas.append(10)

        game.cars[1][1].speed = 100
        game.cars[1][1].y = 0
        game.cars[0][1].speed = 100
        game.cars[0][1].y = 20

        self.assertEqual(len(game.bananas), 6)
        game.currentCarIndex = 1
        game.buySuperShell(1)
        # should kill all bananas
        self.assertEqual(len(game.bananas), 0)
        self.assertEqual(game.cars[1][1].speed, 100)
        self.assertEqual(game.cars[0][1].speed, 1)

    def testSuperShellBananaPartial(self):
        game = monaco.Game()
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        game.bananas.append(15)
        game.bananas.append(14)
        game.bananas.append(13)
        game.bananas.append(12)
        game.bananas.append(11)
        game.bananas.append(10)

        game.cars[1][1].speed = 100
        game.cars[1][1].y = 12
        game.cars[0][1].speed = 100
        game.cars[0][1].y = 20

        self.assertEqual(len(game.bananas), 6)
        game.currentCarIndex = 1
        game.buySuperShell(1)
        # should kill all bananas
        self.assertEqual(len(game.bananas), 3)
        self.assertEqual(game.bananas[0], 10)
        self.assertEqual(game.bananas[1], 11)
        self.assertEqual(game.bananas[2], 12)
        self.assertEqual(game.cars[1][1].speed, 100)
        self.assertEqual(game.cars[0][1].speed, 1)

    def testRevert(self):
        game = monaco.Game()
        car = OverflowBalanceTest()
        game.register(car)
        game.register(monaco.MockCar())
        game.register(monaco.MockCar())
        car.setOverflow(True)
        game.play(3)
        self.assertEqual(game.actionsSold[monaco.ActionType.ACCELERATE], 0)
        self.assertEqual(game.actionsSold[monaco.ActionType.SHELL], 0)
        game.play(3)
        self.assertEqual(game.actionsSold[monaco.ActionType.ACCELERATE], 0)
        self.assertEqual(game.actionsSold[monaco.ActionType.SHELL], 0)
        car.setOverflow(False)
        game.play(3)
        self.assertEqual(game.actionsSold[monaco.ActionType.ACCELERATE], 0)
        self.assertEqual(game.actionsSold[monaco.ActionType.SHELL], 1)


if __name__ == '__main__':
    unittest.main()
