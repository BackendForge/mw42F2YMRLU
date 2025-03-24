from web3 import Web3
import json
import os
from dotenv import load_dotenv
from eth_utils.address import to_checksum_address

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

MEDIAN_ADDRESS = to_checksum_address("0x64DE91F5A373Cd4c28de3600cB34C7C6cE410C85")

median_abi = json.loads('''
[
  {
    "constant": true,
    "inputs": [],
    "name": "peek",
    "outputs": [{"name": "", "type": "bytes32"}, {"name": "", "type": "bool"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "wat",
    "outputs": [{"name": "", "type": "bytes32"}],
    "stateMutability": "view",
    "type": "function"
  }
]
''')

median = w3.eth.contract(address=MEDIAN_ADDRESS, abi=median_abi)

#### Median/contract-not-whitelisted
# val_bytes, valid = median.functions.peek().call()
# symbol = median.functions.wat().call().rstrip(b"\0").decode()

# if valid:
#     price = int.from_bytes(val_bytes, byteorder="big")
#     print(f"{symbol} price from Median: {price / 1e18} DAI")
# else:
#     print(f"{symbol} price is not valid yet.")

event_signature = "0x" + Web3.keccak(text="LogValue(bytes32)").hex()

logs = w3.eth.get_logs({
    "address": MEDIAN_ADDRESS,
    "fromBlock": 17000000,
    "toBlock": 'latest',
    "topics": [event_signature]
})

for log in logs:
    print(log)
    print(w3.eth.get_transaction(log["transactionHash"]))
    print(median.decode_function_input(log["data"]))
    print(median.decode_function_output(log["data"]))
    print()
