from brownie import BallotBox, VoterToken, config, network

from scripts.helpful_scripts import get_account, get_mock_accounts


def deploy_ballot_box():
    candidates, voters = get_mock_accounts()
    account = get_account()
    voter_token = VoterToken.deploy(len(voters), {"from": account})
    ballot_box = BallotBox.deploy(
        voter_token.address,
        voters,
        candidates,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    tx = voter_token.transfer(
        ballot_box.address, voter_token.totalSupply(), {"from": account}
    )

    tx.wait(1)
    ballot_box.distribute({"from": account})

    return ballot_box, voter_token


def main():
    deploy_ballot_box()
