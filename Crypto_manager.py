from db import (get_all_coin_name, get_buy_summ, get_sell_summ, dell_coin_in_db, by_or_sell_coin,
                del_current_coin_operation, get_current_coin_operation)
from parser import get_coin_info, check_for_exist_coin, get_percent_change
from media_downloader import download_file_from_google_drive
from tkinter import messagebox as mb
from gui_config import *
from tkinter import END
from tkinter import ttk
import tkinter as tk
import os


def show_coin_in_portfolio(frame):
    """ виводимо віджети з інформацією про портфоліо в головне меню"""

    for widget in frame.winfo_children():
        widget.destroy()

    sell_count = 0
    profit_summ = 0
    equivalent_summ = 0
    sell_percent_summ = 0
    realized_income_summ = 0
    unrealized_income_summ = 0

    if not get_all_coin_name():
        print("В портфелі немає монет")
        add_coin_menu()
    else:
        for enum, coin in enumerate(get_coin_info(get_all_coin_name())):
            crypto_exchange = coin['price']
            coin_name = coin['name']
            coin_symbol = coin['symbol']

            buy_summ = get_buy_summ(coin['name'].lower())['coins']
            buy_spent_summ = get_buy_summ(coin['name'].lower())['usd']
            buy_avg = get_buy_summ(coin['name'].lower())['avg']

            sell_summ = get_sell_summ(coin['name'].lower())['coins']
            sell_spent_summ = get_sell_summ(coin['name'].lower())['usd']
            sell_avg = get_sell_summ(coin['name'].lower())['avg']

            balance = buy_summ - sell_summ
            equivalent = crypto_exchange * balance
            realized_income = sell_spent_summ - (sell_summ * buy_avg)
            unrealized_income = equivalent - (balance * buy_avg)
            profit = realized_income + unrealized_income
            sell_percent = sell_summ * 100 / buy_summ if buy_summ > 0 else 0

            sell_count += 1 if sell_percent > 0 else 0
            profit_summ += profit
            equivalent_summ += equivalent
            sell_percent_summ += sell_percent
            realized_income_summ += realized_income
            unrealized_income_summ += unrealized_income

            widgets_data = [
                # курс
                (f'{crypto_exchange} $', element_width - 5, name_colour2, 'black', 0),
                # монета
                (f'{coin_name} {coin_symbol}', element_width + 5, name_colour1, 'black', 1),
                # куплено
                (f'{buy_summ}', element_width - 4, by_color2, 'black', 2),
                # витрачено
                (f'{buy_spent_summ} $', element_width - 4, by_color2, 'black', 3),
                # середня ціна
                (f'{buy_avg} $', element_width - 4, by_color2, 'black', 4),
                # продано
                (sell_summ, element_width - 4, sell_color2, 'black', 5),
                # отримано
                (f'{sell_spent_summ} $', element_width - 4, sell_color2, 'black', 6),
                # середня ціна
                (f'{sell_avg} $', element_width - 4, sell_color2, 'black', 7),
                # баланс
                (f'{balance:.4f} {coin_symbol}', element_width, balance_colour1, 'black', 8),
                # еквівалент
                (f'{equivalent:.2f} $', element_width - 3, balance_colour2, 'black', 9),
                # реалізований дохід
                (f"{realized_income:.2f} $", element_width - 3, balance_colour1,
                 '#006400' if realized_income >= 0 else '#640000', 10),
                # нереалізований дохід
                (f"{unrealized_income:.2f} $", element_width - 3, balance_colour2,
                 '#006400' if unrealized_income >= 0 else '#640000', 11),
                # прибуток
                (f"{profit:.2f} $", element_width - 3, balance_colour1,
                 '#006400' if profit >= 0 else '#640000', 12),
                # Продано у %
                (f'{sell_percent:.2f}%' if sell_summ != 0 else '0%', element_width - 3, sell_color2, 'black', 13),
            ]

            for (widget_text, widget_width, widget_background, font_ground, widget_column) in widgets_data:
                (tk.Label(frame, text=widget_text, width=widget_width, height=1, background=widget_background,
                          fg=font_ground if widget_text != 0 else 'black')
                 .grid(row=enum, column=widget_column, sticky='NSEW'))

    usd_equal_lbl.config(text=f"{equivalent_summ:.2f} $")
    realized_profit_lbl.config(text=f"{realized_income_summ:.2f} $")
    unrealized_profit_lbl.config(text=f"{unrealized_income_summ:.2f} $")
    sell_percent_lbl.config(text=f"{(sell_percent_summ / sell_count):.2f} %" if sell_count != 0 else '0 %')
    profit_lbl.config(text=f"{profit_summ:.2f} $")


