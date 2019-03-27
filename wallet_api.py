import csv
from mixin_api import MIXIN_API
from Crypto.PublicKey import RSA

def pubkeyContent(inputContent):
    contentWithoutHeader= inputContent[len("-----BEGIN PUBLIC KEY-----") + 1:]
    contentWithoutTail = contentWithoutHeader[:-1 * (len("-----END PUBLIC KEY-----") + 1)]
    contentWithoutReturn = contentWithoutTail[:64] + contentWithoutTail[65:129] + contentWithoutTail[130:194] + contentWithoutTail[195:]
    return contentWithoutReturn

class MIXIN_config():
    def __init__(self):
        self.private_key       = ""
        self.pin_token         = ""
        self.pay_session_id    = ""
        self.client_id         = ""
        self.client_secret     = ""
        self.pay_pin           = ""

def generateMixinAPI(private_key,pin_token,session_id,user_id,pin,client_secret):
    mixin_config = MIXIN_config()
    mixin_config.private_key       = private_key
    mixin_config.pin_token         = pin_token
    mixin_config.pay_session_id    = session_id
    mixin_config.client_id         = user_id
    mixin_config.client_secret     = client_secret
    mixin_config.pay_pin           = pin
    return  MIXIN_API(mixin_config)


class RSAKey4Mixin():
    def __init__(self):
        key = RSA.generate(1024)
        pubkey = key.publickey()
        private_key = key.exportKey()
        session_key = pubkeyContent(pubkey.exportKey())
        self.session_key = session_key.decode()
        self.private_key = private_key.decode()
 
class userInfo():
    def __init__(self, pin_token = "", session_id = "", user_id = ""):
        self.pin_token = pin_token
        self.session_id = session_id
        self.user_id = user_id
    def fromcreateUserJson(self, userInfojson):
        self.pin_token  = userInfojson.get("data").get("pin_token")
        self.session_id = userInfojson.get("data").get("session_id")
        self.user_id    = userInfojson.get("data").get("user_id")

class Static_Asset():
    def __init__(self, jsonInput):
        self.type     = jsonInput.get("type")
        self.name     = jsonInput.get("name")
        self.asset_id = jsonInput.get("asset_id")
        self.chain_id = jsonInput.get("chain_id")
        self.symbol   = jsonInput.get("symbol")
 
class Asset(Static_Asset):
    def __init__(self, jsonInput):
        self.type     = jsonInput.get("type")
        self.name     = jsonInput.get("name")
        self.asset_id = jsonInput.get("asset_id")
        self.chain_id = jsonInput.get("chain_id")
        self.balance  = jsonInput.get("balance")
        self.symbol   = jsonInput.get("symbol")
        self.public_key   = jsonInput.get("public_key")
        self.account_name = jsonInput.get("account_name")
        self.account_tag  = jsonInput.get("account_tag")
    def deposit_address(self):
        result_desposit = []
        if(self.public_key != ""):
            result_desposit.append({"title":"public_key", "value":self.public_key})
        if(self.account_name!= ""):
            result_desposit.append({"title":"account_name", "value":self.account_name})
        if(self.account_tag!= ""):
            result_desposit.append({"title":"account_tag", "value":self.account_tag})
        return result_desposit

class Withdrawal():
    def __init__(self, jsonInput):
        self.snapshot_id = jsonInput.get("snapshot_id")
        self.transaction_hash = jsonInput.get("transaction_hash")
        self.asset_id = jsonInput.get("asset_id")
        self.amount = jsonInput.get("amount")
        self.trace_id = jsonInput.get("trace_id")
        self.memo = jsonInput.get("memo")
        self.created_at = jsonInput.get("created_at")

class Address():
    def __init__(self, jsonInput):
        self.address_id   = jsonInput.get("address_id")
        self.public_key   = jsonInput.get("public_key")
        self.asset_id     = jsonInput.get("asset_id")
        self.label        = jsonInput.get("label")
        self.account_name = jsonInput.get("account_name")
        self.account_tag  = jsonInput.get("account_tag")
        self.fee          = jsonInput.get("fee")
        self.reserve      = jsonInput.get("reserve")
        self.dust         = jsonInput.get("dust")
        self.updated_at   = jsonInput.get("updated_at")

