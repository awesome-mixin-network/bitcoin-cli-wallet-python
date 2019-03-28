from mixin_api import MIXIN_API
import uuid
import mixin_config
import json
import csv
import time
import umsgpack
import base64
import getpass
import requests
import wallet_api
import exincore_api

PIN             = "945689";
PIN2            = "845689";
MASTER_ID       = "37222956";
EXINCORE_UUID   = "61103d28-3ac2-44a2-ae34-bd956070dab1"
MASTER_UUID     = "28ee416a-0eaa-4133-bc79-9676909b7b4e";
BTC_ASSET_ID    = "c6d0c728-2624-429b-8e0d-d9d19b6592fa";
EOS_ASSET_ID    = "6cfe566e-4aad-470b-8c9a-2fd35b49c68d";
USDT_ASSET_ID   = "815b0b1a-2764-3736-8faa-42d694fa620a"
ETC_ASSET_ID    = "2204c1ee-0ea2-4add-bb9a-b3719cfff93a";
XRP_ASSET_ID    = "23dfb5a5-5d7b-48b6-905f-3970e3176e27";
XEM_ASSET_ID    = "27921032-f73e-434e-955f-43d55672ee31"
ETH_ASSET_ID    = "43d61dcd-e413-450d-80b8-101d5e903357";
DASH_ASSET_ID   = "6472e7e3-75fd-48b6-b1dc-28d294ee1476";
DOGE_ASSET_ID   = "6770a1e5-6086-44d5-b60f-545f9d9e8ffd"
LTC_ASSET_ID    = "76c802a2-7c88-447f-a93e-c29c9e5dd9c8";
SIA_ASSET_ID    = "990c4c29-57e9-48f6-9819-7d986ea44985";
ZEN_ASSET_ID    = "a2c5d22b-62a2-4c13-b3f0-013290dbac60"
ZEC_ASSET_ID    = "c996abc9-d94e-4494-b1cf-2a3fd3ac5714"
BCH_ASSET_ID    = "fd11b6e3-0b87-41f1-a41f-f0e9b49e5bf0"

MIXIN_DEFAULT_CHAIN_GROUP = [BTC_ASSET_ID, EOS_ASSET_ID, USDT_ASSET_ID, ETC_ASSET_ID, XRP_ASSET_ID, XEM_ASSET_ID, ETH_ASSET_ID, DASH_ASSET_ID, DOGE_ASSET_ID, LTC_ASSET_ID, SIA_ASSET_ID, ZEN_ASSET_ID, ZEC_ASSET_ID, BCH_ASSET_ID]



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

def generateMixinAPI(private_key,pin_token,session_id,user_id,pin,client_secret):
    mixin_config.private_key       = private_key
    mixin_config.pin_token         = pin_token
    mixin_config.pay_session_id    = session_id
    mixin_config.client_id         = user_id
    mixin_config.client_secret     = client_secret
    mixin_config.pay_pin           = pin
    return  MIXIN_API(mixin_config)

def str_AssetPrice(asset_price_in_exin):
    minimum_pay_base_asset = asset_price_in_exin.get("minimum_amount")
    maximum_pay_base_asset = asset_price_in_exin.get("maximum_amount")
    price_base_asset       = asset_price_in_exin.get("price")
    base_sym               = asset_price_in_exin.get("base_asset_symbol")
    target_sym             = asset_price_in_exin.get("exchange_asset_symbol")
    supported_by_exchanges = ""
    for eachExchange in asset_price_in_exin.get("exchanges"):
        supported_by_exchanges += eachExchange
        supported_by_exchanges += " "
    return ("%s %s %s, exchange: %s"%(price_base_asset.ljust(8), (asset_price_in_exin.get("base_asset_symbol")+"/"+asset_price_in_exin.get("exchange_asset_symbol")).ljust(15), ("min:"+minimum_pay_base_asset+" max:"+ maximum_pay_base_asset).ljust(20), supported_by_exchanges))

def asset_balance(mixinApiInstance, asset_id):
    asset_result = mixinApiInstance.getAsset(asset_id)
    assetInfo = asset_result.get("data")
    return assetInfo.get("balance")


def btc_balance_of(mixinApiInstance):
    return asset_balance(BTC_ASSET_ID)
