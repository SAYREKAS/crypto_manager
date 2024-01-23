from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import END
import tkinter as tk
from parser import *
from db import *
from gui_config import *


# виводимо віджети з інформацією про портфоліо в головне меню
def show_coin_in_portfolio(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    fr = tk.Frame(frame, background=menu_bg_colour)
    fr.pack()
    fr.config(pady=5)

    balance_summ_count = 0
    realized_profit_count = 0
    unrealized_profit_count = 0
    sell_persent_count = 0
    sell_count = 0
    profit_count = 0

    if not get_all_coin_name():
        print("В портфелі немає монет")
        add_coin_menu()
    else:
        for count, name in enumerate(get_coin_info(get_all_coin_name())):
            # курс__________________________________________________________________________________
            (tk.Label(fr, text=f'{name[2]} $', width=element_width - 5, height=1,
                      background=name_colour2, )
             .grid(row=count + 2, column=0, sticky='NSEW'))
            # монета__________________________________________________________________________________
            (tk.Label(fr, text=f'{name[0]} {name[1]}', width=element_width + 5, height=1,
                      background=name_colour1, )
             .grid(row=count + 2, column=1, sticky='NSEW'))
            # куплено_________________________________________________________________________________
            (tk.Label(fr, text=f'{get_buy_summ(name[0].lower())[0]}', width=element_width - 4, height=1,
                      background=by_color2)
             .grid(row=count + 2, column=2, sticky='NSEW'))
            # витрачено_________________________________________________________________________________
            (tk.Label(fr, text=f'{get_buy_summ(name[0].lower())[1]}', width=element_width - 4, height=1,
                      background=by_color2)
             .grid(row=count + 2, column=3, sticky='NSEW'))
            # середня ціна________________________________________________________________________________
            (tk.Label(fr, text=f'{get_buy_summ(name[0].lower())[2]}', width=element_width - 4, height=1,
                      background=by_color2)
             .grid(row=count + 2, column=4, sticky='NSEW'))
            # продано___________________________________________________________________________________
            (tk.Label(fr, text=f'{get_sell_summ(name[0].lower())[0]}', width=element_width - 4, height=1,
                      background=sell_color2)
             .grid(row=count + 2, column=5, sticky='NSEW'))
            # отримано_________________________________________________________________________________
            (tk.Label(fr, text=f'{get_sell_summ(name[0].lower())[1]}', width=element_width - 4, height=1,
                      background=sell_color2)
             .grid(row=count + 2, column=6, sticky='NSEW'))
            # середня ціна______________________________________________________________________________
            (tk.Label(fr,
                      text=f'{get_sell_summ(name[0].lower())[2]}', width=element_width - 4, height=1,
                      background=sell_color2)
             .grid(row=count + 2, column=7, sticky='NSEW'))
            # баланс____________________________________________________________________________________
            (tk.Label(fr,
                      text=f'{get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]} {name[1]}',
                      width=element_width-3, height=1, background=balance_colour1)
             .grid(row=count + 2, column=8,
                   sticky='NSEW'))
            # еквівалент_________________________________________________________________________________
            (tk.Label(fr,
                      text=f'{round(name[2] * (get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]), 2)} $',
                      width=element_width-3, height=1, background=balance_colour2)
             .grid(row=count + 2, column=9, sticky='NSEW'))

            balance_summ_count += (name[2] * (get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]))
            # реалізований прибуток________________________________________________________________________________
            (tk.Label(fr,
                      text=f"{get_sell_summ(name[0].lower())[1] - (get_sell_summ(name[0].lower())[0] * get_buy_summ(name[0].lower())[2])}",
                      width=element_width-3, height=1, background=balance_colour1)
             .grid(row=count + 2, column=10, sticky='NSEW'))

            realized_profit_count += (get_sell_summ(name[0].lower())[1] -
                                      (get_sell_summ(name[0].lower())[0] * get_buy_summ(name[0].lower())[2]))
            # нереалізований прибуток
            (tk.Label(fr,
                      text=f"{round((name[2] * (get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0])) -
                                    ((get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]) *
                                     get_buy_summ(name[0].lower())[2]), 2)}",
                      width=element_width-3, height=1, background=balance_colour2)
             .grid(row=count + 2, column=11, sticky='NSEW'))

            unrealized_profit_count += (
                    (name[2] * (get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]))
                    - ((get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0])
                       * get_buy_summ(name[0].lower())[2]))
            # прибуток
            (tk.Label(fr,
                      text=f"{round((get_sell_summ(name[0].lower())[1]
                                     - (get_sell_summ(name[0].lower())[0] * get_buy_summ(name[0].lower())[2]))
                                    + ((name[2] * (get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]))
                                       - ((get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0])
                                          * get_buy_summ(name[0].lower())[2])), 2)}",
                      width=element_width-3, height=1, background=balance_colour1)
             .grid(row=count + 2, column=12, sticky='NSEW'))

            profit_count += ((get_sell_summ(name[0].lower())[1] - (
                    get_sell_summ(name[0].lower())[0] * get_buy_summ(name[0].lower())[2]))
                             + ((name[2] * (get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]))
                                - ((get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0])
                                   * get_buy_summ(name[0].lower())[2])))
            # Продано у %
            if get_sell_summ(name[0].lower())[0] != 0:
                (tk.Label(fr, text=f'{get_sell_summ(name[0].lower())[0] * 100 / get_buy_summ(name[0].lower())[0]}%',
                          width=element_width-3, height=1, background=sell_color2)
                 .grid(row=count + 2, column=13, sticky='NSEW'))

                sell_persent_count += (get_sell_summ(name[0].lower())[0] * 100 / get_buy_summ(name[0].lower())[0])
                sell_count += 1
            else:
                (tk.Label(fr, text='0%', width=element_width-3, height=1, background=sell_color2)
                 .grid(row=count + 2, column=13, sticky='NSEW'))

        usd_equal.config(text=f"{round(balance_summ_count, 2)} $")
        realized_profit.config(text=f"{round(realized_profit_count, 2)} $")
        unrealized_profit.config(text=f"{round(unrealized_profit_count, 2)} $")
        if sell_count != 0:
            sell_persent.config(text=f"{round(sell_persent_count / sell_count, 2)} %")
        else:
            sell_persent.config(text=f"0 %")
        profit.config(text=f"{round(profit_count, 2)} $")


