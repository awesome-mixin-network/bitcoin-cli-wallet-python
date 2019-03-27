import urwid
import wallet_api
import pyperclip

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
def verifypin_chosen(button, wallet_obj):
    menu_buttons = []
    response = urwid.Text([u'', button.label, u'\n'])
    menu_buttons.append(response)
    done = menu_button(u'Ok', exit_program)
    menu_buttons.append(done)

    top.open_box(urwid.Filler(urwid.Pile(menu_buttons)))


def manageasset_chosen(button, wallet_obj):
    menu_buttons = []

    response = urwid.Text([u'', button.label, u'\n'])

    menu_buttons.append(response)
    done = menu_button(u'Ok', exit_program)
    menu_buttons.append(done)

    top.open_box(urwid.Filler(urwid.Pile(menu_buttons)))



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

def send_confirm_chosen(button, wallet_asset_uuid_amount_pin_obj):
    wallet_obj = wallet_asset_uuid_amount_pin_obj[0]
    asset_obj  = wallet_asset_uuid_amount_pin_obj[1]
    uuid_obj   = wallet_asset_uuid_amount_pin_obj[2]
    amount_obj = wallet_asset_uuid_amount_pin_obj[3]
    memo_obj   = wallet_asset_uuid_amount_pin_obj[4]
    pin_obj    = wallet_asset_uuid_amount_pin_obj[5]
    #let wallet create uuid for us
    this_uuid  = ""

    transfer_result = wallet_obj.transfer_to(uuid_obj, asset_obj.asset_id, amount_obj, memo_obj, this_uuid, pin_obj)
    if(transfer_result != False):
        response = urwid.Text(["your transaction is confirmed by Mixin Network with snapshot: %s, you can verify on browser:%s"%(transfer_result.snapshot_id, "https://mixin.one/snapshots/" + transfer_result.snapshot_id)])
        done = menu_button(u'Ok', pop_current_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))
    else:
        response = urwid.Text(["your transaction is failed"])
        done = menu_button(u'Ok', pop_current_menu)
        top.open_box(urwid.Filler(urwid.Pile([response, done])))

def send_chosen(button, wallet_asset_obj):

    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]

    menu_buttons = []

    exe_destination_uuid_field = urwid.Edit(u'Destination uuid:\n')
    exe_amount_field = urwid.Edit(u'Amount:\n')
    exe_memo_field = urwid.Edit(u'Memo:\n')
    exe_pin_code_field = urwid.Edit(u'pin:\n', mask=u"")




    menu_buttons.append(exe_destination_uuid_field)
    menu_buttons.append(exe_amount_field)
    menu_buttons.append(exe_memo_field)
    menu_buttons.append(exe_pin_code_field)
    done = menu_button_withobj(u'Send', show_content, (wallet_obj, asset_obj, exe_destination_uuid_field, exe_amount_field, exe_memo_field, exe_pin_code_field))
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

    all_assets = wallet_obj.get_balance()
    for eachAsset in all_assets:
        balance_chosen_menu_buttons.append(menu_button_withobj(eachAsset.name.ljust(15)+":"+ eachAsset.balance, asset_chosen, (wallet_obj, eachAsset)))


    balance_chosen_menu_buttons.append(menu_button(u'Back', pop_current_menu))
    top.open_box(menu(u'user id:' + wallet_obj.userid, balance_chosen_menu_buttons))

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



def asset_chosen(button, wallet_asset_obj):
    wallet_obj = wallet_asset_obj[0]
    asset_obj  = wallet_asset_obj[1]
    asset_chosen_menu_buttons = []
    asset_chosen_menu_buttons.append(menu_button_withobj("send to mixin account", send_chosen, wallet_asset_obj))
    asset_chosen_menu_buttons.append(menu_button_withobj("deposit address", deposit_chosen, wallet_asset_obj))
    asset_chosen_menu_buttons.append(menu_button_withobj("recent transaction", send_chosen, wallet_obj))
    asset_chosen_menu_buttons.append(menu_button_withobj("manage withdraw contacts", manageasset_chosen, wallet_obj))
    asset_chosen_menu_buttons.append(menu_button(u'Back', pop_current_menu))

    top.open_box(menu(asset_obj.name.ljust(15)+":"+ asset_obj.balance, asset_chosen_menu_buttons))


def wallet_chosen(button, wallet_obj):
    wallet_chosen_menu_buttons = []
    wallet_chosen_menu_buttons.append(menu_button_withobj("balance", balance_chosen, wallet_obj))
    wallet_chosen_menu_buttons.append(menu_button_withobj("search snapshots", send_chosen, wallet_obj))
    wallet_chosen_menu_buttons.append(menu_button_withobj("instant exchange token in exin", send_chosen, wallet_obj))
    wallet_chosen_menu_buttons.append(menu_button_withobj("ocean.one exchange", send_chosen, wallet_obj))
    wallet_chosen_menu_buttons.append(menu_button_withobj("verify pin", verifypin_chosen, wallet_obj))
    wallet_chosen_menu_buttons.append(menu_button_withobj("update pin", verifypin_chosen, wallet_obj))
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
def load_wallet(button):
    wallet_records = wallet_api.load_wallet_csv_file('new_users.csv')
    load_wallet_menu_buttons = []
    for each_wallet in wallet_records:
        load_wallet_menu_buttons.append(menu_button_withobj(each_wallet.userid, wallet_chosen, each_wallet))

    load_wallet_menu_buttons.append(menu_button(u'Back', pop_current_menu))
    top.open_box(menu("select wallet", load_wallet_menu_buttons))

def create_wallet(button):
    raise urwid.ExitMainLoop()



menu_top = menu(u'Mixin pywallet', [
    menu_button(u'load wallet', load_wallet),
    sub_menu(u'create wallet', [
        sub_menu(u'Preferences', [
            menu_button(u'Appearance', item_chosen),
        ]),
        menu_button(u'Lock Screen', item_chosen),
    ]),
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
