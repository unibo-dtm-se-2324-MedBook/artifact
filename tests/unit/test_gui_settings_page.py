import pytest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
from artefact.ui.gui.settings_page import SettingsPage

# Stubs / mocks to avoid raising the real Flet Page
class SessionMock:
    def __init__(self):
        self._store = {}
    def get(self, key, default=None):
        return self._store.get(key, default)
    def set(self, key, val):
        self._store[key] = val

class PageMock:
    def __init__(self):
        self.session = SessionMock()
        self.overlay = []
        self.dialog = None
        self.update_calls = 0
    def update(self):
        self.update_calls += 1

class FieldStub:
    def __init__(self, value=''):
        self.value = value
        self.border_color = None
        self.updated = False
    def update(self):
        self.updated = True



@pytest.fixture
def page():
    return PageMock()

@pytest.fixture
def sp(page):
    s = SettingsPage()
    s.page = page
    return s


# Tests
def test_build_and_start_notifications(sp, page, monkeypatch):
    page.session.set('token', 'Token123')
    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.firebase_auth.verify_id_token',
        lambda read_token: {'uid': 'User123'}
    )
    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.firebase_auth.get_user',
        lambda read_uid: SimpleNamespace(display_name = 'Lina_Smith', email = 'user@example.com')
    )
    
    # PageHeader and NavigationBar
    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.PageHeader',
        lambda current_page = None: SimpleNamespace(current_page = current_page)
    )
    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.NavigationBar',
        lambda current_page = None: SimpleNamespace(current_page = current_page)
    )
    
    # NotificationService
    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.NotificationService',
        lambda page, token, page_header = None: 'NOTIF_SVC'
    )

    sp.build()

    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.firebase_auth.get_user',
        lambda uid: SimpleNamespace(display_name='Lina', email='user@example.com')
    )
    sp.load_user_info()

    assert sp.user_name == 'Lina'
    assert sp.user_surname == ''
    assert sp.text_user_name.value == 'Lina'
    assert sp.text_user_surname.value == ''
    assert sp.text_user_email.value == 'user@example.com'


def test_build_does_not_start_notifications(sp, page, monkeypatch):
    page.session.set('token', 'Token1234')
    page.session.set('reminders_started', True)

    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.firebase_auth.verify_id_token',
        lambda read_token: {'uid': 'Uid1234'}
    )
    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.firebase_auth.get_user',
        lambda read_uid: SimpleNamespace(display_name = 'Anna_Kara', email='user2@gmail.com')
    )
    
    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.PageHeader',
        lambda current_page = None: SimpleNamespace(current_page = current_page)
    )
    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.NavigationBar',
        lambda current_page = None: SimpleNamespace(current_page = current_page)
    )
    
    # NotificationService
    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.NotificationService',
        lambda *a, **k: 'SHOULD_NOT_APPEAR'
    )

    sp.build()
    assert page.overlay == []  # no service


# shrink()
def test_shrink_changes_dimensions_and_updates(sp, monkeypatch):
    inner = SimpleNamespace()
    updated = {'called': False}
    def fake_update():
        updated['called'] = True
    sp.settings = SimpleNamespace(controls = [inner], update = fake_update)

    sp.shrink(e = None)

    assert getattr(inner, 'width', None) == 70
    assert hasattr(inner, 'scale')
    assert hasattr(inner, 'border_radius')
    assert updated['called'] is True


def test_edit_info_btn_opens_dialog_and_prefills_hints(sp, page):
    sp.user_name = 'John'
    sp.user_surname = 'Smith'
    sp.user_email = 'smith@gmail.com'

    sp.edit_info_btn()

    assert page.dialog is not None
    assert getattr(page.dialog, 'open', False) is True
    assert page.update_calls >= 1

    assert getattr(sp.name_field, 'hint_text', None) == 'John'
    assert getattr(sp.surname_field, 'hint_text', None) == 'Smith'
    assert getattr(sp.email_field, 'hint_text', None) == 'smith@gmail.com'


def test_close_dialog_closes_and_updates(sp, page):
    page.dialog = SimpleNamespace(open = True)
    sp._close_dialog()
    assert page.dialog.open is False
    assert page.update_calls == 1


def test_save_changes_with_invalid_fields_marks_errors(sp, monkeypatch):
    sp.name_field = FieldStub(value = 'bad_name')
    sp.surname_field = FieldStub(value = 'bad_surname')
    sp.email_field = FieldStub(value = 'bad_email')

    # The validator rejects all values
    sp.validator = SimpleNamespace(
        name_correctness = lambda _: False,
        surname_correctness = lambda _: False,
        email_correctness = lambda _: False,
    )
    sp._save_changes()

    for fld in (sp.name_field, sp.surname_field, sp.email_field):
        assert fld.border_color == 'red'
        assert fld.updated is True


def test_save_changes_success_calls_change_user_info_and_refreshes(sp, page, monkeypatch):
    sp.user_uid = 'Uid123'
    sp.user_name = 'OldName'
    sp.user_surname = 'OldSurname'
    sp.user_email = 'old@gmail.com'

    sp.name_field = FieldStub(value = '')
    sp.surname_field = FieldStub(value = 'NewSurname')
    sp.email_field = FieldStub(value = '')

    sp.validator = SimpleNamespace(
        name_correctness=lambda _: True,
        surname_correctness=lambda _: True,
        email_correctness=lambda _: True,
    )

    # External call of change_user_info
    calls = []
    def fake_change_user_info(name, surname, email, uid, page_ref):
        calls.append((name, surname, email, uid, page_ref))

    monkeypatch.setattr(
        'artefact.ui.gui.settings_page.change_user_info',
        fake_change_user_info
    )

    # Replace load_user_info, _close_dialog, update with counters
    load_calls = {'n': 0}
    close_calls = {'n': 0}
    update_calls = {'n': 0}
    sp.load_user_info = lambda: load_calls.__setitem__('n', load_calls['n'] + 1)
    sp._close_dialog = lambda: close_calls.__setitem__('n', close_calls['n'] + 1)
    sp.update = lambda: update_calls.__setitem__('n', update_calls['n'] + 1)

    # # Surname string is not empty
    sp._save_changes()
    assert calls[0] == ('OldName', 'NewSurname', 'old@gmail.com', 'Uid123', page)

    # Surname string is empty
    sp.surname_field.value = ''
    sp._save_changes()
    assert calls[1] == ('OldName', 'OldSurname', 'old@gmail.com', 'Uid123', page)

    assert load_calls['n'] == 2
    assert close_calls['n'] == 2
    assert update_calls['n'] == 2
