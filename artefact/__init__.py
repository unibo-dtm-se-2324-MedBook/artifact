from flet import *

from artefact.utils.traits import *
from artefact.ui.gui.first_page import FirstPage
from artefact.ui.gui.login_page import LoginPage
from artefact.ui.gui.sign_up_page import SignUpPage
from artefact.ui.gui.main_page import MainPage
from artefact.ui.gui.forgot_password_page import ForgPasswPage
from artefact.ui.gui.settings_page import SettingsPage
from artefact.ui.gui.documents_page import DocumentsPage
from artefact.ui.gui.medication_check_page import MedicineCheckPage

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
        page.window_frameless = True #  a window without the standard frame, title bar, and window control buttons such as minimize, maximize, and close
        page.window_title_bar_buttons_hidden = True
        page.window_title_bar_hidden = True
        page.bgcolor = colors.TRANSPARENT
        page.window_bgcolor = colors.TRANSPARENT

        self.page = page
        self.page.spacing = 0

        self.first_page = FirstPage()
        self.login_page = LoginPage()
        self.signup_page = SignUpPage()
        self.main_page = MainPage()
        self.forgpassw_page = ForgPasswPage()
        self.settings_page = SettingsPage()
        self.documents_page = DocumentsPage()
        self.medicine_check_page = MedicineCheckPage()

        page.on_route_change = self.route_change
        page.go("/first_page")

    def route_change(self, route):
        self.page.controls.clear()

        if self.page.route == "/first_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.first_page]))
        elif self.page.route == "/login_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.login_page]))
        elif self.page.route == "/passw_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.forgpassw_page]))
        elif self.page.route == "/signup_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.signup_page]))
        elif self.page.route == "/main_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.main_page]))
        elif self.page.route == "/settings_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.settings_page]))
        elif self.page.route == "/documents_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.documents_page]))
        elif self.page.route == "/pill_check_page":
            self.page.add(WindowDrag(), Stack(expand=True, controls=[self.medicine_check_page]))
        
        self.page.update()

app(target = App, assets_dir= 'assets')