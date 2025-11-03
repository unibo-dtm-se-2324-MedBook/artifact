import pytest
from types import SimpleNamespace
from unittest.mock import patch
from artefact.ui.gui.components.navigation import NavigationBar


class SessionMock:
    def __init__(self):
        self._store = {}
    def get(self, key, default = None):
        return self._store.get(key, default)
    def set(self, key, value):
        self._store[key] = value
    def clear(self):
        self._store.clear()

class PageMock:
    def __init__(self):
        self.session = SessionMock()
        self.route = '/'
        self.snack_bar = None
        self.update_calls = 0
        self.last_route = None
    def go(self, route: str):
        self.last_route = route
        self.route = route
    def update(self):
        self.update_calls += 1

class CurrentPageStub:
    def __init__(self):
        self.inner = SimpleNamespace()
        self.controls = [self.inner]
        self.updated = False
    def update(self):
        self.updated = True


@pytest.fixture
def page():
    return PageMock()

@pytest.fixture
def nav(page):
    curr = CurrentPageStub()
    nb = NavigationBar(current_page = curr)
    nb.page = page
    return nb


# Tests
def test_build_returns_container(nav):
    root = nav.build()
    assert root is not None

def test_restore_resets_current_page_dimensions_and_updates(nav):
    # there are no required fields in the internal container for the call
    inner = nav.current_page.controls[0]
    assert not hasattr(inner, 'width')
    assert not hasattr(inner, 'border_radius')
    assert not hasattr(inner, 'scale')
    assert nav.current_page.updated is False

    nav.restore(e = None)
    # now we have
    assert hasattr(inner, 'width')
    assert hasattr(inner, 'border_radius')
    assert hasattr(inner, 'scale')
    assert nav.current_page.updated is True

def test_exit_with_token(nav, page, monkeypatch):
    page.session.set('token', 'Tkn123')

    # we call log_out(token)
    token_called = {'token': None}
    def fake_logout(token):
        token_called['token'] = token
    monkeypatch.setattr('artefact.ui.gui.components.navigation.log_out', fake_logout)

    nav.exit(e = None)

    assert token_called['token'] == 'Tkn123' # Right token is used
    assert page.session._store == {} # It clears the session
    assert page.last_route == '/first_page' # It navigates to '/first_page'
    assert page.snack_bar is None


def test_exit_without_token(nav, page, monkeypatch):
    class FakeText:
        def __init__(self, value): 
            self.value = value
    class FakeSnackBar:
        def __init__(self, content, open = False):
            self.content = content
            self.open = open

    monkeypatch.setattr('artefact.ui.gui.components.navigation.Text', FakeText)
    monkeypatch.setattr('artefact.ui.gui.components.navigation.SnackBar', FakeSnackBar)

    # log_out will not be called
    with patch('artefact.ui.gui.components.navigation.log_out') as mock_logout:
        nav.exit(e = None)
        mock_logout.assert_not_called()

    # Snack bar with the required text appeared
    assert page.snack_bar is not None
    assert page.snack_bar.open is True
    assert page.snack_bar.content.value == 'Something is wrong, try again'
    # Update() is called
    assert page.update_calls == 1


BUTTONS = {
    'btn_to_shedule_page': '/main_page',
    'btn_to_documents_page': '/documents_page',
    'btn_check_pill': '/pill_check_page',
    'btn_user_settings_page': '/settings_page'
}

@pytest.mark.parametrize('btn_attr,target_route', BUTTONS.items())
def test_menu_button_go_when_not_on_target(nav, page, btn_attr, target_route):
    page.route = '/some_other_route'
    btn_row = getattr(nav, btn_attr)
    text_button = btn_row.controls[0]
    text_button.on_click(SimpleNamespace())
    assert page.last_route == target_route

@pytest.mark.parametrize('btn_attr,target_route', BUTTONS.items())
def test_menu_button_restore_when_already_on_target(nav, page, btn_attr, target_route):
    page.route = target_route
    nav.current_page.updated = False

    btn_row = getattr(nav, btn_attr)
    text_button = btn_row.controls[0]
    text_button.on_click(SimpleNamespace())

    assert nav.current_page.updated is True
    assert page.last_route in (None, target_route)