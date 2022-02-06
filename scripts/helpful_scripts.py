from brownie import accounts, config, network

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]


class MockNotUsableError(Exception):
    def __init__(
        self, network_env, message="Mock accounts are not usable in this environment"
    ):
        self.network_env = network_env
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} => {self.network_env}"


# Thanks Patrick Collins!
def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def get_mock_accounts():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        candidates = [accounts[1], accounts[2]]
        voters = accounts[3::]
        return candidates, voters
    raise MockNotUsableError(network.show_active())
