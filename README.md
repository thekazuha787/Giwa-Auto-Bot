# Giwa Auto Bot

[![GitHub Repo stars](https://img.shields.io/github/stars/thekazuha787/Giwa-Auto-Bot?style=social)](https://github.com/thekazuha787/Giwa-Auto-Bot)
[![Telegram Channel](https://img.shields.io/badge/Telegram-Channel-blue?logo=telegram)](https://t.me/Offical_Im_kazuha)
[![Python Version](https://img.shields.io/badge/Python-3.12%2B-blueviolet)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Giwa Auto Bot** is an advanced automation tool designed for seamless interaction with the Giwa Sepolia Testnet, an Ethereum Layer 2 (L2) solution powered by the OP Stack and developed by Upbit/Dunamu. This bot facilitates asset bridging, smart contract deployments, NFT minting, and ERC20 token transfers, making it ideal for testnet exploration, development, and automated farming activities. With 1-second block times and high throughput, Giwa enables efficient Web3 infrastructure testing.

# 🚀 Version 2.0  

👨‍💻 Developed by [Kazuha787](https://github.com/thekazuha787)  

📢 **Official Telegram Channel**: [@Offical_Im_kazuha](https://t.me/Offical_Im_kazuha)  

### 🔹 What’s Inside:
- Stay updated with the latest releases  
- Get direct support  
- Join community discussions & share ideas

---

## 🌟 Key Features

- **Cross-Chain Bridging**: Automate ETH transfers between Sepolia (L1) and Giwa Sepolia (L2) with configurable amounts and delays.
- **Smart Contract Deployment**: Deploy Owlto contracts, ERC20 tokens via factory, and interact with GMONChain factories.
- **NFT Minting**: Efficiently mint OmniHub NFTs, with built-in balance checks to prevent redundant operations.
- **ERC20 Token Management**: Deploy custom tokens and send them to random or predefined addresses, with balance verification.
- **Randomized Operations**: Support for random bridging directions and target addresses to simulate diverse activity.
- **Full Automation Mode**: Execute a comprehensive workflow (bridging, deployments, minting, transfers) across multiple accounts.
- **Robust Monitoring**: Real-time logging with color-coded outputs, transaction hashes, block numbers, and direct explorer links.
- **Data Persistence**: Automatically save deployed token details to `tokens.json` for tracking and reuse.
- **Error Resilience**: Integrated retry mechanisms for RPC connections, transactions, and gas estimation.
- **Customizable Parameters**: Dynamically adjust transaction counts, ETH amounts, and inter-transaction delays via an intuitive menu.

The bot supports multi-account processing from a secure input file, ensuring scalability for batch operations.

---

## 🛠️ Technology Stack

- **Core Framework**: Python 3.12+ with asyncio for asynchronous, non-blocking operations.
- **Blockchain Integration**: Web3.py for Ethereum RPC interactions, contract calls, and transaction signing.
- **Account Management**: eth-account for secure private key handling and address generation.
- **HTTP Client**: aiohttp with timeouts and BasicAuth for reliable API calls.
- **User Interface**: Colorama for enhanced terminal output; pytz for timezone-aware logging (WIB/Asia/Jakarta).
- **Utilities**: tabulate for data formatting; json for persistent storage.

This setup ensures high performance and compatibility with standard development environments.

---

## 📋 System Requirements

- **Runtime**: Python 3.12 or higher.
- **Dependencies**: Listed in `requirements.txt` (no internet required post-installation).
- **Network Access**: Stable connection to Sepolia RPC (Alchemy) and Giwa Sepolia RPC.
- **Testnet Funds**: Sepolia ETH from faucets (e.g., [Sepolia Faucet](https://sepoliafaucet.com/)); Giwa tokens from [Giwa Faucet](https://faucet.lambda256.io/giwa-sepolia).
- **Hardware**: Standard CPU (multi-threading supported via asyncio); 512MB+ RAM recommended for multi-account runs.

**Important**: This tool is exclusively for testnet environments. Do not use with mainnet assets.

---

## 🔧 Installation Guide

1. **Repository Cloning**:
   ```
   git clone https://github.com/thekazuha787/Giwa-Auto-Bot.git
   cd Giwa-Auto-Bot
   ```

2. **Dependency Installation**:
   Create or verify `requirements.txt`:
   ```
   web3==6.15.2
   eth-account==0.10.0
   aiohttp==3.9.5
   colorama==0.4.6
   pytz==2024.1
   tabulate==0.9.0
   ```
   Install via:
   ```
   pip install -r requirements.txt
   ```

3. **Configuration Files**:
   - **pv.txt**: Add private keys (one per line, optional label: `private_key:AccountName`).
     ```
     0xYourTestnetPrivateKey1:MainWallet
     0xYourTestnetPrivateKey2:SecondaryWallet
     ```
     *Security Note*: Store securely; never commit to version control.
   - **wallets.txt** (Optional): List target addresses for ERC20 transfers (one per line).
   - **tokens.json**: Auto-generated for tracking deployed tokens.

4. **Environment Setup**:
   - Ensure RPC endpoints are accessible (hardcoded: Alchemy Sepolia, Giwa Sepolia).
   - Fund accounts via testnet faucets.

---

## 🚀 Quick Start

1. **Launch the Bot**:
   ```
   python main.py
   ```
   The interface displays a professional banner and navigable menu.

2. **Interactive Menu**:
   - **1. Bridge Sepolia → Giwa**: L1 to L2 deposits.
   - **2. Bridge Giwa → Sepolia**: L2 to L1 withdrawals.
   - **3. Random Bridge**: Stochastic direction selection.
   - **4. Deploy GMONChain**: Factory interaction for chain deployment.
   - **5. Deploy Smart Contract (Owlto)**: Bytecode-based deployment.
   - **6. Deploy ERC20 Token (Factory)**: Custom token creation (prompts for name, symbol, decimals, supply).
   - **7. Mint OmniHub NFT**: Conditional minting based on ownership.
   - **8. Send ERC20 Random**: Transfer from saved tokens to targets.
   - **9. Set Transaction Count & Amount**: Tune settings (defaults: 1 tx, 0.0001 ETH, 1-3s delays).
   - **10. Auto All**: Sequential execution of options 1-8 for all accounts.
   - **11. Exit**: Graceful termination.

3. **Example Workflow**:
   - Select **10** for automation: Processes bridging (bidirectional), deployments (GMON, Owlto, ERC20), NFT mint, and ERC20 sends per account.
   - Monitor logs for Tx details and [Giwa Explorer](https://sepolia-explorer.giwa.io/) links.
   - Post-run: Review `tokens.json` for deployed assets.

**Pro Tip**: Use option 9 to optimize for gas efficiency and avoid RPC throttling.

---

## 📁 Project Structure

```
Giwa-Auto-Bot/
├── main.py                 # Core Giwa class and entry point
├── pv.txt                  # User-provided private keys (gitignored)
├── wallets.txt             # Optional target addresses
├── tokens.json             # Auto-saved token metadata
├── requirements.txt        # Python dependencies
├── README.md               # This documentation
└── LICENSE                 # MIT License file
```

---

## 🔒 Security & Best Practices

- **Private Key Handling**: Keys are loaded in-memory only; avoid logging or exposing them.
- **Testnet Exclusivity**: Validate all operations on testnets to prevent accidental mainnet use.
- **Rate Limiting**: Built-in random delays (configurable) mitigate RPC bans.
- **Auditing**: Review contract ABIs and RPC URLs before use; update as networks evolve.
- **Backup**: Regularly back up `tokens.json` for continuity.

For issues, join the [Telegram Channel](https://t.me/Offical_Im_kazuha).

---

## ⚠️ Disclaimer

This software is provided "as is" for educational and testnet purposes. The author disclaims all liability for any damages, losses, or unintended consequences. Users assume full responsibility for their actions, including compliance with network terms and secure key management. Not financial advice; use test funds only.

---

## 📈 Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

Report bugs or suggest features via Issues or the Telegram channel.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👏 Acknowledgments

- **Giwa Network**: For innovative L2 infrastructure.
- **OP Stack (Optimism)**: Underlying technology enabling fast blocks.
- **Community**: Thanks to contributors and users in the Telegram channel.
- **Tools**: Web3.py, aiohttp, and Colorama for robust development.

**Empowering Web3 Automation** – Kazuha787  
*Last Updated: September 14, 2025*
