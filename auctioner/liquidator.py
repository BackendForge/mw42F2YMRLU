from web3 import Web3
import json
import os
from dotenv import load_dotenv
from eth_utils.address import to_checksum_address
import logging
from eth_account import Account
from web3.gas_strategies.rpc import rpc_gas_price_strategy

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set up both handlers
handlers = [logging.FileHandler("liquidator.log"), logging.StreamHandler()]

# Configure all handlers with same formatter
for h in handlers:
    h.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    logger.addHandler(h)
# Load environment variables from .env file
load_dotenv()

# Configuration: set your Infura URL and private key in your .env file.
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CUSTOM_LIQUIDATION_ADDRESS = os.getenv("CUSTOM_LIQUIDATION_ADDRESS")
DOG_ADDRESS = os.getenv("DOG_ADDRESS")
# Load the Vat contract ABI.
VAT_ABI = json.load(open("vat_abi.json"))
# Get the Vat contract address from environment variables.
VAT_ADDRESS = os.getenv("VAT_ADDRESS")


DOG_ABI = json.load(open("dog_abi.json"))
CLIPPER_ABI = json.load(open("clipper_abi.json"))
CUSTOM_LIQUIDATION_ABI = json.load(open("custom_liquidation_abi.json"))


# Load the CDP Manager contract ABI.
CDP_MANAGER_ABI = json.load(open("cdp_manager_abi.json"))

# Get the CDP Manager contract address from an environment variable.
CDP_MANAGER_ADDRESS = os.getenv("CDP_MANAGER_ADDRESS")

# Instantiate the CDP Manager contract.


addresses = json.load(open("pulsechain-addresses.json"))

# Initialize Web3 connection
web3 = Web3(Web3.HTTPProvider(RPC_URL))
web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

# Create account object from your private key
account = Account.from_key(PRIVATE_KEY)

dog_contract = web3.eth.contract(address=to_checksum_address(DOG_ADDRESS), abi=DOG_ABI)
vat_contract = web3.eth.contract(address=to_checksum_address(VAT_ADDRESS), abi=VAT_ABI)
cdp_manager = web3.eth.contract(
    address=to_checksum_address(CDP_MANAGER_ADDRESS), abi=CDP_MANAGER_ABI
)


