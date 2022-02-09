import random
import time

import pytest
from brownie import network
from scripts.deploy import deploy_ballot_box
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_mock_accounts,
)

# Run tests with this command to ignore pytest
# deprecation warnings:
# brownie test -W ignore::DeprecationWarning


@pytest.fixture
def ballot_box_and_token():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    return deploy_ballot_box()


def test_distributed(ballot_box_and_token):
    ballot_box, voter_token = ballot_box_and_token
    assert voter_token.balanceOf(ballot_box.address) == 0


def test_voter_has_been_distributed(ballot_box_and_token):
    _, voter_token = ballot_box_and_token
    _, voters = get_mock_accounts()
    random_voter = random.choice(voters)
    assert voter_token.balanceOf(random_voter) == 1
    # sleeping because brownie closes rpc too quick, causing a web3 error
    time.sleep(0.5)


def test_vote(ballot_box_and_token):
    ballot_box, voter_token = ballot_box_and_token
    admin_acc = get_account()
    starting_tx = ballot_box.startElection({"from": admin_acc})
    starting_tx.wait(1)

    candidates, voters = get_mock_accounts()
    voter_acc = random.choice(voters)
    candidate_acc = random.choice(candidates)
    tx_approval = voter_token.approve(
        ballot_box.address, 1, {"from": voter_acc}
    )  # approval done here, must be implemented in dApp too.
    tx_approval.wait(1)

    tx_vote = ballot_box.vote(candidate_acc, {"from": voter_acc})
    tx_vote.wait(1)

    assert voter_token.balanceOf(candidate_acc) == 1


def test_election_mechanism(ballot_box_and_token):
    ballot_box, _ = ballot_box_and_token
    admin_acc = get_account()

    start_tx = ballot_box.startElection({"from": admin_acc})
    start_tx.wait(1)
    # should implement a timing mechanism in production use
    end_tx = ballot_box.endElection({"from": admin_acc})
    end_tx.wait(1)

    assert ballot_box.electionOpen() == False


def test_get_candidates(ballot_box_and_token):
    ballot_box, _ = ballot_box_and_token
    assert len(ballot_box.getCandidates()) == 2
