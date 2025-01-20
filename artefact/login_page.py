from flet import *
from utils.traits import *

class LoginPage(Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)
