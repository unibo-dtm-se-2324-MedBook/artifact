from flet import *

from first_page import FirstPage
from login_page import LoginPage
from sign_up_page import SignUpPage
from main_page import MainPage

class App(UserControl):
    def __init__(self, page:Page):
        super().__init__
        page.window.width = 240
        page.window.height = 450
        page.window_frameless = True #  окно без стандартной рамки, панели заголовка и кнопок управления окна, таких как минимизация, максимизация и закрытие
        page.window_title_bar_buttons_hidden = True
        page.window_title_bar_hidden = True
        # page.bgcolor = colors.TRANSPARENT
        # page.window_bgcolor = colors.TRANSPARENT


app(target = App)