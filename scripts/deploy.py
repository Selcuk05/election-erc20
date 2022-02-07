import json
from textwrap import indent

from brownie import BallotBox, VoterToken, accounts, config, network

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


def deploy_ballot_box(do_send_data_to_frontend=False):
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

    if do_send_data_to_frontend:
        contract_infos = {
            "VoterToken": {"address": voter_token.address, "abi": voter_token.abi},
            "BallotBox": {"address": ballot_box.address, "abi": ballot_box.abi},
        }
        send_info_to_frontend(contract_dict=contract_infos)

    return ballot_box, voter_token


# Make sure you are in the base directory while you deploy the contracts
def send_info_to_frontend(contract_dict):
    with open("./frontend/brownie-info.json", "w+") as f:
        json.dump(contract_dict, f, sort_keys=True, indent=4)


def main():
    deploy_ballot_box(
        do_send_data_to_frontend=True,  # Change this to False if you do not want to do anything about frontend
    )
