import urwid
import wallet_api

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



def send_chosen(button, wallet_obj):
    menu_buttons = []

    response = urwid.Text([u'', button.label, u'\n'])
    menu_buttons.append(response)
    done = menu_button(u'Ok', exit_program)
    menu_buttons.append(done)

    top.open_box(urwid.Filler(urwid.Pile(menu_buttons)))



def deposit_chosen(button, wallet_obj):
    menu_buttons = []

    response = urwid.Text([u'', button.label, u'\n'])
    menu_buttons.append(response)
    done = menu_button(u'Ok', exit_program)
    menu_buttons.append(done)

    top.open_box(urwid.Filler(urwid.Pile(menu_buttons)))



def balance_chosen(button, wallet_obj):
    menu_buttons = []
    response = urwid.Text([u'in ', button.label, u'\n'])
    menu_buttons.append(response)

    done = menu_button(u'Ok', exit_program)
    menu_buttons.append(done)
    top.open_box(urwid.Filler(urwid.Pile(menu_buttons)))


def wallet_chosen(button, wallet_obj):
    menu_buttons = []
    response = urwid.Text([u'You chose ', wallet_obj.userid, u'\n'])
    menu_buttons.append(response)
    menu_buttons.append(menu_button_withobj("balance", balance_chosen, wallet_obj))
    menu_buttons.append(menu_button_withobj("deposit", deposit_chosen, wallet_obj))
    menu_buttons.append(menu_button_withobj("send", send_chosen, wallet_obj))
    menu_buttons.append(menu_button_withobj("search snapshots", send_chosen, wallet_obj))
    menu_buttons.append(menu_button_withobj("instant exchange token in exin", send_chosen, wallet_obj))
    menu_buttons.append(menu_button_withobj("ocean.one exchange", send_chosen, wallet_obj))
    menu_buttons.append(menu_button_withobj("manage asset", manageasset_chosen, wallet_obj))
    menu_buttons.append(menu_button_withobj("verify pin", verifypin_chosen, wallet_obj))
    menu_buttons.append(menu_button_withobj("update pin", verifypin_chosen, wallet_obj))

    top.open_box(urwid.Filler(urwid.Pile(menu_buttons)))


def item_chosen(button):
    response = urwid.Text([u'You chose ', button.label, u'\n'])
    done = menu_button(u'Ok', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def exit_program(button):
    raise urwid.ExitMainLoop()
def load_wallet(button):
    wallet_records = wallet_api.load_wallet_csv_file('new_users.csv')
    menu_buttons = []
    for each_wallet in wallet_records:
        menu_buttons.append(menu_button_withobj(each_wallet.userid, wallet_chosen, each_wallet))

    top.open_box(menu("select wallet", menu_buttons))

def create_wallet(button):
    raise urwid.ExitMainLoop()



menu_top = menu(u'Main Menu', [
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

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

top = CascadingBoxes(menu_top)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
