# CLI/API Bitcoin and alter coin wallet and exchanger written in python script based
![cover](https://github.com/wenewzhang/mixin_labs-python-bot/raw/master/Bitcoin_python.jpg)
### What is this?
a cryptocurrency wallet based on Python and urwid. 
### Why you need this?

1. The wallet is transparent: It is a open source project. Every programmer can review the code.
2. The wallet is secure     : You hold the wallet key. Nobody can steal your asset without the wallet key.
3. The wallet is reliable   : It is based on a transparent and distributed blockchain : [Mixin Network](https://github.com/awesome-mixin-network/index_of_Mixin_Network_resource). The network launched it's main net on 29,Feb, 2019.
4. The wallet is useful     : Not just hold Bitcoin, but also many altercoin(Ethereum, EOS, XRP...).
5. The wallet is fast       : every payment happen on Mixin network can be confirmed in 1 second.
6. The wallet is anonymous  : Every account can be created anonymously. Every payment is anonymous for public.
7. The wallet is powerful   : Anonymous and instantly trade Bitcoin and altercoins, trade can be done in 2 seconds and still hold your asset in your wallet instead of centralized exchange. 
8. The wallet is open       : You can sell or buy any ERC20 token in wallet through open exchange protocol Ocean.one


## Python 3 installation:
This tool is written in Python 3.7.2 So you need to install Python 3.7.2 or above.

macOS
```bash
brew upgrade
brew install python@3
```

Ubuntu, install python 3.7.2 from the third apt source.
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
```

When prompt like below, press Enter to continue:
```bash
Press [ENTER] to continue or Ctrl-c to cancel adding it.
```
Update the source, then install python3.7, python3.7-venv
```bash
sudo apt update
sudo apt install python3.7 python3.7-venv
sudo ln -s /usr/bin/python3.7 /usr/bin/python3
```

check both python3 and python3-venv are installed
```bash
$ python3 -V
Python 3.7.2
```


## Clone the repo and create python env

```bash
git clone https://github.com/awesome-mixin-network/bitcoin-cli-wallet-python.git
cd bitcoin-cli-wallet-python
python3 -m venv ./
```

Active the env now
```bash
source ./bin/activate
```

## Install required packages by "virtual environment"

Use pip to upgrade pip itself, and install required packages.
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Run the code
```bash
python Bitcoin_Wallet_Mixin_consoleGUI.py
```
![gui](https://github.com/awesome-mixin-network/bitcoin-cli-wallet-python/raw/master/screen_shot_wallet.png)