def usdt_balance_of(mixinApiInstance):
    return asset_balance(USDT_ASSET_ID)

def strPresent_of_depositAddress_from(AssetData):

    result_string = ""
    for eachSeg in AssetData.deposit_address():
        result_string += (" %s: %s | "%(eachSeg["title"], eachSeg["value"]))
    return result_string
def strPresent_of_asset_withdrawaddress(thisAddress, asset_id, prefix = " "* 4):
    if(type(thisAddress) is wallet_api.Address):
        address_id = thisAddress.address_id
        address_pubkey = thisAddress.public_key
        address_label = thisAddress.label
        address_accountname = thisAddress.account_name
        address_accounttag = thisAddress.account_tag
        address_fee = thisAddress.fee
        address_dust = thisAddress.dust

    else:
        address_id = thisAddress.get("address_id")
        address_pubkey = thisAddress.get("public_key")
        address_label = thisAddress.get("label")
        address_accountname = thisAddress.get("account_name")
        address_accounttag = thisAddress.get("account_tag")
        address_fee = thisAddress.get("fee")
        address_dust = thisAddress.get("dust")
    Address  = ""
    if address_label != "":
        Address += prefix + "tag          : %s\n"%address_label
    Address += prefix + "id           : %s\n"%address_id

    if address_pubkey!= "":
        Address += prefix + "Address      : %s\n"%address_pubkey

    if address_accountname!= "":
        Address += prefix + "Account name : %s\n"%address_accountname

    if address_accounttag!= "":
        Address += prefix + "Account memo : %s\n"%address_accounttag
    Address += prefix + "fee          : %s\n"%address_fee
    Address += prefix + "dust         : %s\n"%address_dust
    return Address
 
def strPresent_of_btc_withdrawaddress(thisAddress, prefix= " " * 8):
    return strPresent_of_asset_withdrawaddress(thisAddress, BTC_ASSET_ID, prefix)
    
def strPresent_of_usdt_withdrawaddress(thisAddress, prefix = " " * 8):
    return strPresent_of_asset_withdrawaddress(thisAddress, USDT_ASSET_ID, prefix)

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
        Address = "Index %d: %s"%(int(userselect), strPresent_of_asset_withdrawaddress(eachAddress, withdraw_asset_id))
        confirm = input("Type YES and press enter key to remove " + Address + "!!:")
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



def loadSnapshots(UserInstance, timestamp, asset_id = ""):
    snapshots_result_of_account = UserInstance.account_snapshots_after(timestamp, asset_id = asset_id, limit = 500)
    USDT_Snapshots_result_of_account = UserInstance.find_mysnapshot_in(snapshots_result_of_account)
    for singleSnapShot in USDT_Snapshots_result_of_account:
       amount_snap = singleSnapShot.get("amount")
       asset_snap = singleSnapShot.get("asset").get("name")
       created_at_snap = singleSnapShot.get("created_at")
       memo_at_snap = singleSnapShot.get("data")
       id_snapshot = singleSnapShot.get("snapshot_id")
       opponent_id_snapshot = singleSnapShot.get("opponent_id")
       if((float(amount_snap)) < 0):
           try:
               exin_order = umsgpack.unpackb(base64.b64decode(memo_at_snap))
               asset_uuid_in_myorder = str(uuid.UUID(bytes = exin_order["A"]))
               if(asset_uuid_in_myorder == BTC_ASSET_ID):
                   print(created_at_snap + ": You pay " + amount_snap + " " + asset_snap + " to buy BTC from ExinCore")
           except :
               print(created_at_snap + ": You pay " + str(amount_snap) + " " + asset_snap + " to " + opponent_id_snapshot +  " with memo:" + memo_at_snap)

       if((float(amount_snap)) > 0 and memo_at_snap):
           try:
               exin_order = umsgpack.unpackb(base64.b64decode(memo_at_snap))
               if ("C" in exin_order):
                   order_result = exin_order["C"]
                   headString = created_at_snap +": status of your payment to exin is : "
                   if(order_result == 1000):
                       headString = headString + "Successful Exchange"
                   if(order_result == 1001):
                       headString = headString + "The order not found or invalid"
                   if(order_result == 1002):
                       headString = headString + "The request data is invalid"
                   if(order_result == 1003):
                       headString = headString + "The market not supported"
                   if(order_result == 1004):
                       headString = headString + "Failed exchange"
                   if(order_result == 1005):
                       headString = headString + "Partial exchange"
                   if(order_result == 1006):
                       headString = headString + "Insufficient pool"
                   if(order_result == 1007):
                       headString = headString + "Below the minimum exchange amount"
                   if(order_result == 1008):
                       headString = headString + "Exceeding the maximum exchange amount"
                   if ("P" in exin_order):
                       headString = headString + ", your order is executed at price:" +  exin_order["P"] + " USDT" +  " per " + asset_snap
                   if ("F" in exin_order):
                       headString = headString + ", Exin core fee is " + exin_order["F"] + " with fee asset" + str(uuid.UUID(bytes = exin_order["FA"]))
                   if ("T" in exin_order):
                       if (exin_order["T"] == "F"):
                           headString = headString +", your order is refund to you because your memo is not correct"
                       if (exin_order["T"] == "R"):
                           headString = headString +", your order is executed successfully"
                       if (exin_order["T"] == "E"):
                           headString = headString +", exin failed to execute your order"
                   if ("O" in exin_order):
                       headString = headString +", trace id of your payment to exincore is " + str(uuid.UUID(bytes = exin_order["O"]))
                   print(headString)
           except :
               print(created_at_snap +": You receive: " + str(amount_snap) + " " + asset_snap + " from " + opponent_id_snapshot + " with memo:" + memo_at_snap)



