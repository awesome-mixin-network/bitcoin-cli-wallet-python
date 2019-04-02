![cover](https://github.com/wenewzhang/mixin_labs-python-bot/raw/master/Bitcoin_python.jpg)
### 啥东西
一个用[python](https://www.python.org)和[urwid](http://urwid.org)写的多功能数字货币钱包
### 为什么你需要这个东西

#### 透明
这是一个开源项目，所有人都可以看代码。
#### 安全
你持有账户私钥，没人能偷走你的资产。
#### 可靠
基于一个透明且开源运作的分布式区块链项目 ：[Mixin Network](https://github.com/awesome-mixin-network/index_of_Mixin_Network_resource)。主网已经于2019年2月末上线。
#### 有用
不仅仅能保存比特币，还能保存其他币(Ethereum, EOS, XRP...)。
#### 快
确认一笔交易只需要1秒钟。
#### 保护你的隐私
匿名创建账户，匿名交易和付款。
#### 强大
内置1秒闪兑交易所，可以交易比特币和主流加密资产。交易结束资产回到自己的钱包，不用放在中心化交易所，不担心交易所被攻击。 
![exin powered instant and anonymous trade](https://github.com/myrual/bitcoin-cli-wallet-python/raw/master/screen_trade_exin.png)
#### 这是一个开放世界的入口
1. 通过开放式交易所可以在买卖任何ERC20 token。你自己创建都可以。
2. 有真随机数生成器保证的骰子游戏。


## 安装Python 3:
这个钱包基于Python3。

macOS
```bash
brew upgrade
brew install python@3
```

Ubuntu使用第三方源安装python3
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
```

遇到如下提示，敲击Enter
```bash
Press [ENTER] to continue or Ctrl-c to cancel adding it.
```
更新apt，安装 python3.7, python3.7-venv
```bash
sudo apt update
sudo apt install python3.7 python3.7-venv
sudo ln -s /usr/bin/python3.7 /usr/bin/python3
```

确认python3 和Python3-env
```bash
$ python3 -V
Python 3.7.2
```

## 下载代码库并且创建env环境

```bash
git clone https://github.com/awesome-mixin-network/bitcoin-cli-wallet-python.git
cd bitcoin-cli-wallet-python
python3 -m venv ./
```

激活环境
```bash
source ./bin/activate
```

## 安装依赖包

先升级pip，然后安装依赖软件库
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

运行代码
```bash
python Bitcoin_Wallet_Mixin_consoleGUI.py
```
![gui](https://github.com/myrual/bitcoin-cli-wallet-python/raw/master/screen_wallet_open.png)
