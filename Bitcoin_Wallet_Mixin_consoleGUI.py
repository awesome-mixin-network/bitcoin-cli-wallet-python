import urwid
import wallet_api
import pyperclip
import os
import exincore_api
import mixin_asset_id_collection

def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')
def menu_button_withobj(caption, callback, ooo):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback, ooo)
    return urwid.AttrMap(button, None, focus_map='reversed')


def sub_menu(caption, choices):
    contents = menu(caption, choices)
    def open_menu(button):
        return top.open_box(contents)
    return menu_button([caption, u'...'], open_menu)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))
def create_wallet_chosen(button):
    menu_buttons = []

    wallet_name_field = urwid.Edit(u'wallet name:\n')
    menu_buttons.append(wallet_name_field)

    pin_code_field = urwid.Edit(u'pin:\n', mask=u"*")
    menu_buttons.append(pin_code_field)

    url_token_field = urwid.Edit(u'free token url:\n')
    url_token_field.set_edit_text("http://freemixinapptoken.myrual.me/token")
    menu_buttons.append(url_token_field)

    done = menu_button_withobj(u'Create wallet', create_wallet_confirm_chosen, (wallet_api.WalletRecord("","","", "",""), wallet_name_field, pin_code_field, url_token_field))

    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Create a wallet', menu_buttons))


def verify_pin_chosen(button, wallet_obj):
    menu_buttons = []

    exe_pin_code_field = urwid.Edit(u'pin:\n', mask=u"*")

    menu_buttons.append(exe_pin_code_field)
    done = menu_button_withobj(u'Verify', verify_pin_confirm_chosen, (wallet_obj, exe_pin_code_field))

    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Verify pin', menu_buttons))

def update_pin_chosen(button, wallet_obj):
    menu_buttons = []

    old_pin_code_field = urwid.Edit(u'old pin:\n', mask=u"*")
    new_pin_code_field = urwid.Edit(u'new pin:\n', mask=u"*")

    menu_buttons.append(old_pin_code_field)
    menu_buttons.append(new_pin_code_field)

    done = menu_button_withobj(u'Update', update_pin_confirm_chosen, (wallet_obj, old_pin_code_field, new_pin_code_field))

    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Update pin', menu_buttons))


def withdraw_asset_chosen(button, wallet_asset_obj):
    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]


    menu_buttons = []

    withdraw_addresses_result = wallet_obj.get_asset_withdrawl_addresses(asset_obj.asset_id)
    if(withdraw_addresses_result.is_success):
        withdraw_addresses = withdraw_addresses_result.data
    else:
        withdraw_addresses = []
    for each_withdraw_address in withdraw_addresses:
        select_to_detail = menu_button_withobj(each_withdraw_address.label, withdraw_asset_to_address_chosen, (wallet_obj, asset_obj, each_withdraw_address))
        menu_buttons.append(select_to_detail)
    if (asset_obj.chain_id != mixin_asset_id_collection.EOS_ASSET_ID):
        add_new_address = menu_button_withobj(u'Add new', add_withdraw_address_bitcoin_style, wallet_asset_obj)
    else:
        add_new_address = menu_button_withobj(u'Add new', add_withdraw_address_eos_style, wallet_asset_obj)

    menu_buttons.append(add_new_address)
    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(back)

    top.open_box(menu(u'Manage withdraw addresses for ' + asset_obj.name, menu_buttons))


