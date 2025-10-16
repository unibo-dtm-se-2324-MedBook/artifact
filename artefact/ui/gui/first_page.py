from flet import *
from artefact.utils.traits import *
from artefact.utils.validation import Validator
from artefact.service.authentication import check_email

class FirstPage(Container):

    def __init__(self):
        super().__init__()
        self.expand = True         
        self.offset = transform.Offset(0,0,)

        self.validator = Validator()
        self.error_border = 'red'

        self.email = None
        self.first_content = None
        self.content = None

    def build(self):
        self.email = TextField(
            hint_text = 'Email',
            hint_style = TextStyle(size = 12, color = input_hint_color),
            text_style = TextStyle(size = 12, color = input_hint_color))
        
        self.first_content = Column(controls = [
            Row(alignment='center', controls = [Text(value= 'MedBook', weight='bold',size = 20, color='white')]),
            Text(value= 'Health in a convenient format', weight='bold', size = 12, color='white'),
            Container(height = 3),
            Container(
                height=txf_height,
                bgcolor='white',
                border_radius=10,
                content=self.email
            ),
            Container(
                height = txf_height,
                width = btn_width,
                bgcolor= Dark_bgcolor,
                border_radius = 10,
                alignment= alignment.center,
                content= Text(value='Continue', size = 14, color='white'),
                on_click = self.but_continue
            ),
            Container(height = 2)
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
                    padding = padding.only(top = 30, left = 10, right = 10),
                    content= Column(controls=[
                        Container(height=160),
                        Container(
                            padding = 10,
                            bgcolor = '#cc2d2b2c',
                            border_radius = 10,
                            content = self.first_content
                        )
                    ])
                ),
            ])
        )
    
    def but_continue(self, e):
        if not self.validator.email_correctness(self.email.value):
            self.email.border_color = self.error_border
            self.email.update()
        else:
            email_input = self.email.value
            email_exist = check_email(email_input)
            if email_exist:
                self.page.session.set("email", self.email.value)
                self.page.go('/login_page')
            else:
                self.page.session.set("email", self.email.value)
                self.page.go('/signup_page')
            
