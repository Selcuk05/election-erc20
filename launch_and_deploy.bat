@echo off

set /p mnemonic="Enter mnemonic with quotes: "
start cmd /c "ganache-cli -d -m %mnemonic%"
start cmd /c "brownie run scripts\deploy.py && brownie run scripts\start_election.py && pause"