class Liquidator:
    # Instantiate the Clipper contract

    def __init__(self, clipper_contract_address: str):
        self.clipper_contract_address = clipper_contract_address
        self.clipper_contract = web3.eth.contract(
            address=to_checksum_address(clipper_contract_address), abi=CLIPPER_ABI
        )
        self.custom_liquidation_contract = web3.eth.contract(
            address=CUSTOM_LIQUIDATION_ADDRESS, abi=CUSTOM_LIQUIDATION_ABI
        )

    # Fetch detailed auction information required for liquidation
    def get_auction_details(self, auction_id):
        details = self.clipper_contract.functions.sales(auction_id).call()
        # Check your ABI, typically:
        # [pos, tab, lot, usr, tic, top]
        return {
            "tab": details[1],
            "lot": details[2],
            "usr": details[3],
        }

    def get_active_auctions(self):
        """
        Fetches the list of active auction IDs from the Clipper contract.

        Returns:
            list: A list of active auction IDs.
        """
        auction_list = self.clipper_contract.functions.list().call()
        logging.info(f"Active Auctions IDs: {auction_list}")
        return auction_list

    # def trigger_liquidations(self, slice_amount, usr_address):
    #     """
    #     Iterates over active auctions to trigger liquidation via the Clipper contract.

    #     For each auction, the script:
    #     - Retrieves auction details to extract the 'tab' (debt) value.
    #     - Adjusts parameters as needed (here slice_amount is constant, but can be dynamic).
    #     - Builds, signs, and sends the transaction calling the `take` method.

    #     Parameters:
    #         slice_amount (int): The amount to slice from each auction.
    #         usr_address (str): The address to receive any benefits of the liquidation.
    #     """
    #     auctions = self.get_active_auctions()
    #     for auction_id in auctions:
    #         try:
    #             # Fetch auction details; typically, index [4] contains the 'tab' (debt) value.
    #             auction_details = self.clipper_contract.functions.sales(
    #                 auction_id
    #             ).call()
    #             tab_amount = auction_details[
    #                 4
    #             ]  # Verify this index with your ABI documentation

    #             # Build transaction to take the auction
    #             txn = self.clipper_contract.functions.take(
    #                 auction_id,
    #                 slice_amount,
    #                 tab_amount,
    #                 usr_address,
    #                 b"",  # Additional bytes data if required; otherwise empty
    #             ).build_transaction(
    #                 {
    #                     "from": account.address,
    #                     "nonce": web3.eth.get_transaction_count(account.address),
    #                     "gas": 800000,  # Adjust gas limit as needed
    #                     "gasPrice": web3.to_wei("30", "gwei"),
    #                 }
    #             )

    #             # Sign and send the transaction
    #             signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    #             logging.info(
    #                 f"Signing and sending transaction for auction {auction_id}..."
    #             )
    #             # txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    #             # receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    #             # logging.info(f"Liquidated auction {auction_id}: {receipt.transactionHash.hex()}")

    #         except Exception as e:
    #             logging.info(f"Error liquidating auction {auction_id}: {e}")

    def check_profitable(self, auction_id, slice_amount, min_profit_margin=0.1):
        """
        Checks if an auction is profitable for liquidation based on a profit margin.

        Profitability is defined as:
        (tab_amount - slice_amount) / tab_amount >= min_profit_margin

        Parameters:
            auction_id: The ID of the auction.
            slice_amount (int): The liquidation slice amount.
            min_profit_margin (float): The minimum acceptable profit margin (default is 10%).

        Returns:
            bool: True if the auction is profitable, False otherwise.
        """
        details = self.get_auction_details(auction_id)
        logging.info(f"Details: {details} for auction {auction_id}")

        tab_amount = details.get("tab", 0)
        if tab_amount <= 0:
            logging.warning(
                f"Auction {auction_id} has an invalid tab amount: {tab_amount}"
            )
            return False

        profit_margin = (tab_amount - slice_amount) / tab_amount
        if profit_margin >= min_profit_margin:
            logging.info(
                f"Auction {auction_id} is profitable: profit margin {profit_margin:.2%}"
            )
            return True
        else:
            logging.info(
                f"Auction {auction_id} is not profitable: profit margin {profit_margin:.2%}"
            )
            return False

    def calculate_slice_amount(self, auction_id, percentage=0.05):
        """
        Calculates the slice amount as a percentage of the auction's lot size.

        Parameters:
            auction_id (int): The auction ID.
            percentage (float): The fraction of the lot size to purchase (e.g., 0.05 for 5%).

        Returns:
            int: The calculated slice amount.
        """
        details = self.get_auction_details(auction_id)
        lot_size = details.get("lot", 0)
        if lot_size == 0:
            logging.warning(f"Auction {auction_id} has no lot size available.")
            return 0
        slice_amount = int(lot_size * percentage)
        logging.info(
            f"Calculated slice_amount for auction {auction_id}: {slice_amount}"
        )
        return slice_amount

    def check_whole_vault_profitable(
        self, auction_id, market_price, min_profit_margin=0.05
    ):
        """
        Checks if liquidating the entire vault (auction) is profitable.

        Profitability is determined by comparing the effective price (tab/lot)
        with the current market price of the collateral.

        Parameters:
            auction_id (int): The auction ID.
            market_price (float): The current market price of the collateral.
            min_profit_margin (float): Minimum acceptable profit margin (e.g., 0.05 for 5%).

        Returns:
            bool: True if liquidation is profitable, False otherwise.
        """
        details = self.get_auction_details(auction_id)
        logging.info(f"Auction {auction_id} details: {details}")

        tab = details.get("tab", 0)
        lot = details.get("lot", 0)

        if lot <= 0:
            logging.warning(f"Auction {auction_id} has an invalid lot size: {lot}")
            return False

        effective_price = (tab / lot) / 1e27
        profit_margin = (market_price - effective_price) / effective_price

        logging.info(
            f"Auction {auction_id}: Effective price = {effective_price:.4f}, "
            f"Market price = {market_price:.4f}, Profit margin = {profit_margin:.2%}"
        )

        if profit_margin >= min_profit_margin:
            logging.info(
                f"Auction {auction_id} is profitable to liquidate (profit margin {profit_margin:.2%})."
            )
            return True
        else:
            logging.info(
                f"Auction {auction_id} is not profitable (profit margin {profit_margin:.2%})."
            )
            return False

    def trigger_liquidation_via_custom_contract(
        self, auction_id, slice_amount, usr_address, collateral_price_in_dai
    ):
        if not self.check_whole_vault_profitable(auction_id, collateral_price_in_dai):
            logging.info(f"Auction {auction_id} is not profitable to liquidate.")
            return
        details = self.get_auction_details(auction_id)
        tab_amount = details["tab"]

        txn = self.custom_liquidation_contract.functions.triggerLiquidation(
            self.clipper_contract_address,  # address clipper
            auction_id,  # uint256 id
            slice_amount,  # uint256 slice
            tab_amount,  # uint256 tab
            usr_address,  # address usr
            b"",  # bytes calldata data
        ).build_transaction(
            {
                "to": self.clipper_contract_address,
                "from": account.address,
                "nonce": web3.eth.get_transaction_count(account.address),
                "gas": 1000000,
                "gasPrice": int(web3.eth.generate_gas_price() * 1.25),
                "chainId": 369,
            }
        )

        logging.info(f"Triggering liquidation for auction {auction_id}...")
        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        # txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        # receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        # logging.info(f"Liquidation executed for auction {auction_id}, transaction hash: {receipt.transactionHash.hex()}")

    @staticmethod
    def str_to_bytes32(text):
        return Web3.to_bytes(text.encode()).ljust(32, b"\0")

    def get_vault_details(self, vault_urn, ilk):
        """
        Fetches the details for a given vault from the MakerDAO Vat contract.

        Parameters:
            vault_id: The vault identifier (typically the urn address).
            ilk (bytes32 or str): The collateral type identifier, e.g., b"ETH-A" or its hex representation.

        Returns:
            dict: A dictionary with:
                - 'collateral': The collateral amount in wad (18 decimals).
                - 'debt': The actual debt in rad (45 decimals), computed as art * rate.
        """

        ilk_bytes = self.str_to_bytes32(ilk)
        # The Vat contract maintains vault state in the `urns` mapping:
        # urns(ilk, urn) returns a tuple (ink, art)
        #   - ink: collateral amount in wad (18 decimals)
        #   - art: normalized debt in wad (18 decimals)
        ink, art = vat_contract.functions.urns(
            ilk_bytes, to_checksum_address(vault_urn)
        ).call()

        # The Vat contract's ilks mapping stores parameters for each collateral type.
        # ilks(ilk) returns (Art, rate, spot, line, dust)
        # We're interested in the rate for converting art into actual debt.
        _, rate, _, _, dust = vat_contract.functions.ilks(ilk_bytes).call()

        # Calculate the actual debt in rad (45 decimals). This is done by:
        #   debt = art * rate
        # Remember, art and rate are in wad (18 decimals), so the product is in rad (45 decimals).
        debt = art * rate

        return {"collateral": ink, "debt": debt, "dust": dust}

    def get_vault_urn(self, vault_id):
        """
        Fetches the vault's urn address from the CDP Manager contract using the vault_id.

        Parameters:
            vault_id (int): The numeric vault ID.

        Returns:
            str: The checksummed urn address associated with the vault.
        """

        # Call the urns function with the vault_id.
        urn_address = cdp_manager.functions.urns(vault_id).call()
        return to_checksum_address(urn_address)

    def get_vault_discount_price(self, vault_id, ilk, market_price):
        """
        Computes the effective (discounted) price per collateral unit for a vault,
        and the discount percentage compared to the market price.

        Parameters:
            vault_id (int): The numeric vault ID.
            ilk (str): The collateral type (e.g., "ETH-A").
            market_price (float): Current market price in DAI per collateral unit.
            dog_contract: An instantiated Dog contract with the correct ABI.

        Returns:
            tuple: (effective_price, discount_percentage)
                - effective_price: The liquidation price per collateral unit in DAI.
                - discount_percentage: A number between 0 and 1 representing the discount.
                (If collateral is zero, returns (None, None)).
        """
        # 1. Get the vault's urn address and details from the Vat.
        vault_urn = self.get_vault_urn(vault_id)  # assumes you have this implemented
        details = self.get_vault_details(vault_urn, ilk)  # returns a dict with "collateral" and "debt"

        # Convert raw values:
        # Debt is stored in rad (45 decimals). Dividing by 1e27 brings it to wad (18 decimals)
        debt_wad = details["debt"] / 1e27  # debt in DAI (wad, 18 decimals)
        # Collateral is stored in wad (18 decimals)
        collateral_units = details["collateral"] / 1e18  # collateral amount in natural units

        if collateral_units <= 0:
            # Avoid division by zero and warn that there is no collateral backing the vault.
            logging.warning(f"Vault {vault_id} has zero collateral; cannot compute effective price.")
            return 0, 0

        # 2. Retrieve the liquidation bonus factor (chop) from the Dog contract.
        # Note: Check your ABI to see whether chop is at index 0 or 1.
        # For example, if the Dog contract's ilks() returns (chop, lump, dust, etc.),
        # adjust the index accordingly. Here we assume it is at index 0.
        dog_params = dog_contract.functions.ilks(self.str_to_bytes32(ilk)).call()
        chop = dog_params[1]  # if your ABI has chop at index 1, change this accordingly
        chop_float = chop / 1e18  # Convert from wad to a float (e.g., 1.13)

        # 3. Calculate the effective price per collateral unit.
        # Effective price = (debt * chop) / collateral
        effective_price = (debt_wad * chop_float) / collateral_units

        # 4. Calculate the discount percentage compared to the market price.
        discount_percentage = 1 - (effective_price / market_price)

        return effective_price, discount_percentage


    def scan_vaults_and_trigger_liquidation(
        self, vault_ids, ilk, collateral_price, liquidation_ratio
    ):
        """
        Scans a list of vaults for undercollateralization and triggers liquidation via dog.bark.

        Parameters:
          dog_contract_address (str): The Dog contract address.
          vault_ids (list): A list of vault IDs to scan.
          ilk (str or bytes): The collateral type identifier.
          collateral_price (float): Current market price of the collateral in DAI.
          liquidation_ratio (float): Minimum collateralization ratio (e.g., 1.5 for 150%).
        """

        for vault_id in vault_ids:
            vault_urn = self.get_vault_urn(vault_id)
            details = self.get_vault_details(vault_urn, ilk)
            if details is None:
                logging.warning(f"Vault {vault_id}: no details found.")
                continue

            # Adjust for Maker's internal decimals:
            #   - collateral is in wad (18 decimals)
            #   - debt is in rad (45 decimals), so divide by 1e27 to convert to wad-equivalent.
            collateral = details["collateral"]  # already in wad (18 decimals)
            debt = details["debt"] / 1e27  # now in wad (18 decimals)
            debt_readable = debt / 1e18  # now in DAI (18 decimals)
            dust_readable = details["dust"] / 1e45  # now in wad (18 decimals)

            effective_price, discount_percentage = self.get_vault_discount_price(
                vault_id, ilk, collateral_price
            )

            logging.info(
                f"Effective price for vault {vault_id}: {effective_price:.2f} DAI; discount: {discount_percentage:.2%}"
            )
            if effective_price > collateral_price:

                logging.warning(
                    f"Vault {vault_id} effective price is higher than market price; skipping."
                )
                continue

            if debt == 0:
                logging.warning(f"Vault {vault_id} has zero debt; skipping.")
                continue

            # Calculate collateralization ratio.
            # For instance, if the vault has 2,000 DAI debt and dust is 1,000 DAI,
            #  partially liquidating to 900 DAI leftover is not allowed.
            #  But if the vault owner pays down some debt first,
            #  partial liquidation might leave 1,100 DAI, which is above dust.
            coll_ratio = (collateral * effective_price) / debt
            logging.info(
                f"Vault {vault_id} collateralization ratio: {coll_ratio:.2f}; dust: {dust_readable:.2f}, debt: {debt_readable:.2f}"
            )
            if debt_readable > dust_readable:
                logging.warning(
                    f"Vault {vault_id} has debt above dust limit; skipping liquidation."
                )
                continue

            if coll_ratio < liquidation_ratio:
                # The vault is undercollateralized; trigger liquidation.
                try:
                    simulation = dog_contract.functions.bark(
                        self.str_to_bytes32(ilk), vault_urn, account.address
                    ).call()
                    logging.info(f"Simulation: {simulation}")
                    txn = dog_contract.functions.bark(
                        self.str_to_bytes32(ilk), vault_urn, account.address
                    ).build_transaction(
                        {
                            "from": account.address,
                            "nonce": web3.eth.get_transaction_count(account.address),
                            "gas": 800000,
                            "gasPrice": int(web3.eth.generate_gas_price() * 5),
                            "chainId": 369,
                        }
                    )
                    signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
                    logging.info(
                        f"Triggering liquidation for vault {vault_id} via dog.bark..."
                    )
                    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                    receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
                    logging.info(
                        f"Liquidation triggered for vault {vault_id}: {receipt.transactionHash.hex()}"
                    )
                except Exception as e:
                    logging.error(
                        f"Error triggering liquidation for vault {vault_id}: {e}"
                    )
            else:
                logging.info(
                    f"Vault {vault_id} is sufficiently collateralized; skipping liquidation."
                )


