# emit Rely(usr)
import json
import os
from web3 import Web3
from dotenv import load_dotenv
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set up both handlers
handlers = [
    logging.FileHandler("rely.log"),
    logging.StreamHandler()
]

# Configure all handlers with same formatter
for h in handlers:
    h.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(h)

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
if RPC_URL is None:
    raise ValueError("RPC_URL env variable is not set")
# Connect to PulseChain RPC
w3 = Web3(Web3.HTTPProvider(RPC_URL))


latest_block = w3.eth.block_number
start_block = 17237361 # - 1000000
block_chunk = 50000


log_abi = json.loads('''
[
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "usr", "type": "address"}
        ],
        "name": "Rely",
        "type": "event"
    },
    {
        "anonymous": true,
        "inputs": [
            {"indexed": true, "name": "usr", "type": "address"}
        ],
        "name": "RelyAnon",
        "type": "event"
    }                     
]
''')

dummy_contract = w3.eth.contract(abi=log_abi)

# ------------------------------------------------------
# 1. Define the event signatures (function/payload)
#    We'll watch for "LogValue(bytes32)", "LogNote(bytes4,address,bytes32,bytes32,uint256,bytes)"
# ------------------------------------------------------
event_sigs = {
    "Rely":  "Rely(address)",
    # Add any others you need
}

# Create a dictionary: eventName -> topicHash (0x-prefixed)
topics_of_interest = {}
for name, signature in event_sigs.items():
    # Ensure it's 0x-prefixed
    signature_hash = "0x" + w3.keccak(text=signature).hex()  
    topics_of_interest[name] = signature_hash

print("Topics of interest:")
for k, v in topics_of_interest.items():
    print(f"  {k} = {v}")

# ------------------------------------------------------
# 2. Define a function to get logs for a block range
# ------------------------------------------------------
def get_logs_for_range(from_block, to_block, topics):
    """
    Fetch logs matching any of the given topics in the range [from_block, to_block].
    'topics' should be a list of lists for OR queries in topic0, e.g. [[topicA, topicB], None, None].
    """
    # For multiple "OR" topics in the first position, we wrap them in a list of lists
    # https://web3py.readthedocs.io/en/stable/filters.html#using-the-topics-parameter
    try:
        logs = w3.eth.get_logs({
            "fromBlock": from_block,
            "toBlock": to_block,
            "topics": [[t for t in topics]]  # OR condition for topic0
        })
        return logs
    except Exception as e:
        logging.error(f"Error fetching logs in block range {from_block} - {to_block}: {e}")
        return []

# ------------------------------------------------------
# 3. Main loop: chunk through the chain
# ------------------------------------------------------
current_start = start_block

while current_start <= latest_block:
    current_end = min(current_start + block_chunk - 1, latest_block)
    print(f"Scanning blocks {current_start} to {current_end} ...")

    # Build topic list for topic0 (the event signature)
    or_topics = list(topics_of_interest.values())  # e.g. ["0x4a7a8a0f...", "0x1d25aa4f...", ...]

    # Grab logs
    chunk_logs = get_logs_for_range(current_start, current_end, or_topics)

    # Process logs
    for log in chunk_logs:
        topic0 = log['topics'][0].hex().lower()
        tx_hash = log['transactionHash'].hex()
        blknum = log['blockNumber']

        # Identify which event it matched
        matched_event = None
        sent_from = None
        for evt_name, evt_topic in topics_of_interest.items():
            # match value from the topics_of_interest with topic0
            if evt_topic[2:].lower() == topic0:
                matched_event = evt_name
                sent_from = log['address']
                if matched_event == "Rely":
                    val = log['data']
                    print(val)
                    try:
                        decoded_log = dummy_contract.events.Rely().process_log(log)
                    except Exception as e:
                        logging.warning(f"Error decoding log: {e}")
                        try:
                            decoded_log = dummy_contract.events.RelyAnon().process_log(log)
                        except Exception as e:
                            logging.error(f"Error decoding log: {e}")
                            logging.info(f"  Log data: {log['data'].hex()}")
                            # https://scan.mypinata.cloud/ipfs/bafybeih3olry3is4e4lzm7rus5l3h6zrphcal5a7ayfkhzm5oivjro2cp4/#/address/0xae3Bb3f970D5a9746D2575281731Bab65ABdcacC?tab=contract
                            continue
                    
                    address = decoded_log.args.usr
                    # infos = [int(decoded_log.args.val.hex(), 16)]

                logging.info(address)
                break

        logging.info(f"  Found event {matched_event} in TX 0x{tx_hash} at block {blknum}, sent from: {sent_from}")

    # Move to the next chunk
    current_start = current_end + 1

logging.info("Done scanning!")
