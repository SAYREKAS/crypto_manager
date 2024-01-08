from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk
from function import *
from db import *
from gui_config import *


def add_coin_menu():
    # Меню додавання монети в БД
    def get_entry():
        # Отримуємо значення з поля для введення
        value = str(entry_coin_name.get())
        if get_coin_info(value):
            add_coin_to_db(value)
            label2.config(text="Монету додано успішно", background='green')
            show_coin_in_portfolio(fr1)
        elif not get_coin_info(value):
            label2.config(text="монети не існує", background='red')

    # параметри вікна програми
    add_coin = tk.Tk()
    add_coin.title('ADD COIN')
    add_coin.geometry("400x70")
    xx = (1920 // 2) - (400 // 2)
    yy = (1080 // 2) - (70 // 2)
    add_coin.geometry(f"+{xx}+{yy}")
    add_coin.resizable(False, False)
    add_coin.config(background=menu_bg_colour)

    # елементи меню
    label1 = tk.Label(add_coin, text='Введіть ім`я монети', width=30)
    label2 = tk.Label(add_coin, text='', )
    entry_coin_name = tk.Entry(add_coin, width=30)
    button = tk.Button(add_coin, text='Додати', command=get_entry)

    # розташування елементів меню
    label1.grid(row=0, column=0, sticky="nsew")
    entry_coin_name.grid(row=0, column=1, sticky="nsew")
    button.grid(row=2, column=0, columnspan=2, sticky="nsew")
    label2.grid(row=3, column=0, columnspan=2, sticky="nsew")


def buy_coin_menu():
    def entry_value():
        name = coin_name_combo.get()
        cval = coin_value_entry.get()
        uval = usd_value_entry.get()

        if (cval.replace(',', '').replace('.', '').isdigit()
                and uval.replace(',', '').replace('.', '').isdigit()):

            by_coin(coin_name=name,
                    coin_amount=cval.replace(',', '.'),
                    usd_amount=uval.replace(',', '.'))

            show_coin_in_portfolio(fr1)
            info_lbl.config(text=f"успішно", background='green')
        else:
            info_lbl.config(text=f"помилка в данних", background='red')

    # параметри вікна програми
    buy_menu = tk.Tk()
    buy_menu.title('BUY MENU')
    xx = 500
    yy = 100
    resx = (dispx // 2) - (xx // 2)
    resy = (dispy // 2) - (yy // 2)
    buy_menu.geometry(f"+{resx}+{resy}")
    buy_menu.resizable(False, False)
    buy_menu.minsize(xx, yy)
    buy_menu.config(background=menu_bg_colour)

    # елементи меню
    height = 3
    width = 23

    coin_name_lbl = tk.Label(buy_menu, text="coin name", height=height, width=width, )
    coin_name_combo = ttk.Combobox(buy_menu, width=width, values=get_all_coin_name())
    coin_name_combo.current(0)

    coin_value_lbl = tk.Label(buy_menu, text="coin value", height=height, width=width, )
    coin_value_entry = tk.Entry(buy_menu, width=width, )

    usd_value_lbl = tk.Label(buy_menu, text="usd value", height=height, width=width, )
    usd_value_entry = tk.Entry(buy_menu, width=width, )

    info_lbl = tk.Label(buy_menu, text='')
    buy_menu_btn = tk.Button(buy_menu, text='BUY', command=entry_value)

    # розташування елементів меню
    coin_name_lbl.grid(row=0, column=0, sticky='NSEW')
    coin_name_combo.grid(row=1, column=0, sticky='NSEW')

    coin_value_lbl.grid(row=0, column=1, sticky='NSEW')
    coin_value_entry.grid(row=1, column=1, sticky='NSEW')

    usd_value_lbl.grid(row=0, column=2, sticky='NSEW')
    usd_value_entry.grid(row=1, column=2, sticky='NSEW')

    info_lbl.grid(row=2, column=0, sticky='NSEW', columnspan=3)
    buy_menu_btn.grid(row=3, column=0, sticky='NSEW', columnspan=3)


def sell_coin_menu():
    def entry_value():
        name = combo0.get()
        cval = entry0.get()
        uval = entry1.get()
        if (cval.replace(',', '').replace('.', '').isdigit()
                and uval.replace(',', '').replace('.', '').isdigit()):
            sell_coin(coin_name=name,
                      coin_amount=cval.replace(',', '.'),
                      usd_amount=uval.replace(',', '.'))
            show_coin_in_portfolio(fr1)
            lbl3.config(text=f"успішно", background='green')
        else:
            lbl3.config(text=f"помилка в данних", background='red')

    # параметри вікна програми
    buy_menu = tk.Tk()
    buy_menu.title('SELL MENU')
    xx = 500
    yy = 100
    resx = (dispx // 2) - (xx // 2)
    resy = (dispy // 2) - (yy // 2)
    buy_menu.geometry(f"+{resx}+{resy}")
    buy_menu.resizable(False, False)
    buy_menu.minsize(xx, yy)
    buy_menu.config(background=menu_bg_colour)

    # елементи меню
    height = 3
    width = 23
    lbl0 = tk.Label(buy_menu, text="coin name", height=height, width=width, )
    combo0 = ttk.Combobox(buy_menu, width=width, values=get_all_coin_name())
    combo0.current(0)
    lbl1 = tk.Label(buy_menu, text="coin value", height=height, width=width, )
    entry0 = tk.Entry(buy_menu, width=width, )
    lbl2 = tk.Label(buy_menu, text="usd value", height=height, width=width, )
    entry1 = tk.Entry(buy_menu, width=width, )
    lbl3 = tk.Label(buy_menu, text='')
    btn0 = tk.Button(buy_menu, text='SELL', command=entry_value)

    # розташування елементів меню
    lbl0.grid(row=0, column=0, sticky='NSEW')
    combo0.grid(row=1, column=0, sticky='NSEW')
    lbl1.grid(row=0, column=1, sticky='NSEW')
    entry0.grid(row=1, column=1, sticky='NSEW')
    lbl2.grid(row=0, column=2, sticky='NSEW')
    entry1.grid(row=1, column=2, sticky='NSEW')
    lbl3.grid(row=2, column=0, sticky='NSEW', columnspan=3)
    btn0.grid(row=3, column=0, sticky='NSEW', columnspan=3)


def redact_buy_operation():
    xx = 500
    yy = 500

    def del_message(coin_name, operation_id):
        question = mb.askquestion('DELETE OPERATION',
                                  'Do you really want to delete?')

        if question == 'yes':
            # red_buy_menu.destroy()
            del_curent_coin_operation(coin_name, operation_id)
            show_coin_in_portfolio(fr1)
            activate()

        else:
            print('no')

    def activate():

        operations = []

        coin_operation_combo = ttk.Combobox(red_buy_menu, values=[''])
        coin_operation_combo.grid(row=1, column=0, sticky='NSEW', columnspan=4)

        for count, item in enumerate(get_curent_coin_operation(coin_name_conbo.get())):

            if item[3]:
                operations.append(
                    f"{item[0]}:    {item[3]} {coin_name_conbo.get().upper()} {item[4]} USD | {item[1]} {item[2]} ")
            else:
                continue

        if not operations:
            coin_operation_combo.config(values=["no data"])
            coin_operation_combo.current(0)
        else:
            coin_operation_combo.config(values=operations[-10:])
            coin_operation_combo.current(0)

        del_btn = tk.Button(red_buy_menu, text='DELETE')
        del_btn.config(command=lambda: del_message(coin_name_conbo.get(), coin_operation_combo.get().split(':', 1)[0]))
        del_btn.grid(row=2, column=0, sticky='NSEW', columnspan=4)

    # параметри вікна програми
    red_buy_menu = tk.Tk()
    red_buy_menu.title(f"{'REDACT BUY'}")
    resx = (dispx // 2) - (xx // 2)
    resy = (dispy // 2) - (yy // 2)
    red_buy_menu.geometry(f"+{resx}+{resy}")
    red_buy_menu.resizable(False, False)
    red_buy_menu.minsize(xx, yy)
    red_buy_menu.config(background=menu_bg_colour)

    coin_name_conbo = ttk.Combobox(red_buy_menu, width=50, values=get_all_coin_name())
    coin_name_conbo.current(0)
    btn0 = tk.Button(red_buy_menu, text="start", width=15, command=activate)

    coin_name_conbo.grid(row=0, column=0, sticky='NSEW')
    btn0.grid(row=0, column=1, sticky='NSEW', columnspan=2)


def redact_sell_operation():
    pass


def show_coin_in_portfolio(frame_name):
    for count, name in enumerate(get_all_coin_operation()):
        (tk.Label(frame_name, text=f'{str(name).upper()}', width=20, height=1, background=name_colour2, )
         .grid(row=count + 2, column=0, sticky='NSEW'))

        # Покупка
        (tk.Label(frame_name, text=f'{get_buy_summ(name)[0]}', width=15, height=1, background=by_color2)
         .grid(row=count + 2, column=1, sticky='NSEW'))
        (tk.Label(frame_name, text=f'{get_buy_summ(name)[1]}', width=15, height=1, background=by_color2)
         .grid(row=count + 2, column=2, sticky='NSEW'))
        (tk.Label(frame_name, text=f'{get_buy_summ(name)[2]}', width=15, height=1, background=by_color2)
         .grid(row=count + 2, column=3, sticky='NSEW'))

        # Продаж
        (tk.Label(frame_name, text=f'{get_sell_summ(name)[0]}', width=15, height=1, background=sell_color2)
         .grid(row=count + 2, column=4, sticky='NSEW'))
        (tk.Label(frame_name, text=f'{get_sell_summ(name)[1]}', width=15, height=1, background=sell_color2)
         .grid(row=count + 2, column=5, sticky='NSEW'))
        (tk.Label(frame_name, text=f'{get_sell_summ(name)[2]}', width=15, height=1, background=sell_color2)
         .grid(row=count + 2, column=6, sticky='NSEW'))

        # залишок
        (tk.Label(frame_name, text=f'{get_buy_summ(name)[0] - get_sell_summ(name)[0]}',
                  width=15, height=1, background=balance_colour2).grid(row=count + 2, column=7, sticky='NSEW'))


if __name__ == '__main__':
    # параметри вікна програми
    x = (dispx // 2) - (appx // 2)
    y = (dispy // 2) - (appy // 2)
    menu = tk.Tk()
    menu.geometry(f"+{x}+{y}")
    menu.title('CRYPTO MANAGER')
    menu.resizable(True, True)
    menu.minsize(appx, appy)
    menu.config(background=menu_bg_colour)
    menu.iconphoto(False, tk.PhotoImage(file='media/main logo.png'))

    # елементи меню

    menu_bar = tk.Menu(menu, selectcolor='#1E1F22')
    menu_bar.add_command(label="RED COIN", )
    menu_bar.add_command(label="RED BUY", command=redact_buy_operation, )
    menu_bar.add_command(label="RED SELL", command=redact_sell_operation, )
    menu_bar.add_command(label="OPTIONS", )

    fr1 = tk.Frame(menu, background=menu_bg_colour)

    lbl1 = tk.Label(fr1, text="COIN", width=20, height=3, background=name_colour1)

    lbl2 = tk.Label(fr1, text="BUY", width=15, height=3, background=by_color1, )
    lbl3 = tk.Label(fr1, text="USD", width=15, height=3, background=by_color1, )
    lbl4 = tk.Label(fr1, text="AVG PRICE", width=15, height=3, background=by_color1, )

    lbl5 = tk.Label(fr1, text="SELL", width=15, height=3, background=sell_color1, )
    lbl6 = tk.Label(fr1, text="USD", width=15, height=3, background=sell_color1, )
    lbl7 = tk.Label(fr1, text="AVG PRICE", width=15, height=3, background=sell_color1, )
    lbl8 = tk.Label(fr1, text="BALANCE", width=15, height=3, background=balance_colour1, )

    fr2 = tk.Frame(menu, background=menu_bg_colour)

    btn1 = tk.Button(fr2, text="ADD NEW COIN", width=15, background=name_colour1, borderwidth=0.5,
                     command=add_coin_menu)
    btn2 = tk.Button(fr2, text="BUY COIN", width=15, background=by_color1, borderwidth=0.5, command=buy_coin_menu)
    btn3 = tk.Button(fr2, text="SELL COIN", width=15, background=sell_color1, borderwidth=0.5, command=sell_coin_menu)
    # розташування елементів меню

    menu.configure(menu=menu_bar)

    fr1.pack(side='top', pady=10, padx=10, )

    lbl1.grid(row=1, column=0, sticky='NSEW')
    lbl2.grid(row=1, column=1, sticky='NSEW')
    lbl3.grid(row=1, column=2, sticky='NSEW')
    lbl4.grid(row=1, column=3, sticky='NSEW')
    lbl5.grid(row=1, column=4, sticky='NSEW')
    lbl6.grid(row=1, column=5, sticky='NSEW')
    lbl7.grid(row=1, column=6, sticky='NSEW')
    lbl8.grid(row=1, column=7, sticky='NSEW')
    show_coin_in_portfolio(fr1)

    fr2.pack(side='top', padx=10, fill='y')

    btn1.grid(row=0, column=0, sticky='NSEW')
    btn2.grid(row=0, column=1, columnspan=3, sticky='NSEW')
    btn3.grid(row=0, column=4, columnspan=3, sticky='NSEW')

    menu.mainloop()
