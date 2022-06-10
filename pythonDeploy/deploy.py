from dis import Bytecode
import json
from solcx import compile_standard
import solcx

from web3 import Web3

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    ##print(simple_storage_file)

solcx.install_solc("0.6.6")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.6",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connection to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://192.168.86.25:7545"))
chain_id = 1337
my_address = "0x409bD0072BAe89320af9E77B1798Aa9c0f33Ddd0"
private_key = "0x4edcdb082f0a8dd0ac29500047eb38d2f4e8286b6424b5532cb85df1442e29f3"

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)
# 1 Build a transcation
# 2 Sign a transcation
# 3 Send a transcation
transcation = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
print(transcation)
signed_txn = w3.eth.sign_transaction(transcation, private_key=private_key)
