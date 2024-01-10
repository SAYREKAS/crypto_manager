from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import END
import tkinter as tk
from parser import *
from db import *
from gui_config import *


# -------------------------------------------------------------------------------------------------------
# виводимо віджети з інформацією про портфоліо в головне меню
def show_coin_in_portfolio(frame):
    fr = tk.Frame(frame, background=menu_bg_colour)
    fr.grid(row=3, column=0, columnspan=8, sticky='NSEW')
    fr.config(pady=5)

    balance_summ = 0

    for count, name in enumerate(get_coin_info(get_all_coin_name())):
        (tk.Label(fr, text=f'{name[2]} $', width=element_width, height=1,
                  background=name_colour2, )
         .grid(row=count + 2, column=0, sticky='NSEW'))

        (tk.Label(fr, text=f'{name[0]} {name[1]}', width=element_width,
                  height=1, background=name_colour2, )
         .grid(row=count + 2, column=1, sticky='NSEW'))

        # Покупка
        (tk.Label(fr, text=f'{get_buy_summ(name[0].lower())[0]}', width=element_width, height=1, background=by_color2)
         .grid(row=count + 2, column=2, sticky='NSEW'))
        (tk.Label(fr, text=f'{get_buy_summ(name[0].lower())[1]}', width=element_width, height=1, background=by_color2)
         .grid(row=count + 2, column=3, sticky='NSEW'))
        (tk.Label(fr, text=f'{get_buy_summ(name[0].lower())[2]}', width=element_width, height=1, background=by_color2)
         .grid(row=count + 2, column=4, sticky='NSEW'))

        # Продаж
        (tk.Label(fr, text=f'{get_sell_summ(name[0].lower())[0]}', width=element_width, height=1,
                  background=sell_color2)
         .grid(row=count + 2, column=5, sticky='NSEW'))
        (tk.Label(fr, text=f'{get_sell_summ(name[0].lower())[1]}', width=element_width, height=1,
                  background=sell_color2)
         .grid(row=count + 2, column=6, sticky='NSEW'))
        (tk.Label(fr, text=f'{get_sell_summ(name[0].lower())[2]}', width=element_width, height=1,
                  background=sell_color2)
         .grid(row=count + 2, column=7, sticky='NSEW'))

        # залишок
        (tk.Label(fr, text=f'{get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]} {name[1]}',
                  width=element_width, height=1, background=balance_colour2).grid(row=count + 2, column=8,
                                                                                  sticky='NSEW'))
        (tk.Label(fr,
                  text=f'{round(name[2] * (get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]), 2)} $',
                  width=element_width, height=1, background=balance_colour2).grid(row=count + 2, column=9,
                                                                                  sticky='NSEW'))
        balance_summ += (name[2] * (get_buy_summ(name[0].lower())[0] - get_sell_summ(name[0].lower())[0]))
    lbl10.config(text=f"{round(balance_summ, 2)} $")


# -------------------------------------------------------------------------------------------------------
# додаємо монети
def add_coin_menu():
    # Меню додавання монети в БД
    def get_entry():
        # Отримуємо значення з поля для введення
        value = str(entry_coin_name.get())
        if check_for_exis_coin(value):
            add_coin_to_db(value)
            label2.config(text="монету додано успішно", background='green')
            entry_coin_name.delete(0, END)
            show_coin_in_portfolio(fr2)
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


