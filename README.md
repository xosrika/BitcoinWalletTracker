# BitcoinWalletTracker
Python scripts for tracking Bitcoin Wallet's transaction history

## Commands
### wallet (-a account hash | -u account username, predefined in script | -i index of already checked wallets)
Wallet command returns information about chosen Bitcoin Address, last checked address is saved into the system for further investigation.   
### trans
Trans command returns last 10 tranaction where the last cheched address was used as an input or an output. 
### pop
Pop command removes last wallet from the saved wallets and sets previous wallet as the current wallet
### tran (-i index of the tranaction from the current wallet's tranactions | --hash HASH)
Tran command gives more information about the tranaction. We can choose transaction from the list of current wallet's tranactions or give the hash of the tranaction.
### check (-i index of the input address | -o index of the output address)
From the chosen tranaction, we can go and check wallet information from the input or output list. Chosen address wlll be set as the current wallet.
### balance
Check balance of current wallet, also gives balance in dollars.
### dollar [-b B] [-s]
Getting price of given number of bitcoins or satoshi. If none given returns price of 1 bitcoin
### tran_check [-h] [-t T] [-i I] [-o O]
Tran_check gives us opportunity to check specific wallet from the list of tranactions of the currenly set wallet. 
