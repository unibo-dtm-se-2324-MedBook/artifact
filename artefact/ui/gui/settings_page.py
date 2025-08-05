from flet import *
from utils.traits import *
from ui.gui.components.navigation import NavigationBar
from ui.gui.components.page_header import PageHeader
from service.notifications import NotificationService
from firebase_admin import auth as firebase_auth

class SettingsPage(UserControl):
    
    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)

        self.token = ''
        self.user_uid = ''
        self.user_name = ''
        self.user_surname = ''
        self.email = ''
        self.password = ''

        # Button to edit user info
        self.btn_edit_info = ElevatedButton(
            content = Text('Edit information', size = 14, color = Colors.WHITE),
            height = txf_height,
            width = btn_width,
            bgcolor = Dark_bgcolor,
            style = ButtonStyle(shape = RoundedRectangleBorder(radius=10)),
            # on_click = self.show_form
        )

    def build(self):
        page_header = PageHeader(current_page = None)
        
        self.token = self.page.session.get('token')
        decoded_token = firebase_auth.verify_id_token(self.token)
        # self.user_uid = self.page.session.get('uid')
        
        # Check the timer to start notification service only once
        if self.token and not self.page.session.get('reminders_started'):
            notif_service = NotificationService(self.page, self.token, page_header = page_header)
            self.page.overlay.append(notif_service)


        full_name = decoded_token.get('name', '')
        if '_' in full_name:
            self.user_name, self.user_surnname = full_name.split('_', 1)
        else:
            self.user_name, self.user_surnname = full_name, ''
        self.email = self.page.session.get('email')
        # self.password = ''

        def create_row_info(name_info, info_value):
            return Row(alignment = MainAxisAlignment.START, 
                controls = [
                    Text(name_info, size = general_txt_size, weight = FontWeight),
                    Container(
                        width = 100,
                        padding = padding.all(5),
                        border_radius = 10,
                        border = border.all(color = unit_color_dark, width = 1),
                        content = Text(info_value, size = 12)
                    )
                ]
            )
        row_user_name = create_row_info('Name:', self.user_name)
        row_user_surname = create_row_info('Last name:', self.user_surname)
        row_user_email = create_row_info('Email:', self.email)
        # row_user_password = create_row_info('Password:', self.password)

        settings_content = Container(
            content = Column(
                spacing = 4,
                controls = [
                    page_header,
                    Row(alignment = MainAxisAlignment.CENTER,
                        controls = [Text('Personal info', weight = FontWeight.BOLD, size = 16)]
                    ),
                    Container(
                        expand = True,
                        padding = padding.only(top = 10, bottom = 20),
                        content = Column(
                            spacing = 5,
                            controls = [
                                row_user_name,
                                row_user_surname,
                                row_user_email,
                                # row_user_password,
                            ]
                        )
                    ),
                    # self.btn_edit_info
                    Container(
                        margin = padding.only(bottom = 15, top = 10), # b 20
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
                padding = padding.only(top = 15, left = 20, right = 40, bottom = 5), # 15
                clip_behavior = ClipBehavior.ANTI_ALIAS,
                content = settings_content
            )]
        )
        
        page_header.current_page = self.settings
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