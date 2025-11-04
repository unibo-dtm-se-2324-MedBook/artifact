import pytest
from types import SimpleNamespace
from artefact.ui.gui.components.page_header import PageHeader

class PageMock:
    def __init__(self):
        self.dialog = None
        self.update_calls = 0
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
def header(page):
    curr = CurrentPageStub()
    h = PageHeader(current_page=curr)
    h.page = page
    return h


# Tests
def test_build_returns_column(header):
    root = header.build()
    assert root is not None
    assert hasattr(root, 'controls')


def test_shrink_changes_current_page_dimensions_and_updates(header):
    inner = header.current_page.controls[0]
    # there are no required fields in the internal container for the call
    assert not hasattr(inner, 'width')
    assert not hasattr(inner, 'scale')
    assert not hasattr(inner, 'border_radius')
    assert header.current_page.updated is False

    header.shrink(e = None)

    # now we have
    assert hasattr(inner, 'width')
    assert hasattr(inner, 'scale')
    assert hasattr(inner, 'border_radius')
    assert header.current_page.updated is True

def test_btn_menu_on_click_triggers_shrink(header):
    header.current_page.updated = False
    header.btn_menu.on_click(SimpleNamespace())
    assert header.current_page.updated is True

def test_open_notifications_dialog_sets_dialog_marks_read_and_updates(header, page, monkeypatch):
    header.notifications = [
        {'date': '03 Nov', 'medicine_name': 'Pill A'},
        {'date': '03 Nov', 'medicine_name': 'Pill B'},
    ]

    # Count the calls to self.update() by replacing the instance method
    update_calls = {'n': 0}
    header.update = lambda: update_calls.__setitem__('n', update_calls['n'] + 1)

    header.open_notifications_dialog()

    assert header.unread_notif is False
    assert getattr(header.btn_notification, 'icon_color', None) is not None

    assert page.dialog is not None
    assert getattr(page.dialog, 'open', False) is True

    assert page.update_calls == 1
    assert update_calls['n'] == 1

def test_open_notifications_dialog_works_with_empty_list(header, page):
    header.notifications = [] # no notifications
    header.update = lambda: None

    header.open_notifications_dialog()

    assert page.dialog is not None
    assert page.dialog.open is True

def test_close_notif_dialog_closes_and_updates(header, page):
    page.dialog = SimpleNamespace(open = True)
    header.close_notif_dialog()

    assert page.dialog.open is False
    assert page.update_calls == 1

def test_set_unread_true_and_false_update_called(header):
    update_calls = {'n': 0}
    header.update = lambda: update_calls.__setitem__('n', update_calls['n'] + 1)

    # unread = True
    header.set_unread(True)
    assert header.unread_notif is True
    assert getattr(header.btn_notification, 'icon_color', None) is not None
    assert update_calls['n'] == 1

    # unread = False
    header.set_unread(False)
    assert header.unread_notif is False
    assert getattr(header.btn_notification, 'icon_color', None) is not None
    assert update_calls['n'] == 2

def test_btn_notification_on_click_opens_dialog(header, page):
    header.update = lambda: None
    header.btn_notification.on_click(SimpleNamespace())
    assert page.dialog is not None
    assert getattr(page.dialog, 'open', False) is True