mixinApiBotInstance = MIXIN_API(mixin_config)

padding = 70
PromptMsg  = "Read first user from local file new_users.csv        : loaduser\n"
PromptMsg += "Create account and append to new_users.csv           : create\n"
PromptMsg += "Exit                                                 : q\n"
loadedPromptMsg  = "Read account asset non-zero balance".ljust(padding) + ": balance\n"
loadedPromptMsg += "deposit asset ".ljust(padding) + ": deposit\n"
loadedPromptMsg += "send asset ".ljust(padding) + ": send\n"
loadedPromptMsg += "Read transaction of my account".ljust(padding) + ": searchsnapshots\n"
loadedPromptMsg += "Instant exchange BTC, USDT ... : ExinCore ".ljust(padding) + ": instanttrade\n"
loadedPromptMsg += "Ocean.one protocol exchange : ocean.one".ljust(padding) + ": ocean\n"

loadedPromptMsg += "List account withdraw address".ljust(padding) + ": manageassets\n"
loadedPromptMsg += "verify pin".ljust(padding) + ": verifypin\n"
loadedPromptMsg += "updatepin".ljust(padding) + ": updatepin\n"
loadedPromptMsg += "switch account".ljust(padding) + ": switch\n"

global mixinApiNewUserInstance
global mixinWalletInstance
global mixin_account_name
mixinApiNewUserInstance = None
mixinWalletInstance = None
mixin_account_name = None
while ( 1 > 0 ):
    if (mixinApiNewUserInstance != None):
        cmd = input(loadedPromptMsg)
    else:
        cmd = input(PromptMsg)
    if (cmd == 'q' ):
        exit()
    if (cmd == 'switch'):

        mixinApiNewUserInstance = None
    print("Run...")
    if ( cmd == 'loaduser'):
        wallet_records = wallet_api.load_wallet_csv_file('new_users.csv')
        i = 0
        for each_wallet in wallet_records:
            print("%d: user_id-> %s"%(i, each_wallet.userid))
            i = i + 1
        user_index = input(("%d account in your file, load which account: "%len(wallet_records)))
 
        selected_wallet = wallet_records[int(user_index)]
        mixinWalletInstance = selected_wallet
        mixinApiNewUserInstance = generateMixinAPI(selected_wallet.private_key,
                                                            selected_wallet.pin_token,
                                                            selected_wallet.session_id,
                                                            selected_wallet.userid,
                                                            selected_wallet.pin,"")
    if ( cmd == 'balance' ):
        print(time.time())
        all_assets = mixinWalletInstance.get_balance()
        asset_id_groups_in_myassets = []
        for eachAsset in all_assets:
            asset_id_groups_in_myassets.append(eachAsset.asset_id)

        print("Your asset balance is\n===========")

        for eachAsset in all_assets:
            print("%s: %s" %(eachAsset.name.ljust(15), eachAsset.balance))
        print(time.time())

        for eachAssetID in MIXIN_DEFAULT_CHAIN_GROUP:
            if ( not (eachAssetID in asset_id_groups_in_myassets)):
                eachAsset = mixinWalletInstance.get_singleasset_balance(eachAssetID)
                print("%s: %s" %(eachAsset.name.ljust(15), eachAsset.balance))
        print("===========")
    if (cmd == "deposit"):

        all_assets = mixinWalletInstance.get_balance()

        asset_id_groups_in_myassets = []
        print("Your asset deposit address \n===========")

        for eachAsset in all_assets:
            print("%s: %s" %(eachAsset.name.ljust(15), strPresent_of_depositAddress_from(eachAsset)))
            asset_id_groups_in_myassets.append(eachAsset.asset_id)
        for eachAssetID in MIXIN_DEFAULT_CHAIN_GROUP:
            if ( not (eachAssetID in asset_id_groups_in_myassets)):
                this_asset = mixinWalletInstance.get_singleasset_balance(eachAssetID)
                print("%s: %s" %(this_asset.name.ljust(15), strPresent_of_depositAddress_from(this_asset)))
        print("===========")

    if (cmd == "send"):

        all_asset = mixinWalletInstance.get_balance()
        print("select an asset to send" + "===========")

        none_zero_asset = []
        for eachAsset in all_asset:
            if (float(eachAsset.balance)) > 0:
                none_zero_asset.append(eachAsset)
        i = 0
        for eachNoneZero in none_zero_asset:
            print("Send %s: %d" %(eachNoneZero.name.ljust(15), i))
            i = i + 1
        if (i > 0 and i <= len(none_zero_asset)):
            selected_index = int(input("index number:"))
            if selected_index < len(none_zero_asset):
                selected_asset = none_zero_asset[selected_index]
                print("send to mixin network uuid: 0")
                print("send to asset address     : 1")
                address_type = input("your selection:")
                if (address_type == "0"):
                    destination_uuid = input("destination uuid:")
                    amount_tosend     = input("quantity(%s remain):"%selected_asset.balance)
                    memo_input = input("memo:")
                    asset_pin_input = getpass.getpass("pin code:")
                    this_uuid = str(uuid.uuid1())
                    user_confirm = input("Type YES and press enter key to confirm: send %s %s to %s , memo:%s, trace id: %s:"%(amount_tosend, selected_asset.name, destination_uuid, memo_input, this_uuid))
                    if (user_confirm == "YES"):
                        transfer_result = mixinWalletInstance.transfer_to(destination_uuid, selected_asset.asset_id, amount_tosend, memo_input, this_uuid, asset_pin_input)
                        if(transfer_result != False):
                            print(transfer_result)
                if (address_type == "1"):
                    withdraw_addresses = mixinWalletInstance.get_asset_withdrawl_addresses(selected_asset.asset_id)
                    i = 0
                    for eachAddress in withdraw_addresses:
                        btcAddress = strPresent_of_btc_withdrawaddress(eachAddress)
                        print("%s:\n%s"%(str(i).ljust(10, '-'), btcAddress))
                        i = i + 1
                    user_choice = int(input("your choice:"))

                    if (user_choice < len(withdraw_addresses)):
                        selected_withdraw_address = withdraw_addresses[user_choice]
                        withdraw_amount = input("amount to withdraw:")
                        address_id = selected_withdraw_address.address_id
                        address_pubkey = selected_withdraw_address.public_key
                        withdraw_asset_id = selected_withdraw_address.asset_id

                        address_selected = "%s"%(strPresent_of_asset_withdrawaddress(selected_withdraw_address, withdraw_asset_id))
                        confirm = input("Type YES and press enter key to withdraw " + withdraw_amount + " " + selected_asset.name + " to \n" + address_selected + ":")
                        if (confirm == "YES"):
                            this_uuid = str(uuid.uuid1())
                            asset_pin = getpass.getpass("pin:")
                            asset_withdraw_result = mixinWalletInstance.withdraw_asset_to(address_id, withdraw_amount, "withdraw2"+address_pubkey, this_uuid, asset_pin)
                            if(asset_withdraw_result != False):
                                print("Your withdraw is successful , snapshot id: %s"%asset_withdraw_result.snapshot_id)

        else:
            print("no available asset to send")

    if ( cmd == 'searchsnapshots'):
        timestamp = input("input timestamp, history after the time will be searched:")
        snapshots_result_of_account = mixinApiNewUserInstance.account_snapshots_after(timestamp, asset_id = "", limit = 500)
        USDT_Snapshots_result_of_account = mixinApiNewUserInstance.find_mysnapshot_in(snapshots_result_of_account)
        for singleSnapShot in USDT_Snapshots_result_of_account:
            print(singleSnapShot)
            amount_snap = singleSnapShot.get("amount")
            asset_snap = singleSnapShot.get("asset").get("name")
            created_at_snap = singleSnapShot.get("created_at")
            memo_at_snap = singleSnapShot.get("data")
            id_snapshot = singleSnapShot.get("snapshot_id")
            opponent_id_snapshot = singleSnapShot.get("opponent_id")
            if((float(amount_snap)) < 0):
                try:
                    exin_order = umsgpack.unpackb(base64.b64decode(memo_at_snap))
                    asset_uuid_in_myorder = str(uuid.UUID(bytes = exin_order["A"]))
                    if(asset_uuid_in_myorder == BTC_ASSET_ID):
                        print(created_at_snap + ": You pay " + amount_snap + " " + asset_snap + " to buy BTC from ExinCore")
                except :
                    print(created_at_snap + ": You pay " + str(amount_snap) + " " + asset_snap + " to " + opponent_id_snapshot +  " with memo:" + memo_at_snap)

            if((float(amount_snap)) > 0 and memo_at_snap):
                try:
                    exin_order = umsgpack.unpackb(base64.b64decode(memo_at_snap))
                    if ("C" in exin_order):
                        order_result = exin_order["C"]
                        headString = created_at_snap +": status of your payment to exin is : "
                        if(order_result == 1000):
                            headString = headString + "Successful Exchange"
                        if(order_result == 1001):
                            headString = headString + "The order not found or invalid"
                        if(order_result == 1002):
                            headString = headString + "The request data is invalid"
                        if(order_result == 1003):
                            headString = headString + "The market not supported"
                        if(order_result == 1004):
                            headString = headString + "Failed exchange"
                        if(order_result == 1005):
                            headString = headString + "Partial exchange"
                        if(order_result == 1006):
                            headString = headString + "Insufficient pool"
                        if(order_result == 1007):
                            headString = headString + "Below the minimum exchange amount"
                        if(order_result == 1008):
                            headString = headString + "Exceeding the maximum exchange amount"
                        if ("P" in exin_order):
                            headString = headString + ", your order is executed at price:" +  exin_order["P"] + " USDT" +  " per " + asset_snap
                        if ("F" in exin_order):
                            headString = headString + ", Exin core fee is " + exin_order["F"] + " with fee asset" + str(uuid.UUID(bytes = exin_order["FA"]))
                        if ("T" in exin_order):
                            if (exin_order["T"] == "F"):
                                headString = headString +", your order is refund to you because your memo is not correct"
                            if (exin_order["T"] == "R"):
                                headString = headString +", your order is executed successfully"
                            if (exin_order["T"] == "E"):
                                headString = headString +", exin failed to execute your order"
                        if ("O" in exin_order):
                            headString = headString +", trace id of your payment to exincore is " + str(uuid.UUID(bytes = exin_order["O"]))
                        print(headString)
                except :
                    print(created_at_snap +": You receive: " + str(amount_snap) + " " + asset_snap + " from " + opponent_id_snapshot + " with memo:" + memo_at_snap)

                   
    if ( cmd == 'instanttrade'):
        # Pack memo

        exin_assets_price = exincore_api.fetchExinPrice(USDT_ASSET_ID)
        i = 0
        for each_asset_price in exin_assets_price:
            print(str(i).ljust(2) + ":" + str(each_asset_price))
            i = i + 1

        if (len(exin_assets_price) > 0):

            user_select_coin = int(input("which index:"))
            if (user_select_coin < len(exin_assets_price)):
                selected_coin = exin_assets_price[user_select_coin]
                buy_or_sell = input("buy or sell %s:"%selected_coin.exchange_asset_symbol)
     
                if buy_or_sell == "sell":
                    target_asset_id = USDT_ASSET_ID
                    source_asset_id = selected_coin.echange_asset
                if buy_or_sell == "buy":
                    target_asset_id = selected_coin.echange_asset
                    source_asset_id = USDT_ASSET_ID
     
                if buy_or_sell == "sell" or buy_or_sell == "buy":

                    print(selected_coin.debug_str())
                    print("fetching latest price" + selected_coin.echange_asset)
                    asset_price_result = exincore_api.fetchExinPrice(source_asset_id, target_asset_id)
                    asset_price = asset_price_result[0]
                    minimum_pay_base_asset = asset_price.minimum_amount
                    maximum_pay_base_asset = asset_price.maximum_amount
                    price_base_asset       = asset_price.price
                    base_sym               = asset_price.base_asset_symbol
                    target_sym             = asset_price.exchange_asset_symbol
     
                    memo_for_exin = exincore_api.gen_memo_ExinBuy(target_asset_id)
 
                    balance_base_asset = mixinApiNewUserInstance.getAsset(source_asset_id).get("data").get("balance")
                    amount_to_pay =  input("how much you want to pay, %s %s in your balance:"%(balance_base_asset, base_sym))
                    this_uuid = str(uuid.uuid1())
                    estimated_target_amount = str(float(amount_to_pay)/float(price_base_asset))
                    confirm_pay = input("Pay " + amount_to_pay + " " + base_sym + " to buy " + estimated_target_amount + " " + target_sym + " on ExinCore" + ", Type YES and press enter key to confirm")
                    if ( confirm_pay == "YES" ):
                        input_pin = getpass.getpass("pin code:")
     
                        transfer_result = mixinApiNewUserInstance.transferTo(EXINCORE_UUID, source_asset_id, amount_to_pay, memo_for_exin, this_uuid, input_pin)
                        if(transfer_result != False):
                            snapShotID = transfer_result.get("data").get("snapshot_id")
                            print("Pay " + amount_to_pay + " " + base_sym + "to ExinCore to buy " + estimated_target_amount + target_sym + " by uuid:" + this_uuid + ", you can verify the result on https://mixin.one/snapshots/" + snapShotID)
                            checkResult = input("Type YES and press enter key to check latest snapshot:")
                            if (checkResult == "YES"):
                                loadSnapshots(mixinApiNewUserInstance, transfer_result.get("data").get("created_at"), target_asset_id)
     
    if ( cmd == 'create' ):
        thisAccountRSAKeyPair = wallet_api.RSAKey4Mixin()
        account_name  = "Tom Bot"
        print(thisAccountRSAKeyPair.session_key)
        body = {
            "session_secret": thisAccountRSAKeyPair.session_key,
            "full_name": account_name
        }
        token_from_freeweb = mixinApiBotInstance.fetchTokenForCreateUser(body,  "http://freemixinapptoken.myrual.me/token")
        userInfoJson = mixinApiBotInstance.createUser(thisAccountRSAKeyPair.session_key, account_name, token_from_freeweb)
        print(userInfoJson)
        newuserInfo = wallet_api.userInfo()
        newuserInfo.fromcreateUserJson(userInfoJson)
        newuserInfo.private_key = thisAccountRSAKeyPair.private_key

        print(newuserInfo.user_id)
        input("pause")
        wallet_api.append_wallet_into_csv_file(newuserInfo, 'new_users.csv')
        mixinApiNewUserInstance = generateMixinAPI(newuserInfo.private_key,
                                                    newuserInfo.pin_token,
                                                    newuserInfo.session_id,
                                                    newuserInfo.user_id,
                                                    "","")
        defauled_pin = getpass.getpass("input pin:")
        pinInfo = mixinApiNewUserInstance.updatePin(defauled_pin,"")
        print(pinInfo)
        time.sleep(3)
        pinInfo2 = mixinApiNewUserInstance.verifyPin(defauled_pin)
        print(pinInfo2)
        for eachAsset in MIXIN_DEFAULT_CHAIN_GROUP:
            mixinApiNewUserInstance.getAsset(eachAsset)

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
                print("You have : " + eachAssetInfo.get("balance") + eachAssetInfo.get("name"))
                this_uuid = str(uuid.uuid1())
                print("uuid is: " + this_uuid)
                confirm_pay= input("type YES to pay " + eachAssetInfo.get("balance")+ " to MASTER:")
                if ( confirm_pay== "YES" ):
                    transfer_result = mixinApiNewUserInstance.transferTo(MASTER_UUID, eachAssetInfo.get("asset_id"), eachAssetInfo.get("balance"), "", this_uuid, my_pin)
                    if(transfer_result != False):
                        snapShotID = transfer_result.get("data").get("snapshot_id")
                        created_at = transfer_result.get("data").get("created_at")
                        print(created_at + ":Pay BTC to Master ID with trace id:" + this_uuid + ", you can verify the result on https://mixin.one/snapshots/" + snapShotID)
    if ( cmd == 'manageassets' ):
        all_asset = mixinWalletInstance.get_balance()
        asset_id_groups_in_myassets = []
        for eachAsset in all_asset:
            asset_id_groups_in_myassets.append(eachAsset.asset_id)
        print("Your asset is\n===========")

        i = 0
        for eachAsset in all_asset:
            print("%s: %d" %(eachAsset.name.ljust(15), i))
            i += 1


        user_choice = int(input("which asset:"))
        if (user_choice < len(all_asset)):
            selected_asset = all_asset[user_choice]
            withdraw_addresses = mixinWalletInstance.get_asset_withdrawl_addresses(selected_asset.asset_id)
            print("%s: Total %d withdraw address "%(selected_asset.name, len(withdraw_addresses)))
            i = 0
            for eachAddress in withdraw_addresses:
                btcAddress = strPresent_of_btc_withdrawaddress(eachAddress, " " * 8).ljust(100)
                print("%s: %d\n%s"%("Remove".ljust(40, '-') ,i, btcAddress))
                i = i + 1
            print("%s: %d"%("Add new address".ljust(40, '-'), i))
            user_choice = int(input("your choice:"))
            if (user_choice == (len(withdraw_addresses))):
                print("add new address")
                if (selected_asset.chain_id != EOS_ASSET_ID):
                    deposit_address = input("address:")
                    tag_content = input("write a tag:")
                    Confirm = input("address %s with tag %s, Type YES and press enter key to confirm:"%(deposit_address, tag_content))
                    if (Confirm == "YES"):
                        input_pin = getpass.getpass("pin:")
                        add_withdraw_addresses_result = mixinWalletInstance.create_address(selected_asset.asset_id, deposit_address, tag_content, asset_pin = input_pin)
                        address_id = add_withdraw_addresses_result.address_id
                        print("the address :" + deposit_address + " is added to your account with id:" + address_id)
                else:
                    deposit_account = input("account_name:")
                    deposit_memo = input("account_tag(Very important if you withdraw to exchange):")
                    tag_content = input("Tag for the address:")
                    Confirm = input("EOS account: %s, memo: %s, summary: %s. Type YES and press enter key to confirm:"%(deposit_account, deposit_memo, tag_content))
                    if (Confirm == "YES"):
                        input_pin = getpass.getpass("pin:")
                        add_withdraw_addresses_result = mixinWalletInstance.create_address(selected_asset.asset_id, "", tag_content, input_pin, deposit_account, deposit_memo)
                        address_id = add_withdraw_addresses_result.address_id
                        print("the address  is added to your account with id:" + address_id)

            elif (user_choice < len(withdraw_addresses)):
                tobe_delete_address = withdraw_addresses[user_choice]
                print("Following address will be removed\n%s"%strPresent_of_btc_withdrawaddress(tobe_delete_address, " " * 8))
                remove_address_pin = getpass.getpass("asset pin code:")
                remove_address_confirm = input("Type YES and press enter key to confirm:")
                if (remove_address_confirm == "YES"):
                    remove_address_result = mixinWalletInstance.remove_address(tobe_delete_address.address_id, remove_address_pin)
                    print(remove_address_result)



    if ( cmd == 'verifypin' ):
        input_pin = getpass.getpass("input your account pin:")
        userInfo = mixinWalletInstance.verify_pin(input_pin)
        print(userInfo)

    if ( cmd == 'updatepin' ):

        oldPin = getpass.getpass("input old pin:")
        newPin = getpass.getpass("input new pin:")
        print(mixinWalletInstance.update_pin(oldPin, newPin))
