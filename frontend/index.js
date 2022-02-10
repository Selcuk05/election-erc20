const { ethers } = require("ethers");

async function connect() {
    if (typeof window.ethereum !== "undefined") {
        try {
            await ethereum.request({ method: "eth_requestAccounts" });
        } catch (error) {
            console.log(error);
        }
        document.getElementById("connectButton").innerHTML = "Connected";
        const accounts = await ethereum.request({ method: "eth_accounts" });
        console.log(accounts[0])
    } else {
        document.getElementById("connectButton").innerHTML =
            "Please install MetaMask";
    }
}

async function execute(candidate, brownie_info) {
    if (typeof window.ethereum !== "undefined") {
        const ballotBoxAddr = brownie_info.BallotBox.address;
        const ballotBoxAbi = brownie_info.BallotBox.abi;
        const voterTknAddr = brownie_info.VoterToken.address;
        const voterTknAbi = brownie_info.VoterToken.abi;

        if (candidate === "") {
            alert("You need to enter a candidate address!")
            return
        }

        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const signer = provider.getSigner();
        const token_contract = new ethers.Contract(voterTknAddr, voterTknAbi, signer);
        const contract = new ethers.Contract(ballotBoxAddr, ballotBoxAbi, signer);

        var candidates = await contract.getCandidates();
        console.log(candidates);
        if(!candidates.includes(candidate)){
            alert("The candidate address is not valid.");
            return
        }

        var isOpened = await contract.electionOpen();
        if (!isOpened) {
            alert("Election is not open yet!");
            return
        }

        /**
         * ! CAN NOT IMPLEMENT AN APPROVE CHECK BECAUSE ETHERS.JS REFUSES TO GET hasVoted
         * ! AS A FUNCTION. IT IS CORRECT IN THE ABI BUT IT JUST COMPLETELY DENIES THE
         * ! FUNCTION, I WILL TRY IMPLEMENTING SOMETHING ELSE OR NOT IMPLEMENT AN APPROVE
         * ! CHECK AT ALL
         */
        await token_contract.approve(ballotBoxAddr, 1);

        try{
            await contract.vote(candidate);
        }catch(err){
            let reason = err.data.message.replace("VM Exception while processing transaction: revert ", "")
            alert("You currently can not vote due to this reason: " + reason);
            return;
        }
        alert("You have successfully voted!");

    } else {
        document.getElementById("executeButton").innerHTML = "Please connect";
    }
}


async function renewElectionInfo(brownie_info){
    if (typeof window.ethereum !== "undefined") {
        const ballotBoxAddr = brownie_info.BallotBox.address;
        const ballotBoxAbi = brownie_info.BallotBox.abi;
        const voterTknAddr = brownie_info.VoterToken.address;
        const voterTknAbi = brownie_info.VoterToken.abi;

        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const signer = provider.getSigner();
        const token_contract = new ethers.Contract(voterTknAddr, voterTknAbi, signer);
        const contract = new ethers.Contract(ballotBoxAddr, ballotBoxAbi, signer);

        var candidates = await contract.getCandidates();
        var candidateString = "";
        for(let i = 0; i < candidates.length; i++){
            candidate = candidates[i];
            const votes = await token_contract.balanceOf(candidate);
            candidateString += "<strong>Candidate " + i + "</strong></br>" + 
                candidate + "</br>" 
                + votes + " votes" + "</br>";
        }

        document.getElementById("electionInfo").innerHTML = candidateString;

        var isOpened = await contract.electionOpen();
        if(isOpened){
            document.getElementsByClassName("navbar-brand")[0].innerHTML = "Election (OPEN!)"
        }else{
            document.getElementsByClassName("navbar-brand")[0].innerHTML = "Election (Not open)"
        }
    } else {
        document.getElementById("electionInfo").innerHTML = "Please connect";
    }
}

module.exports = {
    connect,
    execute,
    renewElectionInfo,
};
