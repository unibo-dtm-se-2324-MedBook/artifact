from flet import *
from utils.traits import *
from service.authentication import log_out
import calendar
from datetime import datetime

class MainPage(Container):

    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)
        
        self.token = ''

        self.today = datetime.today()
        self.year = self.today.year
        self.month = self.today.month

    def set_token(self, token):
        self.token = token
        self.update()

    def build(self):
        # days_card = Row(scroll = 'auto')
        # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        # for day in days:
        #     days_card.controls.append(
        #         Container(
        #             bgcolor = '#3F888F',
        #             width = 80,
        #             height = 40,
        #             border_radius = 15,
        #             padding = 10,
        #             content = Text(day, color = '#FFFAFA', text_align = 'center')
        #         )
        #     )

        # Creating a visual for navigation
        self.navig = Container(
            bgcolor = Dark_bgcolor,
            border_radius= b_radius,
            padding = padding.only(top=10, left=8, bottom=5),
            content = Column(controls = [
                Row(spacing= 0,
                    controls=[IconButton(icon=Icons.KEYBOARD_RETURN, icon_color='white', on_click=self.restore, icon_size=20, highlight_color ='#FFFAFA')],
                ),
                Container(
                    padding = padding.only(left=15),
                    content= Text("Your portable\nmedical card", size=15, weight="bold", color='white')
                ),

                Container(height=10),
                Row(controls=[
                    TextButton(
                        on_click = self.restore,
                        content = Row(controls = [
                            Icon(icons.SCHEDULE, color="white60"),
                            Text(value="Schedule",
                                size=15,
                                weight=FontWeight.W_300,
                                color="white",
                                font_family="poppins"
                            )
                        ])
                    )
                ]),

                Container(height=5),
                Row(controls=[
                    TextButton(
                        # on_click= self.go_to_page,
                        content = Row(controls = [
                            Icon(icons.EDIT_DOCUMENT, color="white60"),
                            Text("Documents",
                                size=15,
                                weight=FontWeight.W_300,
                                color="white",
                                font_family="poppins"
                            )
                        ])
                    )
                ]),                            

                Container(height=5),
                Row(controls=[
                    TextButton(
                        # on_click= self.go_to_page,
                        content = Row(controls = [
                            Icon(icons.DOCUMENT_SCANNER, color="white60"),
                            Text("Check",
                                size=15,
                                weight=FontWeight.W_300,
                                color="white",
                                font_family="poppins"
                            )
                        ])
                    )
                ]), 

                Container(height=5),
                Row(controls=[
                    TextButton(
                        # on_click= self.go_to_page,
                        content = Row(controls = [
                            Icon(icons.PERSON_OUTLINE, color="white60"),
                            Text(value="Personal info",
                                size=15,
                                weight=FontWeight.W_300,
                                color="white",
                                font_family="poppins"
                            )
                        ])
                    )
                ]),
                
                Container(height=20),
                Row(controls=[
                    TextButton(
                        content = Row(controls = [
                            Icon(icons.EXIT_TO_APP, color="white60"),
                            Text("Exit",
                                size=15,
                                weight=FontWeight.W_300,
                                color="white",
                                font_family="poppins"
                            ) 
                        ]),
                        on_click = self.exit
                        # on_click= lambda _: self.page.go('/first_page'),
                    )
                ])
            ])
        )

        # Creating a visual for Schedule page
        ## Calendar
        self.prev_btn = IconButton(icons.ARROW_BACK, icon_color = unit_color_dark, on_click = self.prev_month)
        self.month_header = Text()
        self.next_btn = IconButton(icons.ARROW_FORWARD, icon_color = unit_color_dark, on_click = self.next_month)
        self.grid = GridView(max_extent = 80, spacing = 5, run_spacing = 5)

        ## Area to add new pill
        self.btn_add = ElevatedButton(
            content = Text('Add the pill', size = 14, color = Colors.WHITE),
            height = txf_height,
            width = btn_width,
            bgcolor = Dark_bgcolor,
            style = ButtonStyle(shape = RoundedRectangleBorder(radius=10)),
            on_click = self.show_form
        )
        self.form = None

        ## Combine
        schedule_content = Container(
            content = Column(
                controls=[
                    Row(
                        alignment = 'spaceBetween',
                        controls=[
                            Container(
                                on_click= self.shrink,
                                content = Icon(icons.MENU, Colors.BLACK)
                            ),
                            Text(value = 'MedBook', weight = FontWeight.BOLD, color = 'black'),
                            Container(
                                # padding= padding.only(right = 16), 
                                content = Icon(name = icons.NOTIFICATIONS_OUTLINED, color = Colors.BLACK)
                            )
                        ]
                    ),
                    Row(alignment = MainAxisAlignment.CENTER,
                        controls = [Text('Schedule', size = 16)]),
                    Row(alignment = 'spaceBetween', #alignment = MainAxisAlignment.CENTER
                        controls = [self.prev_btn, self.month_header, self.next_btn],
                    ),
                    self.grid,
                    Divider(),
                    self.btn_add
                ]
            )
        )
        # self.create_calendar()

        # Schedule page with animation characteristics
        self.schedule = Row(
            alignment='end',
            controls=[Container(
                width = base_width, 
                height = base_height, 
                bgcolor = Light_bgcolor,
                border_radius = b_radius,
                animate = animation.Animation(600, AnimationCurve.DECELERATE),
                animate_scale = animation.Animation(400, curve = 'decelerate'),
                padding = padding.only(top = 15, left = 20, right = 40, bottom = 5),
                clip_behavior = ClipBehavior.ANTI_ALIAS,
                content = schedule_content
                # content = Column(controls = [schedule_content])
            )]
        )

        # Whole Main page (navigation + schedule)
        self.content = Container(
            width = base_width, 
            height = base_height, 
            bgcolor = Light_bgcolor,
            border_radius = b_radius,
            expand = True,
            content = Stack(
                controls = [self.navig, self.schedule]
            )
        )
    
    # Open navigation moving the schedule to the right
    def shrink(self, e):
        self.schedule.controls[0].width = 70
        self.schedule.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        self.schedule.controls[0].border_radius = border_radius.only(top_left=35, top_right=0, bottom_left=35, bottom_right=0)
        self.schedule.update()

    # Close navigation opening the schedule
    def restore(self, e):
        self.schedule.controls[0].width = base_width
        self.schedule.controls[0].border_radius = b_radius
        self.schedule.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        self.schedule.update()

    # Generate calendar
    def create_calendar(self):
        self.grid.controls.clear()
        
        self.month_header.value = f'{calendar.month_name[self.month]} {self.year}'
        first_wday, total_days = calendar.monthrange(self.year, self.month)
        for _ in range(first_wday): # empty cells before the first day
            self.grid.controls.append(Container())

        self.update()

    # Functions to go one month forward or back
    def prev_month(self, e):
        if self.month == 1:
            self.month, self.year = 12, self.year - 1
        else:
            self.month -= 1
        # self.create_calendar()

    def next_month(self, e):
        if self.month == 12:
            self.month, self.year = 1, self.year + 1
        else:
            self.month += 1
        # self.create_calendar()
    
    # Creating the form for new medicine
    def show_form(self, e):
        def create_TextField():
            return TextField(
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
        
        self.medname_field = create_TextField()
        self.qty_field = create_TextField()
        self.date_picker = DatePicker()
        # self.time_picker = TimePicker(value = self.today.time())
        self.note_field = create_TextField()

        self.form = AlertDialog(
            bgcolor = Minor_light_bgcolor,
            inset_padding = padding.symmetric(horizontal = 20, vertical = 20),

            title = Text('New Medicine'),
            title_padding = padding.only(top = 10, bottom = 10, right = 20, left = 20),
            
            content_padding = padding.only(top = 0, left = 20, right = 20, bottom = 10),
            content = Column(
                width = base_width,
                controls = [ 
                    Text('Medication name:', size = general_txt_size),
                    self.medname_field,
                    Text('Quantity of pill:', size = general_txt_size),
                    self.qty_field,
                    Text('Date to take pills:', size = general_txt_size),
                    Container(
                        bgcolor = Colors.WHITE,            
                        padding = padding.only(left = 10),
                        border_radius = 10,
                        border = BorderSide(                       
                            color = unit_color_dark, 
                            width = 1
                        ),
                        content = Row(spacing = 0,
                            alignment = 'spaceBetween',
                            controls = [
                                Text('Selected date', size = 12, color = input_hint_color),
                                IconButton(
                                    icon = Icons.CALENDAR_MONTH_SHARP, 
                                    icon_size = 20,
                                    icon_color = unit_color_dark, 
                                    highlight_color ='#FFFAFA',
                                    style = ButtonStyle(shape = RoundedRectangleBorder(radius = border_radius.only( 
                                        top_right = 10,
                                        bottom_right = 10))
                                    ),
                                    # on_click = lambda _: self.date_picker.pick_date()
                                )
                            ]
                        )
                    ),
                    # Text('Time to take pills', size = general_txt_size),
                    # self.time_picker,
                    Text('Note:', size = general_txt_size),
                    self.note_field
                ], 
            ),
            actions_padding = padding.only(top = 0, bottom = 15, left = 20, right = 20),
            actions = [
                Row(alignment = MainAxisAlignment.END,
                    controls = [    
                        TextButton(
                            content=Text('Cancel', size = general_txt_size, color = Colors.WHITE),
                            height = txf_height,
                            style = ButtonStyle(
                                shape = RoundedRectangleBorder(radius=10),
                                bgcolor = Dark_bgcolor,
                            ),
                            # on_click = lambda e: self.close_form()
                        ),
                        TextButton(
                            content=Text('Save', size = general_txt_size, color = Colors.WHITE),
                            height = txf_height,
                            style = ButtonStyle(
                                shape = RoundedRectangleBorder(radius=10),
                                bgcolor = Dark_bgcolor,
                            ),
                            # on_click = lambda e: self.save_pill()
                        )
                ])
            ],
            modal = True,
        )

        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    # Function of exit clicking the "Exit" button
    def exit(self, e):
        token = self.token
        if token: 
            log_out(token)
            self.page.session.clear()
            self.page.go('/first_page')
        else:
            self.page.snack_bar = SnackBar(Text('Something is wrong, try again'))
            self.page.snack_bar.open = True
            self.page.update() 
            
        


