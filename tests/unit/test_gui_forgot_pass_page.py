import pytest
from types import SimpleNamespace
from artefact.ui.gui.forgot_password_page import ForgPasswPage


class SessionMock:
    def __init__(self):
        self._store = {}
    def get(self, key, default = None):
        return self._store.get(key, default)
    def set(self, key, value):
        self._store[key] = value

class PageMock:
    def __init__(self):
        self.session = SessionMock()
        self.last_route = None
        self.update_calls = 0
    def go(self, route: str):
        self.last_route = route
    def update(self):
        self.update_calls += 1

class TextFieldStub:
    def __init__(self, value = ''):
        self.value = value
        self.border_color = None
        self.updated = False
    def update(self):
        self.updated = True


@pytest.fixture
def page():
    return PageMock()

@pytest.fixture
def fakepage(page):
    passwpage = ForgPasswPage()
    passwpage.page = page
    return passwpage


# Tests
def test_build_created_content_and_email_field(fakepage):
    assert fakepage.content is not None
    assert fakepage.passw_content is not None
    assert fakepage.email_input is not None

    tf = getattr(fakepage.email_input, 'content', None)
    assert tf is not None # email input TextField must be in email_input.content


def test_click_reset_password_navigates_to_login(fakepage, page):
    reset_container = None

    for ctrl in getattr(fakepage.passw_content, 'controls', []): # Looking for the container with the text 'Reset password'
        if hasattr(ctrl, 'on_click') and ctrl.on_click is not None:
            inner = getattr(ctrl, 'content', None)
            if inner and hasattr(inner, 'value') and inner.value == 'Reset password':
                reset_container = ctrl
                break

    assert reset_container is not None, 'Reset button container not found'
    reset_container.on_click(SimpleNamespace())
    assert page.last_route == '/login_page' # Navigate to login_page


def test_click_back_icon_navigates_to_first_page(fakepage, page):
    # Extracting Stack from the root content
    stack = getattr(fakepage.content, 'content', None)
    assert stack is not None and hasattr(stack, 'controls'), 'Stack not found'

    # Find the second container with Column
    containers = [c for c in stack.controls if getattr(c, '__class__', None).__name__ == 'Container']
    assert len(containers) >= 2, 'Expected image container and main column container'

    main_column_container = containers[1]
    column = getattr(main_column_container, 'content', None)
    assert column is not None and hasattr(column, 'controls'), 'Main Column not found'

    # Looking for the container with IconButton inside
    back_container = None
    icon_btn = None
    for ctrl in column.controls:
        if getattr(ctrl, '__class__', None).__name__ == 'Container' and hasattr(ctrl, 'content'):
            inner = ctrl.content
            if getattr(inner, '__class__', None).__name__ == 'IconButton':
                back_container = ctrl
                icon_btn = inner
                break

    assert icon_btn is not None # IconButton for back action was found

    handler = getattr(back_container, 'on_click', None) or getattr(icon_btn, 'on_click', None)
    assert handler is not None, 'on_click handler not found on back icon'

    handler(SimpleNamespace())
    assert page.last_route == '/first_page'


def test_reset_password_invalid_email_sets_error(fakepage):
    fakepage.validator = SimpleNamespace(email_correctness = lambda _: False)

    fakepage.email = TextFieldStub(value = 'wrong@')
    fakepage.reset_password(e = None)

    assert fakepage.email.border_color == fakepage.error_border
    assert fakepage.email.updated is True