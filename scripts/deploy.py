from brownie import BallotBox, VoterToken, config, network

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_mock_accounts,
)


# This is for future testnet/mainnet deployments
def literal_data():
    voters = []
    candidates = []
    return candidates, voters


def deploy_ballot_box():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        candidates, voters = get_mock_accounts()
    else:
        candidates, voters = literal_data()
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
    dist_tx = ballot_box.distribute({"from": account})
    dist_tx.wait(1)

    return ballot_box, voter_token


def main():
    deploy_ballot_box()
