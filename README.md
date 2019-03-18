# Command line Bitcoin wallet written in python script based on Mixin Network
![cover](https://github.com/wenewzhang/mixin_labs-python-bot/raw/master/Bitcoin_python.jpg)
This a command line bitcoin/altcoin wallet written in python script based on Mixin Network. It is a cold wallet, so no one can steal your Bitcoin. If someone managed to copy your private file, they can not steal your asset because they don't know the asset pin. 

The wallet did not save your asset pin in local file.


The battery included python Bitcoin wallet can:
* create unlimited Bitcoin wallet
* read Bitcoin balance
* Withdraw Bitcoin to another Bitcoin address
* Sell USDT to exchange and receive Bitcoin in 1 second
* Sell Bitcoin to exchange and receive USDT in 1 second

Full Mixin network resource [index](https://github.com/awesome-mixin-network/index_of_Mixin_Network_resource)

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

```bash
root@n2:~ python3 -m venv -h
usage: venv [-h] [--system-site-packages] [--symlinks | --copies] [--clear]
            [--upgrade] [--without-pip] [--prompt PROMPT]
            ENV_DIR [ENV_DIR ...]
Creates virtual Python environments in one or more target directories.
positional arguments:
  ENV_DIR               A directory to create the environment in.

optional arguments:
  -h, --help            show this help message and exit
  --system-site-packages
                        Give the virtual environment access to the system
                        site-packages dir.
  --symlinks            Try to use symlinks rather than copies, when symlinks
                        are not the default for the platform.
  --copies              Try to use copies rather than symlinks, even when
                        symlinks are the default for the platform.
  --clear               Delete the contents of the environment directory if it
                        already exists, before environment creation.
  --upgrade             Upgrade the environment directory to use this version
                        of Python, assuming Python has been upgraded in-place.
  --without-pip         Skips installing or upgrading pip in the virtual
                        environment (pip is bootstrapped by default)
  --prompt PROMPT       Provides an alternative prompt prefix for this
                        environment.

Once an environment has been created, you may wish to activate it, e.g. by
sourcing an activate script in its bin directory
```

## Clone the repo

```bash
git clone https://github.com/awesome-mixin-network/bitcoin-cli-wallet-python.git
cd bitcoin-cli-wallet-python
python3 -m venv ./
```

Run **python3 -m venv** , following file and folder are created:
```bash
wenewzha:mixin_labs-python-bot wenewzhang$ ls
bin		include		lib		pyvenv.cfg
```

Once a virtual environment has been created, it can be “activated” using a script in the virtual environment’s binary directory.
```bash
source ./bin/activate
(mixin_labs-python-bot) wenewzha:mixin_labs-python-bot wenewzhang$
```
So that “python” or "pip" invoke from the virtual environment, and you can run installed scripts without having to use their full path.

## Install required packages by "virtual environment"


Use pip to upgrade pip itself, and install required packages.
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Run the code
```bash
python3 Bitcoin_Wallet_Mixin.py
```


The following is console output
```bash
(bitcoin-cli-wallet-python) ➜  bitcoin-cli-wallet-python git:(master) ✗ python Bitcoin_Wallet_Mixin.py 
Read first user from local file new_users.csv        : loaduser
Read account asset balance                           : balance
Read Bitcoin                                         : btcbalance
Read USDT                                            : usdtbalance
Read transaction of my account                       : searchsnapshots
Read one snapshots info of account                   : snapshot
Pay USDT to ExinCore to buy BTC                      : buybtc
Create wallet and update PIN                         : create
transafer all asset to my account in Mixin Messenger : allmoney
List account withdraw address                        : listaddress
Add new withdraw address for Bitcoin                 : addbitcoinaddress
Add new withdraw address for USDT                    : addusdtaddress
Remove withdraw address for Bitcoin                  : removebtcaddress
Remove withdraw address for Bitcoin                  : removeusdtaddress
Withdraw BTC                                         : withdrawbtc
Withdraw USDT                                        : withdrawusdt
verify pin                                           : verifypin
updatepin                                            : updatepin
Exit                                                 : q
```