def manageasset_chosen(button, wallet_asset_obj):
    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]


    menu_buttons = []

    withdraw_addresses_result = wallet_obj.get_asset_withdrawl_addresses(asset_obj.asset_id)
    if withdraw_addresses_result.is_success:
        withdraw_addresses = withdraw_addresses_result.data
    else:
        withdraw_addresses = []
    for each_withdraw_address in withdraw_addresses:
        select_to_detail = menu_button_withobj(each_withdraw_address.label, show_withdraw_address_remove, (wallet_obj, each_withdraw_address))
        menu_buttons.append(select_to_detail)


    #done = menu_button_withobj(u'Send', show_content, (wallet_obj, asset_obj, "12", "23", "memo", "pin"))

    if (asset_obj.chain_id != mixin_asset_id_collection.EOS_ASSET_ID):
        add_new_address = menu_button_withobj(u'Add new', add_withdraw_address_bitcoin_style, wallet_asset_obj)
    else:
        add_new_address = menu_button_withobj(u'Add new', add_withdraw_address_eos_style, wallet_asset_obj)
    back = menu_button(u'Back', pop_current_menu)

    menu_buttons.append(add_new_address)
    menu_buttons.append(back)

    top.open_box(menu(u'Manage withdraw addresses for ' + asset_obj.name, menu_buttons))

def show_content(button, wallet_asset_uuid_amount_pin_obj):
    wallet_obj = wallet_asset_uuid_amount_pin_obj[0]
    asset_obj  = wallet_asset_uuid_amount_pin_obj[1]
    uuid_obj   = wallet_asset_uuid_amount_pin_obj[2]
    amount_obj = wallet_asset_uuid_amount_pin_obj[3]
    memo_obj   = wallet_asset_uuid_amount_pin_obj[4]
    pin_obj    = wallet_asset_uuid_amount_pin_obj[5]
    this_uuid  = ""

    response = urwid.Text([asset_obj.asset_id , uuid_obj.get_edit_text(), amount_obj.get_edit_text(), memo_obj.get_edit_text(), pin_obj.get_edit_text(), this_uuid])

    done = menu_button(u'Ok', pop_current_menu)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def add_withdraw_address_confirm_chosen(button, wallet_asset_uuid_amount_pin_obj):
    wallet_obj = wallet_asset_uuid_amount_pin_obj[0]
    asset_obj  = wallet_asset_uuid_amount_pin_obj[1]
    deposit_address   = wallet_asset_uuid_amount_pin_obj[2]
    tag_content = wallet_asset_uuid_amount_pin_obj[3]
    account_name_obj   = wallet_asset_uuid_amount_pin_obj[4]
    account_tag_obj  = wallet_asset_uuid_amount_pin_obj[5]
    pin_obj    = wallet_asset_uuid_amount_pin_obj[6]
    #let wallet create uuid for us

    create_address_result = wallet_obj.create_address(asset_obj.asset_id, deposit_address.get_edit_text(), tag_content.get_edit_text(), asset_pin = pin_obj.get_edit_text())

    if(create_address_result.is_success):
        response = urwid.Text(["the address :", deposit_address.get_edit_text(), " is added to your account with id:", create_address_result.data.address_id])
        done = menu_button(u'Ok', pop_to_account_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))
    else:
        response = urwid.Text(["Failed deposit_address %s tag_content %s %s"%(deposit_address.get_edit_text(), tag_content.get_edit_text(), create_address_result)])
        done = menu_button(u'Ok', pop_to_account_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))


def withdraw_asset_to_address_confirm_chosen(button, wallet_address_amount_pin_obj):
    wallet_obj   = wallet_address_amount_pin_obj[0]
    address_obj  = wallet_address_amount_pin_obj[1]

    amount_obj   = wallet_address_amount_pin_obj[2]
    memo_obj     = wallet_address_amount_pin_obj[3]
    pin_obj      = wallet_address_amount_pin_obj[4]
    this_uuid  = ""

    withdraw_asset_to_address_result = wallet_obj.withdraw_asset_to(address_obj.address_id, amount_obj.get_edit_text(), memo_obj.get_edit_text(), this_uuid, pin_obj.get_edit_text())
    if(withdraw_asset_to_address_result.is_success):
        #pop_to_account_menu(button)
        response = urwid.Text(["Your withdraw operation is successful, snapshot id is:", withdraw_asset_to_address_result.data.snapshot_id])
        done = menu_button(u'Ok', pop_to_account_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))

    else:
        response = urwid.Text(["Your withdraw asset operation is failed due to ", str(withdraw_asset_to_address_result)])
        done = menu_button(u'Ok', pop_to_account_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))



