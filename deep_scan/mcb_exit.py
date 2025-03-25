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

CONTRACT_ADDRESS = Web3.to_checksum_address("0xBB856d1742fD182a90239D7AE85706C2FE4e5922")
# when() -> 0
# wait() -> 262800
# vow(), vat(), spot(), pot(), live(), dog(), cat()
selector = "0x" + Web3.keccak(text="wait()").hex()

# Encode function call with user address (padded to 32 bytes)
payload = selector # + w3.to_checksum_address(user_address)[2:].zfill(64)

# Call the contract
response = w3.eth.call({
    "to": CONTRACT_ADDRESS,
    "data": payload
})
hmm = int.from_bytes(response, byteorder='big')
print(response.hex())
print(hmm) # returned 0