class Transfer():
    def __init__(self, jsonInput):
        self.amount       = jsonInput.get("amount")
        self.memo         = jsonInput.get("memo")
        self.snapshot_id  = jsonInput.get("snapshot_id")

        self.asset_id     = jsonInput.get("asset_id")
        self.type         = jsonInput.get("type")
        self.trace_id     = jsonInput.get("trace_id")
        self.opponent_id  = jsonInput.get("opponent_id")



class WalletRecord():
    def __init__(self, pin, userid, session_id, pin_token, private_key):
       self.pin = pin
       self.userid = userid
       self.session_id = session_id
       self.pin_token = pin_token
       self.private_key = private_key
       self.mixinAPIInstance = generateMixinAPI(self.private_key,
                                                            self.pin_token,
                                                            self.session_id,
                                                            self.userid,
                                                            self.pin,"")
    def get_balance(self):
        all_assets_json = self.mixinAPIInstance.getMyAssets()
        all_assets = []
        for eachJson in all_assets_json:
            all_assets.append(Asset(eachJson))

        return all_assets
    def get_singleasset_balance(self, input_asset_id):
        single_asset_json = self.mixinAPIInstance.getAsset(input_asset_id)
        return Asset(single_asset_json.get("data"))
    def get_asset_withdrawl_addresses(self, input_asset_id):
        asset_addresses_json = self.mixinAPIInstance.withdrawals_address(input_asset_id).get("data")
        asset_addresses = []
        for each_address_json in asset_addresses_json:
            asset_addresses.append(Address(each_address_json))
        return asset_addresses
    def create_address(self, asset_id, public_key = "", label = "", asset_pin = "", account_name = "", account_tag = ""):
        create_result_json = self.mixinAPIInstance.createAddress(asset_id, public_key , label , asset_pin , account_name , account_tag )
        return Address(create_result_json.get("data"))
    def remove_address(self, to_be_deleted_address_id, input_pin):
        create_result_json = self.mixinAPIInstance.delAddress(to_be_deleted_address_id, input_pin)
        return create_result_json
    def transfer_to(self, destination_uuid, asset_id, amount_tosend, memo_input, this_uuid, asset_pin_input):
        transfer_result_json = self.mixinAPIInstance.transferTo(destination_uuid, asset_id, amount_tosend, memo_input, this_uuid, asset_pin_input)
        if(transfer_result_json != False):
            return Transfer(transfer_result_json.get("data"))

        return False
    def withdraw_asset_to(self, address_id, withdraw_amount, withdraw_memo, withdraw_this_uuid, withdraw_asset_pin):
        asset_withdraw_result_json = self.mixinAPIInstance.withdrawals(address_id, withdraw_amount, withdraw_memo, withdraw_this_uuid, withdraw_asset_pin)
        withdraw_result = Withdrawal(asset_withdraw_result_json.get("data"))
        return withdraw_result

def append_wallet_into_csv_file(this_wallet, file_name):
    with open(file_name, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([this_wallet.private_key,
                            this_wallet.pin_token,
                            this_wallet.session_id,
                            this_wallet.user_id,
                            ""])

def load_wallet_csv_file(file_name):
    with open(file_name, newline='') as csvfile:
        reader  = csv.reader(csvfile)

        wallet_records = []
        for row in reader:

            pin         = row.pop()
            userid      = row.pop()
            session_id  = row.pop()
            pin_token   = row.pop()
            private_key = row.pop()
            wallet_records.append(WalletRecord(pin, userid, session_id, pin_token, private_key))
        return wallet_records
def create_wallet_csv_file(file_name):
    with open(file_name, newline='') as csvfile:
        reader  = csv.reader(csvfile)

        wallet_records = []
        for row in reader:

            pin         = row.pop()
            userid      = row.pop()
            session_id  = row.pop()
            pin_token   = row.pop()
            private_key = row.pop()
            wallet_records.append(WalletRecord(pin, userid, session_id, pin_token, private_key))
        return wallet_records
