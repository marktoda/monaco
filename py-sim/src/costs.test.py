import unittest
import monaco

class CostTest(unittest.TestCase):
    def test_acceleration(self):
        game = monaco.Game()
        self.assertEqual(game.getAccelerationCost(1), 12)
        self.assertEqual(game.getAccelerationCost(2), 26)
        self.assertEqual(game.getAccelerationCost(3), 44)
        self.assertEqual(game.getAccelerationCost(4), 66)
        self.assertEqual(game.getAccelerationCost(5), 93)
        self.assertEqual(game.getAccelerationCost(6), 126)
        self.assertEqual(game.getAccelerationCost(7), 166)
        self.assertEqual(game.getAccelerationCost(8), 215)
        self.assertEqual(game.getAccelerationCost(9), 275)
        self.assertEqual(game.getAccelerationCost(10), 349)
        self.assertEqual(game.getAccelerationCost(11), 439)
        self.assertEqual(game.getAccelerationCost(12), 549)

    def test_shell(self):
        game = monaco.Game()
        self.assertEqual(game.getShellCost(1), 1481)
        self.assertEqual(game.getShellCost(2), 12452)
        self.assertEqual(game.getShellCost(3), 93717)
        self.assertEqual(game.getShellCost(4), 695630)
        self.assertEqual(game.getShellCost(5), 5153833)
        self.assertEqual(game.getShellCost(6), 38174505)
        self.assertEqual(game.getShellCost(7), 282749414)

    def test_super_shell(self):
        game = monaco.Game()
        self.assertEqual(game.getSuperShellCost(1), 2585)
        self.assertEqual(game.getSuperShellCost(2), 24868)
        self.assertEqual(game.getSuperShellCost(3), 216920)
        self.assertEqual(game.getSuperShellCost(4), 1872133)

    def test_banana(self):
        game = monaco.Game()
        self.assertEqual(game.getBananaCost(), 1481)

    def test_shield(self):
        game = monaco.Game()
        self.assertEqual(game.getShieldCost(1), 1111)
        self.assertEqual(game.getShieldCost(2), 9339)
        self.assertEqual(game.getShieldCost(3), 70288)
        self.assertEqual(game.getShieldCost(4), 521722)

if __name__ == '__main__':
    unittest.main()
