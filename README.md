# mw42F2YMRLU

The Free Speech HAS NOT BEEN restored. I have been lied to, deceived with hope and dreams.

Unfortunately, my further research and investigation within the MakerDao protocol deployed on the PulseChain shows me more evidence, that the protocol is not fully decentralized and the governance is not fully transparent.

There are many things that do not add up:

- Oracles - haven't dig deep enough, which are used and which LPs are used by the Oracles
- Vaults - PLS = pWETH 1:1 (sending PLS to pWETH address, returns pWETH in that amount) - arbitrage via borrowing DAI - is that why all `ETH` ilks are fully in debt?
- stETH - same as above, PLS = stETH 1:1. you can literally MINT stETH and borrow DAI against it. Currently fully utilized in the Maker protocol
- whenever price of asset seen in the vault (as a collateral) is higher than the price of the asset in the market, there is an arbitrage opportunity (BUY in the market, MINT in the vault, BORROW DAI, SELL in the market, REPAY DAI, EXIT the vault, PROFIT)
- can you flash loan via other protocols and use the DAI to repay the debt in the Maker protocol?

## On going investigation

- [x] what is sDAI?
- [ ] Oracles used for the protocol, to define ratios with pDAI (Spotter, Median) - how are they calculated?

### Research

- sDAI - coin created by the `https://sparkswap.xyz/`, supposed role 1:1 with eDAI. example arbitrage transaction: `0x2a7eeced336e1a70aeb0e8f9b7437b3fe12f2230d8e127d670a86ad2dae43a22`

`0x30FCB23A906493371b1721C8feb8815804808D74` - sDAI

OSM - Oracle Security Module

The Oracle Security Module (OSM) is a protective delay buffer between MakerDAO's real-time oracles (e.g. Median) and the rest of the protocol (like Spotter and Liquidation Engine).
It holds the "next" price, and updates it once per hour to allow governance actions or pauses before reacting to volatile price changes.

## How to run the script

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
