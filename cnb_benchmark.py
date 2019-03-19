import gevent.monkey
import gevent
gevent.monkey.patch_all()
from Crypto.PublicKey import RSA
from mixin_api import MIXIN_API
import uuid
import mixin_config
import json
import csv
import time
import uuid
import umsgpack
import base64
import getpass

PIN             = "945689";
PIN2            = "845689";
MASTER_ID       = "37222956";
EXINCORE_UUID   = "61103d28-3ac2-44a2-ae34-bd956070dab1"
MASTER_UUID     = "28ee416a-0eaa-4133-bc79-9676909b7b4e";
BTC_ASSET_ID    = "c6d0c728-2624-429b-8e0d-d9d19b6592fa";
EOS_ASSET_ID    = "6cfe566e-4aad-470b-8c9a-2fd35b49c68d";
USDT_ASSET_ID   = "815b0b1a-2764-3736-8faa-42d694fa620a"
CNB_ASSET_ID    = "965e5c6e-434c-3fa9-b780-c50f43cd955c"
BTC_WALLET_ADDR = "14T129GTbXXPGXXvZzVaNLRFPeHXD1C25C";
AMOUNT          = "0.001";

# // Mixin Network support cryptocurrencies (2019-02-19)
# // |EOS|6cfe566e-4aad-470b-8c9a-2fd35b49c68d
# // |CNB|965e5c6e-434c-3fa9-b780-c50f43cd955c
# // |BTC|c6d0c728-2624-429b-8e0d-d9d19b6592fa
# // |ETC|2204c1ee-0ea2-4add-bb9a-b3719cfff93a
# // |XRP|23dfb5a5-5d7b-48b6-905f-3970e3176e27
# // |XEM|27921032-f73e-434e-955f-43d55672ee31
# // |ETH|43d61dcd-e413-450d-80b8-101d5e903357
# // |DASH|6472e7e3-75fd-48b6-b1dc-28d294ee1476
# // |DOGE|6770a1e5-6086-44d5-b60f-545f9d9e8ffd
# // |LTC|76c802a2-7c88-447f-a93e-c29c9e5dd9c8
# // |SC|990c4c29-57e9-48f6-9819-7d986ea44985
# // |ZEN|a2c5d22b-62a2-4c13-b3f0-013290dbac60
# // |ZEC|c996abc9-d94e-4494-b1cf-2a3fd3ac5714
# // |BCH|fd11b6e3-0b87-41f1-a41f-f0e9b49e5bf0

def pubkeyContent(inputContent):
    contentWithoutHeader= inputContent[len("-----BEGIN PUBLIC KEY-----") + 1:]
    contentWithoutTail = contentWithoutHeader[:-1 * (len("-----END PUBLIC KEY-----") + 1)]
    contentWithoutReturn = contentWithoutTail[:64] + contentWithoutTail[65:129] + contentWithoutTail[130:194] + contentWithoutTail[195:]
    return contentWithoutReturn

class MixinConfig:
    private_key = ""
    pin_token = ""
    pay_session_id = ""
    client_secret = ""
    client_id = ""
    pay_pin = ""
def generateMixinAPI(private_key,pin_token,session_id,user_id,pin,client_secret):
    mixinConfigInstance = MixinConfig()
    mixinConfigInstance.private_key       = private_key
    mixinConfigInstance.pin_token         = pin_token
    mixinConfigInstance.pay_session_id    = session_id
    mixinConfigInstance.client_id         = user_id
    mixinConfigInstance.client_secret     = client_secret
    mixinConfigInstance.pay_pin           = pin
    return  MIXIN_API(mixinConfigInstance)


def gen_memo_ExinBuy(asset_id_string):
    return base64.b64encode(umsgpack.packb({"A": uuid.UUID("{" + asset_id_string + "}").bytes})).decode("utf-8")

def asset_balance(mixinApiInstance, asset_id):
    asset_result = mixinApiInstance.getAsset(asset_id)
    assetInfo = asset_result.get("data")
    return assetInfo.get("balance")


def show_asset_balance(mixinApiInstance, asset_id):
    print(asset_balance(mixinApiInstance, asset_id))
def btc_balance_of(mixinApiInstance):
    return asset_balance(BTC_ASSET_ID)
