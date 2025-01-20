from flet import *
from utils.traits import *

class FirstPage(Container):
    def __init__(self):
        super().__init__()
        self.expand = True # атрибут expand может управлять тем, как элемент будет расширяться или сжиматься в пределах контейнера. в библиотеке Flet атрибут expand может использоваться, чтобы заставить элемент (например, кнопку или текстовое поле) занимать все доступное пространство в родительском контейнере.
        self.offset = transform.Offset(0,0,) # для Flet Offset может быть использован для представления смещения в двумерной системе координат
        
        self.email_input = Container(
            height = txf_height,
            bgcolor= 'white',
            border_radius = 10,
            content = TextField(
                hint_text='Email',
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
        
        self.first_content = Column(controls = [
            Row(alignment='center', controls = [Text(value= 'MedBook', weight='bold',size = 20, color='white'
                # font_family = 'poppins bold',
            )]),
            Text(value= 'Health in a convenient format', weight='bold', size = 12, color='white'),
            Container(height = 10),
            self.email_input,
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
                    padding = padding.only(top = 30, left = 10, right = 10),
                    content= Column(controls=[
                        Container(height=130),
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