# видаляємо монети
def dell_coin_menu():
    global label1

    def del_message(coin_name):
        question = mb.askquestion('DELETE MENU',
                                  f'ви впевнені що хочете видалити монету {coin_name} ?')
        if question == 'yes':
            dell_coin.destroy()
            dell_coin_in_db(coin_name)
            show_coin_in_portfolio(fr2)
        else:
            dell_coin.destroy()

    try:
        # параметри вікна програми
        x = 1
        y = 110
        dell_coin = tk.Toplevel(menu)
        dell_coin.title('DELL COIN')
        dell_coin.geometry("400x70")
        xx = (1920 // 2) - (x // 2)
        yy = (1080 // 2) - (y // 2)
        dell_coin.geometry(f"+{xx}+{yy}")
        dell_coin.resizable(False, False)
        dell_coin.config(background=menu_bg_colour)
        dell_coin.minsize(x, y)
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


# -------------------------------------------------------------------------------------------------------

# додаємо запис про купівлю монети
def buy_coin_menu():
    global coin_name_lbl

    def entry_value():
        name = coin_name_combo.get()
        cval = coin_value_entry.get()
        uval = usd_value_entry.get()

        if (cval.replace(',', '').replace('.', '').isdigit()
                and uval.replace(',', '').replace('.', '').isdigit()):

            by_coin(coin_name=name,
                    coin_amount=cval.replace(',', '.'),
                    usd_amount=uval.replace(',', '.'))

            coin_value_entry.delete(0, END)
            usd_value_entry.delete(0, END)

            show_coin_in_portfolio(fr2)
            info_lbl.config(text=f"запис успішно додано", background='green')
        else:
            info_lbl.config(text=f"помилка в данних", background='red')

    try:
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

        fr = tk.Frame(buy_menu)
        fr.pack()

        coin_name_lbl = tk.Label(fr, text="ім'я монети", height=height, width=width, )
        coin_name_lbl.grid(row=0, column=0, sticky='NSEW')

        coin_name_combo = ttk.Combobox(fr, width=width, values=get_all_coin_name())
        coin_name_combo.current(0)
        coin_name_combo.grid(row=1, column=0, sticky='NSEW')

        coin_value_lbl = tk.Label(fr, text="кількість монет", height=height, width=width, )
        coin_value_lbl.grid(row=0, column=1, sticky='NSEW')

        coin_value_entry = tk.Entry(fr, width=width, )
        coin_value_entry.grid(row=1, column=1, sticky='NSEW')

        usd_value_lbl = tk.Label(fr, text="витрачено usd", height=height, width=width, )
        usd_value_lbl.grid(row=0, column=2, sticky='NSEW')

        usd_value_entry = tk.Entry(fr, width=width, )
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
    xx = 50
    yy = 10

    def del_message(coin_name, operation_id):
        question = mb.askquestion('DELETE MENU',
                                  'ви впевнені що хочете видалити?')

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
        del_btn.config(
            command=lambda: del_message(coin_name_conbo.get(), coin_operation_combo.get().split(':', 1)[0]))
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


# -------------------------------------------------------------------------------------------------------

# додаємо запис про продаж монети
def sell_coin_menu():
    global coin_name_lbl

    def entry_value():
        name = coin_name_combo.get()
        cval = coin_value_entry.get()
        uval = usd_value_entry.get()

        if (cval.replace(',', '').replace('.', '').isdigit()
                and uval.replace(',', '').replace('.', '').isdigit()):
            sell_coin(coin_name=name,
                      coin_amount=cval.replace(',', '.'),
                      usd_amount=uval.replace(',', '.'))

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

        fr = tk.Frame(buy_menu)
        fr.pack()

        coin_name_lbl = tk.Label(fr, text="ім'я монети", height=height, width=width, )
        coin_name_lbl.grid(row=0, column=0, sticky='NSEW')

        coin_name_combo = ttk.Combobox(fr, width=width, values=get_all_coin_name())
        coin_name_combo.current(0)
        coin_name_combo.grid(row=1, column=0, sticky='NSEW')

        coin_value_lbl = tk.Label(fr, text="кількість монет", height=height, width=width, )
        coin_value_lbl.grid(row=0, column=1, sticky='NSEW')

        coin_value_entry = tk.Entry(fr, width=width, )
        coin_value_entry.grid(row=1, column=1, sticky='NSEW')

        usd_value_lbl = tk.Label(fr, text="витрачено usd", height=height, width=width, )
        usd_value_lbl.grid(row=0, column=2, sticky='NSEW')

        usd_value_entry = tk.Entry(fr, width=width, )
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
        question = mb.askquestion('DELETE MENU',
                                  'ви впевнені що хочете видалити?')

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
        del_btn.config(
            command=lambda: del_message(coin_name_conbo.get(), coin_operation_combo.get().split(':', 1)[0]))
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
        btn0 = tk.Button(fr, text="знайти операції", width=15, command=activate)

        coin_name_conbo.grid(row=0, column=0, sticky='NSEW')
        btn0.grid(row=0, column=1, sticky='NSEW', columnspan=2)


# -------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    create_db()

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
        menu.iconphoto(False, tk.PhotoImage(file='media/main logo.png'))
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

    fr0.pack(side='top', pady=10, padx=10, fill='x')

    # ______________________________________________FRAME 1__________________________________________________
    fr1 = tk.Frame(fr0, background=menu_bg_colour)

    lbl1 = tk.Label(fr1, text="курс", width=element_width, height=3, borderwidth=0, background=name_colour1, )
    lbl1.grid(row=1, column=0, rowspan=2, sticky='NSEW')

    lbl1 = tk.Label(fr1, text="монета", width=element_width, height=3, borderwidth=0, background=name_colour1, )
    lbl1.grid(row=1, column=1, sticky='NSEW')

    lbl2 = tk.Label(fr1, text="куплено", wraplength=80, width=element_width, height=3, background=by_color1, )
    lbl2.grid(row=1, column=2, sticky='NSEW')

    lbl3 = tk.Label(fr1, text="витрачено USD", wraplength=75, width=element_width, height=3, background=by_color1, )
    lbl3.grid(row=1, column=3, sticky='NSEW')

    lbl4 = tk.Label(fr1, text="середня ціна купівлі", wraplength=80, width=element_width, height=3,
                    background=by_color1, )
    lbl4.grid(row=1, column=4, sticky='NSEW')

    lbl5 = tk.Label(fr1, text="продано", wraplength=80, width=element_width, height=3, background=sell_color1, )
    lbl5.grid(row=1, column=5, sticky='NSEW')

    lbl6 = tk.Label(fr1, text="отримано USD", wraplength=75, width=element_width, height=3, background=sell_color1, )
    lbl6.grid(row=1, column=6, sticky='NSEW')

    lbl7 = tk.Label(fr1, text="середня ціна продажу", wraplength=80, width=element_width, height=3,
                    background=sell_color1, )
    lbl7.grid(row=1, column=7, sticky='NSEW')

    lbl8 = tk.Label(fr1, text="баланс", wraplength=80, width=element_width, height=3, background=balance_colour1, )
    lbl8.grid(row=1, column=8, rowspan=2, sticky='NSEW', )

    lbl9 = tk.Label(fr1, text="еквівалент USD", wraplength=80, width=element_width, height=3,
                    background=balance_colour1, )
    lbl9.grid(row=1, column=9, sticky='NSEW', )

    lbl10 = tk.Label(fr1, text="", wraplength=80, width=element_width,
                     background=balance_colour1, )
    lbl10.grid(row=2, column=9, sticky='NSEW', )

    btn1 = tk.Button(fr1, text="+", wraplength=110, width=element_width, background=name_colour1, borderwidth=1,
                     command=add_coin_menu)
    btn1.grid(row=2, column=1, sticky='NSEW')

    btn2 = tk.Button(fr1, text="+", wraplength=110, width=element_width, background=by_color1, borderwidth=1,
                     command=buy_coin_menu)
    btn2.grid(row=2, column=2, columnspan=3, sticky='NSEW', )

    btn3 = tk.Button(fr1, text="+", wraplength=110, width=element_width, background=sell_color1, borderwidth=1,
                     command=sell_coin_menu)
    btn3.grid(row=2, column=5, columnspan=3, sticky='NSEW')

    fr1.pack(fill='x')

    # ______________________________________________FRAME 2__________________________________________________
    fr2 = tk.Frame(fr0, background=menu_bg_colour)
    fr2.pack(fill='x')

    # ______________________________________________FRAME 3__________________________________________________

    btn4 = tk.Button(fr0, text='оновити', width=element_width, height=1,
                     command=lambda: show_coin_in_portfolio(fr2))
    btn4.pack(fill='x')

    show_coin_in_portfolio(fr2)

    menu.mainloop()
