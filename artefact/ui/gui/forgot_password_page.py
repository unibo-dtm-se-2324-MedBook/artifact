from flet import *
from artefact.utils.traits import *
from artefact.utils.validation import Validator

class ForgPasswPage(Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)
        # self.page = page

        self.validator = Validator()
        self.error_border = 'red'
        
        self.email_input = Container(
            height = txf_height,
            bgcolor= 'white',
            border_radius = 10,
            content = TextField(
                hint_text='Email',
                hint_style=TextStyle(size = 12, color = input_hint_color),
                text_style= TextStyle(size = 12, color = input_hint_color),
            )
        )

        self.passw_content = Column(controls = [
            Row(alignment='center', controls = [Text(value= 'Forgot your password?', weight='bold',size = 15, color='white')]),
            Text(value= "Please, enter your email address below and we'l send you a link to reset your password", size = 12, color='white'),
            Container(height = 2),
            self.email_input,
            Container(
                height = txf_height,
                width = btn_width,
                bgcolor= Dark_bgcolor,
                border_radius = 10,
                alignment= alignment.center,
                content= Text(value='Reset password', size = 14, color='white'),
                on_click = lambda _: self.page.go('/login_page')
                # on_click = self.reset_password
            ),

            Container(height = 1)
        ])

        self.content = Container(
            width = base_width,
            height = base_height,
            border_radius = b_radius,
            bgcolor = "#7b9faf",
            clip_behavior = ClipBehavior.ANTI_ALIAS,
            expand = True,
            content = Stack(controls = [
                Container(
                    width = base_width,
                    height = base_height,
                    top = -70,
                    content = Image(src='artefact/assets/images/first_page_ava2.jpg', scale = 1.1)
                ),
                Container(
                    width = base_width,
                    height = base_height,
                    padding = padding.only(top = 20, left = 10, right = 10),
                    content= Column(controls=[
                        Container(
                            data = 'first_page', 
                            height = 30, 
                            content = IconButton(
                                icon=Icons.KEYBOARD_RETURN, 
                                icon_size=17, 
                                icon_color='white', 
                                bgcolor=Dark_bgcolor, 
                                highlight_color ='#FFFAFA',
                                on_click= lambda _: self.page.go('/first_page')
                            )
                        ),
                        Container(height=100),
                        Container(
                            padding = 10,
                            bgcolor = '#cc2d2b2c',
                            border_radius = 10,
                            content = self.passw_content
                        )
                    ])
                )
            ])
        )
    

    def reset_password(self, e):
        if not self.validator.email_correctness(self.email.value):
            self.email.border_color = self.error_border
            self.email.update()
        