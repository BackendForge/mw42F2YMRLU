import os
from web3 import Web3
from dotenv import load_dotenv
from eth_utils.address import to_checksum_address

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
# ILK_REGISTRY_ADDRESS = "0x5a464C28D19848f44199D003Be5D85Cc519f3163"
ILK_REGISTRY_ADDRESS = to_checksum_address("0x5a464c28d19848f44199d003bef5ecc87d090f87")
ILK_REGISTRY_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "vat_", "type": "address"},
            {"internalType": "address", "name": "dog_", "type": "address"},
            {"internalType": "address", "name": "cat_", "type": "address"},
            {"internalType": "address", "name": "spot_", "type": "address"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },  
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "ilk",
                "type": "bytes32",
            }
        ],
        "name": "AddIlk",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "usr",
                "type": "address",
            }
        ],
        "name": "Deny",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "what",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "data",
                "type": "address",
            },
        ],
        "name": "File",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "ilk",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "what",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "data",
                "type": "address",
            },
        ],
        "name": "File",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "ilk",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "what",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "data",
                "type": "uint256",
            },
        ],
        "name": "File",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "ilk",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "what",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "data",
                "type": "string",
            },
        ],
        "name": "File",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "ilk",
                "type": "bytes32",
            }
        ],
        "name": "NameError",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "usr",
                "type": "address",
            }
        ],
        "name": "Rely",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "ilk",
                "type": "bytes32",
            }
        ],
        "name": "RemoveIlk",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "ilk",
                "type": "bytes32",
            }
        ],
        "name": "SymbolError",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "ilk",
                "type": "bytes32",
            }
        ],
        "name": "UpdateIlk",
        "type": "event",
    },
    {
        "inputs": [{"internalType": "address", "name": "adapter", "type": "address"}],
        "name": "add",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "cat",
        "outputs": [
            {"internalType": "contract CatLike", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "class",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "count",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "dec",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "usr", "type": "address"}],
        "name": "deny",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "dog",
        "outputs": [
            {"internalType": "contract DogLike", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "ilk", "type": "bytes32"},
            {"internalType": "bytes32", "name": "what", "type": "bytes32"},
            {"internalType": "uint256", "name": "data", "type": "uint256"},
        ],
        "name": "file",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "ilk", "type": "bytes32"},
            {"internalType": "bytes32", "name": "what", "type": "bytes32"},
            {"internalType": "string", "name": "data", "type": "string"},
        ],
        "name": "file",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "what", "type": "bytes32"},
            {"internalType": "address", "name": "data", "type": "address"},
        ],
        "name": "file",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "ilk", "type": "bytes32"},
            {"internalType": "bytes32", "name": "what", "type": "bytes32"},
            {"internalType": "address", "name": "data", "type": "address"},
        ],
        "name": "file",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "gem",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "pos", "type": "uint256"}],
        "name": "get",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "ilkData",
        "outputs": [
            {"internalType": "uint96", "name": "pos", "type": "uint96"},
            {"internalType": "address", "name": "join", "type": "address"},
            {"internalType": "address", "name": "gem", "type": "address"},
            {"internalType": "uint8", "name": "dec", "type": "uint8"},
            {"internalType": "uint96", "name": "class", "type": "uint96"},
            {"internalType": "address", "name": "pip", "type": "address"},
            {"internalType": "address", "name": "xlip", "type": "address"},
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "symbol", "type": "string"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "info",
        "outputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "symbol", "type": "string"},
            {"internalType": "uint256", "name": "class", "type": "uint256"},
            {"internalType": "uint256", "name": "dec", "type": "uint256"},
            {"internalType": "address", "name": "gem", "type": "address"},
            {"internalType": "address", "name": "pip", "type": "address"},
            {"internalType": "address", "name": "join", "type": "address"},
            {"internalType": "address", "name": "xlip", "type": "address"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "join",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "list",
        "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "start", "type": "uint256"},
            {"internalType": "uint256", "name": "end", "type": "uint256"},
        ],
        "name": "list",
        "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "pip",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "pos",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "_ilk", "type": "bytes32"},
            {"internalType": "address", "name": "_join", "type": "address"},
            {"internalType": "address", "name": "_gem", "type": "address"},
            {"internalType": "uint256", "name": "_dec", "type": "uint256"},
            {"internalType": "uint256", "name": "_class", "type": "uint256"},
            {"internalType": "address", "name": "_pip", "type": "address"},
            {"internalType": "address", "name": "_xlip", "type": "address"},
            {"internalType": "string", "name": "_name", "type": "string"},
            {"internalType": "string", "name": "_symbol", "type": "string"},
        ],
        "name": "put",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "usr", "type": "address"}],
        "name": "rely",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "remove",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "removeAuth",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "spot",
        "outputs": [
            {"internalType": "contract SpotLike", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "update",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "vat",
        "outputs": [
            {"internalType": "contract VatLike", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "wards",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "xlip",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]
VAT_ABI = [
    {
        "inputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": True,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes4",
                "name": "sig",
                "type": "bytes4",
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "arg1",
                "type": "bytes32",
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "arg2",
                "type": "bytes32",
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "arg3",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "data",
                "type": "bytes",
            },
        ],
        "name": "LogNote",
        "type": "event",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "Line",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [],
        "name": "cage",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "address", "name": "", "type": "address"},
        ],
        "name": "can",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "dai",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "debt",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "usr", "type": "address"}],
        "name": "deny",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "bytes32", "name": "ilk", "type": "bytes32"},
            {"internalType": "bytes32", "name": "what", "type": "bytes32"},
            {"internalType": "uint256", "name": "data", "type": "uint256"},
        ],
        "name": "file",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "bytes32", "name": "what", "type": "bytes32"},
            {"internalType": "uint256", "name": "data", "type": "uint256"},
        ],
        "name": "file",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "bytes32", "name": "ilk", "type": "bytes32"},
            {"internalType": "address", "name": "src", "type": "address"},
            {"internalType": "address", "name": "dst", "type": "address"},
            {"internalType": "uint256", "name": "wad", "type": "uint256"},
        ],
        "name": "flux",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "bytes32", "name": "i", "type": "bytes32"},
            {"internalType": "address", "name": "u", "type": "address"},
            {"internalType": "int256", "name": "rate", "type": "int256"},
        ],
        "name": "fold",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "bytes32", "name": "ilk", "type": "bytes32"},
            {"internalType": "address", "name": "src", "type": "address"},
            {"internalType": "address", "name": "dst", "type": "address"},
            {"internalType": "int256", "name": "dink", "type": "int256"},
            {"internalType": "int256", "name": "dart", "type": "int256"},
        ],
        "name": "fork",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "bytes32", "name": "i", "type": "bytes32"},
            {"internalType": "address", "name": "u", "type": "address"},
            {"internalType": "address", "name": "v", "type": "address"},
            {"internalType": "address", "name": "w", "type": "address"},
            {"internalType": "int256", "name": "dink", "type": "int256"},
            {"internalType": "int256", "name": "dart", "type": "int256"},
        ],
        "name": "frob",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "address", "name": "", "type": "address"},
        ],
        "name": "gem",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "bytes32", "name": "i", "type": "bytes32"},
            {"internalType": "address", "name": "u", "type": "address"},
            {"internalType": "address", "name": "v", "type": "address"},
            {"internalType": "address", "name": "w", "type": "address"},
            {"internalType": "int256", "name": "dink", "type": "int256"},
            {"internalType": "int256", "name": "dart", "type": "int256"},
        ],
        "name": "grab",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "uint256", "name": "rad", "type": "uint256"}],
        "name": "heal",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "usr", "type": "address"}],
        "name": "hope",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "ilks",
        "outputs": [
            {"internalType": "uint256", "name": "Art", "type": "uint256"},
            {"internalType": "uint256", "name": "rate", "type": "uint256"},
            {"internalType": "uint256", "name": "spot", "type": "uint256"},
            {"internalType": "uint256", "name": "line", "type": "uint256"},
            {"internalType": "uint256", "name": "dust", "type": "uint256"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "bytes32", "name": "ilk", "type": "bytes32"}],
        "name": "init",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "live",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "src", "type": "address"},
            {"internalType": "address", "name": "dst", "type": "address"},
            {"internalType": "uint256", "name": "rad", "type": "uint256"},
        ],
        "name": "move",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "usr", "type": "address"}],
        "name": "nope",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"internalType": "address", "name": "usr", "type": "address"}],
        "name": "rely",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "sin",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "bytes32", "name": "ilk", "type": "bytes32"},
            {"internalType": "address", "name": "usr", "type": "address"},
            {"internalType": "int256", "name": "wad", "type": "int256"},
        ],
        "name": "slip",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"internalType": "address", "name": "u", "type": "address"},
            {"internalType": "address", "name": "v", "type": "address"},
            {"internalType": "uint256", "name": "rad", "type": "uint256"},
        ],
        "name": "suck",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "address", "name": "", "type": "address"},
        ],
        "name": "urns",
        "outputs": [
            {"internalType": "uint256", "name": "ink", "type": "uint256"},
            {"internalType": "uint256", "name": "art", "type": "uint256"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "vice",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "wards",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
vat = w3.eth.contract(
    address=to_checksum_address("0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b"),
    abi=VAT_ABI,
)
registry = w3.eth.contract(address=ILK_REGISTRY_ADDRESS, abi=ILK_REGISTRY_ABI)
all_ilks_bytes = registry.functions.list().call()


# Convert bytes32 to human-readable format
all_ilks = [Web3.to_text(ilk).replace("\x00", "") for ilk in all_ilks_bytes]
print(f"Active Ilks: {all_ilks}")



def get_ilk_bytes(ilk: str) -> bytes:
    return Web3.to_bytes(text=ilk).ljust(32, b"\x00")

def get_ilk_details(ilk_bytes: bytes):
    # Call the info() function with the correct ilk
    extra_info = {}
    try:
        ilk_info = registry.functions.info(ilk_bytes).call()

        # Print results
        print(f"Collateral token (gem): {ilk_info[0]}")
        # print(f"Price feed (pip): {ilk_info[1]}")
        print(f"Is Live: {ilk_info[2]}")
        print(f"Decimals: {ilk_info[3]}")
        print(f"Address: {ilk_info[4]}\n")    
    except Exception as e:
        print(f"Error fetching extra info for {ilk}: {e}")
    else:
        extra_info = {
            "collateral_token": ilk_info[0],
            "is_live": ilk_info[2],
            "decimals": ilk_info[3],
            "address": ilk_info[4],
        }
    Art, rate, spot, line, dust = vat.functions.ilks(ilk_bytes).call()
    return {
        "total_debt": Art / 1e18,
        "stability_fee": (rate / 1e27 - 1) * 100,  # APR %
        "liquidation_ratio": 1 / (spot / 1e27),  # e.g., 1.5 → 150%
        "debt_ceiling": line / 1e45,
        "dust_limit": dust / 1e45,
        **extra_info,
    }


for ilk in all_ilks:
    try:
        ilk_bytes = get_ilk_bytes(ilk)
        details = get_ilk_details(ilk_bytes)
        
    except Exception as e:
        print(f"Error fetching details for {ilk}: {e}")
        continue
    print(f"Ilk: {ilk}")
    print(f"Details: {details}")
    print()


def extract_ilks_from_logs():
    ilk_set = set()
    events = w3.eth.get_logs(
        {
            "fromBlock": 8_000_000,
            "toBlock": "latest",
            "address": to_checksum_address(
                "0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b"
            ),
            "topics": [
                "0x7cdd3fde00000000000000000000000000000000000000000000000000000000"
            ],
        }
    )

    for event in events:
        # Ilk is in topic[1], padded to 32 bytes
        ilk_bytes = event["topics"][1]
        ilk = Web3.to_text(ilk_bytes).replace("\x00", "")
        ilk_set.add(ilk)

    return list(ilk_set)


# a = extract_ilks_from_logs()
# print(f"Active Ilks from logs: {a}")
