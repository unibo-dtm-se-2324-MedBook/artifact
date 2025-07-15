from flet import *
# from flet_route import Router, Route, RouteContext

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

        self.first_page = FirstPage(self)
        self.login_page = LoginPage()
        self.signup_page = SignUpPage(self)
        self.main_page = MainPage()
        self.forgpassw_page = ForgPasswPage()

        self.temp_email = '' # temporary email storage
        

        # self.screen_views = Stack( # Stack используется для наложения (или "накладывания") различных элементов друг на друга
        #     expand = True,
        #     controls=[
        #         self.first_page,
        #         # self.login_page,
        #         # self.signup_page,  
        #         # self.main_page, 
        #         # self.forgpassw_page, 
        #     ]
        # )

        page.on_route_change = self.route_change
        page.go("/first_page")
        # self.building()
    
    # def building(self):
    #     self.page.add(WindowDrag(), Stack(expand = True, controls=[self.first_page])) # self.screen_views)

    def route_change(self, route):
        self.page.controls.clear()

        if self.page.route == "/first_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.first_page]))
        elif self.page.route == "/login_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.login_page]))
            if self.temp_email:
                self.login_page.set_email(self.temp_email)
                self.temp_email = ''
        elif self.page.route == "/passw_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.forgpassw_page]))
        elif self.page.route == "/singup_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.signup_page]))
        elif self.page.route == "/main_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.main_page]))
        
        self.page.update()

app(target = App, assets_dir= 'assets')