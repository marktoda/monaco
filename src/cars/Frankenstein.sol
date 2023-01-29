// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "./../interfaces/ICar.sol";

// accelerates to optimize turns-to-win
contract Frankenstein is ICar {
    uint256 constant FLOOR = 5;
    uint256 private prevIdx;
    uint256 private prevSpeed;
    uint256 private turnsInSecond;
    uint256 private shelledCount;
    bool private chilling;

    function takeYourTurn(
        Monaco monaco,
        Monaco.CarData[] calldata allCars,
        uint256[] calldata /*bananas*/,
        uint256 ourCarIndex
    ) external override {
        Monaco.CarData memory ourCar = allCars[ourCarIndex];
        if (ourCarIndex == 1 && prevIdx == 1) {
            turnsInSecond++;
        } else if (ourCarIndex == 1) {
            turnsInSecond = 1;
        } else {
            turnsInSecond = 0;
        }

        if (prevSpeed > 1 && ourCar.speed == 1) {
            shelledCount++;
        }

        uint256 turnsToWin = ourCar.speed == 0 ? 1000 : (1000 - ourCar.y) / ourCar.speed;
        (uint256 turnsToLose, uint256 bestOpponentIdx) = getTurnsToLoseOptimistic(monaco, allCars, ourCarIndex);

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
            stopOpponent(monaco, allCars, ourCar, ourCarIndex, bestOpponentIdx, 100000);
            accelerate(monaco, ourCar, maxAccel(monaco, ourCar.balance));
            return;
        }

        // ACCEL DECISION MAKING
        if (turnsToLose < 1) {
            stopOpponent(monaco, allCars, ourCar, ourCarIndex, bestOpponentIdx, 10000);
        } else if (turnsToLose < 2) {
            stopOpponent(monaco, allCars, ourCar, ourCarIndex, bestOpponentIdx, 5000);
        } else if (turnsToLose < 3) {
            stopOpponent(monaco, allCars, ourCar, ourCarIndex, bestOpponentIdx, 3000);
        } else if (turnsToLose < 4) {
            stopOpponent(monaco, allCars, ourCar, ourCarIndex, bestOpponentIdx, 2000);
        } else if (turnsToLose < 6) {
            stopOpponent(monaco, allCars, ourCar, ourCarIndex, bestOpponentIdx, 1000 / turnsToLose);
        } else if (turnsToLose < 10) {
            stopOpponent(monaco, allCars, ourCar, ourCarIndex, bestOpponentIdx, 500 / turnsToLose);
        }

        if (turnsToLose > 10 && chilling) {
            if (ourCarIndex == 2) {
                // match speed
                uint256 targetSpeed = allCars[1].speed;
                if (targetSpeed > ourCar.speed) {
                    uint256 maxAccelAmt = targetSpeed - ourCar.speed;
                    accelToMax(monaco, ourCar, maxAccelAmt, 4000 / turnsToLose);
                }
            }
            return;
            // else we sit and wait for shelloorr to pass
        } else if (turnsToLose > 10 && turnsInSecond > 1 && shelledCount > 1 && !chilling) {
            // no need to accelerate cuz its a waste, theyre just gonna shell
            stopOpponent(monaco, allCars, ourCar, ourCarIndex, bestOpponentIdx, 2000 / turnsToLose);
            chilling = true;
            return;
        } else {
            uint256 maxAccelCost = turnsToLose == 0 ? 100000 : turnsToLose < 6 ? 5000 / turnsToLose : 10 + (1000 / turnsToLose);
            tryLowerTurnsToWin(monaco, ourCar, turnsToWin, maxAccelCost);
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

        prevIdx = ourCarIndex;
        prevSpeed = ourCar.speed;
    }

    function tryLowerTurnsToWin(Monaco monaco, Monaco.CarData memory ourCar, uint256 turnsToWin, uint256 maxAccelCost) internal returns (uint256 newTurnsToWin) {
        uint256 maxAccelPossible = maxAccel(monaco, maxAccelCost > ourCar.balance ? ourCar.balance : maxAccelCost);
        if (maxAccelPossible == 0) {
            return turnsToWin;
        }

        uint256 bestTurnsToWin = (1000 - ourCar.y) / (ourCar.speed + maxAccelPossible);

        // no amount of accel will lower our ttw
        if (bestTurnsToWin == turnsToWin) {
            return turnsToWin;
        }

        // iterate down and see the least speed that still gets the best ttw
        uint256 leastAccel = maxAccelPossible;
        for (uint256 accel = maxAccelPossible - 1; accel > 0; accel--) {
            newTurnsToWin = (1000 - ourCar.y) / (ourCar.speed + accel);
            if (newTurnsToWin > bestTurnsToWin) {
                leastAccel = accel + 1;
                break;
            }
        }
        accelerate(monaco, ourCar, leastAccel);
    }

    function accelToMax(Monaco monaco, Monaco.CarData memory ourCar, uint256 maxSpeed, uint256 maxCost) internal {
        if (monaco.getAccelerateCost(maxSpeed) < maxCost) {
            accelerate(monaco, ourCar, maxSpeed);
        }

        uint256 totalSpent = monaco.getAccelerateCost(1);
        uint256 totalSpeed = 0;
        while (totalSpent < maxCost && totalSpeed < maxSpeed) {
            if (!accelerate(monaco, ourCar, 1)) {
                return;
            }
            totalSpent += monaco.getAccelerateCost(1);
            totalSpeed++;
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

    function stopOpponent(Monaco monaco, Monaco.CarData[] calldata allCars, Monaco.CarData memory ourCar, uint256 ourCarIdx, uint256 opponentIdx, uint256 maxCost) internal {
        Monaco.CarData memory opponentCar = allCars[opponentIdx];
        // when at the same y, neither bananas nor shells help
        if (opponentCar.y == ourCar.y) {
            return;
        }

        // in front, so use shells
        if (opponentIdx < ourCarIdx) {
            // theyre already slow so no point shelling
            if (opponentCar.speed == 1) {
                return;
            }

            uint256 superCost = monaco.getSuperShellCost(1);
            if (superCost < maxCost) {
                superShell(monaco, ourCar, 1);
                return;
            }

            uint256 shellCost = monaco.getShellCost(1);
            // TODO: check # shells required for bananas
            if (shellCost < maxCost && opponentCar.shield == 0) {
                shell(monaco, ourCar, 1);
            }

            return;
        } else if (monaco.getBananaCost() < maxCost) {
            // behind so banana
            banana(monaco, ourCar);
            return;
        }
    }

    function getTurnsToLoseOptimistic(Monaco monaco, Monaco.CarData[] calldata allCars, uint256 ourCarIndex) internal view returns (uint256 turnsToLose, uint256 bestOpponentIdx) {
        turnsToLose = 1000;
        for (uint256 i = 0; i < allCars.length; i++) {
            if (i != ourCarIndex) {
                Monaco.CarData memory car = allCars[i];
                uint256 maxSpeed = car.speed + maxAccel(monaco, car.balance * 6 / 10);
                uint256 turns = maxSpeed == 0 ? 1000 : (1000 - car.y) / maxSpeed;
                if (turns < turnsToLose) {
                    turnsToLose = turns;
                    bestOpponentIdx = i;
                }
            }
        }
    }

    function getTurnsToLose(Monaco monaco, Monaco.CarData[] calldata allCars, uint256 ourCarIndex) internal view returns (uint256 turnsToLose, uint256 bestOpponentIdx) {
        turnsToLose = 1000;
        for (uint256 i = 0; i < allCars.length; i++) {
            if (i != ourCarIndex) {
                Monaco.CarData memory car = allCars[i];
                uint256 maxSpeed = car.speed + maxAccel(monaco, car.balance);
                uint256 turns = maxSpeed == 0 ? 1000 : (1000 - car.y) / maxSpeed;
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