# додаємо монети
def add_coin_menu():
    # Меню додавання монети в БД
    def get_entry():
        # Отримуємо значення з поля для введення
        value = str(entry_coin_name.get())
        if value != 'tether' and value != 'usd' and value != 'usdt' and value != 'usdc':
            if check_for_exis_coin(value):
                show_coin_in_portfolio(fr2)
                label2.config(text="монету додано успішно", background='green')
                entry_coin_name.delete(0, END)

            elif not get_coin_info(value):
                label2.config(text="монети не існує", background='red')
        else:
            label2.config(text="стейбли знаходяться у окремому пункті меню", background='yellow')
            entry_coin_name.delete(0, END)

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
    label1 = tk.Label(add_coin, text='Введіть ім`я або символ монети', width=30)
    label1.grid(row=0, column=0, sticky="nsew")

    label2 = tk.Label(add_coin, text='', )
    label2.grid(row=3, column=0, columnspan=2, sticky="nsew")

    entry_coin_name = tk.Entry(add_coin, width=30)
    entry_coin_name.grid(row=0, column=1, sticky="nsew")

    button = tk.Button(add_coin, text='Додати', command=get_entry)
    button.grid(row=2, column=0, columnspan=2, sticky="nsew")


# видаляємо монети
def dell_coin_menu():
    global label1

    def del_message(coin_name):
        question = mb.askquestion('DELETE MENU', f'ви впевнені що хочете видалити монету {coin_name} ?')
        if question == 'yes':
            dell_coin.destroy()
            dell_coin_in_db(coin_name)
            show_coin_in_portfolio(fr2)
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
    except Exception:
        label1.config(text="в портфелі немає жодної монети", width=50, height=5, fg='white',
                      background=menu_bg_colour)


# додаємо запис про купівлю монети
def buy_coin_menu():
    global coin_name_lbl

    def entry_value():
        name = coin_name_combo.get()
        cval = coin_value_entry.get()
        uval = usd_value_entry.get()

        if (cval.replace(',', '').replace('.', '').isdigit()) and (uval.replace(',', '').replace('.', '').isdigit()):

            by_or_sell_coin(coin_name=name, coin_amount=cval, usd_amount=uval, is_buy=True)

            coin_value_entry.delete(0, END)
            usd_value_entry.delete(0, END)

            show_coin_in_portfolio(fr2)
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

        for num, text in enumerate(elements):
            (tk.Label(fr, text=text, width=23, height=3, ).grid(row=0, column=num, rowspan=1, sticky='NSEW', ))

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

    except Exception:
        coin_name_lbl.config(text="в портфелі немає жодної монети", width=50, height=5, fg='white',
                             background=menu_bg_colour)


