import json
import tkinter as tk
from dataclasses import field, dataclass

from src.db.db import Db
from src.parser.common import Parser
from src.parser.parser import get_coin_info


class GlobalCounter:
    sell_count: int = 0
    crypto_summ: float = 0
    stable_summ: float = 0
    profit_summ: float = 0
    equivalent_summ: float = 0
    sell_percent_summ: float = 0
    realized_income_summ: float = 0
    unrealized_income_summ: float = 0
    number_of_coins_in_portfolio: int = 0

    all_coin_name: list[str] = field(default_factory=list)
    coin_info: list[Parser] = field(default_factory=list)

    def reset_variable(self, database: Db) -> None:
        """Скидає всі змінні та оновлює інформацію про монети."""
        self.sell_count = 0
        self.crypto_summ = 0
        self.stable_summ = 0
        self.profit_summ = 0
        self.equivalent_summ = 0
        self.sell_percent_summ = 0
        self.realized_income_summ = 0
        self.unrealized_income_summ = 0
        self.number_of_coins_in_portfolio = 0

        self.all_coin_name = database.all_coin_name()
        self.number_of_coins_in_portfolio = len(self.all_coin_name)
        self.coin_info = get_coin_info(self.all_coin_name)


@dataclass
class WindowParam:
    title: str
    background: str = "white"

    app_res_x: int = 500
    app_res_y: int = 500

    disp_res_x: int = 1920
    disp_res_y: int = 1080

    resizable_x: bool = False
    resizable_y: bool = False

    x: int = (disp_res_x // 2) - (app_res_x // 2)
    y: int = (disp_res_y // 2) - (app_res_y // 2)


class MainWindow:
    """
    Класс який створює батьківське вікно програми.
    доступні параметри:
    title, app_res, disp_res, resizable,background
    """

    def __init__(self, param: WindowParam):
        self.param = param

        self.root = tk.Tk()
        self.root.title(param.title)
        self.root.geometry(f"+{param.x}+{param.y}")
        self.root.minsize(param.app_res_x, param.app_res_y)
        self.root.config(background=param.background)
        self.root.resizable(param.resizable_x, param.resizable_y)

    def start(self):
        self.root.mainloop()


class ChildWindow:
    """
    Класс який створює дочірнє вікно для батьківського вікна програми.
    обов'язковий параметер "top_lvl" вказує на батьківське вікно.
    доступні параметри: title, app_res, disp_res, resizable,background

    """

    def __init__(self, top_lvl, param: WindowParam):
        self.param = param

        self.root = tk.Toplevel(top_lvl)
        self.root.title(param.title)
        self.root.geometry(f"+{param.x}+{param.y}")
        self.root.resizable(param.resizable_x, param.resizable_y)
        self.root.minsize(param.app_res_x, param.app_res_y)
        self.root.config(background=param.background)
        self.root.grab_set()


def get_settings():
    try:
        with open('config.json', 'r') as settings_file:
            data = json.load(settings_file)
            return data

    except FileNotFoundError:
        reset_settings()


def reset_settings():
    standart_param = {
        "sorting": 1,
        "reverse": 0,
    }

    with open('config.json', 'w') as settings_file:
        json.dump(standart_param, settings_file)


def update_settings(key, parameter):
    # Відкриваємо файл .json і завантажуємо дані
    with open('config.json', 'r') as f:
        data = json.load(f)

    # Змінюємо значення ключа
    data[key] = parameter

    # Записуємо дані назад у файл
    with open('config.json', 'w') as file:
        json.dump(data, file)


# main menu
name_colour1 = '#ff9947'
name_colour2 = '#ffcc8d'

buy_colour1 = '#3C8A67'
buy_colour2 = '#D9EFE2'

sell_color1 = '#CC1C39'
sell_color2 = '#F1D5CA'

balance_colour1 = '#63AEBF'
balance_colour2 = '#A0CED9'

menu_bg_colour = '#1E1F22'

element_width = 16

#  розширення монітора
dispx = 1920
dispy = 1080

#  розмір вікна програми
appx = 1414
appy = 720

main_menu_param = WindowParam(
    title="CRYPTO MANAGER",
    background=menu_bg_colour
)
dell_coin_menu_param = WindowParam(
    title="Dell coin menu",
    app_res_x=400, app_res_y=70,
    background=menu_bg_colour
)
transaction_menu_param = WindowParam(
    title="Transaction",
    app_res_x=500, app_res_y=100,
    background=menu_bg_colour
)
red_buy_menu_param = WindowParam(
    title="Redact menu",
    app_res_x=500, app_res_y=50,
    background=menu_bg_colour
)
add_coin_menu_param = WindowParam(
    title="Add coin menu",
    app_res_x=400, app_res_y=70,
    background=menu_bg_colour
)
