from flet import *
from utils.traits import *
from ui.gui.components.navigation import NavigationBar
from ui.gui.components.page_header import PageHeader
from service.notifications import NotificationService

class MedicineCheckPage(UserControl):
    
    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)

        # self.validator = Validator()

        self.token = ''
        self.user_uid = ''


        # Button to search for risks
        self.btn_search_risks = ElevatedButton(
            content = Text('Search for risks', size = 14, color = Colors.WHITE),
            height = txf_height,
            width = btn_width,
            bgcolor = Dark_bgcolor,
            style = ButtonStyle(shape = RoundedRectangleBorder(radius=10)),
            on_click = lambda _: self.search_risks_btn()
        )

    
    def build(self):
        page_header = PageHeader(current_page = None)
        
        self.token = self.page.session.get('token')
        self.user_uid = self.page.session.get('uid')

        # Check the timer to start notification service only once
        if self.token and not self.page.session.get('reminders_started'):
            notif_service = NotificationService(self.page, self.token, page_header = page_header)
            self.page.overlay.append(notif_service)


        medicine_check_content = Container(
            content = Column(
                spacing = 4,
                controls = [
                    page_header,
                    Row(alignment = MainAxisAlignment.CENTER,
                        controls = [Text('Medication Safety Check', weight = FontWeight.BOLD, size = 16)]
                    ),
                    Container(
                        expand = True,
                        padding = padding.only(top = 10, bottom = 20),
                        content = Column(
                            spacing = 10,
                            controls = [
                                # row_user_name,
                                # row_user_surname,
                                # row_user_email,
                            ]
                        )
                    ),
                    Container(
                        margin = padding.only(bottom = 15, top = 10),
                        content = self.btn_search_risks
                    )
                ]
            )
        )

        # Properties of Medicines check page: basic and animation
        self.medicine_check = Row(
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
                content = medicine_check_content
            )]
        )
        
        page_header.current_page = self.medicine_check
        navigation = NavigationBar(current_page = self.medicine_check)

        # Combine Navigation + Medicines check page
        self.content = Container(
            width = base_width, 
            height = base_height, 
            bgcolor = Light_bgcolor,
            border_radius = b_radius,
            expand = True,
            content = Stack(
                controls = [navigation, self.medicine_check]
            )
        )

        return self.content
    

    # Open navigation moving the medicine check to the right
    def shrink(self, e):
        self.settings.controls[0].width = 70
        self.settings.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        self.settings.controls[0].border_radius = border_radius.only(top_left=35, top_right=0, bottom_left=35, bottom_right=0)
        self.settings.update()


    # 
    def search_risks_btn():
        pass