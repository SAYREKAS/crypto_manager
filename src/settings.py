import ctypes
import json


# Структура для зберігання інформації про розширення монітора
class ScreenResolution(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int)]


# Отримання розширення монітора
def get_screen_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    resolution = ScreenResolution()
    resolution.width = user32.GetSystemMetrics(0)
    resolution.height = user32.GetSystemMetrics(1)
    return resolution


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
    with open('config.json', 'w') as f:
        json.dump(data, f)


#  розширення монітора
screen_res = get_screen_resolution()
dispx = screen_res.width
dispy = screen_res.height

#  розмір вікна програми
appx = 1414
appy = 720

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