def remove_withdraw_address_confirm_chosen(button, wallet_asset_uuid_amount_pin_obj):
    wallet_obj = wallet_asset_uuid_amount_pin_obj[0]
    address_obj  = wallet_asset_uuid_amount_pin_obj[1]
    pin_obj    = wallet_asset_uuid_amount_pin_obj[2]
    #let wallet create uuid for us
    this_uuid  = ""

    remove_address_result = wallet_obj.remove_address(address_obj.address_id, pin_obj.get_edit_text())
    response = urwid.Text([str(remove_address_result)])
    done = menu_button(u'Ok', pop_to_account_menu)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def create_wallet_confirm_chosen(button, wallet_name_pin_obj):
    wallet_obj = wallet_name_pin_obj[0]
    name_obj   = wallet_name_pin_obj[1]
    pin_obj    = wallet_name_pin_obj[2]
    url_obj    = wallet_name_pin_obj[3]

    thisAccountRSAKeyPair = wallet_api.RSAKey4Mixin()
    body = {
        "session_secret": thisAccountRSAKeyPair.session_key,
        "full_name": name_obj.get_edit_text()
    }

    token2create = wallet_api.fetchTokenForCreateUser(body, url_obj.get_edit_text())

    create_wallet_result = wallet_obj.create_wallet(thisAccountRSAKeyPair.session_key, name_obj.get_edit_text(), token2create)
    if(create_wallet_result.is_success):
        create_wallet_result.data.private_key = thisAccountRSAKeyPair.private_key
        wallet_api.append_wallet_into_csv_file(create_wallet_result.data, "new_users.csv")
        new_wallet = wallet_api.WalletRecord("",create_wallet_result.data.user_id, create_wallet_result.data.session_id, create_wallet_result.data.pin_token, create_wallet_result.data.private_key)

        create_pin_result = new_wallet.update_pin("", pin_obj.get_edit_text())
        if(create_pin_result.is_success):
            response = urwid.Text(["Successfully created wallet with your pin"])
        else:
            response = urwid.Text(["Wallet is created, pin is not created. Update pin please"])
        done_button = menu_button(u'Ok', pop_current_and_more_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done_button])))
    else:
        response = urwid.Text(["Failed to create account"])
        done = menu_button(u'Ok', pop_current_and_more_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))

def verify_pin_confirm_chosen(button, wallet_asset_uuid_amount_pin_obj):
    wallet_obj = wallet_asset_uuid_amount_pin_obj[0]
    pin_obj    = wallet_asset_uuid_amount_pin_obj[1]
    verify_result = wallet_obj.verify_pin(pin_obj.get_edit_text())
    if(verify_result.is_success):
        verify_url = "Successfully verified pin"
        response = urwid.Text(["Successfully verified pin"])
        done_button = menu_button(u'Ok', pop_to_account_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done_button])))
    else:
        response = urwid.Text(["Failed to verify pin"])
        done = menu_button(u'Ok', pop_current_and_more_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))

def update_pin_confirm_chosen(button, wallet_asset_uuid_amount_pin_obj):
    wallet_obj = wallet_asset_uuid_amount_pin_obj[0]
    old_pin_obj    = wallet_asset_uuid_amount_pin_obj[1]
    new_pin_obj    = wallet_asset_uuid_amount_pin_obj[2]
    update_result = wallet_obj.update_pin(old_pin_obj.get_edit_text(), new_pin_obj.get_edit_text())
    if(update_result.is_success):
        response = urwid.Text(["Successfully update pin"])
        done_button = menu_button(u'Ok', pop_to_account_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done_button])))
    else:
        response = urwid.Text(["Failed to update pin"])
        done = menu_button(u'Ok', pop_current_and_more_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))

