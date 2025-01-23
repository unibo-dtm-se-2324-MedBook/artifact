from flet import *
from utils.traits import *

class LoginPage(Container):
    def __init__(self, page:Page):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)
        self.page = page

        self.view_passw = Text(value= 'View', color = Dark_bgcolor)
        self.password = TextField(
            password = True,
            suffix=Container(
                on_click= self.show_hide_passw,
                content= self.view_passw),
            hint_text = 'Password',
            hint_style = TextStyle(size = 12, color = input_hint_color),
            text_style = TextStyle( size = 12, color = input_hint_color))
        
        self.login_content = Column(controls = [
            Row(alignment='center', controls = [Text(value= 'Login', weight='bold',size = 15, color='white')]),
            Column(
                spacing = 0,
                controls=[
                    Text(value= 'Anastasiia Bakhmutova', weight='bold', size = 12, color='white'
                            #  self.name + ' ' + self.surname, 
                    ),
                    Text(value= 'bakh@mail.com', size = 12, color='white'
                            #  self.email, 
                    ),
                ]
            ),
            Container(
                height=txf_height,
                bgcolor='white',
                border_radius=10,
                content=self.password
            ),
            
            Container(
                height = txf_height,
                width = btn_width,
                bgcolor= Dark_bgcolor,
                border_radius = 10,
                alignment= alignment.center,
                content= Text(value='Continue', size = 14, color='white')
            ),
            Container(height = 3),
            Container(
                content = Row(alignment='center', controls = [Text(value="Forgot your password?", color = 'white', size = 12)]),
                on_click= lambda _: self.page.go('/forgot_passw')
            )
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

    def show_hide_passw(self, e):
        status = self.password.password
        if status == True:
            self.password.password = False
            self.view_passw.value = 'Hide'
        else: 
            self.password.password = True
            self.view_passw.value = 'View'
        self.password.update()
        self.view_passw.update()

    