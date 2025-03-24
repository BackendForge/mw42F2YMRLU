from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
# Setup
w3 = Web3(Web3.HTTPProvider(RPC_URL))

OSM_ADDRESS = Web3.to_checksum_address(
    "0x81FE72B5A8d1A857d176C3E7d5Bd2679A9B85763"
)  # ETH-A OSM
DOG_ADDRESS = Web3.to_checksum_address("0x135954d155898D42C90D2a57824C690e0c7BEf1B")
# Event selector for diss(address)
selector = "0x" + Web3.keccak(text="diss(address)").hex()


# Convert DOG address to topic format
dog_topic = "0x" + DOG_ADDRESS.lower()[2:].rjust(64, "0")

# Build filter
logs = w3.eth.get_logs(
    {
        "fromBlock": 17000000,
        "toBlock": "latest",
        "address": OSM_ADDRESS,
        "topics": [
            selector,  # Topic0 = function selector
            None,  # Topic1 = sender (optional)
            dog_topic,  # Topic2 = target of diss()
        ],
    }
)

# Parse logs
if logs:
    for log in logs:
        print(
            f"DOG was unwhitelisted in tx: {log['transactionHash'].hex()} at block {log['blockNumber']}"
        )
else:
    print(
        "❌ No diss() logs found for DOG — maybe it was never whitelisted or not yet unwhitelisted."
    )


selector = "0x" + Web3.keccak(text="kiss(address)").hex()
# Build filter
logs = w3.eth.get_logs(
    {
        "fromBlock": 17000000,
        "toBlock": "latest",
        "address": OSM_ADDRESS,
        "topics": [
            selector,  # Topic0 = function selector
            None,  # Topic1 = sender (optional)
            dog_topic,  # Topic2 = target of diss()
        ],
    }
)

# Parse logs
if logs:
    for log in logs:
        print(
            f"DOG was whitelisted in tx: {log['transactionHash'].hex()} at block {log['blockNumber']}"
        )
else:
    print(
        "❌ No kiss() logs found for DOG — maybe it was never whitelisted or not yet unwhitelisted."
    )
