from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

CHAINLOG_ADDR = Web3.to_checksum_address("0xdA0Ab1e0017DEbCd72Be8599041a2aa3bA7e740F")

chainlog_abi = json.loads('''
[
  {
    "constant": true,
    "inputs": [{"name": "key", "type": "bytes32"}],
    "name": "getAddress",
    "outputs": [{"name": "", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
  }
]
''')

chainlog = w3.eth.contract(address=CHAINLOG_ADDR, abi=chainlog_abi)

def get_address_from_chainlog(label):
    key = Web3.to_bytes(text=label).ljust(32, b'\0')
    return chainlog.functions.getAddress(key).call()

dai_token = get_address_from_chainlog("MCD_DAI")
dai_join = get_address_from_chainlog("MCD_JOIN_DAI")

print("DAI Token Address:", dai_token)
print("DaiJoin Address:", dai_join)
