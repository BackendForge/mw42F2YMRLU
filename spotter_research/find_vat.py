from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
w3 = Web3(Web3.HTTPProvider(RPC_URL))  # or your forked chain

DAIJOIN_ADDRESS = "0x9759A6Ac90977b93B58547b4A71c78317f391A28"  # Replace with known or guessed DaiJoin

dai_join_abi = json.loads('''
[
    {"constant":true,"inputs":[],"name":"vat","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[],"name":"dai","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}
]
''')

dai_join = w3.eth.contract(address=Web3.to_checksum_address(DAIJOIN_ADDRESS), abi=dai_join_abi)

vat_used = dai_join.functions.vat().call()
dai_token = dai_join.functions.dai().call()

print("Vat used by DaiJoin:", vat_used)
print("DAI token address:", dai_token)