if __name__ == "__main__":
    # Example execution:
    # Define the slice amount based on your liquidation strategy.
    slice_amount = 1000  # Adjust as required
    usr_address = account.address  # Using our own address for liquidation benefits
    logging.info(f"Using account address: {usr_address}")
    vault_ids = [
        31067,
        31057,
        31050,
        30755,
        30823,
        30661,
        30584,
        30629,
        31054,
        30592,
        30598,
        30588,
        30595,
        30591,
        30607,
        30617,
        30636,
        30713,
        30970,
        31002,
        31004,
        31015,
        31017,
        31031,
        31036,
        31038,
        31040,
        30801,
        31053,
        30669,
        30687,
        30773,
        30789,
        30793,
        30835,
        30840,
        30870,
        30877,
        30884,
        30889,
        30896,
        30925,
        30932,
        30937,
        30944,
        30990,
        30993,
        30996,
        30999,
        31006,
        31009,
        31012,
        31019,
        31022,
        31025,
        31028,
        31033,
        31045,
        31048,
        31060,
        30653,
        31103,
        31070,
        30934,
        30946,
        31062,
        30790,
        30794,
        30836,
        30871,
        30878,
        30885,
        30890,
        30926,
        30938,
        30991,
        30994,
        31000,
        30997,
        31007,
        31010,
        31013,
        31020,
        31023,
        31026,
        31029,
        31043,
        31046,
        31049,
        31052,
        31055,
        30780,
        30618,
        30639,
        30604,
        30609,
        31058,
        31059,
        31063,
        31071,
        31072,
        31073,
        31075,
        31076,
        31078,
        30971,
        31005,
        31016,
        31018,
        31032,
        31039,
        31041,
        31003,
        31068,
        31069,
        31074,
        31081,
        31082,
        31083,
        31084,
        31085,
        31086,
        31087,
        31088,
        31089,
        31090,
        31092,
        31094,
        31095,
        31096,
        31097,
        31098,
        31099,
        31100,
        31101,
        31102,
        31080,
        30670,
        30671,
        30905,
        30630,
        31104,
        30662,
        30656,
        30912,
        30918,
        30824,
        30859,
        30864,
        30919,
        31021,
        30672,
        30673,
        30674,
        30675,
        30688,
        30689,
        30690,
        30691,
        30692,
        30693,
        30694,
        30695,
        30696,
        30697,
        30698,
        30699,
        30700,
        30701,
        30702,
        30703,
        30704,
        30705,
        30706,
        30707,
        30708,
        30709,
        30710,
        30711,
        30714,
        30715,
        30716,
        30717,
        30718,
        30719,
        30720,
        30721,
        30722,
        30723,
        30724,
        30725,
        30726,
        30756,
        30757,
        30774,
        30775,
        30776,
        30777,
        30778,
        30779,
        30782,
        30783,
        30791,
        30795,
        30802,
        30803,
        30804,
        30805,
        30806,
        30807,
        30808,
        30809,
        30810,
        30811,
        30812,
        30813,
        30814,
        30815,
        30837,
        30841,
        30843,
        30844,
        30845,
        30847,
        30849,
        30850,
        30851,
        30853,
        30855,
        30857,
        30858,
        30860,
        30861,
        30862,
        30872,
        30879,
        30886,
        30891,
        30897,
        30898,
        30899,
        30900,
        30901,
        30902,
        30903,
        30906,
        30907,
        30909,
        30913,
        30914,
        30920,
        30927,
        30939,
        30992,
        30995,
        30998,
        31001,
        31008,
        31011,
        31030,
        30784,
        30611,
        30608,
        30676,
        30677,
        30644,
        30664,
        31171,
        31199,
        33319,
        31109,
        31110,
        31125,
        31126,
        31127,
        31169,
        30582,
        30580,
        31200,
        33282,
        33298,
        33299,
        33340,
        33321,
        33312,
        31105,
        31106,
        31108,
        33353,
        33418,
        33419,
        33422,
    ]

    # 1. sort addresses items
    addresses = dict(sorted(addresses.items()))
    for name, address in addresses.items():
        if name.startswith("MCD_CLIP_ETH_A") and not name.startswith("MCD_CLIP_CALC"):
            # if name.startswith("MCD_CLIP_") and not name.startswith("MCD_CLIP_CALC"):
            logger.info(f"Processing {name} with address {address}")

            liquidator = Liquidator(address)
            #####
            auctions = liquidator.get_active_auctions()
            
            if not auctions:
                logger.info(f"No active auctions available for {name}")
            else:
                for auction_id in auctions:
                    try:
                        liquidator.trigger_liquidation_via_custom_contract(
                            auction_id, slice_amount, usr_address, 0.016141
                        )
                    except Exception as e:
                        logging.error(f"Error liquidating auction {auction_id}: {e}")
            #####
            liquidator.scan_vaults_and_trigger_liquidation(
                vault_ids, "ETH-A", 0.016, 1.5
            )

