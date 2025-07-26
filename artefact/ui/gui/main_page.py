from flet import *
from utils.traits import *
from service.authentication import log_out
import calendar
import datetime as dt

class MainPage(Container):

    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)
        
        self.token = ''

         # Creating a visual for navigation
        self.navig = Container(
            bgcolor = Dark_bgcolor,
            border_radius= b_radius,
            padding = padding.only(top=10, left=8, bottom=5),
            content = Column(controls = [
                Row(spacing = 0,
                    controls = [IconButton(
                        icon = Icons.KEYBOARD_RETURN, icon_color='white', 
                        on_click=self.restore, 
                        icon_size=20, 
                        highlight_color ='#FFFAFA')
                    ],
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

                Container(height = 5),
                Row(controls=[
                    TextButton(
                        # on_click= self.go_to_page,
                        content = Row(controls = [
                            Icon(icons.PERSON_OUTLINE, color="white60"),
                            Text(value="Personal info",
                                size = 15,
                                weight = FontWeight.W_300,
                                color = "white",
                                font_family = "poppins"
                            )
                        ])
                    )
                ]),
                
                Container(height = 20),
                Row(controls=[
                    TextButton(
                        content = Row(controls = [
                            Icon(icons.EXIT_TO_APP, color="white60"),
                            Text("Exit",
                                size = 15,
                                weight = FontWeight.W_300,
                                color = "white",
                                font_family = "poppins"
                            ) 
                        ]),
                        on_click = self.exit
                    )
                ])
            ])
        )

        # Creating a visual for Schedule page
        ## Calendar
        self.today = dt.datetime.today()
        self.year = self.today.year
        self.month = self.today.month

        self.prev_btn = IconButton(icons.ARROW_BACK, icon_color = unit_color_dark, on_click = self.prev_month)
        self.next_btn = IconButton(icons.ARROW_FORWARD, icon_color = unit_color_dark, on_click = self.next_month)
        
        # Weekday headers
        weekdays = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
        self.weekdays_row = Row(
            spacing = 0,
            controls = [
                Container(
                    width = calendar_width / 7,
                    height = 20,
                    alignment = alignment.center,
                    # padding = padding.only(bottom = 2),
                    margin = padding.only(bottom = 5),
                    content = Text(day, size = calendar_txt, weight = FontWeight.BOLD), # text_align = 'center' 
                    border = border.only(
                        top=border.BorderSide(1, unit_color_dark),
                        bottom = border.BorderSide(1, unit_color_dark)
                    )
                ) for day in weekdays
            ]
        )

        # Container for the calendar with days
        self.calendar = Container(
            # expand=True,
            height = calendar_height,
            width = calendar_width,
            border = border.only(
                            top = border.BorderSide(1, unit_color_dark),
                            bottom = border.BorderSide(1, unit_color_dark)
            ),
            padding = padding.all(0),
            margin  = margin.all(0),
            content = Column(spacing = 0, tight=True, controls = [])
            # content = Column(spacing = 0, expand  = True, controls = [])
        )

        # Button to add new pill
        self.btn_add_pill = ElevatedButton(
            content = Text('Add the pill', size = 14, color = Colors.WHITE),
            height = txf_height,
            width = btn_width,
            bgcolor = Dark_bgcolor,
            style = ButtonStyle(shape = RoundedRectangleBorder(radius=10)),
            on_click = self.show_form
        )
        self.form = None 


    def set_token(self, token):
        self.token = token
        self.update()


    def build(self):
        # Creating a visual for timetable
        month_header = Text(f"{calendar.month_name[self.month]} {self.year}", size = 16)

        weeks = calendar.monthcalendar(self.year, self.month)
        rows = []
        row_height = calendar_height / 6
        cell_width = calendar_width  / 7

        for week in weeks:
            cells = []
            for day in week:
                cells.append(
                    Container(
                        width = cell_width,
                        height = row_height,
                        padding = padding.all(0),
                        margin = margin.all(0),
                        border = border.only(
                            top = border.BorderSide(1, unit_color_dark),
                            bottom = border.BorderSide(1, unit_color_dark)
                        ),
                        content = Column(
                            spacing = 0,
                            # expand  = True,
                            tight   = True,
                            controls = [
                                # dates
                                Container(
                                    content = Text(str(day) if day else '', size = calendar_txt),
                                    alignment = alignment.center,
                                    padding = padding.all(0),
                                    margin = margin.all(0),
                                ),
                                # markers
                                Container(
                                    expand  = True,
                                    padding = padding.all(0),
                                    margin = margin.all(0),
                                    content = None,
                                )
                            ]
                        )
                    )
                )
            # rows.append(Row(spacing = 0, expand  = True, controls = cells))
            rows.append(Row(spacing = 0, tight=True, controls = cells))
        self.calendar.content.controls = rows


        ## Combine
        schedule_content = Container(
            content = Column(
                # expand=True,
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
                                content = Icon(name = icons.NOTIFICATIONS_OUTLINED, color = Colors.BLACK)
                            )
                        ]
                    ),
                    Row(alignment = MainAxisAlignment.CENTER,
                        controls = [Text('Schedule', size = 16)]),
                    Row(alignment = 'spaceBetween',
                        controls = [self.prev_btn, month_header, self.next_btn],
                    ),
                    Column(
                        spacing = 0,       
                        controls = [
                            self.weekdays_row,
                            self.calendar,
                        ]
                    ),
                    Container(
                        # margin = padding.only(bottom = 10),
                        content = self.btn_add_pill
                    )
                ]
            )
        )

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
                padding = padding.only(top = 15, left = 20, right = 40, bottom = 15), #5
                clip_behavior = ClipBehavior.ANTI_ALIAS,
                content = schedule_content
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
    # def create_calendar(self):
    #     self.grid.controls.clear()
        
    #     self.month_header.value = f'{calendar.month_name[self.month]} {self.year}'
    #     first_wday, total_days = calendar.monthrange(self.year, self.month)
    #     for _ in range(first_wday): # empty cells before the first day
    #         self.grid.controls.append(Container())

    #     self.update()
    
    
    def generate_calendar(self):
        self.month_header.value = f"{calendar.month_name[self.month]} {self.year}"
        self.grid.controls.clear()

        first_wday, total_days = calendar.monthrange(self.year, self.month)
    #     # Empty cells before first day
        for _ in range(first_wday):
            self.grid.controls.append(Container(width=(base_width-60)/7, height=40))

    #     # Day cells
        for day in range(1, total_days + 1):
            # date_str = f"{self.year}-{self.month:02d}-{day:02d}"
    #         ev_list = self.events.get(date_str, [])
    #         # Create small dots for events
    #         markers = [
    #             Container(width=8, height=8, bgcolor=colors.BLUE, border_radius=4)
    #             for _ in ev_list[:3]  # show up to 3 dots
    #         ]
    #         # If more than 3 events, add a '+' indicator
    #         if len(ev_list) > 3:
    #             markers.append(Text(f"+{len(ev_list)-3}", size=8))

            day_cell = Container(
                content=Column([
                    Text(str(day), size=12),
                    # Row(markers, alignment=MainAxisAlignment.CENTER)
                ], alignment=MainAxisAlignment.START),
                width=(base_width-60)/7,
                height=40,
                border=border.all(1, colors.GREY),
                # on_click=lambda e, d=day: self.open_day_events(d)
            )
            self.grid.controls.append(day_cell)

        self.update()

    # Functions to go one month forward or back
    def prev_month(self, e):
        if self.month == 1:
            self.month, self.year = 12, self.year - 1
        else:
            self.month -= 1
        # self.generate_calendar()
        self.update()

    def next_month(self, e):
        if self.month == 12:
            self.month, self.year = 1, self.year + 1
        else:
            self.month += 1
        # self.generate_calendar()
        self.update()
    
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
        self.selected_date = Text(str(self.today.date()), size = 12, color = input_hint_color)
        # self.time_picker = TimePicker(value = self.today.time())
        self.note_field = create_TextField()

        self.form = AlertDialog(
            bgcolor = minor_light_bgcolor,
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
                                self.selected_date,
                                IconButton(
                                    icon = Icons.CALENDAR_MONTH_SHARP, 
                                    icon_size = 20,
                                    icon_color = unit_color_dark, 
                                    highlight_color ='#FFFAFA',
                                    style = ButtonStyle(shape = RoundedRectangleBorder(radius = border_radius.only( 
                                        top_right = 10,
                                        bottom_right = 10))
                                    ),
                                    on_click=lambda e: self.page.open(
                                        DatePicker(
                                            first_date = dt.datetime(year = 2024, month = 10, day = 1),
                                            last_date = dt.datetime(year = 2026, month = 10, day = 1),
                                            on_change = self.handle_change,
                                            on_dismiss = self.handle_dismissal,
                                        )
                                    )

                                )
                            ]
                        )
                    ),
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
                            on_click = lambda _: self.close_form()
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

    def handle_change(self, e):
        self.selected_date.value = e.control.value.strftime('%Y/%m/%d')
        self.page.update()

    def handle_dismissal(self, e):
        self.page.add(Text(f"DatePicker dismissed"))
        
    # 'Cancel' button: function to close the Form of adding new medicine
    def close_form(self):
        self.form.open = False
        self.page.update()

    # Function of exit clicking the "Exit" button in navigation
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
            
        


