import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
# Connect to PulseChain RPC
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Example: If you know the Vat address, try this:
vat_address = "0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b"  # replace with real Vat address on PulseChain

# Check if this Vat is registered in a Chainlog
# Guessing possible Chainlog address — often the same as mainnet
possible_chainlogs = [
    "0x9d8a62f656a8d1615c1294fd71e9cfb3e4855a4f",
    "0xdA0Ab1e0017DEbCd72Be8599041a2aa3bA7e740F"  # Add others if known
]

chainlog_abi = json.loads('''[
    {"constant":true,"inputs":[{"name":"key","type":"bytes32"}],"name":"getAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}
]''')

for addr in possible_chainlogs:
    try:
        chainlog = w3.eth.contract(address=Web3.to_checksum_address(addr), abi=chainlog_abi)
        addr_vat = chainlog.functions.getAddress(Web3.to_bytes(text="MCD_VAT").ljust(32, b'\0')).call()
        if Web3.to_checksum_address(addr_vat) == Web3.to_checksum_address(vat_address):
            print("✅ Found correct Chainlog:", addr)
            break
    except Exception as e:
        continue
