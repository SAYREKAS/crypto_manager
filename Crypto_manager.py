import zlib
import base64
import tempfile
import threading
from db import *
import tkinter as tk
from tkinter import END
from tkinter import ttk
from tkinter import messagebox as mb
from parser import response, get_coin_info, check_for_exist_coin, response_update
from settings import (appx, appy, dispx, dispy, element_width, name_colour1, buy_colour1, buy_colour2,
                      sell_color1, sell_color2, balance_colour1, balance_colour2, menu_bg_colour, get_settings,
                      reset_settings, update_settings)

ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBysAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

# глобальні перемінні
sell_count: int = 0
crypto_summ: float = 0
stable_summ: float = 0
profit_summ: float = 0
equivalent_summ: float = 0
sell_percent_summ: float = 0
realized_income_summ: float = 0
unrealized_income_summ: float = 0

number_of_coins_in_portfolio: int = 0
all_coin_name: tuple = ()
coin_info: list = []


class MainWindow:
    """
    Класс який створює батьківське вікно програми.
    доступні параметри:
    title, app_res, disp_res, resizable,background
    """

    def __init__(self, title='my ap', app_res=(500, 500), disp_res=(1920, 1080), resizable=(False, False),
                 background='white'):
        x = (disp_res[0] // 2) - (app_res[0] // 2)
        y = (disp_res[1] // 2) - (app_res[1] // 2)

        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"+{x}+{y}")
        self.root.minsize(app_res[0], app_res[1])
        self.root.config(background=background)
        self.root.resizable(resizable[0], resizable[1])
        self.root.iconbitmap(default=ICON_PATH)

    def start(self):
        self.root.mainloop()


class ChildWindow:
    """
    Класс який створює дочірнє вікно для батьківського вікна програми.
    обов'язковий параметер "top_lvl" вказує на батьківське вікно.
    доступні параметри: title, app_res, disp_res, resizable,background

    """

    def __init__(self, top_lvl, title='my children window', app_res=(500, 500), disp_res=(1920, 1080),
                 resizable=(False, False), background='white'):
        x = (disp_res[0] // 2) - (app_res[0] // 2)
        y = (disp_res[1] // 2) - (app_res[1] // 2)

        self.root = tk.Toplevel(top_lvl)
        self.root.title(title)
        self.root.geometry(f"+{x}+{y}")
        self.root.resizable(resizable[0], resizable[1])
        self.root.minsize(app_res[0], app_res[1])
        self.root.config(background=background)
        self.root.grab_set()


def refresh_frame(frame):
    """знищуємо старі віджети у фреймі"""
    for widget in frame.winfo_children():
        widget.destroy()


def reset_global_variable():
    """присвоюємо глобальним перемінним стандартні значення,перед записом/зчитуванням в/з них актуальної інформації"""

    global sell_count, crypto_summ, stable_summ, profit_summ, equivalent_summ, sell_percent_summ, \
        realized_income_summ, unrealized_income_summ, number_of_coins_in_portfolio, all_coin_name, \
        coin_info

    sell_count = 0
    crypto_summ = 0
    stable_summ = 0
    profit_summ = 0
    equivalent_summ = 0
    sell_percent_summ = 0
    realized_income_summ = 0
    unrealized_income_summ = 0

    all_coin_name = get_all_coin_name()
    number_of_coins_in_portfolio = len(all_coin_name)
    coin_info = get_coin_info(all_coin_name)


def show_coin_in_portfolio():
    """ виводимо віджети з інформацією про портфоліо в головне меню"""

    global sell_count, profit_summ, equivalent_summ, sell_percent_summ, realized_income_summ, \
        unrealized_income_summ, crypto_summ, stable_summ

    reset_global_variable()
    refresh_frame(fr2)

    # читаємо файл з налаштуваннями
    try:
        sorting = get_settings()['sorting']
        reverse = get_settings()['reverse']
    except Exception as e:
        reset_settings()
        sorting = get_settings()['sorting']
        reverse = get_settings()['reverse']
        e.add_note('Файл з налаштуваннями перезаписано')
        print()

    # заповнюємо новими даними

    crypto = []
    stable = []

    if not all_coin_name:
        print("В портфелі немає монет")
        add_coin_menu()
    else:
        for enum, coin in enumerate(coin_info):
            buy_summ = get_buy_summ(coin['name'].lower())['coins']
            buy_spent_summ = get_buy_summ(coin['name'].lower())['usd']
            buy_avg = get_buy_summ(coin['name'].lower())['avg']

            sell_summ = get_sell_summ(coin['name'].lower())['coins']
            sell_spent_summ = get_sell_summ(coin['name'].lower())['usd']
            sell_avg = get_sell_summ(coin['name'].lower())['avg']

            balance = round(buy_summ - sell_summ, 4)
            equivalent = round(coin['price'] * balance, 2)
            realized_income = round(sell_spent_summ - (sell_summ * buy_avg), 2)
            unrealized_income = round(equivalent - (balance * buy_avg), 2)
            profit = round(realized_income + unrealized_income, 2)
            sell_percent = round(sell_summ * 100 / buy_summ if buy_summ > 0 else 0.0, 2)

            sell_count += 1 if sell_percent > 0 else 0
            profit_summ += profit
            equivalent_summ += equivalent
            sell_percent_summ += sell_percent
            realized_income_summ += realized_income
            unrealized_income_summ += unrealized_income

            crypto_summ += equivalent if 'stablecoin' not in coin['tags'] else 0
            stable_summ += equivalent if 'stablecoin' in coin['tags'] else 0

            if 'stablecoin' not in coin['tags']:
                crypto.append((
                    (coin['price'], '$'),
                    (coin['name'], coin['symbol']),
                    (buy_summ, ''),
                    (buy_spent_summ, '$'),
                    (buy_avg, '$'),
                    (sell_summ, ''),
                    (sell_spent_summ, '$'),
                    (sell_avg, '$'),
                    (balance, coin['symbol']),
                    (equivalent, '$'),
                    (unrealized_income, '$'),
                    (realized_income, '$'),
                    (profit, '$'),
                    (sell_percent, '%'),
                ))

            elif 'stablecoin' in coin['tags']:
                stable.append((
                    (coin['price'], '$'),
                    (coin['name'], coin['symbol']),
                    (buy_summ, ''),
                    (buy_spent_summ, '$'),
                    (buy_avg, '$'),
                    (sell_summ, ''),
                    (sell_spent_summ, '$'),
                    (sell_avg, '$'),
                    (balance, coin['symbol']),
                    (equivalent, '$'),
                    (unrealized_income, '$'),
                    (realized_income, '$'),
                    (profit, '$'),
                    (sell_percent, '%'),
                ))

    def create_labels(data_list, title, start_row):
        (tk.Label(fr2, text=title, background='gray', fg='white', font=("Verdana", 9))
         .grid(row=start_row, column=0, columnspan=14, pady=(10, 0), sticky='NSEW'))

        for enum_row, coin_data in enumerate(data_list):
            for num_column, (data, end_text) in enumerate(coin_data):
                (tk.Label(fr2, text=f"{data} {end_text}", font=("Verdana", 8), height=1,
                          width=12 if num_column not in [1, 8] else 20,
                          background='#23211E' if enum_row % 2 == 0 else '#1B1A17',
                          fg='white' if num_column not in [10, 11, 12] else 'white'
                          if data == 0 else 'green' if data > 0 else 'red')
                 .grid(row=enum_row + start_row + 1, column=num_column, sticky='NSEW'))

    if crypto:
        create_labels(sorted(crypto, key=lambda x: x[sorting], reverse=reverse), 'КРИПТОВАЛЮТА', 0)
    if stable:
        create_labels(sorted(stable, key=lambda x: x[sorting], reverse=reverse), 'СТАБІЛЬНІ МОНЕТИ',
                      number_of_coins_in_portfolio + 1)

    usd_equal_lbl.config(text=f"{equivalent_summ:.2f} $")
    realized_profit_lbl.config(text=f"{realized_income_summ:.2f} $")
    unrealized_profit_lbl.config(text=f"{unrealized_income_summ:.2f} $")
    sell_percent_lbl.config(text=f"{(sell_percent_summ / sell_count):.2f} %" if sell_count != 0 else '0 %')
    profit_lbl.config(text=f"{profit_summ:.2f} $")


def show_percent_change():
    refresh_frame(fr4)

    # малюємо шапку
    (tk.Label(fr4, text='зміни в цінах', fg='white', background='#808080', width=45, font=("Helvetica", 12))
     .grid(row=0, column=0, columnspan=7, sticky='NS', pady=(0, 5)))

    # малюємо заголовкі стовпців
    for column, item in enumerate(['', '1h', '24h', '7d', '30d', '60d', '90d', ]):
        (tk.Label(fr4, text=item, fg='white', background=menu_bg_colour, anchor="e", font=("Verdana", 8))
         .grid(row=1, column=column, sticky='NSEW', ))

    for row, coin in enumerate(coin_info):
        coin_name = coin['name']
        coin_stable = True if 'stablecoin' in coin['tags'] else False
        percent_change = coin['percent_change']

        # малюємо рядки з іменем монети
        if not coin_stable:
            (tk.Label(fr4, text=coin_name, fg='white', background=menu_bg_colour, anchor="w", font=("Verdana", 8))
             .grid(row=row + 2, column=0, sticky='NSEW', ))

            # малюємо рядки зі змінами в ціні за різні періоди
            for column, f in enumerate(percent_change):
                (tk.Label(fr4, text=f"{f}%", fg='green' if f > 0 else 'red', background=menu_bg_colour,
                          anchor="e", font=("Verdana", 8))
                 .grid(row=row + 2, column=column + 1, sticky='NSEW', ))


def show_portfolio_statistic():
    (tk.Label(fr5, text='статистика', fg='white', background='#808080', width=45, font=("Helvetica", 12))
     .grid(row=0, column=0, columnspan=2, sticky='NSEW', pady=(0, 5)))

    widget = (
        ('монет у портфелі', f'{number_of_coins_in_portfolio}'),
        ('вартість стейбли $', f"{stable_summ:.2f} $"),
        ('вартість крипто $', f"{crypto_summ:.2f} $"),
        ('вартість портфель $', f"{equivalent_summ:.2f} $"),
        ('стейбли  /  крипто %',
         f"{stable_summ * 100 / equivalent_summ:.1f}%  /  {crypto_summ * 100 / equivalent_summ:.1f}%"
         if equivalent_summ > 0 else "0%  /  0%"),
    )

    for enum, (widget_text, value) in enumerate(widget):
        (tk.Label(fr5, text=widget_text, background=menu_bg_colour, fg='white', anchor="w", font=("Verdana", 8))
         .grid(row=enum + 1, column=0, sticky='NSEW'))
        (tk.Label(fr5, text=value, background=menu_bg_colour, fg='white', anchor="e", font=("Verdana", 8))
         .grid(row=enum + 1, column=1, sticky='NSEW'))


def menu_update():
    show_coin_in_portfolio()
    show_percent_change()
    show_portfolio_statistic()


def settings_menu():
    pass
    # ChildWindow(menu.root, app_res=(600, 300))


def add_coin_menu():
    """додаємо монети в БД"""

    def get_entry():
        # Отримуємо значення з поля для введення
        value = str(entry_coin_name.get())

        if check_for_exist_coin(value):
            menu_update()
            lbl2.config(text="монету додано успішно", background='green')
            entry_coin_name.delete(0, END)
        else:
            lbl2.config(text="монети не існує", background='red')

    # параметри вікна програми
    add_coin = ChildWindow(top_lvl=menu.root, title='ADD COIN', app_res=(400, 70), background=menu_bg_colour)

    # елементи меню
    lbl1 = tk.Label(add_coin.root, text='Введіть ім`я або символ монети', width=30)
    lbl1.grid(row=0, column=0, sticky="nsew")

    lbl2 = tk.Label(add_coin.root, text='', )
    lbl2.grid(row=3, column=0, columnspan=2, sticky="nsew")

    entry_coin_name = tk.Entry(add_coin.root, width=30)
    entry_coin_name.grid(row=0, column=1, sticky="nsew")

    button = tk.Button(add_coin.root, text='Додати', command=get_entry)
    button.grid(row=2, column=0, columnspan=2, sticky="nsew")


def dell_coin_menu():
    """видаляємо монети з БД"""

    def del_message(coin_name):
        question = mb.askquestion('DELETE MENU', f'ви впевнені що хочете видалити монету {coin_name} ?')
        if question == 'yes':
            dell_coin.root.destroy()
            dell_coin_in_db(coin_name)
            menu_update()
        else:
            dell_coin.root.destroy()

    # параметри вікна програми
    dell_coin = ChildWindow(top_lvl=menu.root, title='DELL COIN', app_res=(400, 70), background=menu_bg_colour)

    # елементи меню
    fr = tk.Frame(dell_coin.root)
    fr.pack(side='top', pady=10, padx=10, )

    label1 = tk.Label(fr, text='виберіть ім`я монети яку потрібно видалити', wraplength=200, width=50, )
    label1.grid(row=0, column=0, sticky="NSEW")

    entry_coin_name = ttk.Combobox(fr, width=30, values=all_coin_name)
    entry_coin_name.current(0)
    entry_coin_name.grid(row=1, column=0, sticky="NSEW")

    button = tk.Button(fr, text='видалити', )
    button.config(command=lambda: del_message(entry_coin_name.get()))
    button.grid(row=2, column=0, columnspan=2, sticky="NSEW")


def buy_or_sell_coin_menu(is_buy=True):
    """додаємо запис про купівлю монети в БД"""

    def entry_value():
        name = coin_name_combo.get()
        cval = coin_value_entry.get()
        uval = usd_value_entry.get()

        if (cval.replace(',', '').replace('.', '').isdigit()) and (uval.replace(',', '').replace('.', '').isdigit()):
            by_or_sell_coin(coin_name=name, coin_amount=cval, usd_amount=uval, is_buy=True if is_buy else False)
            coin_value_entry.delete(0, END)
            usd_value_entry.delete(0, END)
            show_coin_in_portfolio()
            info_lbl.config(text=f"запис успішно додано", background='green')
        else:
            info_lbl.config(text=f"помилка в данних", background='red')

    # параметри вікна програми
    buy_menu = ChildWindow(top_lvl=menu.root, title='BUY MENU' if is_buy else 'SELL MENU', app_res=(500, 100),
                           background=menu_bg_colour)

    # елементи меню
    fr = tk.Frame(buy_menu.root)
    fr.pack()

    elements = (
        "ім'я монети" if is_buy else "ім'я монети",
        "куплено монет" if is_buy else "продано монет",
        "витрачено usd" if is_buy else "отримано usd",
    )
    for enum, elements_text in enumerate(elements):
        (tk.Label(fr, text=elements_text, width=23, height=3, ).grid(row=0, column=enum, rowspan=1, sticky='NSEW', ))

    coin_name_combo = ttk.Combobox(fr, width=23, values=all_coin_name)
    coin_name_combo.current(0)
    coin_name_combo.grid(row=1, column=0, sticky='NSEW')

    coin_value_entry = tk.Entry(fr, width=23, )
    coin_value_entry.grid(row=1, column=1, sticky='NSEW')

    usd_value_entry = tk.Entry(fr, width=23, )
    usd_value_entry.grid(row=1, column=2, sticky='NSEW')

    info_lbl = tk.Label(fr, text='')
    info_lbl.grid(row=2, column=0, sticky='NSEW', columnspan=3)

    buy_menu_btn = tk.Button(fr, text='зробити запис про купівлю' if is_buy else 'зробити запис про продаж',
                             command=entry_value)
    buy_menu_btn.grid(row=3, column=0, sticky='NSEW', columnspan=3)


def redact_buy_or_sell_operation(is_buy=True):
    """видаляємо запис про купівлю монети в БД"""

    def del_message(coin_name, operation_id):
        question = mb.askquestion('DELETE MENU', f'ви впевнені що хочете видалити {coin_name}?')

        if question == 'yes':
            del_current_coin_operation(coin_name, operation_id)
            show_coin_in_portfolio()
            activate()
        else:
            print('no')

    def activate():
        operations = []

        coin_operation_combo = ttk.Combobox(fr, values=[''])
        coin_operation_combo.grid(row=1, column=0, sticky='NSEW', columnspan=4)

        for count, item in enumerate(get_current_coin_operation(coin_name_combo.get())):
            if is_buy:
                if item[3]:
                    operations.append(
                        f"{item[0]} | Дата: {item[1]} | Час {item[2]} | Придбано - "
                        f"{item[3]} {coin_name_combo.get().upper()} за {item[4]}$")
                else:
                    continue

            if not is_buy:
                if item[5]:
                    operations.append(
                        f"{item[0]} | Дата: {item[1]} | Час {item[2]} | Придбано - "
                        f"{item[5]} {coin_name_combo.get().upper()} за {item[6]}$")
                else:
                    continue

        if not operations:
            coin_operation_combo.config(values=["немає даних"])
            coin_operation_combo.current(0)
        else:
            coin_operation_combo.config(values=operations[-10:])
            coin_operation_combo.current(0)

        del_btn = tk.Button(fr, text='видалити')
        del_btn.config(command=lambda: del_message(coin_name_combo.get(), coin_operation_combo.get().split(' ', 1)[0]))
        del_btn.grid(row=2, column=0, sticky='NSEW', columnspan=4)

    # параметри вікна програми
    red_buy_menu = ChildWindow(top_lvl=menu.root, title='REDACT BUY' if is_buy else 'REDACT SELL',
                               app_res=(500, 50), background=menu_bg_colour)
    # елементи меню
    fr = tk.Frame(red_buy_menu.root)
    fr.pack(side='top', pady=10, padx=10, )

    if not all_coin_name:
        err_lbl = tk.Label(fr, text="в портфелі немає жодної монети", width=50, height=5, fg='white',
                           background=menu_bg_colour)
        err_lbl.pack()
    else:
        coin_name_combo = ttk.Combobox(fr, width=50, values=all_coin_name)
        coin_name_combo.current(0)
        coin_name_combo.grid(row=0, column=0, sticky='NSEW')

        btn0 = tk.Button(fr, text="знайти операції", width=15, command=activate)
        btn0.grid(row=0, column=1, sticky='NSEW', columnspan=2)


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':
    response()

    # Запускаємо цикл який оновлює інформацію про монети в файлі
    t = threading.Thread(target=response_update)
    t.daemon = True
    t.start()

    menu = MainWindow(app_res=(appx, appy), disp_res=(dispx, dispy), background=menu_bg_colour, title='CRYPTO MANAGER')
    menu.root.bind("<MouseWheel>", on_mousewheel)

    # ______________________________________________SETTING_BAR_____________________________________________
    menu_bar = tk.Menu(menu.root, selectcolor='#1E1F22')
    menu_bar.add_command(label="Редагувати монети", command=dell_coin_menu)
    menu_bar.add_command(label="Редагувати покупки", command=lambda: redact_buy_or_sell_operation(is_buy=True), )
    menu_bar.add_command(label="Редагувати продажі", command=lambda: redact_buy_or_sell_operation(is_buy=False), )
    menu.root.configure(menu=menu_bar)

    # ______________________________________________CANVAS__________________________________________________
    canvas = tk.Canvas(menu.root, background=menu_bg_colour, highlightbackground=menu_bg_colour)
    canvas.pack(fill="both", expand=True, pady=20, padx=20)

    # ______________________________________________FRAME_0__________________________________________________
    fr0 = tk.Frame(canvas, background=menu_bg_colour)
    fr0.pack(fill="both", expand=True, )
    fr0.bind("<Configure>", lambda x: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window(canvas.winfo_width() // 2, canvas.winfo_height() // 2, window=fr0, anchor="n")

    # ______________________________________________FRAME_1__________________________________________________
    fr1 = tk.Frame(fr0, background=menu_bg_colour, )
    fr1.pack(fill="both", expand=True, )
    widget_fr1 = (("курс", name_colour1, lambda: (update_settings("sorting", 0), show_coin_in_portfolio())),
                  ("ім'я", name_colour1, lambda: (update_settings("sorting", 1), show_coin_in_portfolio())),
                  ("куплено\nмонет", buy_colour1, lambda: print('не сортується')),
                  ("витрачено\nUSD", buy_colour1, lambda: print('не сортується')),
                  ("середня ціна\nкупівлі", buy_colour1, lambda: print('не сортується')),
                  ("продано\nмонет", sell_color1, lambda: print('не сортується')),
                  ("отримано\nUSD", sell_color1, lambda: print('не сортується')),
                  ("середня ціна\nпродажу", sell_color1, lambda: print('не сортується')),
                  ("баланс", balance_colour1, lambda: print('не сортується')),
                  ("еквівалент\nUSD", balance_colour2, lambda:
                  (update_settings("sorting", 9), show_coin_in_portfolio())),
                  ("нереалізований\nдохід", balance_colour2, lambda:
                  (update_settings("sorting", 10), show_coin_in_portfolio())),
                  ("реалізований\nдохід", balance_colour2, lambda:
                  (update_settings("sorting", 11), show_coin_in_portfolio())),
                  ("прибуток", balance_colour2, lambda: (update_settings("sorting", 12), show_coin_in_portfolio())),
                  ("продано %", balance_colour2, lambda: (update_settings("sorting", 13), show_coin_in_portfolio())),
                  )

    for enum_column, (text, colour, command) in enumerate(widget_fr1):
        (tk.Button(fr1, text=text, width=12 if enum_column not in [1, 8] else 20, height=2, borderwidth=0,
                   background=colour, fg='black', font=("Helvetica", 9),
                   cursor="hand2" if enum_column not in [2, 3, 4, 5, 6, 7, 8] else 'arrow', command=command)
         .grid(row=1, column=enum_column, rowspan=2 if text == "баланс" else 1, sticky='NSEW', ))

    usd_equal_lbl = tk.Label(fr1, text="-", background='#ADB7C0', fg='black', )
    usd_equal_lbl.grid(row=2, column=9, sticky='NSEW', )

    realized_profit_lbl = tk.Label(fr1, text="-", background='#ADB7C0', fg='black', )
    realized_profit_lbl.grid(row=2, column=10, sticky='NSEW', )

    unrealized_profit_lbl = tk.Label(fr1, text="-", background='#ADB7C0', fg='black', )
    unrealized_profit_lbl.grid(row=2, column=11, sticky='NSEW', )

    profit_lbl = tk.Label(fr1, text="-", background='#ADB7C0', fg='black', )
    profit_lbl.grid(row=2, column=12, sticky='NSEW', )

    sell_percent_lbl = tk.Label(fr1, text="-", background='#ADB7C0', fg='black', )
    sell_percent_lbl.grid(row=2, column=13, sticky='NSEW', )

    btn1 = tk.Button(fr1, text="+", background='#ffe4ce', borderwidth=0, fg='black', font=("Helvetica", 9),
                     cursor="hand2", command=add_coin_menu)
    btn1.grid(row=2, column=0, columnspan=2, sticky='NSEW')

    btn2 = tk.Button(fr1, text="+", background=buy_colour2, borderwidth=0, fg='black', font=("Helvetica", 9),
                     cursor="hand2", command=lambda: buy_or_sell_coin_menu(is_buy=True))
    btn2.grid(row=2, column=2, columnspan=3, sticky='NSEW', )

    btn3 = tk.Button(fr1, text="+", background=sell_color2, borderwidth=0, fg='black', font=("Helvetica", 9),
                     cursor="hand2", command=lambda: buy_or_sell_coin_menu(is_buy=False))
    btn3.grid(row=2, column=5, columnspan=3, sticky='NSEW')

    # ______________________________________________FRAME_2__________________________________________________
    fr2 = tk.Frame(fr0, background=menu_bg_colour)
    fr2.pack(fill="both", expand=True, )

    refresh_btn = tk.Button(fr0, text='оновити', width=element_width, cursor="hand2", command=lambda: menu_update())
    refresh_btn.pack(fill='x', pady=(10, 0))
    # ______________________________________________FRAME_3__________________________________________________
    fr3 = tk.Frame(fr0, background=menu_bg_colour)
    fr3.pack(fill="both", expand=True, )

    # ______________________________________________FRAME_4__________________________________________________
    fr4 = tk.Frame(fr0, background=menu_bg_colour, )
    fr4.pack(side='left', anchor='n', pady=20, padx=10, )

    # ______________________________________________FRAME_5__________________________________________________
    fr5 = tk.Frame(fr0, background=menu_bg_colour, )
    fr5.pack(side='left', anchor='n', pady=20, padx=10, )

    menu_update()
    menu.start()
