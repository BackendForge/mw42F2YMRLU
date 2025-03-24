from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

OSM_ADDRESS = Web3.to_checksum_address("0x81FE72B5A8d1A857d176C3E7d5Bd2679A9B85763")

osm_abi = json.loads('''
[
  {"constant":true,"inputs":[],"name":"src","outputs":[{"name":"","type":"address"}],"stateMutability":"view","type":"function"}
]
''')

osm = w3.eth.contract(address=OSM_ADDRESS, abi=osm_abi)
median_address = osm.functions.src().call()
print("Median used by OSM:", median_address)
# Median used by OSM: 0x64DE91F5A373Cd4c28de3600cB34C7C6cE410C85