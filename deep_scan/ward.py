# Found event Rely in TX 0x756e855ef62a76093e67768daedab94e7eeb926c4b1c1f13ab4b0889ae0e52e1 at block 22866211, sent from: 0xf5a05b8774910FE5dCa36E8b2292C2ccC0c8A191

# leads to
# 0xB8698CfFFdAAf26ca21fE8aA560c18cc2b2f5996

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

CONTRACT_ADDRESS = Web3.to_checksum_address(
    "0xBB856d1742fD182a90239D7AE85706C2FE4e5922"
)
USER_ADDRESS = Web3.to_checksum_address("0xB8698CfFFdAAf26ca21fE8aA560c18cc2b2f5996")

selector = "0x" + Web3.keccak(text="wards(address)").hex()

# Encode function call with user address (padded to 32 bytes)
payload = selector + w3.to_checksum_address(USER_ADDRESS)[2:].zfill(64)

# Call the contract
response = w3.eth.call({"to": CONTRACT_ADDRESS, "data": payload})
hmm = int.from_bytes(response, byteorder="big")
print(response.hex())
print(hmm)  # returned 0
