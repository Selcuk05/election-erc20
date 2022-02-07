import json
import time

from brownie import Contract

from scripts.helpful_scripts import get_account

# Make sure you have deployed with the
# do_send_data_to_frontend parameter
# set to True


def main():
    start_election(0, 1, 0)


# This method also implements the election mechanism.
def start_election(hours: int, minutes: int, seconds: int):
    data = ""
    with open("./frontend/brownie-info.json", "r") as f:
        data = json.load(f)
    ballot_box = Contract.from_abi(
        "BallotBox", address=data["BallotBox"]["address"], abi=data["BallotBox"]["abi"]
    )
    admin_acc = get_account()
    tx = ballot_box.startElection({"from": admin_acc})
    tx.wait(1)
    print("Election has started")
    # ! vvvv this probably isnt a good way to do this, might change in the future.
    time.sleep(hours * 3600 + minutes * 60 + seconds)
    tx_end = ballot_box.endElection({"from": admin_acc})
