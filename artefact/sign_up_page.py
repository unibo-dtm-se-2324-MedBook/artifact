from flet import *
from utils.traits import *

class SignUpPage(Container):

    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)
        
        self.name = self.create_txtField('Name')
        self.surname = self.create_txtField('Surname')
        self.email =  self.create_txtField('Email') 
        
        self.view_passw = Text(value= 'View', color = Dark_bgcolor)
        self.password = TextField(
            password = True,
            suffix=Container(
                on_click= self.show_hide_passw,
                content= self.view_passw),
            hint_text = 'Password',
            hint_style = TextStyle(size = 12, color = input_hint_color),
            text_style = TextStyle( size = 12, color = input_hint_color))

        self.sighup_content = Column(controls = [
            Row(alignment='center', controls = [Text(value= 'Sigh Up', weight='bold',size = 12, color='white')]),
            Column(
                spacing = 0,
                controls=[
                    Text(value= "Seems you don't have account.", size = 12, color='white'
                            #  self.name + ' ' + self.surname,     
                    ),
                    Text(value= "Let's get you signed up!", size = 12, color='white'
                            #  self.email,     
                    ),
                ]
            ),

            Container(
                height=txf_height,
                bgcolor='white',
                border_radius=10,
                content=self.name
            ),
            Container(
                height=txf_height,
                bgcolor='white',
                border_radius=10,
                content=self.surname
            ),
            Container(
                height=txf_height,
                bgcolor='white',
                border_radius=10,
                content=self.email
            ),
            Container(
                height=txf_height,
                bgcolor='white',
                border_radius=10,
                content=self.password
            ),

            Column(
                spacing = 0,
                controls=[
                    Text(value= "By clicking button below,", size = 12, color='white'),
                    Row(
                        spacing = 0,
                        controls = [
                            Text(value= "I agree to", size = 12, color='white'
                                    #  self.email,     
                            ),
                            Text(value= " Terms of Privacy Policy", size = 12, color='#FFFAFA', italic= True 
                                    #  self.email,     
                            )
                        ]
                    )
                ]
            ),

            Container(
                height = txf_height,
                width = btn_width,
                bgcolor= Dark_bgcolor,
                border_radius = 10,
                alignment= alignment.center,
                content= Text(value='Agree and Continue', size = 14, color='white')
            ),
            Container(height = 10)
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
                        Container(padding = 10, bgcolor = '#cc2d2b2c', border_radius = 10, content = self.sighup_content)
                    ])
                )
            ])
        )

    def create_txtField(self, hint_name):
            return TextField(
                hint_text = hint_name,
                hint_style = TextStyle(size = 12, color = input_hint_color),
                text_style = TextStyle(size = 12, color = input_hint_color))

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