# видаляємо запис про купівлю монети
def redact_buy_operation():
    def del_message(coin_name, operation_id):
        question = mb.askquestion('DELETE MENU', 'ви впевнені що хочете видалити?')

        if question == 'yes':
            del_curent_coin_operation(coin_name, operation_id)
            show_coin_in_portfolio(fr2)
            activate()

        else:
            print('no')

    def activate():

        operations = []

        coin_operation_combo = ttk.Combobox(fr, values=[''])
        coin_operation_combo.grid(row=1, column=0, sticky='NSEW', columnspan=4)

        for count, item in enumerate(get_curent_coin_operation(coin_name_conbo.get())):

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


# додаємо запис про продаж монети
def sell_coin_menu():
    global coin_name_lbl

    def entry_value():
        name = coin_name_combo.get()
        cval = coin_value_entry.get()
        uval = usd_value_entry.get()

        if (cval.replace(',', '').replace('.', '').isdigit()) and (uval.replace(',', '').replace('.', '').isdigit()):
            by_or_sell_coin(coin_name=name, coin_amount=cval, usd_amount=uval, is_buy=False)

            coin_value_entry.delete(0, END)
            usd_value_entry.delete(0, END)

            show_coin_in_portfolio(fr2)
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
            "куплено монет",
            "витрачено usd",
        ]

        for num, text in enumerate(elements):
            (tk.Label(fr, text=text, width=23, height=3, ).grid(row=0, column=num, rowspan=1, sticky='NSEW', ))

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

    except Exception:
        coin_name_lbl.config(text="в портфелі немає жодної монети", width=50, height=5, fg='white',
                             background=menu_bg_colour)


# видаляємо запис про продаж монети
def redact_sell_operation():
    xx = 50
    yy = 10

    def del_message(coin_name, operation_id):
        question = mb.askquestion('DELETE MENU', 'ви впевнені що хочете видалити?')

        if question == 'yes':
            del_curent_coin_operation(coin_name, operation_id)
            show_coin_in_portfolio(fr2)
            activate()

        else:
            print('no')

    def activate():

        operations = []

        coin_operation_combo = ttk.Combobox(fr, values=[''])
        coin_operation_combo.grid(row=1, column=0, sticky='NSEW', columnspan=4)

        for count, item in enumerate(get_curent_coin_operation(coin_name_conbo.get())):

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


