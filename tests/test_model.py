import unittest
from unittest.mock import patch, MagicMock
import importlib

MODULE_UNDER_TEST = 'artefact'

# Simulates a window object (page.window) that has the required attributes
class FakeWindow:
    def __init__(self):
        self.width = None
        self.height = None


# Simulates a Flet page with .add(), .update(), .go() methods and a controls collection
class FakePage:
    def __init__(self):
        self.window = FakeWindow()
        self.window_frameless = None
        self.window_title_bar_buttons_hidden = None
        self.window_title_bar_hidden = None
        self.bgcolor = None
        self.window_bgcolor = None
        self.spacing = None
        self.controls = []
        self.route = '/'
        self.on_route_change = None

    def add(self, *controls):
        self.controls.extend(controls)

    def update(self):
        pass

    # Change the route and trigger the handler if one is set App.__init__
    def go(self, new_route: str):
        self.route = new_route
        if callable(self.on_route_change):
            self.on_route_change(None)


# Initialization, basic routing between pages
class TestAppRouting(unittest.TestCase):
    
    def setUp(self): # before tests
        self.p_app = patch('flet.app', MagicMock(name = 'flet.app'))
        self.p_app.start()

        # Import the module from App (under patches - no real UI)
        self.app_module = importlib.import_module(MODULE_UNDER_TEST)

        self.p_first = patch('artefact.FirstPage', return_value = MagicMock(name = 'FirstPage'))
        self.p_login = patch('artefact.LoginPage', return_value = MagicMock(name = 'LoginPage'))
        self.p_signup = patch('artefact.SignUpPage', return_value = MagicMock(name = 'SignUpPage'))
        self.p_forg = patch('artefact.ForgPasswPage', return_value = MagicMock(name = 'ForgPasswPage'))
        self.p_main = patch('artefact.MainPage', return_value = MagicMock(name = 'MainPage'))
        self.p_settings = patch('artefact.SettingsPage', return_value = MagicMock(name = 'SettingsPage'))
        self.p_docs = patch('artefact.DocumentsPage', return_value = MagicMock(name = 'DocumentsPage'))
        self.p_med = patch('artefact.MedicineCheckPage', return_value = MagicMock(name = 'MedicineCheckPage'))

        for p in (self.p_first, self.p_login, self.p_signup, self.p_main, self.p_forg, self.p_settings, self.p_docs, self.p_med):
            p.start()

        # Create a fake page and App instance
        self.fake_page = FakePage()
        self.app_instance = self.app_module.App(self.fake_page)

    def tearDown(self): # after tests
        for p in (self.p_first, self.p_login, self.p_signup, self.p_main, self.p_forg, self.p_settings, self.p_docs, self.p_med):
            p.stop()
        self.p_app.stop()

    def _assert_top_stack_contains(self, expected_placeholder_name: str):
        self.assertGreaterEqual(len(self.fake_page.controls), 2, 'At least two controls: WindowDrag and Stack')
        window_drag, stack = self.fake_page.controls[0], self.fake_page.controls[1]

        self.assertTrue(hasattr(stack, 'controls'), 'The second control should be a Stack with .controls')
        self.assertGreaterEqual(len(stack.controls), 1, 'Stack must contain at least one page')
        first_child = stack.controls[0]

        self.assertTrue(isinstance(first_child, MagicMock)) # Check the type - it really is MagicMock
        self.assertEqual(first_child._mock_name, expected_placeholder_name) # Compare name of mock with setUp

    def test_initial_route_is_first_page(self):
        self._assert_top_stack_contains('FirstPage')
        # In __init__ page.go('/first_page') was already called, which means controls should be filled in

    def test_route_change_to_login_page(self):
        self.fake_page.go('/login_page')
        self._assert_top_stack_contains('LoginPage')

    def test_route_change_to_signup_page(self):
        self.fake_page.go('/signup_page')
        self._assert_top_stack_contains('SignUpPage')
    
    def test_route_change_to_forgot_password_page(self):
        self.fake_page.go('/passw_page')
        self._assert_top_stack_contains('ForgPasswPage')
    
    def test_route_change_to_main_page(self):
        self.fake_page.go('/main_page')
        self._assert_top_stack_contains('MainPage')

    def test_route_change_to_settings_page(self):
        self.fake_page.go('/settings_page')
        self._assert_top_stack_contains('SettingsPage')

    def test_route_change_to_documents_page(self):
        self.fake_page.go('/documents_page')
        self._assert_top_stack_contains('DocumentsPage')

    def test_route_change_to_pill_check_page(self):
        self.fake_page.go('/pill_check_page')
        self._assert_top_stack_contains('MedicineCheckPage')


class TestInitExtras(unittest.TestCase):
    def setUp(self):
        self.mod = importlib.import_module(MODULE_UNDER_TEST)


    def test_windowdrag_build_constructs_nested_controls(self):
        inner_container = MagicMock(name = 'inner_container') # inner_container -> Container(bgcolor='black')
        outer_container = MagicMock(name = 'outer_container') # outer_container -> Container(content=<WindowDragArea(...)>)

        with patch.object(self.mod, 'Container', autospec=True) as mock_container, \
             patch.object(self.mod, 'WindowDragArea', autospec=True) as mock_wda:
            mock_container.side_effect = [inner_container, outer_container]
            wda_instance = MagicMock(name='wda_instance')
            mock_wda.return_value = wda_instance

            wd = self.mod.WindowDrag()
            result = wd.build()

            self.assertIs(result, outer_container)

            first_call = mock_container.call_args_list[0]
            _, first_kwargs = first_call
            self.assertEqual(first_kwargs.get('bgcolor'), 'black')

            mock_wda.assert_called_once()
            wda_kwargs = mock_wda.call_args.kwargs
            self.assertEqual(wda_kwargs.get('height'), 10)
            self.assertIs(wda_kwargs.get('content'), inner_container)

            second_call = mock_container.call_args_list[1]
            _, second_kwargs = second_call
            self.assertIs(second_kwargs.get('content'), wda_instance)


    # Cover: app(target = App, assets_dir = 'assets')
    def test_main_invokes_flet_app(self):
        with patch.object(self.mod, 'app', autospec=True) as mock_app:
            self.mod.main()

            mock_app.assert_called_once()
            kwargs = mock_app.call_args.kwargs

            self.assertIs(kwargs.get('target'), self.mod.App)
            self.assertEqual(kwargs.get('assets_dir'), 'assets')