def Pay2Exin_confirm_chosen(button, wallet_asset_uuid_amount_pin_obj):
    wallet_obj    = wallet_asset_uuid_amount_pin_obj[0]
    asset_id_obj  = wallet_asset_uuid_amount_pin_obj[1]
    uuid_exin_obj = wallet_asset_uuid_amount_pin_obj[2]
    amount_obj    = wallet_asset_uuid_amount_pin_obj[3]
    memo_obj      = wallet_asset_uuid_amount_pin_obj[4]
    pin_obj       = wallet_asset_uuid_amount_pin_obj[5]
    this_uuid     = ""

    transfer_result = wallet_obj.transfer_to(uuid_exin_obj, asset_id_obj, amount_obj, memo_obj, this_uuid, pin_obj.get_edit_text())
    if(transfer_result.is_success):
        verify_url = "https://mixin.one/snapshots/" + transfer_result.data.snapshot_id
        response = urwid.Text([str(transfer_result.data), ". You can verify on browser:\n%s"%verify_url])
        done_button = menu_button(u'Ok', pop_to_account_menu)
        copy_button = menu_button_withobj(("copy %s to clip board"%(verify_url)), copy_content_to_system_clip, verify_url)
        top.open_box(urwid.Filler(urwid.Pile([response, copy_button, done_button])))
    else:
        response = urwid.Text([str(transfer_result)])
        done = menu_button(u'Ok', pop_current_and_more_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))


def PayExin_input_pin_chosen(button, wallet_tradepair_amount):
    wallet_obj     = wallet_tradepair_amount[0]
    tradeprice_obj = wallet_tradepair_amount[1]
    amount_obj     = wallet_tradepair_amount[2]
    amount_to_pay = amount_obj.get_edit_text()
    price_base_asset = tradeprice_obj.price
    estimated_target_amount = str(float(amount_to_pay)/float(price_base_asset))


    menu_buttons = []

    memo_for_exin = exincore_api.gen_memo_ExinBuy(tradeprice_obj.echange_asset)

    exe_pin_code_field = urwid.Edit(u'pin:\n', mask=u"*")
    menu_buttons.append(exe_pin_code_field)
    done = menu_button_withobj(u'Pay ', Pay2Exin_confirm_chosen, (wallet_obj, tradeprice_obj.base_asset, exincore_api.EXINCORE_UUID, amount_to_pay, memo_for_exin, exe_pin_code_field))


    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Pay ' + amount_to_pay + " " + tradeprice_obj.base_asset_symbol+ " to buy " + estimated_target_amount + " " + tradeprice_obj.exchange_asset_symbol + " on ExinCore" , menu_buttons))

def send_confirm_chosen(button, wallet_asset_uuid_amount_pin_obj):
    wallet_obj = wallet_asset_uuid_amount_pin_obj[0]
    asset_obj  = wallet_asset_uuid_amount_pin_obj[1]
    uuid_obj   = wallet_asset_uuid_amount_pin_obj[2]
    amount_obj = wallet_asset_uuid_amount_pin_obj[3]
    memo_obj   = wallet_asset_uuid_amount_pin_obj[4]
    pin_obj    = wallet_asset_uuid_amount_pin_obj[5]
    #let wallet create uuid for us
    this_uuid  = ""

    transfer_result = wallet_obj.transfer_to(uuid_obj.get_edit_text(), asset_obj.asset_id, amount_obj.get_edit_text(), memo_obj.get_edit_text(), this_uuid, pin_obj.get_edit_text())
    if(transfer_result.is_success):
        verify_url = "https://mixin.one/snapshots/" + transfer_result.data.snapshot_id
        response = urwid.Text([str(transfer_result.data), ". You can verify on browser:\n%s"%verify_url])
        done_button = menu_button(u'Ok', pop_to_account_menu)
        copy_button = menu_button_withobj(("copy %s to clip board"%(verify_url)), copy_content_to_system_clip, verify_url)
        top.open_box(urwid.Filler(urwid.Pile([response, copy_button, done_button])))
    else:
        response = urwid.Text([str(transfer_result)])
        done = menu_button(u'Ok', pop_current_and_more_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))
