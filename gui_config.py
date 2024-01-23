import ctypes


# Структура для зберігання інформації про розширення екрану
class ScreenResolution(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int)]


# Отримання розширення екрану
def get_screen_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()  # Встановлення DPI-свідомості процесу
    resolution = ScreenResolution()
    resolution.width = user32.GetSystemMetrics(0)  # Ширина екрану
    resolution.height = user32.GetSystemMetrics(1)  # Висота екрану
    return resolution


screen_res = get_screen_resolution()

#  розширення монітора
dispx = screen_res.width
dispy = screen_res.height

#  розмір вікна програми
appx = 1500
appy = 650

# main menu
name_colour1 = '#ff9947'
name_colour2 = '#ffcc8d'

by_color1 = '#3C8A67'
by_color2 = '#D9EFE2'

sell_color1 = '#CC1C39'
sell_color2 = '#F1D5CA'

balance_colour1 = '#63AEBF'
balance_colour2 = '#A0CED9'

menu_bg_colour = '#1E1F22'

element_width = 16
