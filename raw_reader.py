from web3 import Web3
from eth_utils.address import to_checksum_address


# Connect to Ethereum network (Replace with your RPC endpoint)
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# MakerDAO CDP Manager contract address
CDP_MANAGER = to_checksum_address("0x5ef30b9986345249bc32d8928b7ee64de9435e39")

# Your Ethereum address (Replace with your actual address)
user_address = to_checksum_address("YOUR_WALLET_ADDRESS")

# Function selector for "owns(address)"
function_selector = "0x65a0f9c4"

# Encode function call with user address (padded to 32 bytes)
payload = function_selector + w3.to_checksum_address(user_address)[2:].zfill(64)

# Call the contract
response = w3.eth.call({
    "to": CDP_MANAGER,
    "data": payload
})

# Decode response (vaultId is a uint256)
vault_id = int.from_bytes(response, byteorder='big')
print(f"Your vault ID is: {vault_id}")