def tradepair_sell_chosen(button, wallet_asset_obj):

    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]

    menu_buttons = []

    exe_destination_uuid_field = urwid.Edit(u'Destination uuid:\n')
    exe_amount_field = urwid.Edit(u'Amount:\n')
    exe_memo_field = urwid.Edit(u'Memo:\n')
    exe_pin_code_field = urwid.Edit(u'pin:\n', mask=u"*")


    menu_buttons.append(exe_destination_uuid_field)
    menu_buttons.append(exe_amount_field)
    menu_buttons.append(exe_memo_field)
    menu_buttons.append(exe_pin_code_field)
    done = menu_button_withobj(u'Send', send_confirm_chosen, (wallet_obj, asset_obj, exe_destination_uuid_field, exe_amount_field, exe_memo_field, exe_pin_code_field))
    #done = menu_button_withobj(u'Send', show_content, (wallet_obj, asset_obj, "12", "23", "memo", "pin"))

    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Send ' + asset_obj.name, menu_buttons))



def tradepair_buy_chosen(button, wallet_asset_obj):

    wallet_obj        = wallet_asset_obj[0]
    base_asset_id     = wallet_asset_obj[1]
    target_asset_id = wallet_asset_obj[2]

    menu_buttons = []
    asset_price_result = exincore_api.fetchExinPrice(base_asset_id, target_asset_id)
    #confirm price again
    this_trade_price = asset_price_result[0]
    minimum_pay_base_asset = this_trade_price.minimum_amount
    maximum_pay_base_asset = this_trade_price.maximum_amount
    price_base_asset       = this_trade_price.price
    base_sym               = this_trade_price.base_asset_symbol
    target_sym             = this_trade_price.exchange_asset_symbol
     
    single_balance = wallet_obj.get_singleasset_balance(base_asset_id)
    if single_balance.is_success:
        pay_amount_field = urwid.Edit(u'Pay amount(%s in your balance):\n'%single_balance.data.balance)
        menu_buttons.append(pay_amount_field)
        done = menu_button_withobj(u'Input pin to buy '+ this_trade_price.exchange_asset_symbol, PayExin_input_pin_chosen, (wallet_obj, this_trade_price, pay_amount_field))

        back = menu_button(u'Back', pop_current_menu)
        menu_buttons.append(done)
        menu_buttons.append(back)

    top.open_box(menu(this_trade_price.price + " " + this_trade_price.base_asset_symbol + " -> " + " 1 " + this_trade_price.exchange_asset_symbol, menu_buttons))


def send_chosen(button, wallet_asset_obj):

    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]

    menu_buttons = []

    exe_destination_uuid_field = urwid.Edit(u'Destination uuid:\n')
    exe_amount_field = urwid.Edit(u'Amount:\n')
    exe_memo_field = urwid.Edit(u'Memo:\n')
    exe_pin_code_field = urwid.Edit(u'pin:\n', mask=u"*")




    menu_buttons.append(exe_destination_uuid_field)
    menu_buttons.append(exe_amount_field)
    menu_buttons.append(exe_memo_field)
    menu_buttons.append(exe_pin_code_field)
    done = menu_button_withobj(u'Send', send_confirm_chosen, (wallet_obj, asset_obj, exe_destination_uuid_field, exe_amount_field, exe_memo_field, exe_pin_code_field))
    #done = menu_button_withobj(u'Send', show_content, (wallet_obj, asset_obj, "12", "23", "memo", "pin"))

    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Send ' + asset_obj.name, menu_buttons))



def deposit_chosen(button, wallet_asset_obj):
    deposit_chosen_menu_buttons = []

    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]
 
    response = urwid.Text([u'Deposit address of ', asset_obj.name])
    deposit_chosen_menu_buttons.append(response)

    deposit_address_title_value_segments = asset_obj.deposit_address()
    for each_seg in deposit_address_title_value_segments:

        response = urwid.Text([u'', each_seg["title"] + " : " + each_seg["value"]])
        deposit_chosen_menu_buttons.append(response)
        deposit_chosen_menu_buttons.append(urwid.Divider())

        deposit_chosen_menu_buttons.append(menu_button_withobj(("copy %s"%(each_seg["title"])), copy_content_to_system_clip, each_seg["value"]))


    deposit_chosen_menu_buttons.append(menu_button(u'Back', pop_current_menu))
    top.open_box(urwid.Filler(urwid.Pile(deposit_chosen_menu_buttons)))



