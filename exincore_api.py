import requests
import uuid
import base64
import umsgpack


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
        result = "%s %s %s, exchange: %s"%(self.price.ljust(8), (self.base_asset_symbol)+"/"+self.exchange_asset_symbol.ljust(15), "min:"+self.minimum_amount+" max:"+ self.maximum_amount+ self.base_asset_symbol.ljust(20), self.supported_by_exchanges)
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


