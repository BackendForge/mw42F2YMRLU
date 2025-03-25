from web3 import Web3
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set up both handlers
handlers = [
    logging.FileHandler("chainlog.log"),
    logging.StreamHandler()
]

# Configure all handlers with same formatter
for h in handlers:
    h.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(h)

w3 = Web3(Web3.HTTPProvider(RPC_URL))

CHAINLOG_ADDR = Web3.to_checksum_address("0xdA0Ab1e0017DEbCd72Be8599041a2aa3bA7e740F")

chainlog_abi = json.loads(
    """
[
    {
        "constant": true,
        "inputs": [{"internalType": "bytes32", "name": "key", "type": "bytes32"}],
        "name": "getAddress",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "list",
        "outputs": [{"name": "", "type": "bytes32[]"}],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }                         
]
"""
)

chainlog = w3.eth.contract(address=CHAINLOG_ADDR, abi=chainlog_abi)


# Helper to convert name to bytes32 (right-padded)
def label_to_bytes32(label):
    return Web3.to_bytes(text=label).ljust(32, b"\0")


# MCD_DOG	Liquidation contract (v2)
# MCD_END	Global shutdown module
# MCD_CLIP_ETH_A	Clipper for ETH-A ilk
def get_address(label):
    key = label_to_bytes32(label)
    return chainlog.functions.getAddress(key).call()


# labels = [ "MCD_DOG", "MCD_END", "MCD_CLIP_ETH_A", "MCD_SPOT"]
labels_encoded = chainlog.functions.list().call()
keys = {}
for label in labels_encoded:
    key_str = label.rstrip(b"\0").decode("utf-8")
    keys[key_str] = get_address(key_str)
    logging.info(f"{key_str} address: {keys[key_str]}")
logging.info(keys)

# save to file
with open("chainlog.json", "w") as f:
    json.dump(keys, f)