def usdt_balance_of(mixinApiInstance):
    return asset_balance(USDT_ASSET_ID)

def strPresent_of_asset_withdrawaddress(thisAddress, asset_id):
    address_id = thisAddress.get("address_id")
    address_pubkey = thisAddress.get("public_key")
    address_label = thisAddress.get("label")
    address_accountname = thisAddress.get("account_name")
    address_accounttag = thisAddress.get("account_tag")
    address_fee = thisAddress.get("fee")
    address_dust = thisAddress.get("dust")
    Address = "tag: %s,  id: %s, address: %s, fee: %s, dust: %s"%(address_label, address_id, address_pubkey, address_fee, address_dust)
    return Address
 
def strPresent_of_btc_withdrawaddress(thisAddress):
    return strPresent_of_asset_withdrawaddress(thisAddress, BTC_ASSET_ID)
    
def strPresent_of_usdt_withdrawaddress(thisAddress):
    return strPresent_of_asset_withdrawaddress(thisAddress, USDT_ASSET_ID)

def remove_withdraw_address_of(mixinApiUserInstance, withdraw_asset_id, withdraw_asset_name):
    USDT_withdraw_addresses_result = mixinApiUserInstance.withdrawals_address(withdraw_asset_id)
    USDT_withdraw_addresses = USDT_withdraw_addresses_result.get("data")
    i = 0
    print("%s withdraw address is:======="%withdraw_asset_name)
    for eachAddress in USDT_withdraw_addresses:
        usdtAddress = strPresent_of_usdt_withdrawaddress(eachAddress)
        print("index %d, %s"%(i, usdtAddress))
        i = i + 1

    userselect = input("which address index you want to remove")
    if (int(userselect) < i):
        eachAddress = USDT_withdraw_addresses[int(userselect)]
        address_id = eachAddress.get("address_id")
        Address = "index %d: %s"%(int(userselect), strPresent_of_asset_withdrawaddress(eachAddress, withdraw_asset_id))
        confirm = input("Type YES to remove " + Address + "!!:")
        if (confirm == "YES"):
            input_pin = input("pin:")
            mixinApiUserInstance.delAddress(address_id, input_pin)
 
def explainUserData(inputJsonData):
    result = {"user_id": inputJsonData.get("user_id"), "full_name":inputJsonData.get("full_name")}
    return result
def explainAssetData(inputJsonData):
    this_account_name = inputJsonData.get("account_name")
    this_asset_id     = inputJsonData.get("asset_id")
    this_chain_id     = inputJsonData.get("chain_id")
    this_asset_symbol = inputJsonData.get("symbol")
    this_asset_name   = inputJsonData.get("name")


    strPresent = ""

    name = this_asset_name
    if (this_chain_id == "43d61dcd-e413-450d-80b8-101d5e903357") and (this_asset_id != "43d61dcd-e413-450d-80b8-101d5e903357"):
        #ETH based token
        name = name + "(ERC20 token)"
    if (this_chain_id == "6cfe566e-4aad-470b-8c9a-2fd35b49c68d") and (this_asset_id != "6cfe566e-4aad-470b-8c9a-2fd35b49c68d"):
        #ETH based token
        name = name + "(issued on EOS)"

    if this_account_name == "":
        #no need to show account name for EOS or Tron
        strPresent = strPresent + "%s : %s , deposit is confirmed after %s confirmation, deposit to address:%s"%(name, inputJsonData.get("balance"), inputJsonData.get("confirmations"), inputJsonData.get("public_key"))
    else:
        strPresent = strPresent + "%s : %s , deposit is confirmed after %s confirmation, deposit to {account :%s, tag:%s} "%(name, inputJsonData.get("balance"), inputJsonData.get("confirmations"), inputJsonData.get("account_name"), inputJsonData.get("account_tag"))
       
    return strPresent



def explainData(inputJsonData):
    data = inputJsonData.get("data")
    if "type" in data:
        if (data.get("type") == "user"):
            result = explainUserData(data)
            return result
        if (data.get("type") == "asset"):
            result = explainAssetData(data)
            return result


