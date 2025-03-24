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
    logging.FileHandler("spotter.log"),
    logging.StreamHandler()
]

# Configure all handlers with same formatter
for h in handlers:
    h.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(h)

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Addresses 0x65C79FCB50Ca1594B025960e539eD7A9E37D4B2F
SPOTTER_ADDRESS = Web3.to_checksum_address("0x65C79fcB50Ca1594B025960e539eD7A9a6D434A3")  # MakerDAO Spotter on mainnet

# ABIs (trimmed to what we need)
spotter_abi = json.loads('''
[
    {
        "constant": true,
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "ilks",
        "outputs": [
            {"internalType": "contract PipLike", "name": "pip", "type": "address"},
            {"internalType": "uint256", "name": "mat", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
''')

median_abi = json.loads('''
[
    {
        "constant": true,
        "inputs": [],
        "name": "peek",
        "outputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
''')

# Load contract
spotter = w3.eth.contract(address=SPOTTER_ADDRESS, abi=spotter_abi)

# Helper: convert ilk name to bytes32
def str_to_bytes32(text):
    return Web3.to_bytes(text.encode()).ljust(32, b'\0')

# Example: Get Median (pip) for ETH-A
active_ilks = ['ETH-A', 'ETH-B', 'ETH-C', 'BAT-A', 'USDC-A', 'USDC-B', 'WBTC-A', 'TUSD-A', 'ZRX-A', 'KNC-A', 'MANA-A', 'USDT-A', 'PAXUSD-A', 'COMP-A', 'LRC-A', 'LINK-A', 'BAL-A', 'YFI-A', 'GUSD-A', 'UNI-A', 'RENBTC-A', 'AAVE-A', 'UNIV2DAIETH-A', 'UNIV2WBTCETH-A', 'UNIV2USDCETH-A', 'UNIV2DAIUSDC-A', 'UNIV2ETHUSDT-A', 'UNIV2LINKETH-A', 'UNIV2UNIETH-A', 'UNIV2WBTCDAI-A', 'UNIV2AAVEETH-A', 'UNIV2DAIUSDT-A', 'PSM-USDC-A', 'RWA001-A', 'RWA002-A', 'RWA003-A', 'RWA004-A', 'RWA005-A', 'RWA006-A', 'PSM-PAX-A', 'MATIC-A', 'GUNIV3DAIUSDC1-A', 'WSTETH-A', 'RWA013-A', 'WBTC-B', 'WBTC-C', 'PSM-GUSD-A', 'GUNIV3DAIUSDC2-A', 'CRVV1ETHSTETH-A', 'WSTETH-B', 'RWA008-A', 'RWA009-A', 'TELEPORT-FW-A', 'RWA007-A', 'RETH-A', 'DIRECT-COMPV2-DAI', 'GNO-A', 'RWA010-A', 'RWA011-A', 'RWA012-A', 'DIRECT-AAVEV2-DAI', 'DIRECT-SPARK-DAI']
for ilk in active_ilks:
    ilk_bytes = str_to_bytes32(ilk)
    ilk_data = spotter.functions.ilks(ilk_bytes).call()
    pip_address = ilk_data[0]

    logging.info(f"Pip address (Median) for {ilk}: {pip_address}")


## CODE BELLOW CAN EXECUTE ONLY THE AUTHORIZED CONTRACTS
# Read the current price from the Median
# median = w3.eth.contract(address=pip_address, abi=median_abi)
# (price_bytes, valid) = median.functions.peek().call()

# if valid:
#     price = int.from_bytes(price_bytes, byteorder='big')
#     print(f"Price: {price} (internal precision, often 1e18)")
# else:
#     print("Median price is not valid")
