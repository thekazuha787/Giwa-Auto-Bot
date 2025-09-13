from web3 import Web3
from web3.exceptions import TransactionNotFound
from eth_account import Account
from aiohttp import ClientResponseError, ClientSession, ClientTimeout, BasicAuth
from datetime import datetime
from colorama import *
import asyncio, random, re, os, pytz
from tabulate import tabulate
import sys
import json

wib = pytz.timezone('Asia/Jakarta')

class Giwa:
    def __init__(self) -> None:
        self.L1_NETWORK = {
            "name": "Sepolia ETH",
            "rpc_url": "https://ethereum-sepolia-rpc.publicnode.com",
            "explorer": "https://sepolia.etherscan.io/tx/",
            "contract": "0x956962C34687A954e611A83619ABaA37Ce6bC78A",
            "abi": [
                {
                    "type": "function",
                    "name": "depositTransaction",
                    "stateMutability": "payable",
                    "inputs": [
                        { "internalType": "address", "name": "_to", "type": "address" },
                        { "internalType": "uint256", "name": "_value", "type": "uint256" },
                        { "internalType": "uint64", "name": "_gasLimit", "type": "uint64" },
                        { "internalType": "bool", "name": "_isCreation", "type": "bool" },
                        { "internalType": "bytes", "name": "_data", "type": "bytes" }
                    ],
                    "outputs": []
                }
            ]
        }
        self.L2_NETWORK = {
            "name": "Giwa Sepolia",
            "rpc_url": "https://sepolia-rpc.giwa.io",
            "explorer": "https://sepolia-explorer.giwa.io/tx/",
            "contract": "0x4200000000000000000000000000000000000016",
            "abi": [
                {
                    "type": "function",
                    "name": "initiateWithdrawal",
                    "stateMutability": "payable",
                    "inputs": [
                        { "internalType": "address", "name": "_target", "type": "address" },
                        { "internalType": "uint256", "name": "_gasLimit", "type": "uint256" },
                        { "internalType": "bytes", "name": "_data", "type": "bytes" }
                    ],
                    "outputs": []
                }
            ]
        }
        self.bridge_count = 1      # Default
        self.bridge_amount = 0.0001  # Default
        self.min_delay = 1         # Default
        self.max_delay = 3         # Default

        # Updated menu options with new Send ERC20 Random option
        self.menu_options = [
            {"label": "Bridge Sepolia → Giwa", "value": 1},
            {"label": "Bridge Giwa → Sepolia", "value": 2},
            {"label": "Random Bridge", "value": 3},
            {"label": "Deploy GMONChain", "value": 4},
            {"label": "Deploy Smart Contract (Owlto)", "value": 5},
            {"label": "Deploy ERC20 Token (Factory)", "value": 6},
            {"label": "Mint OmniHub NFT", "value": 7},
            {"label": "Send ERC20 Random", "value": 8},  # New option
            {"label": "Set Transaction Count & Amount", "value": 9},
            {"label": "Auto All (Run All Accounts)", "value": 10},
            {"label": "Exit", "value": 11}
        ]

        self.owlto_hex_data = "0x60806040527389a512a24e9d63e98e41f681bf77f27a7ef89eb76000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163460405161009f90610185565b60006040518083038185875af1925050503d80600081146100dc576040519150601f19603f3d011682016040523d82523d6000602084013e6100e1565b606091505b5050905080610125576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161011c9061019a565b60405180910390fd5b506101d6565b60006101386007836101c5565b91507f4661696c757265000000000000000000000000000000000000000000000000006000830152602082019050919050565b60006101786000836101ba565b9150600082019050919050565b60006101908261016b565b9150819050919050565b600060208201905081810360008301526101b38161012b565b9050919050565b600081905092915050565b600082825260208201905092915050565b603f806101e46000396000f3fe6080604052600080fdfea264697066735822122095fed2c557b62b9f55f8b3822b0bdc6d15fd93abb95f37503d3f788da6cbb30064736f6c63430008000033"
        
        # Token Factory Contract Details
        self.token_factory_address = "0x6BeC646B360e0F054FD833EDD56BC9289F0a60CA"
        self.deployment_fee = Web3.to_wei(0.001, "ether")
        self.factory_abi = [
            {
                "type": "function",
                "name": "createToken",
                "stateMutability": "payable",
                "inputs": [
                    {"name": "n", "type": "string"},
                    {"name": "s", "type": "string"},
                    {"name": "d", "type": "uint8"},
                    {"name": "humanSupply", "type": "uint256"}
                ],
                "outputs": [{"name": "tokenAddr", "type": "address"}]
            },
            {
                "type": "event",
                "name": "TokenCreated",
                "inputs": [
                    {"indexed": True, "name": "creator", "type": "address"},
                    {"indexed": False, "name": "token", "type": "address"},
                    {"indexed": False, "name": "name", "type": "string"},
                    {"indexed": False, "name": "symbol", "type": "string"},
                    {"indexed": False, "name": "decimals", "type": "uint8"},
                    {"indexed": False, "name": "supply", "type": "uint256"}
                ],
                "anonymous": False
            }
        ]
        
        # ERC20 ABI for sending tokens
        self.erc20_abi = [
            {
                "constant": True,
                "inputs": [],
                "name": "name",
                "outputs": [{"name": "", "type": "string"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "symbol",
                "outputs": [{"name": "", "type": "string"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [{"name": "owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "", "type": "uint256"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            },
            {
                "constant": False,
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "value", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"name": "", "type": "bool"}],
                "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        
        self.gmon_factory = "0xa3d9fbd0edb10327ecb73d2c72622e505df468a2"
        self.gmon_selector = "0x775c300c"
        self.gmon_value = Web3.to_wei(0.000035, "ether")
        self.omnihub_nft_contract = "0x5893B6684057eaBDeCB400526C8410EAFca6d541"
        self.omnihub_mint_data = "0xa25ffea800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
        self.omnihub_mint_value = Web3.to_wei(0.001, "ether")
        self.nft_abi = [
            {
                "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            }
        ]

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self):
        banner_lines = [
            f"{Fore.GREEN + Style.BRIGHT}██████╗ ██╗██╗    ██╗ █████╗ {Style.RESET_ALL}",
            f"{Fore.GREEN + Style.BRIGHT}██╔════╝ ██║██║    ██║██╔══██╗{Style.RESET_ALL}",
            f"{Fore.GREEN + Style.BRIGHT}██║  ███╗██║██║ █╗ ██║███████║{Style.RESET_ALL}",
            f"{Fore.GREEN + Style.BRIGHT}██║   ██║██║██║███╗██║██╔══██║{Style.RESET_ALL}",
            f"{Fore.GREEN + Style.BRIGHT}╚██████╔╝██║╚███╔███╔╝██║  ██║{Style.RESET_ALL}",
            f"{Fore.GREEN + Style.BRIGHT} ╚═════╝ ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝{Style.RESET_ALL}",
            "",
            f"{Fore.BLUE + Style.BRIGHT}         LETS FUCK THIS TESTNET BY KAZUHA787       {Style.RESET_ALL}",
            f"{Fore.YELLOW + Style.BRIGHT}  Giwa - Testnet - Bot v2.0 - CREATED BY KAZUHA     {Style.RESET_ALL}",
            ""
        ]
        for line in banner_lines:
            print(line)

    def display_menu(self):
        print(f"\n{Fore.CYAN + Style.BRIGHT}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW + Style.BRIGHT}Main Menu:{Style.RESET_ALL}")
        print(f"{Fore.CYAN + Style.BRIGHT}{'=' * 50}{Style.RESET_ALL}")
        
        for option in self.menu_options:
            print(f"{Fore.GREEN + Style.BRIGHT}{option['value']}. {Style.RESET_ALL}{option['label']}")
        
        print(f"{Fore.CYAN + Style.BRIGHT}{'=' * 50}{Style.RESET_ALL}")

    def format_log_message(self, message):
        name = "Unknown"
        if "| AccountName:" in message:
            parts = message.split("| AccountName:")
            name_part = parts[1].split("|", 1)[0].strip()
            name = name_part
            message = parts[0] + "|".join(parts[1].split("|")[1:]) if len(parts) > 1 else parts[0]

        if "Tx Hash:" in message:
            parts = message.split("Tx Hash:")
            return f"{Fore.CYAN + Style.BRIGHT}[ {name} ]{Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{parts[0]}Tx Hash:{Fore.GREEN + Style.BRIGHT}{parts[1]}{Style.RESET_ALL}"
        
        elif "Explorer:" in message:
            parts = message.split("Explorer:")
            return f"{Fore.CYAN + Style.BRIGHT}[ {name} ]{Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{parts[0]}Explorer:{Fore.GREEN + Style.BRIGHT}{parts[1]}{Style.RESET_ALL}"
        
        elif "Success" in message or "successful" in message or "Confirmed" in message:
            return f"{Fore.GREEN + Style.BRIGHT}[ {name} ] | {message}{Style.RESET_ALL}"
        
        elif "Warning" in message or "Insufficient" in message:
            return f"{Fore.YELLOW + Style.BRIGHT}[ {name} ] | {message}{Style.RESET_ALL}"
        
        elif "Error" in message or "Failed" in message:
            return f"{Fore.RED + Style.BRIGHT}[ {name} ] | {message}{Style.RESET_ALL}"
        
        elif "Processing" in message or "Starting" in message:
            return f"{Fore.MAGENTA + Style.BRIGHT}[ {name} ] | {message}{Style.RESET_ALL}"
        
        else:
            return f"{Fore.CYAN + Style.BRIGHT}[ {name} ]{Style.RESET_ALL}{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}"

    def log(self, message, name=None):
        if name:
            message = f"{message} | AccountName: {name}"
        print(self.format_log_message(message), flush=True)

    def welcome(self):
        self.clear_terminal()
        self.display_banner()

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def format_number(self, num, decimals=4):
        return f"{float(num):.{decimals}f}"
        
    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address
            return address
        except Exception as e:
            return None
        
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account
        except Exception as e:
            return None
    
    def get_short_address(self, address):
        return f"{address[:6]}...{address[-4:]}" if address else "N/A"

    def save_token_to_json(self, token_data):
        """Save token details to tokens.json file"""
        try:
            # Load existing data
            if os.path.exists('tokens.json'):
                with open('tokens.json', 'r') as f:
                    tokens = json.load(f)
            else:
                tokens = []
            
            # Add new token
            tokens.append(token_data)
            
            # Save updated data
            with open('tokens.json', 'w') as f:
                json.dump(tokens, f, indent=4)
            
            self.log(f"Token details saved to tokens.json", name="System")
        except Exception as e:
            self.log(f"Error saving token to JSON: {str(e)}", name="System")

    async def get_web3_with_check(self, address: str, network: dict, retries=3, timeout=60):
        request_kwargs = {"timeout": timeout}

        for attempt in range(retries):
            try:
                web3 = Web3(Web3.HTTPProvider(network["rpc_url"], request_kwargs=request_kwargs))
                web3.eth.get_block_number()
                return web3
            except Exception as e:
                if attempt < retries:
                    await asyncio.sleep(3)
                    continue
                raise Exception(f"Failed to Connect to RPC: {str(e)}")
        
    async def get_token_balance(self, address: str, network: dict):
        try:
            web3 = await self.get_web3_with_check(address, network)

            balance = web3.eth.get_balance(address)
            token_balance = balance / (10**18)

            return token_balance
        except Exception as e:
            self.log(f"Error: {str(e)}", name="System")
            return None
        
    async def send_raw_transaction_with_retries(self, account, web3, tx, retries=5):
        for attempt in range(retries):
            try:
                signed_tx = web3.eth.account.sign_transaction(tx, account)
                raw_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                tx_hash = web3.to_hex(raw_tx)
                return tx_hash
            except TransactionNotFound:
                pass
            except Exception as e:
                pass
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Hash Not Found After Maximum Retries")

    async def wait_for_receipt_with_retries(self, web3, tx_hash, retries=5):
        for attempt in range(retries):
            try:
                receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
                return receipt
            except TransactionNotFound:
                pass
            except Exception as e:
                pass
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Receipt Not Found After Maximum Retries")
    
    async def perform_deposit(self, account: str, address: str, network: dict):
        try:
            web3 = await self.get_web3_with_check(address, network)

            amount_to_wei = web3.to_wei(self.bridge_amount, "ether")

            token_contract = web3.eth.contract(address=web3.to_checksum_address(network["contract"]), abi=network["abi"])
            deposit_data = token_contract.functions.depositTransaction(address, amount_to_wei, 21000, False, b'')

            estimated_gas = deposit_data.estimate_gas({"from":address, "value":amount_to_wei})
            max_priority_fee = web3.to_wei(0.001, "gwei")
            max_fee = max_priority_fee

            deposit_tx = deposit_data.build_transaction({
                "from": address,
                "value": amount_to_wei,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, deposit_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)

            block_number = receipt.blockNumber

            return tx_hash, block_number

        except Exception as e:
            return None, None
    
    async def perform_withdraw(self, account: str, address: str, network: dict):
        try:
            web3 = await self.get_web3_with_check(address, network)

            amount_to_wei = web3.to_wei(self.bridge_amount, "ether")

            token_contract = web3.eth.contract(address=web3.to_checksum_address(network["contract"]), abi=network["abi"])
            withdraw_data = token_contract.functions.initiateWithdrawal(address, 21000, b'')

            estimated_gas = withdraw_data.estimate_gas({"from":address, "value":amount_to_wei})
            max_priority_fee = web3.to_wei(0.001, "gwei")
            max_fee = max_priority_fee

            withdraw_tx = withdraw_data.build_transaction({
                "from": address,
                "value": amount_to_wei,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, withdraw_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)

            block_number = receipt.blockNumber

            return tx_hash, block_number

        except Exception as e:
            return None, None

    async def deploy_contract(self, account: str, address: str, bytecode: str, value_wei: int = 0, gas_limit: int = 2000000, wait_receipt: bool = True):
        try:
            web3 = await self.get_web3_with_check(address, self.L2_NETWORK)

            nonce = web3.eth.get_transaction_count(address, "pending")
            gas_price = web3.eth.gas_price

            tx = {
                'from': address,
                'nonce': nonce,
                'gasPrice': gas_price,
                'gas': gas_limit,
                'to': None,
                'value': value_wei,
                'data': bytecode,
                'chainId': web3.eth.chain_id,
            }

            signed_tx = web3.eth.account.sign_transaction(tx, account)
            tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_tx.raw_transaction))

            if wait_receipt:
                receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
                if receipt.status == 1 and receipt.contractAddress:
                    return tx_hash, receipt.contractAddress, receipt.blockNumber
                else:
                    raise Exception(f"Deployment failed")
            else:
                return tx_hash, None, None

        except Exception as e:
            return None, None, None

    async def deploy_token_factory(self, account: str, address: str, name: str, symbol: str, decimals: int = 18, supply: int = 1000000):
        """Deploy ERC20 token using factory contract"""
        try:
            web3 = await self.get_web3_with_check(address, self.L2_NETWORK)
            
            # Factory contract
            factory_contract = web3.eth.contract(
                address=web3.to_checksum_address(self.token_factory_address), 
                abi=self.factory_abi
            )
            
            # Build transaction
            tx_data = factory_contract.functions.createToken(
                name,
                symbol,
                decimals,
                supply
            ).build_transaction({
                'from': address,
                'value': self.deployment_fee,
                'nonce': web3.eth.get_transaction_count(address, 'pending'),
                'gasPrice': web3.eth.gas_price,
                'chainId': web3.eth.chain_id
            })
            
            # Estimate gas
            try:
                estimated_gas = web3.eth.estimate_gas(tx_data)
                tx_data['gas'] = int(estimated_gas * 1.2)
            except:
                tx_data['gas'] = 3000000
            
            # Send transaction
            tx_hash = await self.send_raw_transaction_with_retries(account, web3, tx_data)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            
            # Extract token address from logs
            token_address = None
            if receipt and receipt.logs:
                for log in receipt.logs:
                    try:
                        decoded = factory_contract.events.TokenCreated().process_log(log)
                        if decoded:
                            token_address = decoded['args']['token']
                            break
                    except:
                        continue
            
            return tx_hash, token_address, receipt.blockNumber if receipt else None
            
        except Exception as e:
            self.log(f"Token deployment error: {str(e)}", name="System")
            return None, None, None

    async def call_contract(self, account: str, address: str, to: str, data: str, value_wei: int = 0, gas_limit: int = 350000, wait_receipt: bool = False):
        try:
            web3 = await self.get_web3_with_check(address, self.L2_NETWORK)

            nonce = web3.eth.get_transaction_count(address, "pending")
            gas_price = web3.eth.gas_price

            tx = {
                'from': address,
                'nonce': nonce,
                'gasPrice': gas_price,
                'gas': gas_limit,
                'to': web3.to_checksum_address(to),
                'value': value_wei,
                'data': data,
                'chainId': web3.eth.chain_id,
            }

            signed_tx = web3.eth.account.sign_transaction(tx, account)
            tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_tx.raw_transaction))

            if wait_receipt:
                receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
                return tx_hash, receipt.blockNumber if receipt else None
            else:
                return tx_hash, None

        except Exception as e:
            return None, None

    async def get_nft_balance(self, address: str, contract: str):
        try:
            web3 = await self.get_web3_with_check(address, self.L2_NETWORK)
            nft_contract = web3.eth.contract(address=web3.to_checksum_address(contract), abi=self.nft_abi)
            balance = nft_contract.functions.balanceOf(address).call()
            return balance
        except Exception as e:
            return None
        
    async def print_timer(self):
        delay_time = random.randint(self.min_delay, self.max_delay)
        for remaining in range(delay_time, 0, -1):
            print(
                f"{Fore.CYAN + Style.BRIGHT}[ System ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Wait For{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Seconds For Next Tx...{Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            await asyncio.sleep(1)
        print(" " * 80, end="\r")

    def request_input(self, prompt_text, input_type="text", default_value=""):
        while True:
            try:
                value = input(f"{Fore.GREEN + Style.BRIGHT}{prompt_text}{f' [{default_value}]' if default_value else ''}: {Style.RESET_ALL}").strip()
                
                if value == "" and default_value != "":
                    value = default_value
                
                if input_type == "number":
                    value = float(value) if '.' in value else int(value)
                    if value <= 0:
                        print(f"{Fore.RED + Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
                        continue
                
                return value
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Please enter a valid {input_type}.{Style.RESET_ALL}")
                continue
            except KeyboardInterrupt:
                print(f"\n{Fore.RED + Style.BRIGHT}Operation cancelled.{Style.RESET_ALL}")
                sys.exit(0)

    def configure_transaction_settings(self):
        """New function to set transaction count, amount, and delays"""
        print(f"\n{Fore.CYAN + Style.BRIGHT}=== Configure Transaction Settings ==={Style.RESET_ALL}")
        
        # Bridge count
        bridge_count = self.request_input("Enter number of transactions per account", "number", str(self.bridge_count))
        self.bridge_count = int(bridge_count)
        
        # Bridge amount
        bridge_amount = self.request_input("Enter ETH amount per bridge (e.g., 0.0001)", "number", str(self.bridge_amount))
        self.bridge_amount = float(bridge_amount)
        
        # Min delay
        min_delay = self.request_input("Enter minimum delay between transactions (seconds)", "number", str(self.min_delay))
        self.min_delay = int(min_delay)
        
        # Max delay
        max_delay = self.request_input("Enter maximum delay between transactions (seconds)", "number", str(self.max_delay))
        self.max_delay = int(max_delay)
        
        print(f"\n{Fore.GREEN + Style.BRIGHT}✓ Settings Updated:{Style.RESET_ALL}")
        print(f"   Transactions: {self.bridge_count}")
        print(f"   Amount: {self.bridge_amount} ETH")
        print(f"   Delay: {self.min_delay}-{self.max_delay} seconds")
        input(f"\n{Fore.YELLOW + Style.BRIGHT}Press Enter to continue...{Style.RESET_ALL}")

    def get_erc20_details(self):
        name = self.request_input("Token Name", default_value="kazuha787")
        symbol = self.request_input("Token Symbol", default_value="kazuha")
        decimals = self.request_input("Token Decimals", "number", default_value="18")
        supply = self.request_input("Total Supply", "number", default_value="1000000")
        return name, symbol, int(decimals), int(supply)

    def print_question(self):
        while True:
            self.welcome()
            self.display_menu()
            
            try:
                option = self.request_input(f"Select an option (1-{len(self.menu_options)})", "number")
                
                if option < 1 or option > len(self.menu_options):
                    print(f"{Fore.RED + Style.BRIGHT}Please enter a number between 1 and {len(self.menu_options)}.{Style.RESET_ALL}")
                    import time
                    time.sleep(2)
                    continue
                
                # Handle exit
                if option == 11:
                    self.log("Exiting...")
                    import time
                    time.sleep(1)
                    sys.exit(0)
                
                # Handle transaction settings
                if option == 9:
                    self.configure_transaction_settings()
                    continue
                
                # Handle Auto All
                if option == 10:
                    return option
                
                # For other options, ask for count if needed (options 1-8)
                if option in [1, 2, 3, 4, 5, 6, 7, 8]:
                    print(f"\n{Fore.GREEN + Style.BRIGHT}Option {option} Selected.{Style.RESET_ALL}")
                    print(f"{Fore.CYAN + Style.BRIGHT}Current Settings:{Style.RESET_ALL}")
                    print(f"   Transactions: {self.bridge_count}")
                    print(f"   Amount: {self.bridge_amount} ETH")
                    print(f"   Delay: {self.min_delay}-{self.max_delay} seconds\n")
                    
                    confirm = self.request_input("Use these settings? (y/n)", default_value="y").lower()
                    if confirm != "y":
                        self.configure_transaction_settings()
                    
                    return option
                    
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Please enter a number.{Style.RESET_ALL}")
                import time
                time.sleep(2)
        
    async def process_perform_deposit(self, account: str, address: str, network: dict, custom_name: str):
        tx_hash, block_number = await self.perform_deposit(account, address, network)
        if tx_hash and block_number:
            self.log(f"Success: Deposit confirmed", name=custom_name)
            self.log(f"Block: {block_number}", name=custom_name)
            self.log(f"Tx Hash: {tx_hash}", name=custom_name)
            self.log(f"Explorer: {network['explorer']}{tx_hash}", name=custom_name)
        else:
            self.log(f"Error: Deposit failed", name=custom_name)
        
    async def process_perform_withdraw(self, account: str, address: str, network: dict, custom_name: str):
        tx_hash, block_number = await self.perform_withdraw(account, address, network)
        if tx_hash and block_number:
            self.log(f"Success: Withdrawal confirmed", name=custom_name)
            self.log(f"Block: {block_number}", name=custom_name)
            self.log(f"Tx Hash: {tx_hash}", name=custom_name)
            self.log(f"Explorer: {network['explorer']}{tx_hash}", name=custom_name)
        else:
            self.log(f"Error: Withdrawal failed", name=custom_name)

    async def process_deploy_owlto(self, account: str, address: str, custom_name: str):
        self.log(f"Processing: Deploy Smart Contract Owlto", name=custom_name)
        tx_hash, contract_addr, block = await self.deploy_contract(account, address, self.owlto_hex_data, wait_receipt=True)
        if tx_hash:
            self.log(f"Success: Owlto deployed at {contract_addr}", name=custom_name)
            self.log(f"Block: {block}", name=custom_name)
            self.log(f"Tx Hash: {tx_hash}", name=custom_name)
            self.log(f"Explorer: {self.L2_NETWORK['explorer']}{tx_hash}", name=custom_name)
        else:
            self.log(f"Error: Owlto deploy failed", name=custom_name)

    async def process_deploy_erc20(self, account: str, address: str, custom_name: str):
        self.log(f"Processing: Deploy ERC20 Token via Factory", name=custom_name)
        name, symbol, decimals, supply = self.get_erc20_details()
        
        tx_hash, token_address, block_number = await self.deploy_token_factory(
            account, address, name, symbol, decimals, supply
        )
        
        if tx_hash and token_address:
            # Save token details to JSON
            token_data = {
                "timestamp": datetime.now(wib).strftime("%Y-%m-%d %H:%M:%S"),
                "deployer_address": address,
                "account_name": custom_name,
                "token_name": name,
                "token_symbol": symbol,
                "token_decimals": decimals,
                "total_supply": supply,
                "contract_address": token_address,
                "transaction_hash": tx_hash,
                "block_number": block_number,
                "network": self.L2_NETWORK["name"],
                "explorer_link": f"{self.L2_NETWORK['explorer']}{tx_hash}"
            }
            self.save_token_to_json(token_data)
            
            self.log(f"Success: ERC20 deployed (Name: {name}, Symbol: {symbol}) at {token_address}", name=custom_name)
            self.log(f"Block: {block_number}", name=custom_name)
            self.log(f"Tx Hash: {tx_hash}", name=custom_name)
            self.log(f"Explorer: {self.L2_NETWORK['explorer']}{tx_hash}", name=custom_name)
        else:
            self.log(f"Error: ERC20 deploy failed - Check factory address or balance", name=custom_name)

    async def process_deploy_gmon(self, account: str, address: str, custom_name: str):
        self.log(f"Processing: Deploy GMONChain", name=custom_name)
        tx_hash, block = await self.call_contract(account, address, self.gmon_factory, self.gmon_selector, self.gmon_value, wait_receipt=False)
        if tx_hash:
            self.log(f"Success: GMONChain sent", name=custom_name)
            self.log(f"Tx Hash: {tx_hash}", name=custom_name)
            self.log(f"Explorer: {self.L2_NETWORK['explorer']}{tx_hash}", name=custom_name)
        else:
            self.log(f"Error: GMONChain failed", name=custom_name)

    async def process_mint_nft(self, account: str, address: str, custom_name: str):
        self.log(f"Processing: Mint OmniHub NFT", name=custom_name)
        balance = await self.get_nft_balance(address, self.omnihub_nft_contract)
        if balance is not None and balance > 0:
            self.log(f"Skip: Already owns {balance} NFT", name=custom_name)
            return
        tx_hash, block = await self.call_contract(account, address, self.omnihub_nft_contract, self.omnihub_mint_data, self.omnihub_mint_value, wait_receipt=False)
        if tx_hash:
            self.log(f"Success: NFT mint sent", name=custom_name)
            self.log(f"Tx Hash: {tx_hash}", name=custom_name)
            self.log(f"Explorer: {self.L2_NETWORK['explorer']}{tx_hash}", name=custom_name)
        else:
            self.log(f"Error: NFT mint failed", name=custom_name)
            
    async def get_random_address(self):
        """Generate a random Ethereum address"""
        acct = Account.create()
        return acct.address
        
    async def load_wallets_from_file(self):
        """Load wallets from wallets.txt file"""
        try:
            if not os.path.exists('wallets.txt'):
                self.log("Warning: wallets.txt not found, will use random addresses", name="System")
                return []
            
            with open('wallets.txt', 'r') as file:
                wallets = [line.strip() for line in file if line.strip()]
            
            valid_wallets = []
            for wallet in wallets:
                # Remove any potential comments or extra spaces
                wallet = wallet.split('#')[0].strip()
                if wallet and len(wallet) == 42 and wallet.startswith('0x'):
                    # Keep as lowercase for now, will convert to checksum when used
                    valid_wallets.append(wallet.lower())
            
            return valid_wallets
        except Exception as e:
            self.log(f"Error loading wallets: {str(e)}", name="System")
            return []
            
    async def send_erc20_random(self, account: str, address: str, custom_name: str):
        """Send ERC20 tokens to random addresses or from wallets.txt"""
        self.log(f"Processing: Send ERC20 Random", name=custom_name)
        
        # Load tokens from tokens.json
        try:
            if not os.path.exists('tokens.json'):
                self.log(f"Error: tokens.json not found. Deploy a token first.", name=custom_name)
                return
                
            with open('tokens.json', 'r') as f:
                tokens_data = json.load(f)
                
            if not tokens_data:
                self.log(f"Error: No tokens found in tokens.json", name=custom_name)
                return
                
            # Display available tokens
            print(f"\n{Fore.CYAN + Style.BRIGHT}Available Tokens:{Style.RESET_ALL}")
            for i, token in enumerate(tokens_data):
                print(f"{i+1}. {token['token_name']} ({token['token_symbol']}) - {token['contract_address'][:6]}...{token['contract_address'][-4:]}")
            
            # Let user select token
            token_index = self.request_input(f"Select token (1-{len(tokens_data)})", "number") - 1
            if token_index < 0 or token_index >= len(tokens_data):
                self.log(f"Error: Invalid token selection", name=custom_name)
                return
                
            selected_token = tokens_data[token_index]
            token_address = selected_token['contract_address']
            token_symbol = selected_token['token_symbol']
            token_name = selected_token['token_name']
            
            # Get amount to send
            amount = self.request_input(f"Enter amount of {token_symbol} to send", "number", "1")
            times = self.request_input(f"Enter number of transfers", "number", "1")
            min_delay = self.request_input(f"Enter minimum delay between transfers (seconds)", "number", "1")
            max_delay = self.request_input(f"Enter maximum delay between transfers (seconds)", "number", "3")
            
            # Load target wallets
            target_wallets = await self.load_wallets_from_file()
            
            # Connect to L2 network
            web3 = await self.get_web3_with_check(address, self.L2_NETWORK)
            
            # Create token contract instance
            token_contract = web3.eth.contract(
                address=web3.to_checksum_address(token_address), 
                abi=self.erc20_abi
            )
            
            # Get sender's token balance
            try:
                sender_balance = token_contract.functions.balanceOf(address).call()
                decimals = token_contract.functions.decimals().call()
                balance_human = sender_balance / (10 ** decimals)
                
                self.log(f"Your balance: {balance_human} {token_symbol}", name=custom_name)
                
                # Check if enough balance
                total_amount_needed = amount * times
                if total_amount_needed > balance_human:
                    self.log(f"Error: Insufficient balance. Need {total_amount_needed} but have {balance_human}", name=custom_name)
                    return
            except Exception as e:
                self.log(f"Error checking balance: {str(e)}", name=custom_name)
                return
            
            # Process transfers
            for i in range(times):
                self.log(f"Transfer {i+1} of {times}", name=custom_name)  # Fixed: replaced {times} with actual variable
                
                # Select target address
                if target_wallets:
                    target_address = random.choice(target_wallets)
                    # Convert to checksum address
                    target_address = web3.to_checksum_address(target_address)
                else:
                    target_address = await self.get_random_address()
                    # Convert to checksum address
                    target_address = web3.to_checksum_address(target_address)
                    self.log(f"Using random address: {target_address}", name=custom_name)
                
                try:
                    # Convert amount to token units
                    amount_in_wei = int(amount * (10 ** decimals))
                    
                    # Build transfer transaction
                    transfer_tx = token_contract.functions.transfer(
                        target_address, 
                        amount_in_wei
                    ).build_transaction({
                        'from': address,
                        'nonce': web3.eth.get_transaction_count(address, 'pending'),
                        'gasPrice': web3.eth.gas_price,
                        'chainId': web3.eth.chain_id
                    })
                    
                    # Estimate gas
                    try:
                        estimated_gas = web3.eth.estimate_gas(transfer_tx)
                        transfer_tx['gas'] = int(estimated_gas * 1.2)
                    except:
                        transfer_tx['gas'] = 100000
                    
                    # Send transaction
                    tx_hash = await self.send_raw_transaction_with_retries(account, web3, transfer_tx)
                    receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
                    
                    if receipt and receipt.status == 1:
                        self.log(f"Success: Sent {amount} {token_symbol} to {target_address[:6]}...{target_address[-4:]}", name=custom_name)
                        self.log(f"Tx Hash: {tx_hash}", name=custom_name)
                        self.log(f"Explorer: {self.L2_NETWORK['explorer']}{tx_hash}", name=custom_name)
                    else:
                        self.log(f"Error: Transfer failed", name=custom_name)
                        
                except Exception as e:
                    self.log(f"Error sending tokens: {str(e)}", name=custom_name)
                
                # Wait before next transfer
                if i < times - 1:
                    delay = random.randint(int(min_delay), int(max_delay))
                    for remaining in range(delay, 0, -1):
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {custom_name} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}Waiting {remaining} seconds...{Style.RESET_ALL}",
                            end="\r",
                            flush=True
                        )
                        await asyncio.sleep(1)
                    print(" " * 80, end="\r")
                    
            self.log(f"Completed sending {times} transfers of {amount} {token_symbol}", name=custom_name)
            
        except Exception as e:
            self.log(f"Error in send ERC20 random: {str(e)}", name=custom_name)

    async def process_option_1(self, account: str, address: str, custom_name: str):
        self.log(f"Processing: Sepolia → Giwa bridge", name=custom_name)
        self.log(f"Amount: {self.bridge_amount} ETH", name=custom_name)

        balance = await self.get_token_balance(address, self.L1_NETWORK)
        self.log(f"Balance: {self.format_number(balance)} ETH", name=custom_name)

        if balance is None:
            self.log(f"Error: Failed to fetch balance", name=custom_name)
            return

        if balance <= self.bridge_amount:
            self.log(f"Warning: Insufficient ETH balance", name=custom_name)
            return

        await self.process_perform_deposit(account, address, self.L1_NETWORK, custom_name)
        
    async def process_option_2(self, account: str, address: str, custom_name: str):
        self.log(f"Processing: Giwa → Sepolia bridge", name=custom_name)
        self.log(f"Amount: {self.bridge_amount} ETH", name=custom_name)

        balance = await self.get_token_balance(address, self.L2_NETWORK)
        self.log(f"Balance: {self.format_number(balance)} ETH", name=custom_name)

        if balance is None:
            self.log(f"Error: Failed to fetch balance", name=custom_name)
            return

        if balance <= self.bridge_amount:
            self.log(f"Warning: Insufficient ETH balance", name=custom_name)
            return

        await self.process_perform_withdraw(account, address, self.L2_NETWORK, custom_name)

    async def auto_all_process(self, accounts):
        """New function: Run all actions on all accounts automatically"""
        self.log("Starting Auto All Process...", name="System")
        
        separator = "=" * 60
        
        for idx, account_line in enumerate(accounts):
            parts = account_line.strip().split(':', 1)
            account = parts[0]
            custom_name = parts[1] if len(parts) > 1 else f"Account{idx+1}"
            address = self.generate_address(account)
            
            if not address:
                self.log("Invalid private key", name=custom_name)
                continue
            
            print(f"\n{Fore.CYAN + Style.BRIGHT}{separator}{Style.RESET_ALL}")
            self.log(f"Auto Processing Account #{idx + 1}", name=custom_name)
            print(f"{Fore.CYAN + Style.BRIGHT}{separator}{Style.RESET_ALL}")

            # 1. Bridge Sepolia → Giwa
            self.log(f"→ Step 1: Bridge Sepolia → Giwa", name=custom_name)
            await self.process_option_1(account, address, custom_name)
            await asyncio.sleep(random.randint(self.min_delay, self.max_delay))
            
            # 2. Bridge Giwa → Sepolia
            self.log(f"→ Step 2: Bridge Giwa → Sepolia", name=custom_name)
            await self.process_option_2(account, address, custom_name)
            await asyncio.sleep(random.randint(self.min_delay, self.max_delay))
            
            # 3. Deploy GMONChain
            self.log(f"→ Step 3: Deploy GMONChain", name=custom_name)
            await self.process_deploy_gmon(account, address, custom_name)
            await asyncio.sleep(random.randint(self.min_delay, self.max_delay))
            
            # 4. Deploy Smart Contract
            self.log(f"→ Step 4: Deploy Smart Contract", name=custom_name)
            await self.process_deploy_owlto(account, address, custom_name)
            await asyncio.sleep(random.randint(self.min_delay, self.max_delay))
            
            # 5. Deploy ERC20
            self.log(f"→ Step 5: Deploy ERC20 Token", name=custom_name)
            await self.process_deploy_erc20(account, address, custom_name)
            await asyncio.sleep(random.randint(self.min_delay, self.max_delay))
            
            # 6. Mint NFT
            self.log(f"→ Step 6: Mint OmniHub NFT", name=custom_name)
            await self.process_mint_nft(account, address, custom_name)
            await asyncio.sleep(random.randint(self.min_delay, self.max_delay))
            
            # 7. Send ERC20 Random (new step)
            self.log(f"→ Step 7: Send ERC20 Random", name=custom_name)
            await self.send_erc20_random(account, address, custom_name)
            await asyncio.sleep(random.randint(self.min_delay, self.max_delay))

            if idx < len(accounts) - 1:
                self.log("Moving to next account...", name=custom_name)
                await asyncio.sleep(5)

        self.log("Auto All Process Completed!", name="System")

    async def process_accounts(self, account: str, address: str, option: int, custom_name: str):
        if option == 1:
            self.log(f"Starting: Sepolia → Giwa bridges ({self.bridge_count}x)", name=custom_name)
            for i in range(self.bridge_count):
                self.log(f"Bridge {i+1} of {self.bridge_count}", name=custom_name)
                await self.process_option_1(account, address, custom_name)
                if i < self.bridge_count - 1:
                    await self.print_timer()

        elif option == 2:
            self.log(f"Starting: Giwa → Sepolia bridges ({self.bridge_count}x)", name=custom_name)
            for i in range(self.bridge_count):
                self.log(f"Bridge {i+1} of {self.bridge_count}", name=custom_name)
                await self.process_option_2(account, address, custom_name)
                if i < self.bridge_count - 1:
                    await self.print_timer()

        elif option == 3:
            self.log(f"Starting: Random bridges ({self.bridge_count}x)", name=custom_name)
            for i in range(self.bridge_count):
                self.log(f"Bridge {i+1} of {self.bridge_count}", name=custom_name)
                bridge = random.choice([self.process_option_1, self.process_option_2])
                await bridge(account, address, custom_name)
                if i < self.bridge_count - 1:
                    await self.print_timer()

        elif option == 4:
            self.log(f"Starting: GMONChain deploys ({self.bridge_count}x)", name=custom_name)
            for i in range(self.bridge_count):
                self.log(f"Deploy {i+1} of {self.bridge_count}", name=custom_name)
                await self.process_deploy_gmon(account, address, custom_name)
                if i < self.bridge_count - 1:
                    await self.print_timer()

        elif option == 5:
            self.log(f"Starting: Owlto deployments ({self.bridge_count}x)", name=custom_name)
            for i in range(self.bridge_count):
                self.log(f"Deploy {i+1} of {self.bridge_count}", name=custom_name)
                await self.process_deploy_owlto(account, address, custom_name)
                if i < self.bridge_count - 1:
                    await self.print_timer()

        elif option == 6:
            self.log(f"Starting: ERC20 deployments ({self.bridge_count}x)", name=custom_name)
            for i in range(self.bridge_count):
                self.log(f"Deploy {i+1} of {self.bridge_count}", name=custom_name)
                await self.process_deploy_erc20(account, address, custom_name)
                if i < self.bridge_count - 1:
                    await self.print_timer()

        elif option == 7:
            self.log(f"Starting: NFT mints ({self.bridge_count}x)", name=custom_name)
            for i in range(self.bridge_count):
                self.log(f"Mint {i+1} of {self.bridge_count}", name=custom_name)
                await self.process_mint_nft(account, address, custom_name)
                if i < self.bridge_count - 1:
                    await self.print_timer()
                    
        elif option == 8:  # New option: Send ERC20 Random
            self.log(f"Starting: Send ERC20 Random ({self.bridge_count}x)", name=custom_name)
            for i in range(self.bridge_count):
                self.log(f"Send {i+1} of {self.bridge_count}", name=custom_name)
                await self.send_erc20_random(account, address, custom_name)
                if i < self.bridge_count - 1:
                    await self.print_timer()

    async def main(self):
        try:
            with open('pv.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            
            if not accounts:
                self.log("Error: No accounts found in accounts.txt", name="System")
                return
            
            option = self.print_question()

            if option == 10:  # Auto All
                self.welcome()
                await self.auto_all_process(accounts)
                input(f"\n{Fore.YELLOW + Style.BRIGHT}Auto All completed. Press Enter to continue...{Style.RESET_ALL}")
                await self.main()
                return

            self.welcome()
            self.log(f"Total Accounts: {len(accounts)}", name="System")
            
            separator = "=" * 60
            for idx, account_line in enumerate(accounts):
                parts = account_line.strip().split(':', 1)
                account = parts[0]
                custom_name = parts[1] if len(parts) > 1 else f"Account{idx+1}"

                address = self.generate_address(account)
                
                print(f"\n{Fore.CYAN + Style.BRIGHT}{separator}{Style.RESET_ALL}")
                self.log(f"Processing Account #{idx + 1}", name=custom_name)
                print(f"{Fore.CYAN + Style.BRIGHT}{separator}{Style.RESET_ALL}")

                if not address:
                    self.log("Error: Invalid private key", name=custom_name)
                    continue
                
                await self.process_accounts(account, address, option, custom_name)
                
                if idx < len(accounts) - 1:
                    self.log("Moving to next account...", name=custom_name)
                    await asyncio.sleep(3)

            print(f"\n{Fore.CYAN + Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
            self.log("All accounts have been processed!", name="System")
            print(f"{Fore.CYAN + Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
            
            input(f"\n{Fore.YELLOW + Style.BRIGHT}Press Enter to continue...{Style.RESET_ALL}")
            
            await self.main()

        except FileNotFoundError:
            self.log("Error: 'pv.txt' file not found", name="System")
            self.log("Please create pv.txt and add your private keys", name="System")
            input(f"\n{Fore.YELLOW + Style.BRIGHT}Press Enter to exit...{Style.RESET_ALL}")
            return
        except KeyboardInterrupt:
            print(f"\n{Fore.RED + Style.BRIGHT}Bot stopped by user{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"Critical Error: {str(e)}", name="System")
            input(f"\n{Fore.YELLOW + Style.BRIGHT}Press Enter to exit...{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Giwa()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"\n{Fore.CYAN + Style.BRIGHT}[ System ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Giwa Testnet Bot - Stopped by user{Style.RESET_ALL}"
        )
    except Exception as e:
        print(
            f"\n{Fore.RED + Style.BRIGHT}Fatal Error: {str(e)}{Style.RESET_ALL}"
        )