def balance_chosen(button, wallet_obj):
    balance_chosen_menu_buttons = []

    balance_result = wallet_obj.get_balance()
    if (balance_result.is_success):
        all_assets = balance_result.data
        if (len(all_assets) == 0):
            for eachAssetID in mixin_asset_id_collection.MIXIN_DEFAULT_CHAIN_GROUP:
                this_asset = wallet_obj.get_singleasset_balance(eachAssetID)
        else:
            for eachAsset in all_assets:
                balance_chosen_menu_buttons.append(menu_button_withobj(eachAsset.name.ljust(15)+":"+ eachAsset.balance, asset_chosen, (wallet_obj, eachAsset)))
            usdt_balance_on_btc = wallet_obj.get_singleasset_balance(mixin_asset_id_collection.USDT_ASSET_ID)
            if(usdt_balance_on_btc.data.balance == "0"):
                balance_chosen_menu_buttons.append(menu_button_withobj(usdt_balance_on_btc.data.name.ljust(15)+":"+ usdt_balance_on_btc.data.balance, asset_chosen, (wallet_obj, usdt_balance_on_btc.data)))


    balance_chosen_menu_buttons.append(menu_button(u'Back', pop_current_menu))
    top.open_box(menu(u'user id:' + wallet_obj.userid, balance_chosen_menu_buttons))

def exin_chosen(button, wallet_obj):
    exin_trade_pair_chosen_menu_buttons = []

    trade_asset_list = exincore_api.fetchExinPrice(mixin_asset_id_collection.USDT_ASSET_ID)
    for eachPair in trade_asset_list:
        exin_trade_pair_chosen_menu_buttons.append(menu_button_withobj(str(eachPair), exin_tradepair_chosen, (wallet_obj, eachPair)))

    exin_trade_pair_chosen_menu_buttons.append(menu_button(u'Back', pop_current_menu))
    top.open_box(menu(u'Exin instant trade:', exin_trade_pair_chosen_menu_buttons))


def balance_send_to_mixin(button, wallet_asset_obj):
    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]

    response = urwid.Text([u'Send ', asset_obj.name])
    done = menu_button(u'Ok', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))



def copy_content_to_system_clip(button, to_copy_content):
    pyperclip.copy(to_copy_content)
    response = urwid.Text([u'Content has been copied to your clipboard'])
    done = menu_button(u'Ok', pop_current_menu)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def remove_withdraw_address_chosen(button, wallet_asset_obj):

    wallet_obj = wallet_asset_obj[0]
    address_obj  = wallet_asset_obj[1]

    menu_buttons = []

    exe_pin_code_field = urwid.Edit(u'pin:\n', mask=u"*")
    menu_buttons.append(exe_pin_code_field)

    done = menu_button_withobj(u'Remove', remove_withdraw_address_confirm_chosen, (wallet_obj, address_obj, exe_pin_code_field))
    #done = menu_button_withobj(u'Send', show_content, (wallet_obj, asset_obj, "12", "23", "memo", "pin"))

    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Remove address' + address_obj.label, menu_buttons))
def withdraw_asset_to_address_chosen(button, wallet_asset_address_obj):

    wallet_obj  = wallet_asset_address_obj[0]

    asset_obj   = wallet_asset_address_obj[1]
    address_obj = wallet_asset_address_obj[2]

    menu_buttons = []
    withdraw_amount_field = urwid.Edit(u'Amount:\n')
    menu_buttons.append(withdraw_amount_field)

    withdraw_memo_field = urwid.Edit(u'Memo:\n')
    menu_buttons.append(withdraw_memo_field)
    withdraw_pin_code_field = urwid.Edit(u'pin:\n', mask=u"*")
    menu_buttons.append(withdraw_pin_code_field)

    done = menu_button_withobj(u'Withdraw', withdraw_asset_to_address_confirm_chosen, (wallet_obj, address_obj, withdraw_amount_field, withdraw_memo_field, withdraw_pin_code_field))

    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Withdraw asset to ' + str(address_obj), menu_buttons))