def withdraw_asset(withdraw_asset_id, withdraw_asset_name):
    this_asset_balance = asset_balance(mixinApiNewUserInstance, withdraw_asset_id)
    withdraw_amount = input("%s %s in your account, how many %s you want to withdraw: "%(withdraw_asset_name, this_asset_balance, withdraw_asset_name))
    withdraw_addresses_result = mixinApiNewUserInstance.withdrawals_address(withdraw_asset_id)
    withdraw_addresses = withdraw_addresses_result.get("data")
    i = 0
    print("current " + withdraw_asset_name +" address:=======")
    for eachAddress in withdraw_addresses:
        Address = "index %d: %s"%(i, strPresent_of_asset_withdrawaddress(eachAddress, withdraw_asset_id))
        print(Address)
        i = i + 1

    userselect = input("which address index is your destination")
    if (int(userselect) < i):
        eachAddress = withdraw_addresses[int(userselect)]
        address_id = eachAddress.get("address_id")
        address_pubkey = eachAddress.get("public_key")
        address_selected = "index %d: %s"%(int(userselect), strPresent_of_asset_withdrawaddress(eachAddress, withdraw_asset_id))
        confirm = input("Type YES to withdraw " + withdraw_amount + withdraw_asset_name + " to " + address_selected + "!!:")
        if (confirm == "YES"):
            this_uuid = str(uuid.uuid1())
            asset_pin = getpass.getpass("pin:")
            asset_withdraw_result = mixinApiNewUserInstance.withdrawals(address_id, withdraw_amount, "withdraw2"+address_pubkey, this_uuid, asset_pin)
            return asset_withdraw_result
    return None



mixinApiBotInstance = MIXIN_API(mixin_config)
def account2accountWith(private_key, pin_token, session_id, userid, pin, target_userid, asset_id, amount):
    botInstance = generateMixinAPI(private_key,
                                                            pin_token,
                                                            session_id,
                                                            userid,
                                                            pin,"")
    thisuuid = str(uuid.uuid1())
    kickofftimer = time.time()
    result = botInstance.transferTo(target_userid, asset_id, amount, "bench", thisuuid, pin)
    if result != False:
        if not("data" in result):
            print(result)
            print("HTTP OK:Internal Server Error: transfer %s %s from %s to %s with traceid %s"%(amount, asset_id, botInstance.client_id, target_userid, thisuuid))
        else:
            print("from %s to  %s with snap:%s within %d seconds"%(userid, target_userid, result.get("data").get("snapshot_id"), time.time() - kickofftimer))
    else:

        print("HTTP 500:transfer %s %s from %s to %s with traceid %s"%(amount, asset_id, botInstance.client_id, target_userid, thisuuid))
def RobotOpenFireTo(private_key, pin_token, session_id, userid, pin, target_group, eachPayAmount):
    startime = time.time()
    botInstance = generateMixinAPI(private_key,
                                                            pin_token,
                                                            session_id,
                                                            userid,
                                                            pin,"")
    threads = []
    for eachTargid in target_group:
        if (eachTargid != userid):
            account2accountWith(private_key, pin_token, session_id, userid, pin, eachTargid, CNB_ASSET_ID, eachPayAmount)
    print("one group end with len %d finished in %d"%(len(target_group), time.time() - startime))

