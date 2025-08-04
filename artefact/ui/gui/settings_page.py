from flet import *
from utils.traits import *

class SettingsPage(UserControl):

    def __init__(self, token = None):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)