def show_withdraw_address_remove(button, wallet_asset_obj):
    wallet_obj = wallet_asset_obj[0]
    address_obj  = wallet_asset_obj[1]

    menu_buttons = []

    if(address_obj.label != ""):
        menu_buttons.append(urwid.Text([u'Label:'.ljust(20), address_obj.label]))
    if(address_obj.public_key!= ""):
        menu_buttons.append(urwid.Text([u'Deposit address:'.ljust(20), address_obj.public_key]))
    if(address_obj.account_name!= ""):
        menu_buttons.append(urwid.Text([u'Account name:'.ljust(20), address_obj.account_name]))
    if(address_obj.account_tag!= ""):
        menu_buttons.append(urwid.Text([u'Account tag:'.ljust(20), address_obj.account_tag]))
    if(address_obj.fee!= ""):
        menu_buttons.append(urwid.Text([u'fee:'.ljust(20), address_obj.fee]))
    if(address_obj.reserve != ""):
        menu_buttons.append(urwid.Text([u'reserve:'.ljust(20), address_obj.reserve]))
    if(address_obj.dust!= ""):
        menu_buttons.append(urwid.Text([u'dust:'.ljust(20), address_obj.dust]))


    done = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    remove = menu_button_withobj(u'Remove', remove_withdraw_address_chosen, (wallet_obj, address_obj))
    menu_buttons.append(remove)

    top.open_box(menu(u'Withdraw address detail', menu_buttons))

def add_withdraw_address_eos_style(button, to_copy_content):
    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]

    menu_buttons = []

    deposit_address_field = urwid.Edit(u'Deposit address:\n')
    label_field = urwid.Edit(u'Account label:\n')
    pin_code_field = urwid.Edit(u'pin:\n', mask=u"*")


    menu_buttons.append(deposit_address_field)
    menu_buttons.append(label_field)
    menu_buttons.append(pin_code_field)
    done = menu_button_withobj(u'Add ', add_withdraw_address_confirm_chosen, (wallet_obj, asset_obj, deposit_address_field, label_field, "", "",pin_code_field))
    #done = menu_button_withobj(u'Send', show_content, (wallet_obj, asset_obj, "12", "23", "memo", "pin"))

    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Add withdraw address for ' + asset_obj.name, menu_buttons))


def add_withdraw_address_bitcoin_style(button, wallet_asset_obj):
    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]

    menu_buttons = []

    deposit_address_field = urwid.Edit(u'Deposit address:\n')
    label_field = urwid.Edit(u'Account label:\n')
    pin_code_field = urwid.Edit(u'pin:\n', mask=u"*")


    menu_buttons.append(deposit_address_field)
    menu_buttons.append(label_field)
    menu_buttons.append(pin_code_field)
    done = menu_button_withobj(u'Add ', add_withdraw_address_confirm_chosen, (wallet_obj, asset_obj, deposit_address_field, label_field, "", "",pin_code_field))
    #done = menu_button_withobj(u'Send', show_content, (wallet_obj, asset_obj, "12", "23", "memo", "pin"))

    back = menu_button(u'Back', pop_current_menu)
    menu_buttons.append(done)
    menu_buttons.append(back)

    top.open_box(menu(u'Add withdraw address for ' + asset_obj.name, menu_buttons))

def asset_chosen(button, wallet_asset_obj):
    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]
    asset_chosen_menu_buttons = []
    asset_chosen_menu_buttons.append(menu_button_withobj("send to mixin account", send_chosen, wallet_asset_obj))
    asset_chosen_menu_buttons.append(menu_button_withobj("withdraw to other address", withdraw_asset_chosen, wallet_asset_obj))
    asset_chosen_menu_buttons.append(menu_button_withobj("show deposit address", deposit_chosen, wallet_asset_obj))
    asset_chosen_menu_buttons.append(menu_button_withobj("manage withdraw contacts", manageasset_chosen, wallet_asset_obj))
    #asset_chosen_menu_buttons.append(menu_button_withobj("recent transaction", send_chosen, wallet_obj)) 

    asset_chosen_menu_buttons.append(menu_button(u'Back', pop_current_menu))

    top.open_box(menu(asset_obj.name.ljust(15)+":"+ asset_obj.balance, asset_chosen_menu_buttons))
