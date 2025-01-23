from flet import *

from utils.traits import *
from first_page import FirstPage
from login_page import LoginPage
from sign_up_page import SignUpPage
from main_page import MainPage
from forgot_password_page import ForgPasswPage

class WindowDrag(UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return Container(content=WindowDragArea(height = 10, content = Container(bgcolor='black')))


class App(UserControl):
    def __init__(self, page:Page):
        super().__init__()
        page.window.width = base_width
        page.window.height = base_height
        page.window_frameless = True #  окно без стандартной рамки, панели заголовка и кнопок управления окна, таких как минимизация, максимизация и закрытие
        page.window_title_bar_buttons_hidden = True
        page.window_title_bar_hidden = True
        page.bgcolor = colors.TRANSPARENT
        page.window_bgcolor = colors.TRANSPARENT

        self.page = page
        self.page.spacing = 0

        # self.first_page = FirstPage(self.page)
        self.first_page = FirstPage()

        self.login_page = LoginPage(self.page)
        self.signup_page = SignUpPage(self.page)
        self.main_page = MainPage(self.page)
        self.forgpassw_page = ForgPasswPage(self.page)
        
        print(f"self.first_page content: {self.first_page}"),
        
        self.screen_views = Stack( # Stack используется для наложения (или "накладывания") различных элементов друг на друга
            expand = True,
            controls=[
                self.first_page,
                # self.login_page,
                # self.signup_page,  
                # self.main_page, 
                # self.forgpassw_page, 
            ]
        )
        
        self.building()
    
    def building(self):
        self.page.add(WindowDrag(), self.screen_views)
        # self.page.update()

app(target = App, assets_dir= 'assets')