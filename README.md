# election-erc20
A decentralized application for elections using the ERC20 token protocol.
This is currently a incomplete project.

Requirements:
```
pip install eth-brownie
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

To-do:
- Front-end (In development)
- Deployment onto Kovan testnet
- Implementing election start-end mechanism (In development)

## Contribution
You can open a pull request or issue at any point you think you can add a feature or you have found a mistake/error.
