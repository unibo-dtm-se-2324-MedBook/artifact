from flet import *
from utils.traits import *
from ui.gui.navigation import NavigationBar

class SettingsPage(UserControl):
    
    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)

        self.token = ''
        self.user_uid = ''

        # Button to edit user info
        self.btn_edit_info = ElevatedButton(
            content = Text('Edit', size = 14, color = Colors.WHITE),
            height = txf_height,
            width = btn_width,
            bgcolor = Dark_bgcolor,
            style = ButtonStyle(shape = RoundedRectangleBorder(radius=10)),
            # on_click = self.show_form
        )

    def build(self):
        self.token = self.page.session.get('token')
        # self.uid = self.page.session.get('uid')
        
        settings_content = Container(
            content = Column(
                spacing = 4,
                controls = [
                    Row(
                        alignment = 'spaceBetween',
                        controls = [
                            Container(
                                on_click= self.shrink,
                                content = Icon(icons.MENU, Colors.BLACK)
                            ),
                            Text(value = 'MedBook',  color = 'black'),
                            # self.btn_notif
                        ]
                    ),
                    Divider(),
                    Container(
                        margin = padding.only(bottom = 20, top = 10),
                        content = self.btn_edit_info
                    )
                ]
            )
        )

        # Properties of Schedule page: basic and animation
        self.settings = Row(
            alignment='end',
            controls=[Container(
                width = base_width, 
                height = base_height, 
                bgcolor = Light_bgcolor,
                border_radius = b_radius,
                animate = animation.Animation(600, AnimationCurve.DECELERATE),
                animate_scale = animation.Animation(400, curve = 'decelerate'),
                padding = padding.only(top = 15, left = 20, right = 40, bottom = 15), #5
                clip_behavior = ClipBehavior.ANTI_ALIAS,
                content = settings_content
            )]
        )
        # Import navigation
        navigation = NavigationBar(current_page = self.settings)

        # Combine Navigation + Schedule
        self.content = Container(
            width = base_width, 
            height = base_height, 
            bgcolor = Light_bgcolor,
            border_radius = b_radius,
            expand = True,
            content = Stack(
                controls = [navigation, self.settings]
            )
        )

        return self.content

    # Open navigation moving the settings to the right
    def shrink(self, e):
        self.settings.controls[0].width = 70
        self.settings.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        self.settings.controls[0].border_radius = border_radius.only(top_left=35, top_right=0, bottom_left=35, bottom_right=0)
        self.settings.update()