master_node_file = "bench_users.csv"
slave_node_file = "slave_user.csv"
slave_node_file2 = "slave_user2.csv"
PromptMsg  = "Read first user from local file bench_users.csv      : loadmaster\n"
PromptMsg += "Read account asset non-zero balance                  : deposit\n"
PromptMsg += "Read single asset balance                            : singlebalance\n"
PromptMsg += "Read transaction of my account                       : searchsnapshots\n"
PromptMsg += "Read one snapshots info of account                   : snapshot\n"
PromptMsg += "Pay USDT to ExinCore to buy BTC                      : buybtc\n"
PromptMsg += "Create master account                                : createmaster\n"
PromptMsg += "Create slave account                                 : createslave\n"
PromptMsg += "Create slave account2                                : createslave2\n"
PromptMsg += "transafer all asset to my account in Mixin Messenger : allmoney\n"
PromptMsg += "verify pin                                           : verifypin\n"
PromptMsg += "transfer master CNB 2 slave                          : master2slave\n"
PromptMsg += "show all slave balance                               : slavebalance\n"
PromptMsg += "slave 2 master                                       : slave2master\n"
PromptMsg += "slave 2 slave                                        : slave2slave\n"
PromptMsg += "Exit                                                 : q\n"
while ( 1 > 0 ):
    cmd = input(PromptMsg)
    if (cmd == 'q' ):
        exit()
    print("Run...")
    if ( cmd == 'loadmaster'):
        with open(master_node_file, newline='') as csvfile:
            reader  = csv.reader(csvfile)
            row = next(reader)
            pin         = row.pop()
            userid      = row.pop()
            session_id  = row.pop()
            pin_token   = row.pop()
            private_key = row.pop()
            mixinApiNewUserInstance = generateMixinAPI(private_key,
                                                            pin_token,
                                                            session_id,
                                                            userid,
                                                            pin,"")
            userInfo = mixinApiNewUserInstance.verifyPin(pin)
            asset_result = mixinApiNewUserInstance.getAsset(CNB_ASSET_ID)
            print(explainData(asset_result))
    if ( cmd == 'deposit' ):
        asset_result = mixinApiNewUserInstance.getAsset(CNB_ASSET_ID)
        print(explainData(asset_result))
        amount_todeposit_inmessenger = input("how many asset you want to deposit through mixin messenger:")
        print('https://mixin.one/pay?recipient=' + mixinApiNewUserInstance.client_id + '&asset=' + CNB_ASSET_ID + '&amount=' + amount_todeposit_inmessenger + '&trace=' + str(uuid.uuid1()) + '&memo=depositCNB')


    if ( cmd == 'singlebalance' ):
        balance_promotmsg =  "Bitcoin balance  : btc\n"

        balance_promotmsg += "USDT balance     : usdt\n"
        balance_promotmsg += "Ethereum balance : ETH\n"
        balance_promotmsg += "EOS balance      : EOS\n"
        balance_promotmsg += "any asset        : anyasset\n"
        cmd_inline = input(balance_promotmsg)

        if ( cmd_inline == 'btc' ):
            asset_result = mixinApiNewUserInstance.getAsset(BTC_ASSET_ID)
            print(explainData(asset_result))
 
        if ( cmd_inline == 'usdt' ):
            asset_result = mixinApiNewUserInstance.getAsset(USDT_ASSET_ID)
            print(explainData(asset_result))

        if ( cmd_inline == 'ETH' ):
            asset_result = mixinApiNewUserInstance.getAsset("43d61dcd-e413-450d-80b8-101d5e903357")
            print(explainData(asset_result))
        if ( cmd_inline == 'EOS' ):
            asset_result = mixinApiNewUserInstance.getAsset(EOS_ASSET_ID)
            print(explainData(asset_result))
        if ( cmd_inline == 'anyasset' ):
            asset_result = mixinApiNewUserInstance.getAsset(input("input asset id:"))
            print(explainData(asset_result))

    if ( cmd == 'createmaster' ):
        key = RSA.generate(1024)
        pubkey = key.publickey()
        private_key = key.exportKey()
        session_key = pubkeyContent(pubkey.exportKey())
        # print(session_key)
        input_session = session_key.decode()
        account_name  = "Tom Bot"
        body = {
            "session_secret": input_session,
            "full_name": account_name
        }
        token_from_freeweb = mixinApiBotInstance.fetchTokenForCreateUser(body,  "http://freemixinapptoken.myrual.me/token")
        userInfo = mixinApiBotInstance.createUser(input_session, account_name, token_from_freeweb)
        with open(master_node_file, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([private_key.decode(),
                                userInfo.get("data").get("pin_token"),
                                userInfo.get("data").get("session_id"),
                                userInfo.get("data").get("user_id"),
                                PIN])
        mixinApiNewUserInstance = generateMixinAPI(private_key.decode(),
                                                    userInfo.get("data").get("pin_token"),
                                                    userInfo.get("data").get("session_id"),
                                                    userInfo.get("data").get("user_id"),
                                                    PIN,"")
        pinInfo = mixinApiNewUserInstance.updatePin(PIN,"")
        pinInfo2 = mixinApiNewUserInstance.verifyPin(PIN)
        print(pinInfo2)
    if ( cmd == 'createslave' ):
        total_slave = input("how many slave:")
        for i in range(int(total_slave)):
            key = RSA.generate(1024)
            pubkey = key.publickey()
            private_key = key.exportKey()
            session_key = pubkeyContent(pubkey.exportKey())
            # print(session_key)
            input_session = session_key.decode()
            account_name  = "Tom Bot"
            body = {
                "session_secret": input_session,
                "full_name": account_name
            }
            token_from_freeweb = mixinApiBotInstance.fetchTokenForCreateUser(body,  "http://freemixinapptoken.myrual.me/token")
            userInfo = mixinApiBotInstance.createUser(input_session, account_name, token_from_freeweb)
            with open(slave_node_file, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([private_key.decode(),
                                    userInfo.get("data").get("pin_token"),
                                    userInfo.get("data").get("session_id"),
                                    userInfo.get("data").get("user_id"),
                                    PIN])
                mixinApiNewUserInstance = generateMixinAPI(private_key.decode(),
                                                        userInfo.get("data").get("pin_token"),
                                                        userInfo.get("data").get("session_id"),
                                                        userInfo.get("data").get("user_id"),
                                                        PIN,"")
                pinInfo = mixinApiNewUserInstance.updatePin(PIN,"")
                pinInfo2 = mixinApiNewUserInstance.verifyPin(PIN)
                print(pinInfo2)

    if ( cmd == 'createslave2' ):
        total_slave = input("how many slave2:")
        for i in range(int(total_slave)):
            key = RSA.generate(1024)
            pubkey = key.publickey()
            private_key = key.exportKey()
            session_key = pubkeyContent(pubkey.exportKey())
            # print(session_key)
            input_session = session_key.decode()
            account_name  = "Tom Bot"
            body = {
                "session_secret": input_session,
                "full_name": account_name
            }
            token_from_freeweb = mixinApiBotInstance.fetchTokenForCreateUser(body,  "http://freemixinapptoken.myrual.me/token")
            userInfo = mixinApiBotInstance.createUser(input_session, account_name, token_from_freeweb)
            with open(slave_node_file2, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([private_key.decode(),
                                    userInfo.get("data").get("pin_token"),
                                    userInfo.get("data").get("session_id"),
                                    userInfo.get("data").get("user_id"),
                                    PIN])
                mixinApiNewUserInstance = generateMixinAPI(private_key.decode(),
                                                        userInfo.get("data").get("pin_token"),
                                                        userInfo.get("data").get("session_id"),
                                                        userInfo.get("data").get("user_id"),
                                                        PIN,"")
                pinInfo = mixinApiNewUserInstance.updatePin(PIN,"")
                pinInfo2 = mixinApiNewUserInstance.verifyPin(PIN)
                print(pinInfo2)



# c6d0c728-2624-429b-8e0d-d9d19b6592fa
    if ( cmd == 'allmoney' ):
        AssetsInfo = mixinApiNewUserInstance.getMyAssets()
        availableAssset = []
        my_pin = getpass.getpass("pin:")
        for eachAssetInfo in AssetsInfo: 
            if (eachAssetInfo.get("balance") == "0"):
                continue
            if (float(eachAssetInfo.get("balance")) > 0):
                availableAssset.append(eachAssetInfo)
                this_uuid = str(uuid.uuid1())
                transfer_result = mixinApiNewUserInstance.transferTo(MASTER_UUID, eachAssetInfo.get("asset_id"), eachAssetInfo.get("balance"), "", this_uuid, my_pin)
                snapShotID = transfer_result.get("data").get("snapshot_id")
                created_at = transfer_result.get("data").get("created_at")
    if ( cmd == 'verifypin' ):
        input_pin = getpass.getpass("input your account pin:")
        print(mixinApiNewUserInstance.verifyPin(input_pin))
    if ( cmd == 'slavebalance'):
        with open(slave_node_file2, newline='') as csvfile:
            reader  = csv.reader(csvfile)

            slave2_record = []
            for row in reader:
                slave2_record.append(row)
            print("slave2 has %d"%len(slave2_record))
 
        with open(slave_node_file, newline='') as csvfile:
            reader  = csv.reader(csvfile)

            threads = []
            slaveone_record = []
            for row in reader:
                master_pin         = row.pop()
                master_userid      = row.pop()
                master_session_id  = row.pop()
                master_pin_token   = row.pop()
                master_private_key = row.pop()
                botInstance = generateMixinAPI(master_private_key,
                                                            master_pin_token,
                                                            master_session_id,
                                                            master_userid,
                                                            master_pin,"")
                threads.append(gevent.spawn(show_asset_balance, botInstance, CNB_ASSET_ID))
                slaveone_record.append(row)
            print("slaveone record %d"%len(slaveone_record))
            gevent.joinall(threads)

    if ( cmd == 'master2slave'):
        amount_to_pay = input("amount:")
        loop_count = int(input("count:"))
        with open(master_node_file, newline='') as csvfile:
            masterreader  = csv.reader(csvfile)
            row = next(masterreader)
            master_pin         = row.pop()
            master_userid      = row.pop()
            master_session_id  = row.pop()
            master_pin_token   = row.pop()
            master_private_key = row.pop()
 
            target_userid_group = []
            with open(slave_node_file, newline='') as csvfile:
                reader  = csv.reader(csvfile)
                for row in reader:
                    tmppin         = row.pop()
                    tmpuserid      = row.pop()
                    target_userid_group.append(tmpuserid)
            for i in range(loop_count):
                RobotOpenFireTo(master_private_key, master_pin_token, master_session_id, master_userid, master_pin, target_userid_group, amount_to_pay)
                print("%d round finished"%i)
    if ( cmd == 'slave2master'):
        amount_to_pay = input("amount:")
        with open(master_node_file, newline='') as csvfile:
            masterreader  = csv.reader(csvfile)
            row = next(masterreader)
            master_pin         = row.pop()
            master_userid      = row.pop()
 
            target_userid_group = []
            threads = []
            with open(slave_node_file, newline='') as csvfile:
                reader  = csv.reader(csvfile)
                for row in reader:

                    slave_pin         = row.pop()
                    slave_userid      = row.pop()
                    slave_session_id  = row.pop()
                    slave_pin_token   = row.pop()
                    slave_private_key = row.pop()
                    threads.append(gevent.spawn_later(10, account2accountWith, slave_private_key, slave_pin_token, slave_session_id, slave_userid, slave_pin, master_userid, CNB_ASSET_ID, amount_to_pay))
            gevent.joinall(threads)
    if ( cmd == 'slave2slave'):
        amount_to_pay = input("amount:")

        all_target_userid_group = []
        threads = []
        with open(slave_node_file2, newline='') as csvfile:
            reader  = csv.reader(csvfile)
            for row in reader:
                tmppin         = row.pop()
                tmpuserid      = row.pop()
                all_target_userid_group.append(tmpuserid)

        target_userid_group = all_target_userid_group
        with open(slave_node_file, newline='') as csvfile:
            reader  = csv.reader(csvfile)
            for row in reader:
                slave_pin         = row.pop()
                slave_userid      = row.pop()
                slave_session_id  = row.pop()
                slave_pin_token   = row.pop()
                slave_private_key = row.pop()

                threads.append(gevent.spawn_later(10, RobotOpenFireTo, slave_private_key, slave_pin_token, slave_session_id, slave_userid, slave_pin, target_userid_group,  amount_to_pay))
        gevent.joinall(threads)
    if ( cmd == 'slave2slavetwo'):
        amount_to_pay = input("amount:")
        account_amount = input("account_number:")
        all_target_userid_group = []
        with open(slave_node_file2, newline='') as csvfile:
            reader  = csv.reader(csvfile)
            for row in reader:
                tmppin         = row.pop()
                tmpuserid      = row.pop()
                all_target_userid_group.append(tmpuserid)

        target_userid_group = all_target_userid_group[0:int(account_amount)]

        threads = []
        with open(slave_node_file, newline='') as csvfile:
            reader  = csv.reader(csvfile)
            i = 0
            for row in reader:
                slave_pin         = row.pop()
                slave_userid      = row.pop()
                slave_session_id  = row.pop()
                slave_pin_token   = row.pop()
                slave_private_key = row.pop()
                threads.append(gevent.spawn_later(20, account2accountWith, slave_private_key, slave_pin_token, slave_session_id, slave_userid, slave_pin, target_userid_group[i], CNB_ASSET_ID, amount_to_pay))
        gevent.joinall(threads)

