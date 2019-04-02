# Bitcoin and alter coin wallet written in python
![cover](https://github.com/wenewzhang/mixin_labs-python-bot/raw/master/Bitcoin_python.jpg)
<p align="center">
<a href="README-cn.md"><img src="https://img.shields.io/badge/language-中文文档-red.svg?longCache=true&style=flat-square"></a>
</p>


### What is this?
a cryptocurrency wallet based on Python and urwid. 
### Why you need this?

#### Transparent
It is a open source project. Every programmer can review the code.
#### Secure
You hold the wallet key. Nobody can steal your asset without the wallet key.
#### Reliable
It is based on a transparent and distributed blockchain : [Mixin Network](https://github.com/awesome-mixin-network/index_of_Mixin_Network_resource). The network launched it's main net on 29,Feb, 2019.
#### Useful
Not just hold Bitcoin, but also many altercoin(Ethereum, EOS, XRP...).
#### Fast
Every payment happen on Mixin network can be confirmed in 1 second.
#### Protect your privacy
Anonymously create account, anonymously pay and transfer cryptocurrency.
#### Still powerful
Instantly trade Bitcoin and altercoins, asset is in your wallet instead of a centralized exchange. 
![exin powered instant and anonymous trade](https://github.com/myrual/bitcoin-cli-wallet-python/raw/master/screen_trade_exin.png)
#### Portal to an open world
1. You can sell or buy any ERC20 token inside wallet through open exchange protocol Ocean.one
2. You can play fair dice game


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
![gui](https://github.com/myrual/bitcoin-cli-wallet-python/raw/master/screen_wallet_open.png)
