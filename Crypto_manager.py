from tkinter import ttk
from tkinter import messagebox as mb
import tkinter as tk
from parser import *
from db import *
from gui_config import *


def show_coin_in_portfolio():
    fr11 = tk.Frame(fr1, background=menu_bg_colour)
    fr11.grid(row=3, column=0, columnspan=8, sticky='NSEW')

    for count, name in enumerate(get_all_coin_operation()):
        (tk.Label(fr11, text=f'{str(name).upper()}', width=20, height=1, background=name_colour2, )
         .grid(row=count + 2, column=0, sticky='NSEW'))

        # Покупка
        (tk.Label(fr11, text=f'{get_buy_summ(name)[0]}', width=15, height=1, background=by_color2)
         .grid(row=count + 2, column=1, sticky='NSEW'))
        (tk.Label(fr11, text=f'{get_buy_summ(name)[1]}', width=15, height=1, background=by_color2)
         .grid(row=count + 2, column=2, sticky='NSEW'))
        (tk.Label(fr11, text=f'{get_buy_summ(name)[2]}', width=15, height=1, background=by_color2)
         .grid(row=count + 2, column=3, sticky='NSEW'))

        # Продаж
        (tk.Label(fr11, text=f'{get_sell_summ(name)[0]}', width=15, height=1, background=sell_color2)
         .grid(row=count + 2, column=4, sticky='NSEW'))
        (tk.Label(fr11, text=f'{get_sell_summ(name)[1]}', width=15, height=1, background=sell_color2)
         .grid(row=count + 2, column=5, sticky='NSEW'))
        (tk.Label(fr11, text=f'{get_sell_summ(name)[2]}', width=15, height=1, background=sell_color2)
         .grid(row=count + 2, column=6, sticky='NSEW'))

        # залишок
        (tk.Label(fr11, text=f'{get_buy_summ(name)[0] - get_sell_summ(name)[0]}',
                  width=15, height=1, background=balance_colour2).grid(row=count + 2, column=7, sticky='NSEW'))


def add_coin_menu():
    # Меню додавання монети в БД
    def get_entry():
        # Отримуємо значення з поля для введення
        value = str(entry_coin_name.get())
        if get_coin_info(value):
            add_coin_to_db(value)
            label2.config(text="монету додано успішно", background='green')
            show_coin_in_portfolio()
        elif not get_coin_info(value):
            label2.config(text="монети не існує", background='red')

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
    label1 = tk.Label(add_coin, text='Введіть ім`я монети', width=30)
    label2 = tk.Label(add_coin, text='', )
    entry_coin_name = tk.Entry(add_coin, width=30)
    button = tk.Button(add_coin, text='Додати', command=get_entry)

    # розташування елементів меню
    label1.grid(row=0, column=0, sticky="nsew")
    entry_coin_name.grid(row=0, column=1, sticky="nsew")
    button.grid(row=2, column=0, columnspan=2, sticky="nsew")
    label2.grid(row=3, column=0, columnspan=2, sticky="nsew")


