// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "forge-std/Test.sol";

import "../src/Monaco.sol";
import "../src/cars/ExampleCar.sol";

import "../src/cars/samples/ThePackage.sol";

import {c000r} from "../src/cars/samples/c000r.sol";
import {PermaShield} from "../src/cars/samples/PermaShield.sol";
import {Nothing} from "../src/cars/samples/Nothing.sol";
import {Sauce} from "../src/cars/samples/Saucepoint.sol";
import {MadCar} from "../src/cars/samples/MadCar.sol";
import {Floor} from "../src/cars/samples/Floor.sol";

uint256 constant CAR_LEN = 3;
uint256 constant ABILITY_LEN = 5;

// Data structure containing information regarding a turn
struct GameTurn{

    address[CAR_LEN] cars;
    uint256[CAR_LEN] balance;
    uint256[CAR_LEN] speed;
    uint256[CAR_LEN] y;
    uint256[CAR_LEN] shield;

    uint256[ABILITY_LEN] costs;
    uint256[ABILITY_LEN] bought;
    uint256[] bananas;

    // for this turn
    address currentCar;
    uint256[ABILITY_LEN] usedAbilities;
}

contract CostTest is Test {

    error MonacoTest__getCarIndex_carNotFound(address car);
    error MonacoTest__getAbilityCost_abilityNotFound(uint256 abilityIndex);

    Monaco monaco;
    address[CAR_LEN] cars;
    Nothing w1;

    function setUp() public {
        monaco = new Monaco();
        w1 = new Nothing();
        ICar w2 = new Nothing();
        ICar w3 = new Nothing();
        monaco.register(w1);
        monaco.register(w2);
        monaco.register(w3);
    }

    function testAccelerationCost() public {
        monaco.play(10);
        w1.buyAcceleration(1);
        monaco.play(10);
        w1.buyAcceleration(5);
        monaco.play(100);
    }

}
