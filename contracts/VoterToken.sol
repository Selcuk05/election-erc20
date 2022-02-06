// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract VoterToken is ERC20 {

    constructor(uint256 voterCount) ERC20("Voter Token", "VOTE"){
        _mint(msg.sender, voterCount);
    }
}