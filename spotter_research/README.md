# Oracle research

1. [chainlog_discovery.py](chainlog_discovery.py) - script to discover the chainlog addresses of the MakerDAO Oracles. Assumes you have correct VAT address.
2. [chainlog.py](chainlog.py) - script to interact with the chainlog contract.
3. [find_dai_join.py](find_dai_join.py) - script to find the DAI join address. (requires the chain-log address)
4. [find_vat.py](find_vat.py) - script to find the VAT address. (requires the DAI join address)
5. [find_spotter.py](find_spotter.py) - script to find the spotter address. (requires the VAT address)
6. [spotter.py](spotter.py) - script to interact with the spotter contract.
7. [osm_read.py](osm_read.py) - script to read the price from the OSM contract.
8. [osm_poke.py](osm_poke.py) - script to poke the OSM contract.
9. [when_dog.py](when_dog.py) - script to find the when OSM address un/whitelisted on the Dog contract.
10. [spotter_read.py](spotter_read.py) - script to read the price from the spotter contract.
11. [spotter_check.py](spotter_check.py) - script to check if the spotter is connected to expected OSM.
12. [median_from_osm.py](median_from_osm.py) - script to find the median address from the OSM address.
13. [median_read.py](median_read.py) - script to read the price from the median contract.

## Chainlog - 0xdA0Ab1e0017DEbCd72Be8599041a2aa3bA7e740F

- DAI Token Address: 0x6B175474E89094C44Da98b954EedeAC495271d0F
- DaiJoin Address: 0x9759A6Ac90977b93B58547b4A71c78317f391A28
- Vat used by DaiJoin: 0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B

## Who can call peek()?

- MCD_SPOT (Spotter): Gets price for collateral
- MCD_DOG (Liquidator): Gets price during liquidation
- MCD_END (Shutdown): Gets price for shutdown accounting
- CLIPPERs: Use prices during auctions

Maker Keepers (external bots) watch prices via oracles like Median

They poke the OSM or update feeds (e.g., Median → OSM) via `poke()` function.

…it moves the `next()` price (pulled from the Median) into the `cur()` slot of the OSM.
This makes the price available to the system via `peek()` and `read()`.

                       +-------------------+
                       |    Median (ETH)   |
                       +-------------------+
                                |
                                |  <- updates every minute via keepers
                                v
+-------------------+    call   +-------------------+
|      Spotter      | <---------|       OSM         |
+-------------------+    peek() +-------------------+
                                |
                                |  <- updated once/hour via poke()
                                v
                       delayed price buffer

### OSM_DOG `0x135954d155898D42C90D2a57824C690e0c7BEf1B`

Normally, Dog (the liquidation engine) should be able to read the OSM price when triggering liquidations — it uses this price to verify whether a vault is undercollateralized.

### OSM_MOM `0x76416A4d5190d071bfed309861527431304aA14f`

Governance-owned manager that can whitelist contracts on OSMs (via kiss(address))

## What next?

Who is the `0x48Fc8b22ae5319786A8E25Ef49B1B49942000000` address?
