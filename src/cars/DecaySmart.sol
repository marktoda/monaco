// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "./../interfaces/ICar.sol";

contract DecaySmart is ICar {
    uint256 constant FLOOR = 5;


    function takeYourTurn(
        Monaco monaco,
        Monaco.CarData[] calldata allCars,
        uint256[] calldata /*bananas*/,
        uint256 ourCarIndex
    ) external override {
        Monaco.CarData memory ourCar = allCars[ourCarIndex];
        uint256 turnsToWin = ourCar.speed == 0 ? 1000 : (1000 - ourCar.y) / ourCar.speed;
        (uint256 turnsToLose, uint256 bestOpponentIdx) = getTurnsToLose(monaco, allCars, ourCarIndex);

        // were about to win this turn, no need to accelerate
        // just shell everyone
        if (turnsToWin == 0) {
            if (!superShell(monaco, ourCar, 1)) {
                shell(monaco, ourCar, maxShell(monaco, ourCar.balance));
            }
            return;
        }

        // if we can buy enough acceleration to win right away, do it
        uint256 accelToWin = (1000 - ourCar.y) - ourCar.speed;
        if (maxAccel(monaco, ourCar.balance) >= accelToWin) {
            accelerate(monaco, ourCar, accelToWin);
            // stopOpponent
            accelerate(monaco, ourCar, maxAccel(monaco, ourCar.balance));
        }

        // ACCEL DECISION MAKING
        if (turnsToLose == 0) {
            stopOpponent(monaco, allCars, ourCarIndex, bestOpponentIdx, 10000);
            accelerate(monaco, ourCar, maxAccel(monaco, ourCar.balance));
            // avoid div/0
            turnsToLose = 1;
        } else if (turnsToLose < 5) {
            stopOpponent(monaco, allCars, ourCarIndex, bestOpponentIdx, 200);
            accelerate(monaco, ourCar, 20 / turnsToLose);
        } else {
            accelToFloor(monaco, ourCar, turnsToLose);
        }


        // so cheap, why not
        if (monaco.getShellCost(1) < FLOOR) {
            shell(monaco, ourCar, 1);
        }
        if (monaco.getSuperShellCost(1) < FLOOR) {
            superShell(monaco, ourCar, 1);
        }
        if (monaco.getShieldCost(1) < FLOOR) {
            shield(monaco, ourCar, 1);
        }
        if (monaco.getBananaCost() < FLOOR) {
            banana(monaco, ourCar);
        }

    }

    function accelToFloor(Monaco monaco, Monaco.CarData memory ourCar, uint256 turnsToLose) internal {
        uint256 floor = 5 + (500 / turnsToLose);
        while (monaco.getAccelerateCost(1) < floor) {
            if (!accelerate(monaco, ourCar, 1)) {
                return;
            }
        }
    }

    function stopOpponent(Monaco monaco, Monaco.CarData[] calldata allCars, uint256 ourCarIdx, uint256 opponentIdx, uint256 maxCost) internal {
        // in front, so use shells
        if (opponentIdx < ourCarIdx) {
            // theyre already slow so no point shelling
            if (allCars[opponentIdx].speed == 1) {
                return;
            }

            uint256 superCost = monaco.getSuperShellCost(1);
            if (!superShell(monaco, allCars[ourCarIdx], 1)) {
                // TODO: try to send enough shells to kill all bananas and the oppo
                shell(monaco, allCars[ourCarIdx], 1);
            }
        } else if (monaco.getBananaCost() < maxCost) {
            // behind so banana
            banana(monaco, allCars[ourCarIdx]);
        }
    }

    function getTurnsToLose(Monaco monaco, Monaco.CarData[] calldata allCars, uint256 ourCarIndex) internal returns (uint256 turnsToLose, uint256 bestOpponentIdx) {
        turnsToLose = 1000;
        for (uint256 i = 0; i < allCars.length; i++) {
            if (i != ourCarIndex) {
                Monaco.CarData memory car = allCars[i];
                uint256 maxSpeed = car.speed + maxAccel(monaco, car.balance);
                uint256 turns = car.speed == 0 ? 1000 : (1000 - car.y) / maxSpeed;
                if (turns < turnsToLose) {
                    turnsToLose = turns;
                    bestOpponentIdx = i;
                }
            }
        }
    }

    function maxAccel(Monaco monaco, uint256 balance) internal view returns (uint256 amount) {
        uint256 current = 25;
        uint256 min = 0;
        uint256 max = 50;
        while (max - min > 1) {
            uint256 cost = monaco.getAccelerateCost(current);
            if (cost > balance) {
                max = current;
            } else if (cost < balance) {
                min = current;
            } else {
                return current;
            }
            current = (max + min) / 2;
        }
        return min;

    }

    function maxShell(Monaco monaco, uint256 balance) internal view returns (uint256 amount) {
        uint256 best = 0;
        for (uint256 i = 1; i < 1000; i++) {
            if (monaco.getShellCost(i) > balance) {
                return best;
            }
            best = i;
        }
    }

    function accelerate(Monaco monaco, Monaco.CarData memory ourCar, uint256 amount) internal returns (bool success) {
        if (ourCar.balance > monaco.getAccelerateCost(amount)) {
            ourCar.balance -= uint32(monaco.buyAcceleration(amount));
            return true;
        }
        return false;
    }

    function shell(Monaco monaco, Monaco.CarData memory ourCar, uint256 amount) internal returns (bool success) {
        if (ourCar.balance > monaco.getShellCost(amount)) {
            ourCar.balance -= uint32(monaco.buyShell(amount));
            return true;
        }
        return false;
    }

    function superShell(Monaco monaco, Monaco.CarData memory ourCar, uint256 amount) internal returns (bool success) {
        if (ourCar.balance > monaco.getSuperShellCost(amount)) {
            ourCar.balance -= uint32(monaco.buySuperShell(amount));
            return true;
        }
        return false;
    }

    function shield(Monaco monaco, Monaco.CarData memory ourCar, uint256 amount) internal returns (bool success) {
        if (ourCar.balance > monaco.getShieldCost(amount)) {
            ourCar.balance -= uint32(monaco.buyShield(amount));
            return true;
        }
        return false;
    }

    function banana(Monaco monaco, Monaco.CarData memory ourCar) internal returns (bool success) {
        if (ourCar.balance > monaco.getBananaCost()) {
            ourCar.balance -= uint32(monaco.buyBanana());
            return true;
        }
        return false;
    }

    function sayMyName() external pure returns (string memory) {
        return "DN";
    }
}
