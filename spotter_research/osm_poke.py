import os
from web3 import Web3
import json
from eth_account import Account
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
# Setup
w3 = Web3(Web3.HTTPProvider(RPC_URL))  # or your fork
w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

OSM_ADDRESS = Web3.to_checksum_address("0x81FE72B5A8d1A857d176C3E7d5Bd2679A9B85763")  # ETH-A OSM

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if PRIVATE_KEY is None:
    raise ValueError("PRIVATE_KEY env variable is not set")
ACCOUNT = Account.from_key(PRIVATE_KEY)
SENDER = ACCOUNT.address

# ABI for poke()
osm_abi = json.loads('[{"constant":false,"inputs":[],"name":"poke","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
osm = w3.eth.contract(address=OSM_ADDRESS, abi=osm_abi)

# Build transaction
tx = osm.functions.poke().build_transaction({
    'from': SENDER,
    'nonce': w3.eth.get_transaction_count(SENDER),
    'gas': 145555,
    'gasPrice': int(w3.eth.generate_gas_price() * 1.05),
    'chainId': 369
})

# Sign and send
signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"poke() sent, tx hash: {tx_hash.hex()}")

# Wait for receipt
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Confirmed in block:", receipt.blockNumber)
