from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

osm_address = Web3.to_checksum_address("0x81FE72B5A8d1A857d176C3E7d5Bd2679A9B85763")

# 'kiss(address)' selector
kiss_selector = "0x" + Web3.keccak(text="kiss(address)").hex()

# Define filter
logs = w3.eth.get_logs({
    "fromBlock": 17000000,
    "toBlock": "latest",
    "address": osm_address,
    "topics": [kiss_selector]
})

print(f"Found {len(logs)} kiss() events in OSM")
for log in logs:
    print(log)
