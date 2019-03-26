import csv

class WalletRecord():
    def __init__(self, pin, userid, session_id, pin_token, private_key):
       self.pin = pin
       self.userid = userid
       self.session_id = session_id
       self.pin_token = pin_token
       self.private_key = private_key

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
