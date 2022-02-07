# election-erc20
A decentralized application for elections using the ERC20 token protocol.
This is currently a incomplete project.

Requirements:
```
pip install eth-brownie
npm install ganache-cli
```

Optional:
```
pip install slither-analyzer
```

**Run unit tests:**
```
brownie test -W ignore::DeprecationWarning
```

**Run Slither vulnerability tests:**
```
slither . --filter-paths "openzeppelin"
```

## Front-end
Thanks to @PatrickAlphaC for providing with the [MetaMask connection codebase](https://github.com/PatrickAlphaC/html-js-ethers-connect/).<br>
At the frontend folder;
```python
yarn # Installs dependencies
yarn build # Bundles the JavaScript
yarn http-server # Runs the server
```
If you changed any JS code in index.js and want to bundle it, you can run `yarn build` any time.

Steps to test the front-end (for now, locally)
- Launch Ganache: `ganache-cli`
- Deploy contracts (in base folder): `brownie run scripts/deploy.py`
- Start election (in base folder): `brownie run scripts/start_election.py`
- [Import Ganache account into MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360015489331-How-to-import-an-Account)
    * You should get the private key from ganache-cli, choose one of the private keys after the second one (0 = admin, 1 and 2 = candidates)
    * Make sure you are in the network 'Localhost 8545' in MetaMask
- Launch local host (in folder: frontend): `yarn http-server`
    * after 'Available on:', the second link is the right link
- Connect your wallet from the front-end
- Get a candidate's address from ganache-cli
    * Choose either address 1 or address 2 because these are the candidates (0 = admin, others are voters)
- Follow the inputs in the front-end and see the responses in the console (F12)

You have successfully voted with a mock account! <br>
This will be integrated into a testnet too when the project is complete for testnet.

**Ganache/MetaMask tip:** If you do not want to import ganache keys into MetaMask every time you launch a new one,<br>
you can launch a single consistent ganache instance using the mnemonic with this command: `ganache-cli -d -m 'your_mnemonic'`<br>
If you want to use this, make sure that you store your initial mnemonic somewhere.
**Note that you will still have to deploy at every new launch!**

To-do:
- Front-end (In development)
- Deployment onto Kovan testnet
- Implementing election start-end mechanism (In development)

## Contribution
You can open a pull request or issue at any point you think you can add a feature or you have found a mistake/error.
