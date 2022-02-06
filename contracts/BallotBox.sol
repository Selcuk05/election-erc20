// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./VoterToken.sol";

contract BallotBox is Ownable {
    // -- constructor -- : get candidates (for voting) and voters (for availability check)
    // 1. distribute: distribute 1 token to each voter
    // 2. startElection: start the election
    // 3. vote: will be called by voters to vote for their choice of candidate
    // 4. endElection: end the election

    using SafeERC20 for IERC20;

    IERC20 public token;

    address[] public voters;
    mapping(address => uint256) hasVoted;
    address[] public candidates;

    bool public electionOpen;

    event ElectionStarted();
    event ElectionEnded();

    constructor(address _voterTknAddr, address[] memory _voters, address[] memory _candidates){
        voters = _voters;
        candidates = _candidates;
        token = IERC20(_voterTknAddr);
    }

    function distribute() external onlyOwner {
        for(uint256 i = 0; i < voters.length; i++){
            token.safeTransfer(voters[i], 1); // 1 token = 1 vote
        }
    }

    function startElection() external onlyOwner {
        electionOpen = true;
        emit ElectionStarted();
    }

    function endElection() external onlyOwner {
        electionOpen = false;
        emit ElectionEnded();
    }

    function isVoter(address _target) internal returns(bool) {
        for(uint256 i = 0; i < voters.length; i++){
            if(_target == voters[i]){
                return true;
            }
        }
        return false;
    }

    function isCandidate(address _target) internal returns(bool) {
        for(uint256 i = 0; i < candidates.length; i++){
            if(_target == candidates[i]){
                return true;
            }
        }
        return false;
    }

    function vote(address _candidate) external {
        require(electionOpen, "Election is not open yet");
        require(!isCandidate(msg.sender), "Caller is candidate");
        require(isCandidate(_candidate), "No such candidate exists");
        require(isVoter(msg.sender), "Caller not in voter list");
        require(hasVoted[msg.sender] == 0, "Caller has already voted");
        // approve -> approve from client to make BallotBox contract to transfer tokens 
        // transferFrom -> BallotBox contract will transfer from msg.sender to _candidate
        hasVoted[msg.sender] = 1;
        token.safeTransferFrom(msg.sender, _candidate, 1);
    }

}