from flet import *
from utils.traits import *
from ui.gui.components.navigation import NavigationBar
from ui.gui.components.page_header import PageHeader
from service.notifications import NotificationService
from service import documents_page_service

class DocumentsPage(UserControl):
    
    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)

        self.token = ''
        self.user_uid = ''

        self.doc_grid = GridView(
            expand = True,
            runs_count = 2,
            max_extent = 260,
            child_aspect_ratio = 1.0,
            spacing = 10,
            run_spacing = 10
        )

        # Button to upload new file
        self.file_picker = FilePicker(on_result = self.on_file_picked)
        self.btn_add_file = ElevatedButton(
            content = Text('Add new file', size = general_txt_size, color = Colors.WHITE),
            height = txf_height,
            width = btn_width,
            bgcolor = Dark_bgcolor,
            style = ButtonStyle(shape = RoundedRectangleBorder(radius = 10)),
            # on_click = lambda _: self.upload_file()
            on_click = lambda _: self.file_picker.pick_files(
                allow_multiple = False,
                allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
            )
        )


    def build(self):
        self.page.overlay.append(self.file_picker)

        page_header = PageHeader(current_page = None)
        
        self.token = self.page.session.get('token')
        self.user_uid = self.page.session.get('uid')
        print('user_uid = ', self.user_uid)

        # Check the timer to start notification service only once
        if self.token and not self.page.session.get('reminders_started'):
            notif_service = NotificationService(self.page, self.token, page_header = page_header)
            self.page.overlay.append(notif_service)
        

        document_content = Container(
            content = Column(
                spacing = 4,
                controls = [
                    page_header,
                    Row(alignment = MainAxisAlignment.CENTER,
                        controls = [Text('Documents', weight = FontWeight.BOLD, size = 16)]
                    ),
                    Container(
                        expand = True,
                        # padding = padding.only(top = 10, bottom = 20),
                        # content = Column(
                        # spacing = 10,
                        # controls = [
                        content = self.doc_grid
                    ),
                    Container(
                        margin = padding.only(bottom = 15, top = 10), # b 20
                        content = self.btn_add_file
                    )
                ]
            )
        )

        # Properties of Documents page: basic and animation
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
                content = document_content
            )]
        )

        page_header.current_page = self.settings
        navigation = NavigationBar(current_page = self.settings)

        # Combine Navigation + Documents page
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
        
        self.load_user_documents()
        return self.content

    # Open navigation moving the documents page to the right
    def shrink(self, e):
        self.settings.controls[0].width = 70
        self.settings.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        self.settings.controls[0].border_radius = border_radius.only(top_left=35, top_right=0, bottom_left=35, bottom_right=0)
        self.settings.update()


    def on_file_picked(self, e: FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            documents_page_service.upload_user_document(self.user_uid, self.token, file_path)
            self._load_user_documents()

    def _load_user_documents(self):
        pass