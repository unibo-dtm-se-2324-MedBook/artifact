from flet import *
from utils.traits import *
from ui.gui.components.navigation import NavigationBar
from ui.gui.components.page_header import PageHeader
from service.notifications import NotificationService
from utils.validation import Validator
from utils.constants import SEX_OPTIONS, COUNTRY_OPTIONS

class MedicineCheckPage(UserControl):
    
    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)

        self.validator = Validator()
        self.error_border = 'red'

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

        # Results area
        self.results_caption = Text(size=12)
        
        self.results_chart_holder = Container(
            content = Text('Chart will appear here', size = general_txt_size, italic = True),
            alignment = alignment.center,
            padding = padding.all(10),
            visible = False
        )

        self.results_list = Column(
            controls = [],
            spacing = 4,
            visible = False
        )

        self.results_section = Column(
            # scroll = ScrollMode.AUTO,
            # expand = True,
            visible = False, 
            controls = [
                Divider(),
                Text('Results', size = 16, weight = 'bold'),
                self.results_caption,
                self.results_chart_holder,
                Divider(),
                Text('Top reactions', size = 14, weight = 'bold'),
                self.results_list,
            ],
        )

    
    def build(self):
        page_header = PageHeader(current_page = None)
        
        self.token = self.page.session.get('token')
        self.user_uid = self.page.session.get('uid')

        # Check the timer to start notification service only once
        if self.token and not self.page.session.get('reminders_started'):
            notif_service = NotificationService(self.page, self.token, page_header = page_header)
            self.page.overlay.append(notif_service)

        
        row_drug, self.user_drug = self._create_txtfield_info('Drug:', 'Ibuprofen')
        row_age, self.user_age = self._create_txtfield_info('Age (years):', '26')
        row_weight, self.user_weight = self._create_txtfield_info('Weight (kg):', '60')
        row_height, self.user_height = self._create_txtfield_info('Height (cm):', '176')

        row_sex, self.user_sex, self.container_user_sex = self._create_dropdown_info('Gender', SEX_OPTIONS)
        row_country, self.user_country, self.container_user_country = self._create_dropdown_info('Country', COUNTRY_OPTIONS)

        medicine_check_content = Container(
            content = Column(
                spacing = 4,
                controls = [
                    page_header,
                    ListView(
                        expand = True,
                        spacing = 4,
                        padding = padding.only(top = 0, bottom = 15, right=15),
                        controls = [
                            Row(alignment = MainAxisAlignment.CENTER,
                                controls = [Text('MedCheck', weight = FontWeight.BOLD, size = 16)]
                            ),
                            # Text('Please, enter your details', size = general_txt_size, italic = True),
                            Container(
                                expand = True,
                                padding = padding.only(top = 5, bottom = 5),
                                content = Column(
                                    spacing = 10,
                                    controls = [
                                        row_drug,
                                        row_sex,
                                        row_age, 
                                        row_weight, 
                                        row_height,
                                        row_country
                                    ]
                                )
                            ),
                            Container(
                                margin = padding.only(bottom = 15),
                                content = self.btn_search_risks
                            ),
                            # self.results_section
                        ]
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

    # Creating TextField with common design for maintaining user information
    def _create_txtfield_info(self, name_info, hint_name):
            txt_field = TextField(
                expand = True,

                hint_text = hint_name,
                hint_style = TextStyle(size = 12, color = input_hint_color),
                text_style = TextStyle(size = 12, color = input_hint_color),
                text_align = TextAlign.LEFT,

                height = txf_height,
                bgcolor = Colors.WHITE,
                border_radius = 10,
                border_color = unit_color_dark,
                border_width = 1,
                focused_border_color = unit_color_dark,
                focused_border_width = 2
            )
            
            return Row(alignment = MainAxisAlignment.START, 
                controls = [
                    Text(name_info, size = general_txt_size, weight = FontWeight),
                    txt_field
                ]
            ), txt_field
    
    # Creating Dropdown with common design for maintaining user information
    def _create_dropdown_info(self, name_info, from_list_name):
            options = [dropdown.Option(text = i['label'], key = str(i['value'])) for i in from_list_name]
            options_list = Dropdown(
                options = options,
                value = None,
                dense = True,
                expand = True,
                text_style = TextStyle(size = 12, color = input_hint_color),
                hint_style = TextStyle(size = 12, color = input_hint_color),
            )
            container_dd = Container(
                expand = True,
                height = txf_height,
                clip_behavior = ClipBehavior.HARD_EDGE,
                content = options_list
            )

            return Row(alignment = MainAxisAlignment.START, 
                controls = [
                    Text(name_info, size = general_txt_size, weight = FontWeight),
                    container_dd
                ]
            ), options_list, container_dd

    # Function for generating a query to the API database by pressing a 'Search for risks' button
    def search_risks_btn(self):
        if not self.validator.drug_name_correctness(self.user_drug.value):
            self.user_drug.border_color = self.error_border
            self.user_drug.update()
        if not self.validator.drug_name_correctness(self.user_age.value):
            self.user_age.border_color = self.error_border
            self.user_age.update()
        if not self.validator.drug_name_correctness(self.user_weight.value):
            self.user_weight.border_color = self.error_border
            self.user_weight.update()
        if not self.validator.validate_dropdown(self.user_sex):
            self.container_user_sex.border = border.all(1, self.error_border)
            self.container_user_sex.border_radius = 5
            self.container_user_sex.update()
        if not self.validator.validate_dropdown(self.user_country):
            self.container_user_country.border = border.all(1, self.error_border)
            self.container_user_country.border_radius = 5
            self.container_user_country.update()
        else:
            drug = self.user_drug.value
            age = self.user_age.value
            weight = self.user_weight.value
            height = self.user_height.value
            gender = self.user_sex.value
            country = self.user_country.value

