from flet import *
from utils.traits import *

class LoginPage(Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)

        self.password_input = Container(
            height = txf_height,
            bgcolor= 'white',
            border_radius = 10,
            content = TextField(
                hint_text='Password',
                hint_style=TextStyle(
                    size = 12,
                    # font_family= 'poppins Regular',
                    color = input_hint_color
                ),
                text_style= TextStyle(
                    size = 12,
                    #font_family= 'poppins Regular',
                    color = input_hint_color
                ),
                # border = InputBorder.NONE,
                # content_padding= content_padding,
            )
        )
        
        self.login_content = Column(controls = [
            Row(alignment='center', controls = [Text(value= 'Login', weight='bold',size = 15, color='white'
                # font_family = 'poppins bold',
            )]),
            Column(
                spacing = 0,
                controls=[
                    Text(value= 'Anastasiia Bakhmutova', weight='bold', size = 12, color='white'
                            #  self.name + ' ' + self.surname, 
                            
                        # font_family = 'poppins Semibold',
                    ),
                    Text(value= 'bakh@mail.com', size = 12, color='white'
                            #  self.email, 
                            
                        # font_family = 'poppins light',
                    ),
                ]
            ),
            self.password_input,
            Container(
                height = txf_height,
                width = btn_width,
                bgcolor= Dark_bgcolor,
                border_radius = 10,
                alignment= alignment.center,
                content= Text(value='Continue', size = 14, color='white'
                    # font_family= 'poppins Medium',
                )
            ),
            Container(height = 3),
            Row(alignment='center', controls = [Text(value="Forgot your password?", color = 'white', size = 12)
                #font_family= 'poppins Regular',
            ]) 
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
                        Container(data = 'first_page', height = 30, content = IconButton(icon=Icons.KEYBOARD_RETURN, icon_size=17, icon_color='white', bgcolor=Dark_bgcolor, highlight_color ='#FFFAFA')),
                        Container(height=100),
                        Container(
                            padding = 10,
                            bgcolor = '#cc2d2b2c',
                            border_radius = 10,
                            content = self.login_content
                        )
                    ])
                )
            ])
        )