def exin_tradepair_chosen(button, wallet_asset_obj):
    wallet_obj = wallet_asset_obj[0]
    tradepair_obj  = wallet_asset_obj[1]
    tradepair_chosen_menu_buttons = []
    tradepair_chosen_menu_buttons.append(menu_button_withobj("buy",  tradepair_buy_chosen,  (wallet_obj, tradepair_obj.base_asset, tradepair_obj.echange_asset)))
    tradepair_chosen_menu_buttons.append(menu_button_withobj("sell", tradepair_buy_chosen, (wallet_obj, tradepair_obj.echange_asset, tradepair_obj.base_asset)))

    tradepair_chosen_menu_buttons.append(menu_button(u'Back', pop_current_menu))

    top.open_box(menu(tradepair_obj.base_asset_symbol + " <-> " + tradepair_obj.exchange_asset_symbol, tradepair_chosen_menu_buttons))


def wallet_chosen(button, wallet_obj):
    wallet_chosen_menu_buttons = []
    wallet_chosen_menu_buttons.append(menu_button_withobj("balance", balance_chosen, wallet_obj))
    #wallet_chosen_menu_buttons.append(menu_button_withobj("search snapshots", send_chosen, wallet_obj))
    wallet_chosen_menu_buttons.append(menu_button_withobj("instant exchange token in exin", exin_chosen, wallet_obj))
    #wallet_chosen_menu_buttons.append(menu_button_withobj("ocean.one exchange", send_chosen, wallet_obj))
    wallet_chosen_menu_buttons.append(menu_button_withobj("verify pin", verify_pin_chosen, wallet_obj))
    wallet_chosen_menu_buttons.append(menu_button_withobj("update pin", update_pin_chosen, wallet_obj))
    wallet_chosen_menu_buttons.append(menu_button(u'Back', pop_current_menu))

    top.open_box(menu(u'user id:' + wallet_obj.userid, wallet_chosen_menu_buttons))

def item_chosen(button):
    response = urwid.Text([u'You chose ', button.label, u'\n'])
    done = menu_button(u'Ok', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def exit_program(button):
    raise urwid.ExitMainLoop()
def pop_current_menu(button):
    top.close_box()

def pop_current_and_more_menu(button):
    top.close_box()
    top.close_box()
def pop_current_and_more_more_menu(button):
    top.close_box()
    top.close_box()
    top.close_box()
def pop_to_account_menu(button):
    top.back_to_account()
def load_wallet(button):
    if(os.path.isfile("new_users.csv")):
        wallet_records = wallet_api.load_wallet_csv_file('new_users.csv')
        load_wallet_menu_buttons = []
        for each_wallet in wallet_records:
            load_wallet_menu_buttons.append(menu_button_withobj(each_wallet.userid, wallet_chosen, each_wallet))

        load_wallet_menu_buttons.append(menu_button(u'Back', pop_current_menu))
        top.open_box(menu("select wallet", load_wallet_menu_buttons))
    else:
        response = urwid.Text([u'No local wallet record, Please create one', u'\n'])
        done = menu_button(u'Ok', pop_current_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))



menu_top = menu(u'Mixin pywallet', [
    menu_button(u'load wallet', load_wallet),
    menu_button(u'create wallet', create_wallet_chosen),
    menu_button('exit', exit_program)
])


class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 10

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u'/'))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1
    def back_to_account(self):
        while (self.box_level > 3):
            self.original_widget = self.original_widget[0]
            self.box_level -= 1

    def close_box(self):
        if self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

top = CascadingBoxes(menu_top)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')], handle_mouse=False).run()