def show_percent_change(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    # малюємо шапку
    (tk.Label(frame, text='зміни в цінах', font='size=10', fg='white', background='#808080', width=45)
     .grid(row=0, column=0, columnspan=7, sticky='NS', pady=(0, 5)))

    # малюємо заголовкі стовпців
    for enum, f in enumerate(['', '1h', '24h', '7d', '30d', '60d', '90d', ]):
        (tk.Label(frame, text=f, fg='white', background=menu_bg_colour, anchor="e")
         .grid(row=1, column=enum, sticky='NSEW', ))

    # малюємо рядки з іменем монети
    for enum, coin in enumerate(get_all_coin_name()):
        (tk.Label(frame, text=coin.upper(), fg='white', background=menu_bg_colour, anchor="w")
         .grid(row=enum + 2, column=0, sticky='NSEW', ))

        # малюємо рядки зі змінами в ціні за різні періоди
        for enum1, f in enumerate(get_percent_change(coin)):
            (tk.Label(frame, text=f"{f}%", fg='green' if f > 0 else 'red', background=menu_bg_colour, anchor="e")
             .grid(row=enum + 2, column=enum1 + 1, sticky='NSEW', ))


def show_portfolio_statistic(frame):
    (tk.Label(frame, text='статистика', font='size=10', fg='white', background='#808080', width=45)
     .grid(row=0, column=0, columnspan=2, sticky='NS', pady=(0, 5)))

    widget = [
        ('вартість портфелю', f"**** $"),
        ('стейбли / криптовалюта', f"**% / **%"),
    ]
    for enum, (widget_text, value) in enumerate(widget):
        (tk.Label(frame, text=widget_text, background=menu_bg_colour, fg='white', )
         .grid(row=enum + 1, column=0, ))
        (tk.Label(frame, text=value, background=menu_bg_colour, fg='white', )
         .grid(row=enum + 1, column=1, ))


def add_coin_menu():
    """додаємо монети в БД"""

    def get_entry():
        # Отримуємо значення з поля для введення
        value = str(entry_coin_name.get())

        if check_for_exist_coin(value):
            show_coin_in_portfolio(fr2)
            show_percent_change(fr4)
            lbl2.config(text="монету додано успішно", background='green')
            entry_coin_name.delete(0, END)
        else:
            lbl2.config(text="монети не існує", background='red')

    # параметри вікна програми
    add_coin = tk.Toplevel(menu)
    add_coin.title('ADD COIN')
    add_coin.geometry("400x70")
    xx = (1920 // 2) - (400 // 2)
    yy = (1080 // 2) - (70 // 2)
    add_coin.geometry(f"+{xx}+{yy}")
    add_coin.resizable(False, False)
    add_coin.config(background=menu_bg_colour)
    add_coin.grab_set()

    # елементи меню
    lbl1 = tk.Label(add_coin, text='Введіть ім`я або символ монети', width=30)
    lbl1.grid(row=0, column=0, sticky="nsew")

    lbl2 = tk.Label(add_coin, text='', )
    lbl2.grid(row=3, column=0, columnspan=2, sticky="nsew")

    entry_coin_name = tk.Entry(add_coin, width=30)
    entry_coin_name.grid(row=0, column=1, sticky="nsew")

    button = tk.Button(add_coin, text='Додати', command=get_entry)
    button.grid(row=2, column=0, columnspan=2, sticky="nsew")


def dell_coin_menu():
    """видаляємо монети з БД"""

    def del_message(coin_name):
        question = mb.askquestion('DELETE MENU', f'ви впевнені що хочете видалити монету {coin_name} ?')
        if question == 'yes':
            dell_coin.destroy()
            dell_coin_in_db(coin_name)
            show_coin_in_portfolio(fr2)
            show_percent_change(fr4)
        else:
            dell_coin.destroy()

    try:
        dell_coin = tk.Toplevel(menu)
        dell_coin.title('DELL COIN')
        dell_coin.geometry("400x70")
        xx = (1920 // 2) - (1 // 2)
        yy = (1080 // 2) - (110 // 2)
        dell_coin.geometry(f"+{xx}+{yy}")
        dell_coin.resizable(False, False)
        dell_coin.config(background=menu_bg_colour)
        dell_coin.minsize(1, 110)
        dell_coin.grab_set()

        # елементи меню
        fr = tk.Frame(dell_coin)
        fr.pack(side='top', pady=10, padx=10, )

        label1 = tk.Label(fr, text='виберіть ім`я монети яку потрібно видалити', wraplength=200, width=50, )
        label1.grid(row=0, column=0, sticky="NSEW")

        entry_coin_name = ttk.Combobox(fr, width=30, values=get_all_coin_name())
        entry_coin_name.current(0)
        entry_coin_name.grid(row=1, column=0, sticky="NSEW")

        button = tk.Button(fr, text='видалити', )
        button.config(command=lambda: del_message(entry_coin_name.get()))
        button.grid(row=2, column=0, columnspan=2, sticky="NSEW")
    except Exception as error:
        print(error)


def buy_coin_menu():
    """додаємо запис про купівлю монети в БД"""

    def entry_value():
        name = coin_name_combo.get()
        cval = coin_value_entry.get()
        uval = usd_value_entry.get()

        if (cval.replace(',', '').replace('.', '').isdigit()) and (uval.replace(',', '').replace('.', '').isdigit()):
            by_or_sell_coin(coin_name=name, coin_amount=cval, usd_amount=uval, is_buy=True)
            coin_value_entry.delete(0, END)
            usd_value_entry.delete(0, END)
            show_coin_in_portfolio(fr2)
            show_percent_change(fr4)
            info_lbl.config(text=f"запис успішно додано", background='green')
        else:
            info_lbl.config(text=f"помилка в данних", background='red')

    try:
        buy_menu = tk.Toplevel(menu)
        buy_menu.title('BUY MENU')
        resx = (dispx // 2) - (500 // 2)
        resy = (dispy // 2) - (100 // 2)
        buy_menu.geometry(f"+{resx}+{resy}")
        buy_menu.resizable(False, False)
        buy_menu.minsize(500, 100)
        buy_menu.config(background=menu_bg_colour)
        buy_menu.grab_set()

        # елементи меню
        fr = tk.Frame(buy_menu)
        fr.pack()

        elements = [
            "ім'я монети",
            "куплено монет",
            "витрачено usd",
        ]
        for enum, elements_text in enumerate(elements):
            (tk.Label(fr, text=elements_text, width=23, height=3, ).grid(row=0, column=enum, rowspan=1,
                                                                         sticky='NSEW', ))

        coin_name_combo = ttk.Combobox(fr, width=23, values=get_all_coin_name())
        coin_name_combo.current(0)
        coin_name_combo.grid(row=1, column=0, sticky='NSEW')

        coin_value_entry = tk.Entry(fr, width=23, )
        coin_value_entry.grid(row=1, column=1, sticky='NSEW')

        usd_value_entry = tk.Entry(fr, width=23, )
        usd_value_entry.grid(row=1, column=2, sticky='NSEW')

        info_lbl = tk.Label(fr, text='')
        info_lbl.grid(row=2, column=0, sticky='NSEW', columnspan=3)

        buy_menu_btn = tk.Button(fr, text='зробити запис про купівлю', command=entry_value)
        buy_menu_btn.grid(row=3, column=0, sticky='NSEW', columnspan=3)

    except Exception as error:
        print(error)


def redact_buy_operation():
    """видаляємо запис про купівлю монети в БД"""

    def del_message(coin_name, operation_id):
        question = mb.askquestion('DELETE MENU', f'ви впевнені що хочете видалити {coin_name}?')

        if question == 'yes':
            del_current_coin_operation(coin_name, operation_id)
            show_coin_in_portfolio(fr2)
            show_percent_change(fr4)
            activate()
        else:
            print('no')

    def activate():
        operations = []

        coin_operation_combo = ttk.Combobox(fr, values=[''])
        coin_operation_combo.grid(row=1, column=0, sticky='NSEW', columnspan=4)

        for count, item in enumerate(get_current_coin_operation(coin_name_conbo.get())):
            if item[3]:
                operations.append(
                    f"{item[0]}:    {item[3]} {coin_name_conbo.get().upper()} {item[4]} USD | {item[1]} {item[2]} ")
            else:
                continue

        if not operations:
            coin_operation_combo.config(values=["немає даних"])
            coin_operation_combo.current(0)
        else:
            coin_operation_combo.config(values=operations[-10:])
            coin_operation_combo.current(0)

        del_btn = tk.Button(fr, text='видалити')
        del_btn.config(command=lambda: del_message(coin_name_conbo.get(), coin_operation_combo.get().split(':', 1)[0]))
        del_btn.grid(row=2, column=0, sticky='NSEW', columnspan=4)

    # параметри вікна програми
    red_buy_menu = tk.Toplevel(menu)
    red_buy_menu.title(f"{'REDACT BUY'}")
    resx = (dispx // 2) - (50 // 2)
    resy = (dispy // 2) - (10 // 2)
    red_buy_menu.geometry(f"+{resx}+{resy}")
    red_buy_menu.resizable(False, False)
    red_buy_menu.minsize(50, 10)
    red_buy_menu.config(background=menu_bg_colour)
    red_buy_menu.grab_set()

    fr = tk.Frame(red_buy_menu)
    fr.pack(side='top', pady=10, padx=10, )

    if not get_all_coin_name():
        err_lbl = tk.Label(fr, text="в портфелі немає жодної монети", width=50, height=5, fg='white',
                           background=menu_bg_colour)
        err_lbl.pack()
    else:
        coin_name_conbo = ttk.Combobox(fr, width=50, values=get_all_coin_name())
        coin_name_conbo.current(0)
        coin_name_conbo.grid(row=0, column=0, sticky='NSEW')

        btn0 = tk.Button(fr, text="знайти операції", width=15, command=activate)
        btn0.grid(row=0, column=1, sticky='NSEW', columnspan=2)


def sell_coin_menu():
    """додаємо запис про продаж монети в БД"""

    def entry_value():
        name = coin_name_combo.get()
        cval = coin_value_entry.get()
        uval = usd_value_entry.get()

        if (cval.replace(',', '').replace('.', '').isdigit()) and (uval.replace(',', '').replace('.', '').isdigit()):
            by_or_sell_coin(coin_name=name, coin_amount=cval, usd_amount=uval, is_buy=False)
            coin_value_entry.delete(0, END)
            usd_value_entry.delete(0, END)
            show_coin_in_portfolio(fr2)
            show_percent_change(fr4)
            info_lbl.config(text=f"запис успішно додано", background='green')
        else:
            info_lbl.config(text=f"помилка в данних", background='red')

        # параметри вікна програми

    try:
        buy_menu = tk.Toplevel(menu)
        buy_menu.title('SELL MENU')
        resx = (dispx // 2) - (500 // 2)
        resy = (dispy // 2) - (100 // 2)
        buy_menu.geometry(f"+{resx}+{resy}")
        buy_menu.resizable(False, False)
        buy_menu.minsize(500, 100)
        buy_menu.config(background=menu_bg_colour)
        buy_menu.grab_set()

        # елементи меню

        fr = tk.Frame(buy_menu)
        fr.pack()

        elements = [
            "ім'я монети",
            "продано монет",
            "отримано usd",
        ]

        for enum, elements_text in enumerate(elements):
            (tk.Label(fr, text=elements_text, width=23, height=3, ).grid(row=0, column=enum, rowspan=1,
                                                                         sticky='NSEW', ))

        coin_name_combo = ttk.Combobox(fr, width=23, values=get_all_coin_name())
        coin_name_combo.current(0)
        coin_name_combo.grid(row=1, column=0, sticky='NSEW')

        coin_value_entry = tk.Entry(fr, width=23, )
        coin_value_entry.grid(row=1, column=1, sticky='NSEW')

        usd_value_entry = tk.Entry(fr, width=23, )
        usd_value_entry.grid(row=1, column=2, sticky='NSEW')

        info_lbl = tk.Label(fr, text='')
        info_lbl.grid(row=2, column=0, sticky='NSEW', columnspan=3)

        buy_menu_btn = tk.Button(fr, text='зробити запис про продаж', command=entry_value)
        buy_menu_btn.grid(row=3, column=0, sticky='NSEW', columnspan=3)

    except Exception as error:
        print(error)


def redact_sell_operation():
    """видаляємо запис про продаж монети з БД"""

    xx = 50
    yy = 10

    def del_message(coin_name, operation_id):
        question = mb.askquestion('DELETE MENU', f'ви впевнені що хочете видалити{coin_name}?')

        if question == 'yes':
            del_current_coin_operation(coin_name, operation_id)
            show_coin_in_portfolio(fr2)
            show_percent_change(fr4)
            activate()
        else:
            print('no')

    def activate():
        operations = []

        coin_operation_combo = ttk.Combobox(fr, values=[''])
        coin_operation_combo.grid(row=1, column=0, sticky='NSEW', columnspan=4)

        for count, item in enumerate(get_current_coin_operation(coin_name_conbo.get())):
            if item[5]:
                operations.append(
                    f"{item[0]}:    {item[5]} {coin_name_conbo.get().upper()} {item[6]} USD | {item[1]} {item[2]} ")
            else:
                continue

        if not operations:
            coin_operation_combo.config(values=["немає даних"])
            coin_operation_combo.current(0)
        else:
            coin_operation_combo.config(values=operations[-10:])
            coin_operation_combo.current(0)

        del_btn = tk.Button(fr, text='видалити')
        del_btn.config(command=lambda: del_message(coin_name_conbo.get(), coin_operation_combo.get().split(':', 1)[0]))
        del_btn.grid(row=2, column=0, sticky='NSEW', columnspan=4)

    # параметри вікна програми
    red_buy_menu = tk.Toplevel(menu)
    red_buy_menu.title(f"{'REDACT BUY'}")
    resx = (dispx // 2) - (xx // 2)
    resy = (dispy // 2) - (yy // 2)
    red_buy_menu.geometry(f"+{resx}+{resy}")
    red_buy_menu.resizable(False, False)
    red_buy_menu.minsize(xx, yy)
    red_buy_menu.config(background=menu_bg_colour)
    red_buy_menu.grab_set()

    fr = tk.Frame(red_buy_menu)
    fr.pack(side='top', pady=10, padx=10, )

    if not get_all_coin_name():
        err_lbl = tk.Label(fr, text="в портфелі немає жодної монети", width=50, height=5, fg='white',
                           background=menu_bg_colour)
        err_lbl.pack()
    else:
        coin_name_conbo = ttk.Combobox(fr, width=50, values=get_all_coin_name())
        coin_name_conbo.current(0)
        coin_name_conbo.grid(row=0, column=0, sticky='NSEW')

        btn0 = tk.Button(fr, text="знайти операції", width=15, command=activate)
        btn0.grid(row=0, column=1, sticky='NSEW', columnspan=2)


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':

    x = (dispx // 2) - (appx // 2)
    y = (dispy // 2) - (appy // 2)

    menu = tk.Tk()
    menu.title('CRYPTO MANAGER')
    menu.geometry(f"+{x}+{y}")
    menu.minsize(appx, appy)
    menu.config(background=menu_bg_colour)
    menu.resizable(False, False)
    menu.bind("<MouseWheel>", on_mousewheel)

    try:
        menu.iconphoto(False, tk.PhotoImage(file='media/logo.png'))
        print('ok')
    except Exception as e:
        try:
            file_id = '1T6CzadYdlO_r5ZgrMVybJ1EGmlf-L2r8'
            destination = os.path.join('media', 'logo.png')
            download_file_from_google_drive(id=file_id, destination=destination)
            menu.iconphoto(False, tk.PhotoImage(file='media/logo.png'))
            print('logo.png download...')
        except Exception as e:
            print(e)

    # ______________________________________________SETTING_BAR______________________________________________

    menu_bar = tk.Menu(menu, selectcolor='#1E1F22')
    menu_bar.add_command(label="редагувати монети", command=dell_coin_menu)
    menu_bar.add_command(label="редагувати покупки", command=redact_buy_operation, )
    menu_bar.add_command(label="редагувати продажі", command=redact_sell_operation, )
    menu.configure(menu=menu_bar)

    # ______________________________________________CANVAS______________________________________________

    canvas = tk.Canvas(menu, background=menu_bg_colour, highlightbackground=menu_bg_colour)
    canvas.pack(fill="both", expand=True, pady=20, padx=20)

    # ______________________________________________FRAME_0__________________________________________________

    fr0 = tk.Frame(canvas, background=menu_bg_colour)
    fr0.pack()
    fr0.bind("<Configure>", lambda x: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window(canvas.winfo_width() // 2, canvas.winfo_height() // 2, window=fr0, anchor="n")

    # ______________________________________________FRAME_1__________________________________________________

    fr1 = tk.Frame(fr0, background=menu_bg_colour, )
    fr1.pack(pady=(0, 5))
    widget_fr1 = [
        ("курс", name_colour2, element_width - 5),
        ("монета", name_colour1, element_width + 5),
        ("куплено", by_color1, element_width - 4),
        ("витрачено\nUSD", by_color1, element_width - 4),
        ("середня ціна\nкупівлі", by_color1, element_width - 4),
        ("продано", sell_color1, element_width - 4),
        ("отримано\nUSD", sell_color1, element_width - 4),
        ("середня ціна\nпродажу", sell_color1, element_width - 4),
        ("баланс", balance_colour1, element_width),
        ("еквівалент\nUSD", balance_colour2, element_width - 3),
        ("реалізований\nдохід", balance_colour1, element_width - 3),
        ("нереалізований\nдохід", balance_colour2, element_width - 3),
        ("прибуток", balance_colour1, element_width - 3),
        ("продано %", sell_color2, element_width - 3), ]

    for num, (text, bg_colour, widtg) in enumerate(widget_fr1):
        (tk.Label(fr1, text=text, width=widtg, height=3, background=bg_colour, )
         .grid(row=1, column=num, rowspan=2 if text == "курс" or text == "баланс" else 1, sticky='NSEW', ))

    usd_equal_lbl = tk.Label(fr1, text="-", width=element_width - 3, background=balance_colour2, )
    usd_equal_lbl.grid(row=2, column=9, sticky='NSEW', )

    realized_profit_lbl = tk.Label(fr1, text="-", width=element_width - 3, background=balance_colour1, )
    realized_profit_lbl.grid(row=2, column=10, sticky='NSEW', )

    unrealized_profit_lbl = tk.Label(fr1, text="-", width=element_width - 3, background=balance_colour2, )
    unrealized_profit_lbl.grid(row=2, column=11, sticky='NSEW', )

    profit_lbl = tk.Label(fr1, text="-", width=element_width - 3, background=balance_colour1, )
    profit_lbl.grid(row=2, column=12, sticky='NSEW', )

    sell_percent_lbl = tk.Label(fr1, text="-", width=element_width - 3, background=sell_color2, )
    sell_percent_lbl.grid(row=2, column=13, sticky='NSEW', )

    btn1 = tk.Button(fr1, text="+", background=name_colour1, borderwidth=0, command=add_coin_menu)
    btn1.grid(row=2, column=1, sticky='NSEW')

    btn2 = tk.Button(fr1, text="+", background=by_color1, borderwidth=0, command=buy_coin_menu)
    btn2.grid(row=2, column=2, columnspan=3, sticky='NSEW', )

    btn3 = tk.Button(fr1, text="+", background=sell_color1, borderwidth=0, command=sell_coin_menu)
    btn3.grid(row=2, column=5, columnspan=3, sticky='NSEW')

    # ______________________________________________FRAME_2__________________________________________________

    fr2 = tk.Frame(fr0, background=menu_bg_colour)
    fr2.pack()
    show_coin_in_portfolio(fr2)

    # ______________________________________________FRAME_3__________________________________________________

    fr3 = tk.Frame(fr0, background=menu_bg_colour)
    fr3.pack()

    refresh_btn = tk.Button(fr0, text='оновити', width=element_width, height=1,
                            command=lambda: (show_coin_in_portfolio(fr2), show_percent_change(fr4)))
    refresh_btn.pack(fill='x', pady=(5, 0))

    # ______________________________________________FRAME_4__________________________________________________

    fr4 = tk.Frame(fr0, background=menu_bg_colour, )
    fr4.pack(side='left', anchor='n', pady=20, padx=10, )
    show_percent_change(fr4)

    # ______________________________________________FRAME_5__________________________________________________

    fr5 = tk.Frame(fr0, background=menu_bg_colour, )
    fr5.pack(side='left', anchor='n', pady=20, padx=10, )
    show_portfolio_statistic(fr5)

    menu.mainloop()