if __name__ == '__main__':
    create_db()
    add_coin_to_db('tether')

    # параметри вікна програми
    x = (dispx // 2) - (appx // 2)
    y = (dispy // 2) - (appy // 2)
    menu = tk.Tk()
    menu.geometry(f"+{x}+{y}")
    menu.title('CRYPTO MANAGER')
    menu.resizable(False, False)
    menu.minsize(appx, appy)
    menu.config(background=menu_bg_colour)
    try:
        menu.iconphoto(False, tk.PhotoImage(file='media/logo.png'))
    except Exception:
        print("no file img")

    # ______________________________________________SETTING BAR______________________________________________

    menu_bar = tk.Menu(menu, selectcolor='#1E1F22')
    menu_bar.add_command(label="редагувати монети", command=dell_coin_menu)
    menu_bar.add_command(label="редагувати покупки", command=redact_buy_operation, )
    menu_bar.add_command(label="редагувати продажі", command=redact_sell_operation, )
    menu.configure(menu=menu_bar)

    # ______________________________________________FRAME 0__________________________________________________

    fr0 = tk.Frame(menu, background=menu_bg_colour)

    fr0.pack(pady=20, padx=20, )

    # ______________________________________________FRAME 1__________________________________________________

    fr1 = tk.Frame(fr0, background=menu_bg_colour)
    fr1.pack()

    widget_lbl = [
        ("курс", name_colour2, element_width - 5),
        ("монета", name_colour1, element_width + 5),
        ("куплено", by_color1, element_width - 4),
        ("витрачено\nUSD", by_color1, element_width - 4),
        ("середня ціна\nкупівлі", by_color1, element_width - 4),
        ("продано", sell_color1, element_width - 4),
        ("отримано\nUSD", sell_color1, element_width - 4),
        ("середня ціна\nпродажу", sell_color1, element_width - 4),
        ("баланс", balance_colour1, element_width-3),
        ("еквівалент\nUSD", balance_colour2, element_width-3),
        ("реалізований\nдохід", balance_colour1, element_width-3),
        ("нереалізований\nдохід", balance_colour2, element_width-3),
        ("прибуток", balance_colour1, element_width-3),
        ("продано %", sell_color2, element_width-3),
    ]
    for num, (text, bg_colour, widtg) in enumerate(widget_lbl):
        if text == "курс" or text == "баланс":
            (tk.Label(fr1, text=text, width=widtg, height=3, background=bg_colour, )
             .grid(row=1, column=num, rowspan=2, sticky='NSEW', ))
        else:
            (tk.Label(fr1, text=text, width=widtg, height=3, background=bg_colour, )
             .grid(row=1, column=num, rowspan=1, sticky='NSEW', ))

    usd_equal = tk.Label(fr1, text="-", width=element_width-3, background=balance_colour2, )
    usd_equal.grid(row=2, column=9, sticky='NSEW', )

    realized_profit = tk.Label(fr1, text="-", width=element_width-3, background=balance_colour1, )
    realized_profit.grid(row=2, column=10, sticky='NSEW', )

    unrealized_profit = tk.Label(fr1, text="-", width=element_width-3, background=balance_colour2, )
    unrealized_profit.grid(row=2, column=11, sticky='NSEW', )

    profit = tk.Label(fr1, text="-", width=element_width-3, background=balance_colour1, )
    profit.grid(row=2, column=12, sticky='NSEW', )

    sell_persent = tk.Label(fr1, text="-", width=element_width-3, background=sell_color2, )
    sell_persent.grid(row=2, column=13, sticky='NSEW', )

    btn1 = tk.Button(fr1, text="+", background=name_colour1, borderwidth=0, command=add_coin_menu)
    btn1.grid(row=2, column=1, sticky='NSEW')

    btn2 = tk.Button(fr1, text="+", background=by_color1, borderwidth=0, command=buy_coin_menu)
    btn2.grid(row=2, column=2, columnspan=3, sticky='NSEW', )

    btn3 = tk.Button(fr1, text="+", background=sell_color1, borderwidth=0, command=sell_coin_menu)
    btn3.grid(row=2, column=5, columnspan=3, sticky='NSEW')

    # ______________________________________________FRAME 2__________________________________________________

    fr2 = tk.Frame(fr0, background=menu_bg_colour)
    fr2.pack()

    show_coin_in_portfolio(fr2)

    # ______________________________________________FRAME 3__________________________________________________

    fr3 = tk.Frame(fr0, background=menu_bg_colour)
    fr3.pack()

    btn4 = tk.Button(fr0, text='оновити', width=element_width, height=1, command=lambda: show_coin_in_portfolio(fr2))
    btn4.pack(fill='x')

    # ______________________________________________FRAME 4__________________________________________________

    fr4 = tk.Frame(fr0, background=menu_bg_colour)
    fr4.pack(side='left', pady=20, )

    lbl = tk.Label(fr4, width=15, text='баланс usdt', background='gray', fg='white', font='size=10')
    lbl.grid(row=0, column=0, )

    balance = tk.Label(fr4, width=10, text=round(abs(get_sell_summ('tether')[0] - get_buy_summ('tether')[0]), 2),
                       background='gray', fg='white', font='size=10')
    balance.grid(row=0, column=1, )

    entry = tk.Entry(fr4, borderwidth=0)
    add_btn = tk.Button(fr4, text='add', borderwidth=0)

    # додаємо usdt
    btn5 = tk.Button(fr4, width=3, text='+', background='gray', borderwidth=0.5, fg='green',
                     command=lambda: (btn5.grid_forget(),
                                      btn6.grid_forget(),
                                      entry.grid(row=0, column=2, sticky='NSEW'),
                                      add_btn.grid(row=0, column=3, sticky='NSEW'),
                                      add_btn.config(command=lambda: (
                                          by_or_sell_coin('tether', entry.get(), entry.get(), is_buy=True),
                                          balance.config(
                                              text=round(
                                                  abs(get_sell_summ('tether')[0] - get_buy_summ('tether')[0]),
                                                  2)), entry.delete(0, END),
                                          entry.grid_forget(),
                                          add_btn.grid_forget(),
                                          btn5.grid(row=0, column=2),
                                          btn6.grid(row=0, column=3)))))
    btn5.grid(row=0, column=2)

    # віднімаємо usdt
    btn6 = tk.Button(fr4, width=3, text='-', background='gray', borderwidth=0.5, fg='red',
                     command=lambda: (btn5.grid_forget(),
                                      btn6.grid_forget(),
                                      entry.grid(row=0, column=2, sticky='NSEW'),
                                      add_btn.grid(row=0, column=3, sticky='NSEW'),
                                      add_btn.config(command=lambda: (
                                          by_or_sell_coin('tether', entry.get(), entry.get(), is_buy=False),
                                          balance.config(
                                              text=round(
                                                  abs(get_sell_summ('tether')[0] - get_buy_summ('tether')[0]),
                                                  2)), entry.delete(0, END),
                                          entry.grid_forget(),
                                          add_btn.grid_forget(),
                                          btn5.grid(row=0, column=2),
                                          btn6.grid(row=0, column=3)))))
    btn6.grid(row=0, column=3)

    menu.mainloop()
