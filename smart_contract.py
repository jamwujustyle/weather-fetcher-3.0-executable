from web3 import Web3

infura_url = "https://sepolia.infura.io/v3/9e46cd5c5c944f31a9738202e83c0e0b"
web3 = Web3(Web3.HTTPProvider(infura_url))


if web3.is_connected():
    print("Successfully connected to Infura Sepolia")
else:
    print("failed to connect to Infura Sepolia")

abi = [
    {
        "inputs": [{"internalType": "int256", "name": "average", "type": "int256"}],
        "name": "addAverage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "averages",
        "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getAllAverages",
        "outputs": [{"internalType": "int256[]", "name": "", "type": "int256[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "getAverage",
        "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getAveragesCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

contract_address = "0xf4Bb3bFB524E76e66BC2860944100431DF3B4880"

contract = web3.eth.contract(address=contract_address, abi=abi)
wallet_address = "0x74fBBb0Be04653f29bd4b2601431E87f9B811319"


def add_average(value):
    txn = contract.functions.addAverage(value).build_transaction(
        {
            "chainId": 11155111,
            "gas": 2000000,
            "gasPrice": web3.to_wei("20", "gwei"),
            "nonce": web3.eth.get_transaction_count(wallet_address),
        }
    )
    signed_txn = web3.eth.account.sign_transaction(
        txn,
        private_key="00be00eb4bbd4c9f28e744f01efbeec08914f252ae7669c50f441905331a835b",
    )
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Transaction hash:", tx_hash.hex())


def get_averages_count():
    return contract.functions.getAveragesCount().call()


def get_average(index):
    return contract.functions.getAverage(index).call()


def get_all_averages():
    return contract.functions.getAllAverages().call()
