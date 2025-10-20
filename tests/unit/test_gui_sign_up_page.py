import pytest
from types import SimpleNamespace
from unittest.mock import patch
from artefact.ui.gui.sign_up_page import SignUpPage

# Stubs / mocks to avoid raising the real Flet Page
class SessionMock:
    def __init__(self):
        self._store = {}
    def get(self, key, default=None):
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
    def __init__(self, value = "", is_password = False):
        self.value = value
        self.password = is_password
        self.border_color = None
        self.updated = False
    def update(self):
        self.updated = True

class TextStub:
    def __init__(self, value = ""):
        self.value = value
        self.updated = False
    def update(self):
        self.updated = True

# Return a new mock Page object for each test
@pytest.fixture
def page():
    return PageMock()

# Preparing 'fake' sign up page
@pytest.fixture
def sp(page, monkeypatch):
    s = SignUpPage()
    s.page = page
    s.view_passw = TextStub("View")
    s.password = TextFieldStub(value = "", is_password = True)
    return s

#  Tests
def test_build_sets_email_from_session(sp, page, monkeypatch):
    page.session.set("email", "newuser@example.com") # we simulate the path from FirstPage -> SignUpPage

    sp.email = TextFieldStub(value = "")
    sp.name = TextFieldStub(value = "")
    sp.surname = TextFieldStub(value = "")
    root = sp.build()

    assert sp.email.value == "newuser@example.com"
    assert root is sp.content and sp.content is not None

# 
def test_create_txtField_returns_configured_textfield(page):
    s = SignUpPage()
    s.page = page
    tf = s.create_txtField("Email")

    assert getattr(tf, "hint_text", None) == "Email"
    assert getattr(tf, "text_align", None) is not None


def test_show_hide_passw_toggles_and_updates(sp):
    sp.password = TextFieldStub(value = "", is_password = True) # password is hidden
    sp.view_passw = TextStub("View")

    sp.show_hide_passw(e = None)
    assert sp.password.password is False
    assert sp.view_passw.value == "Hide"
    assert sp.password.updated is True and sp.view_passw.updated is True

    sp.password.updated = False
    sp.view_passw.updated = False
    sp.show_hide_passw(e=None)
    assert sp.password.password is True
    assert sp.view_passw.value == "View"
    assert sp.password.updated is True and sp.view_passw.updated is True

# All validators return False
def test_signup_all_invalid_sets_borders_and_no_navigation(sp, monkeypatch, page):
    sp.validator = SimpleNamespace(
        name_correctness=lambda _: False,
        surname_correctness=lambda _: False,
        email_correctness=lambda _: False,
        password_correctness=lambda _: False,
    )

    sp.name = TextFieldStub(value = "")
    sp.surname = TextFieldStub(value = "")
    sp.email = TextFieldStub(value = "")
    sp.password = TextFieldStub(value = "", is_password = True)

    sp.signup(e = None)

    for fld in (sp.name, sp.surname, sp.email, sp.password):
        assert fld.border_color == sp.error_border
        assert fld.updated is True

    assert page.last_route is None

# All validators return True
def test_signup_valid_invokes_create_user_and_navigates(sp, monkeypatch, page):
    sp.validator = SimpleNamespace(
        name_correctness=lambda _: True,
        surname_correctness=lambda _: True,
        email_correctness=lambda _: True,
        password_correctness=lambda _: True,
    )

    sp.name = TextFieldStub(value = "Name")
    sp.surname = TextFieldStub(value = "Surname")
    sp.email = TextFieldStub(value = "mail@example.com")
    sp.password = TextFieldStub(value = "StrongPwd123", is_password = True)

    with patch("artefact.ui.gui.sign_up_page.create_user") as mock_create:
        sp.signup(e = None)

    # Check that we called create_user with the correct arguments
    mock_create.assert_called_once_with("Name", "Surname", "mail@example.com", "StrongPwd123")
    assert page.last_route == "/login_page"


def test_back_icon_navigates_to_first_page(sp, page):
    sp.email = TextFieldStub(value = "")
    sp.name = TextFieldStub(value = "")
    sp.surname = TextFieldStub(value = "")
    sp.build()

    # Get the Stack from the root self.content
    stack = getattr(sp.content, "content", None)
    assert stack is not None and hasattr(stack, "controls")

    # The second container contains a Column with a header and content
    containers = [c for c in stack.controls if getattr(c, "__class__", None).__name__ == "Container"]
    assert len(containers) >= 2
    main_col_container = containers[1]
    column = getattr(main_col_container, "content", None)
    assert column is not None and hasattr(column, "controls")

    back_container = None
    for ctrl in column.controls:
        if getattr(ctrl, "__class__", None).__name__ == "Container" and hasattr(ctrl, "content"):
            icon_btn = getattr(ctrl, "content", None)
            handler = getattr(icon_btn, "on_click", None) if icon_btn else None
            if handler:
                back_container = icon_btn
                break

    assert back_container is not None # Back IconButton is found

    back_container.on_click(SimpleNamespace())
    assert page.last_route == "/first_page"