import json
from web3 import Web3
import hashlib

# Replace these with your actual RPC endpoints:
MAINNET_RPC = "https://rpc-ethereum.g4mm4.io"
PULSECHAIN_RPC = "https://rpc-pulsechain.g4mm4.io"

# Connect to networks
w3_mainnet = Web3(Web3.HTTPProvider(MAINNET_RPC))
w3_pulse = Web3(Web3.HTTPProvider(PULSECHAIN_RPC))

# using mainnet-addresses.json and pulsechain-addresses.json, compare every contract, baesd on json KEYS and VALUES(addresses)

pulsechain_data = json.load(open("pulsechain-addresses.json"))
mainnet_data = json.load(open("mainnet-addresses.json"))

diffs = []
non_existing = []
the_same = []

for contract_name in pulsechain_data.keys():
    CC_ADDRESS_PULSE = pulsechain_data[contract_name]
    try:
        CC_ADDRESS_MAINNET = mainnet_data[contract_name]
    except KeyError:
        print(f"Contract {contract_name} not found on mainnet.")
        non_existing.append(contract_name)
        continue


    # Retrieve bytecode
    bytecode_mainnet = w3_mainnet.eth.get_code(Web3.to_checksum_address(CC_ADDRESS_MAINNET))
    bytecode_pulse = w3_pulse.eth.get_code(Web3.to_checksum_address(CC_ADDRESS_PULSE))

    # Compute keccak256 hash of bytecode for easy comparison
    hash_mainnet = hashlib.sha256(bytecode_mainnet).hexdigest()
    hash_pulse = hashlib.sha256(bytecode_pulse).hexdigest()

    print("{} Bytecode Hash Comparison:".format(contract_name))
    print("  Mainnet:", hash_mainnet)
    print("  PulseChain:", hash_pulse)

    if hash_mainnet == hash_pulse:
        print("The bytecode is identical.")
        the_same.append(contract_name)
    else:
        print("The bytecode differs; check for deployment or compiler differences.")
        diffs.append(contract_name)
else:
    print("All contracts compared.")
    print("Differences found in the following contracts:")
    print(diffs)
    print("Contracts not found on mainnet:")
    print(non_existing)
    print("Contracts with identical bytecode:")
    print(the_same)