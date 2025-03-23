# mw42F2YMRLU

The Free Speech is being restored. Loading. . .

## How to

- install Python 3.11+
- install the required packages with `pip install -r requirements.txt`
- get `.env` ready, you can use `.env.example` as a template
- run the script with `python ilk_discovery.py`

## Extra stuff

Just enjoy, spread the love and the knowledge.

### Manually using the solidity contract with Maker

1. get underlying asset of the Ilk
2. open a vault -> save the address of the Vault

    ```bash
    SEND_MESSAGE_TO = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39"
    DATA = "0x6090dec54554482d42000000000000000000000000000000000000000000000000000000000000000000000000000000<YOUR_WALLET_ADDRESS>".lower()
    MAGIC_GAS = 313131
    ```

3. approve asset for the GEM-JOIN

    ```bash
    SEND_MESSAGE_TO = "0x2F0b23f53734252Bda2277357e97e1517d6B042A" # pWETH
    DATA = "0x3b4da69f000000000000000000000000<YOUR_VAULT_ADDRESS>00000000000000000000000000000000000000000000000be6092017967d0000".lower()
    MAGIC_GAS = 111111
    ```

4. send collateral to the vault

    ```bash
    SEND_MESSAGE_TO = "0x2F0b23f53734252Bda2277357e97e1517d6B042A"
    DATA = "0x3b4da69f000000000000000000000000<YOUR_VAULT_ADDRESS>00000000000000000000000000000000000000000000000be6092017967d0000".lower()
    MAGIC_GAS = 111111
    ```

5. Optional - lock asset in the GEM-JOIN
6. get vault ID - use `raw_reader.py`
7. deploy custom smart contract
8. cdpAllow your vault to be used by the custom smart contract

    ```bash
    SEND_MESSAGE_TO = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39"
    DATA = "0x0b63fb62000000000000000000000000000000000000000000000000000000000000827900000000000000000000000020231eB701a298fE84bD04d2966adecfBED131500000000000000000000000000000000000000000000000000000000000000001"
    MAGIC_GAS = 66666
    ```

9. DRIP (to Jug) - to refresh the stability fee

    ```bash
    SEND_MESSAGE_TO = "0x19c0976f590D67707E62397C87829d896Dc0f1F1"
    DATA = "0x44e2a5a84554482d42000000000000000000000000000000000000000000000000000000"
    MAGIC_GAS = 111111
    ```

10. Call `justBorrowAndExit` on the custom smart contract
11. Enjoy your DAI - don't forget to repay the debt!!!!
