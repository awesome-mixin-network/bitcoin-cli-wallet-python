import requests
import uuid
import base64
import umsgpack
EXINCORE_UUID   = "61103d28-3ac2-44a2-ae34-bd956070dab1"


class Asset_pair_price():
    def __init__(self, asset_price_in_exin):
        self.minimum_amount = asset_price_in_exin.get("minimum_amount")
        self.maximum_amount = asset_price_in_exin.get("maximum_amount")
        self.price       = asset_price_in_exin.get("price")
        self.base_asset_symbol               = asset_price_in_exin.get("base_asset_symbol")
        self.exchange_asset_symbol             = asset_price_in_exin.get("exchange_asset_symbol")
        self.base_asset               = asset_price_in_exin.get("base_asset")
        self.echange_asset             = asset_price_in_exin.get("exchange_asset")
        self.supported_by_exchanges = ""

        for eachExchange in asset_price_in_exin.get("exchanges"):
            self.supported_by_exchanges += eachExchange
            self.supported_by_exchanges += " "
    def __str__(self):
        result = "%s %s %s, exchange: %s"%(self.price.ljust(8), (self.base_asset_symbol)+"/"+self.exchange_asset_symbol.ljust(15), "min:"+self.minimum_amount.ljust(10)+" max:"+ self.maximum_amount.ljust(10)+ self.base_asset_symbol.ljust(20), self.supported_by_exchanges)
        return result
    def debug_str(self):
        result = "%s %s %s, exchange: %s base:%s target:%s"%(self.price.ljust(8), (self.base_asset_symbol)+"/"+self.exchange_asset_symbol.ljust(15), "min:"+self.minimum_amount+" max:"+ self.maximum_amount+ self.base_asset_symbol.ljust(20), self.supported_by_exchanges, self.base_asset, self.echange_asset)
        return result


def fetchExinPrice(source_asset_id, target_asset_id = ""):
    result_fetchPrice = requests.get('https://exinone.com/exincore/markets', params={'base_asset':source_asset_id, "exchange_asset":target_asset_id})
    exin_response = result_fetchPrice.json()

    datalist_in_response = []
    if (exin_response.get("code") == 0):
        for eachData in exin_response.get("data"):
            datalist_in_response.append(Asset_pair_price(eachData))
    return datalist_in_response

def gen_memo_ExinBuy(asset_id_string):
    return base64.b64encode(umsgpack.packb({"A": uuid.UUID("{" + asset_id_string + "}").bytes})).decode("utf-8")

def memo_is_pay_to_exin(memo_at_snap):
    try:
        exin_order = umsgpack.unpackb(base64.b64decode(memo_at_snap))
        print("pack ok")
        asset_uuid_in_myorder = str(uuid.UUID(bytes = exin_order["A"]))
        return asset_uuid_in_myorder
    except :
        print("unpack failed")
        return False
def memo_is_pay_from_exin(input_snapshot):
    memo_at_snap = input_snapshot.memo
    try:
        exin_order = umsgpack.unpackb(base64.b64decode(memo_at_snap))
        if ("C" in exin_order):
            order_result = exin_order["C"]
            headString = ": status of your payment to exin is : "
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
                headString = headString + ", your order is executed at price:" +  exin_order["P"] + input_snapshot.asset.symbol
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
            return headString
        else:
            return False
    except :
        return False


def about_me(input_snapshot):
    if(input_snapshot.opponent_id == EXINCORE_UUID):
        if(input_snapshot.is_sent()):
            asset_id = memo_is_pay_to_exin(input_snapshot.memo)
            return ("Pay " + input_snapshot.amount + " " + input_snapshot.asset.symbol + " to ExinCore to buy asset with id: " + asset_id + " by trace id:" + input_snapshot.trace_id + ", you can verify the result on https://mixin.one/snapshots/" + input_snapshot.snapshot_id)
        if(input_snapshot.is_received()):
            exin_result = memo_is_pay_from_exin(input_snapshot)
            return exin_result