def dell_coin_menu():
    def del_message(coin_name):
        question = mb.askquestion('DELETE MENU',
                                  f'ви впевнені що хочете видалити монету {coin_name} ?')

        if question == 'yes':
            dell_coin_in_db(coin_name)
            show_coin_in_portfolio()
            dell_coin.destroy()
        else:
            print('no')

    # параметри вікна програми
    x = 400
    y = 200
    dell_coin = tk.Toplevel(menu)
    dell_coin.title('DELL COIN')
    dell_coin.geometry("400x70")
    xx = (1920 // 2) - (x // 2)
    yy = (1080 // 2) - (y // 2)
    dell_coin.geometry(f"+{xx}+{yy}")
    menu.minsize(x, y)
    dell_coin.resizable(False, False)
    dell_coin.config(background=menu_bg_colour)
    dell_coin.grab_set()

    # елементи меню
    label1 = tk.Label(dell_coin, text='виберіть ім`я монети яку потрібно видалити', wraplength=200, width=30, )

    entry_coin_name = ttk.Combobox(dell_coin, width=30, values=get_all_coin_name())
    entry_coin_name.current(0)

    button = tk.Button(dell_coin, text='видалити', )
    button.config(command=lambda: del_message(entry_coin_name.get()))

    # розташування елементів меню
    label1.grid(row=0, column=0, sticky="nsew")
    entry_coin_name.grid(row=1, column=0, sticky="nsew")
    button.grid(row=2, column=0, columnspan=2, sticky="nsew")


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

            show_coin_in_portfolio()
            info_lbl.config(text=f"запис успішно додано", background='green')
        else:
            info_lbl.config(text=f"помилка в данних", background='red')

    # параметри вікна програми
    buy_menu = tk.Toplevel(menu)
    buy_menu.title('BUY MENU')
    xx = 500
    yy = 100
    resx = (dispx // 2) - (xx // 2)
    resy = (dispy // 2) - (yy // 2)
    buy_menu.geometry(f"+{resx}+{resy}")
    buy_menu.resizable(False, False)
    buy_menu.minsize(xx, yy)
    buy_menu.config(background=menu_bg_colour)
    buy_menu.grab_set()

    # елементи меню
    height = 3
    width = 23

    coin_name_lbl = tk.Label(buy_menu, text="ім'я монети", height=height, width=width, )
    coin_name_combo = ttk.Combobox(buy_menu, width=width, values=get_all_coin_name())
    coin_name_combo.current(0)

    coin_value_lbl = tk.Label(buy_menu, text="кількість монет", height=height, width=width, )
    coin_value_entry = tk.Entry(buy_menu, width=width, )

    usd_value_lbl = tk.Label(buy_menu, text="витрачено usd", height=height, width=width, )
    usd_value_entry = tk.Entry(buy_menu, width=width, )

    info_lbl = tk.Label(buy_menu, text='')
    buy_menu_btn = tk.Button(buy_menu, text='зробити запис про купівлю', command=entry_value)

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
            show_coin_in_portfolio()
            lbl3.config(text=f"запис успішно додано", background='green')
        else:
            lbl3.config(text=f"помилка в данних", background='red')

    # параметри вікна програми
    buy_menu = tk.Toplevel(menu)
    buy_menu.title('SELL MENU')
    xx = 500
    yy = 100
    resx = (dispx // 2) - (xx // 2)
    resy = (dispy // 2) - (yy // 2)
    buy_menu.geometry(f"+{resx}+{resy}")
    buy_menu.resizable(False, False)
    buy_menu.minsize(xx, yy)
    buy_menu.config(background=menu_bg_colour)
    buy_menu.grab_set()

    # елементи меню
    height = 3
    width = 23
    lbl0 = tk.Label(buy_menu, text="ім'я монети", height=height, width=width, )
    combo0 = ttk.Combobox(buy_menu, width=width, values=get_all_coin_name())
    combo0.current(0)
    lbl1 = tk.Label(buy_menu, text="кількість монет", height=height, width=width, )
    entry0 = tk.Entry(buy_menu, width=width, )
    lbl2 = tk.Label(buy_menu, text="витрачено usd", height=height, width=width, )
    entry1 = tk.Entry(buy_menu, width=width, )
    lbl3 = tk.Label(buy_menu, text='')
    btn0 = tk.Button(buy_menu, text='зробити запис про продаж', command=entry_value)

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
    xx = 50
    yy = 10

    def del_message(coin_name, operation_id):
        question = mb.askquestion('DELETE MENU',
                                  'ви впевнені що хочете видалити?')

        if question == 'yes':
            del_curent_coin_operation(coin_name, operation_id)
            show_coin_in_portfolio()
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
            coin_operation_combo.config(values=["немає даних"])
            coin_operation_combo.current(0)
        else:
            coin_operation_combo.config(values=operations[-10:])
            coin_operation_combo.current(0)

        del_btn = tk.Button(red_buy_menu, text='видалити')
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

    coin_name_conbo = ttk.Combobox(red_buy_menu, width=50, values=get_all_coin_name())
    coin_name_conbo.current(0)
    btn0 = tk.Button(red_buy_menu, text="знайти операції", width=15, command=activate)

    coin_name_conbo.grid(row=0, column=0, sticky='NSEW')
    btn0.grid(row=0, column=1, sticky='NSEW', columnspan=2)


def redact_sell_operation():
    xx = 50
    yy = 10

    def del_message(coin_name, operation_id):
        question = mb.askquestion('DELETE MENU',
                                  'ви впевнені що хочете видалити?')

        if question == 'yes':
            del_curent_coin_operation(coin_name, operation_id)
            show_coin_in_portfolio()
            activate()

        else:
            print('no')

    def activate():

        operations = []

        coin_operation_combo = ttk.Combobox(red_buy_menu, values=[''])
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

        del_btn = tk.Button(red_buy_menu, text='видалити')
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

    coin_name_conbo = ttk.Combobox(red_buy_menu, width=50, values=get_all_coin_name())
    coin_name_conbo.current(0)
    btn0 = tk.Button(red_buy_menu, text="знайти операції", width=15, command=activate)

    coin_name_conbo.grid(row=0, column=0, sticky='NSEW')
    btn0.grid(row=0, column=1, sticky='NSEW', columnspan=2)


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
    try:
        menu.iconphoto(False, tk.PhotoImage(file='media/main logo.png'))
    except Exception:
        print("no file img")

    # елементи меню

    menu_bar = tk.Menu(menu, selectcolor='#1E1F22')
    menu_bar.add_command(label="редагувати монети", command=dell_coin_menu)
    menu_bar.add_command(label="редагувати покупки", command=redact_buy_operation, )
    menu_bar.add_command(label="редагувати продажі", command=redact_sell_operation, )

    fr1 = tk.Frame(menu, background=menu_bg_colour)

    lbl1 = tk.Button(fr1, text="монета", width=20, height=3, borderwidth=0, background=name_colour1,
                     command=lambda: show_coin_in_portfolio())

    lbl2 = tk.Label(fr1, text="куплено", wraplength=80, width=15, height=3, background=by_color1, )
    lbl3 = tk.Label(fr1, text="витрачено USD", wraplength=75, width=15, height=3, background=by_color1, )
    lbl4 = tk.Label(fr1, text="середня ціна купівлі", wraplength=80, width=15, height=3, background=by_color1, )

    lbl5 = tk.Label(fr1, text="продано", wraplength=80, width=15, height=3, background=sell_color1, )
    lbl6 = tk.Label(fr1, text="отримано USD", wraplength=75, width=15, height=3, background=sell_color1, )
    lbl7 = tk.Label(fr1, text="середня ціна продажу", wraplength=80, width=15, height=3, background=sell_color1, )
    lbl8 = tk.Label(fr1, text="баланс", wraplength=80, width=15, height=3, background=balance_colour1, )

    fr2 = tk.Frame(menu, background=menu_bg_colour)

    btn1 = tk.Button(fr2, text="додати нову монету", wraplength=110, width=25, background=name_colour1, borderwidth=0.5,
                     command=add_coin_menu)
    btn2 = tk.Button(fr2, text="внести дані про купівлю монети", wraplength=110, width=25, background=by_color1,
                     borderwidth=0.5, command=buy_coin_menu)
    btn3 = tk.Button(fr2, text="внести дані про продаж монети", wraplength=110, width=25, background=sell_color1,
                     borderwidth=0.5, command=sell_coin_menu)

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
    show_coin_in_portfolio()

    fr2.pack(side='top', padx=10, fill='y')

    btn1.grid(row=0, column=0, sticky='NSEW')
    btn2.grid(row=0, column=1, columnspan=3, sticky='NSEW')
    btn3.grid(row=0, column=4, columnspan=3, sticky='NSEW')

    menu.mainloop()
