// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "./../../interfaces/ICar.sol";

contract Nothing is ICar {
    uint256 private buy = 0;

    function takeYourTurn(
        Monaco monaco,
        Monaco.CarData[] calldata allCars,
        uint256[] calldata, /*bananas*/
        uint256 ourCarIndex
    ) external {
        if (buy > 0) {
            monaco.buyAcceleration(buy);

        }
    }

    function buyAcceleration(uint256 amt) external {
        buy = amt;
    }

    function sayMyName() external pure returns (string memory) {
        return "Nothing";
    }
}
