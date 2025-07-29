from flet import *
from utils.traits import *
from service.authentication import log_out
import calendar
import datetime as dt
from service.database import save_pill_database, load_medicines_for_user
from firebase_admin import auth as firebase_auth

# class MainPage(Container):
class MainPage(UserControl):

    def __init__(self, token = None):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)
        
        # self.token = ''
        self.token = token
        self.user_uid = ''

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
        self.data_by_date = {}
        ## Calendar
        self.today = dt.datetime.today()
        self.year = self.today.year
        self.month = self.today.month

        self.prev_btn = IconButton(
            icons.ARROW_BACK, 
            icon_color = unit_color_dark, 
            icon_size = 16, 
            width = 32,
            height = 32,
            on_click = self.prev_month)
        self.next_btn = IconButton(
            icons.ARROW_FORWARD, 
            icon_color = unit_color_dark, 
            icon_size = 16, 
            width = 32,
            height = 32,
            on_click = self.next_month)
        
        ## Weekday headers
        weekdays = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
        self.weekdays_row = Row(
            spacing = 0,
            controls = [
                Container(
                    width = calendar_width / 7,
                    height = 25,
                    alignment = alignment.center,
                    padding = padding.only(bottom = 5),
                    content = Text(day, size = calendar_txt, weight = FontWeight.BOLD),
                    border = border.only(
                        bottom = border.BorderSide(2, unit_color_dark)
                    )
                ) for day in weekdays
            ]
        )

        ## Container for the calendar with days
        self.calendar = Container(
            height = calendar_height,
            width = calendar_width,
            # border = border.only(
            #                 top = border.BorderSide(1, unit_color_dark),
            #                 bottom = border.BorderSide(1, unit_color_dark)
            # ),
            padding = padding.all(0),
            margin  = margin.all(0),
            content = Column(spacing = 0, tight = True, controls = [])
        )

        ## Button to add new pill
        self.btn_add_pill = ElevatedButton(
            content = Text('Add the pill', size = 14, color = Colors.WHITE),
            height = txf_height,
            width = btn_width,
            bgcolor = Dark_bgcolor,
            style = ButtonStyle(shape = RoundedRectangleBorder(radius=10)),
            on_click = self.show_form
        )
        self.form = None 


    # def set_token(self, token):
    #     self.token = token
    #     self.update()


    def build(self):
        self.month_header = Text(f'{calendar.month_name[self.month]} {self.year}', size = general_txt_size, italic = True)

        if self.token:
            self.user_uid = firebase_auth.verify_id_token(self.token)['uid']
            print('uid = ', self.user_uid)
            self.data_by_date = load_medicines_for_user(self.user_uid, self.token, self.year, self.month)
            print('After calling load_medicines_for_user', self.data_by_date)
        else: print('token wasn"t found')
        self._generate_calendar()

        # Combine visual elements of Schedule page
        schedule_content = Container(
            content = Column(
                spacing = 5,
                controls=[
                    Row(
                        alignment = 'spaceBetween',
                        controls=[
                            Container(
                                on_click= self.shrink,
                                content = Icon(icons.MENU, Colors.BLACK)
                            ),
                            Text(value = 'MedBook',  color = 'black'),
                            Container(
                                content = Icon(name = icons.NOTIFICATIONS_OUTLINED, color = Colors.BLACK)
                            )
                        ]
                    ),
                    Divider(),
                    Row(alignment = MainAxisAlignment.CENTER,
                        controls = [Text('Schedule', weight = FontWeight.BOLD, size = 16)]),
                    Row(alignment = 'spaceBetween',
                        controls = [self.prev_btn, self.month_header, self.next_btn],
                    ),
                    Column(
                        spacing = 0,     
                        controls = [
                            self.weekdays_row,
                            self.calendar,
                        ]
                    ),
                    Container(
                        margin = padding.only(bottom = 20, top = 10),
                        content = self.btn_add_pill
                    )
                ]
            )
        )

        # Properties of Schedule page: basic and animation
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

        # Combine Navigation + Schedule
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

        return self.content

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

    # Build the part of calendar with dates and markers
    def _generate_calendar(self):
        weeks = calendar.monthcalendar(self.year, self.month)
        rows = []
        row_height = calendar_height / 6
        cell_width = calendar_width  / 7

        for week in weeks:
            cells = []
            for day in week:
                date_key = f'{self.year}/{self.month:02d}/{day:02d}'
                pills = self.data_by_date.get(date_key, [])
                # 
                print('Pills = ', pills)
                
                markers = []
                corners = [
                    {"left": 2, "top": 2}, # 2px
                    {"right": 2, "top": 2},
                    {"left": 2, "bottom": 2},
                ]

                for i in range(min(len(pills), 3)):
                    color = (colors.BLUE_ACCENT_200, colors.PURPLE_ACCENT_200, colors.TEAL_ACCENT_200)[i]
                    markers.append(
                        Container(
                            width = 6,
                            height = 6,
                            bgcolor = color,
                            border_radius = 3,
                            **corners[i]
                        )
                    )
                if len(pills) > 3:
                    markers.append(
                        Container(
                            content = Text(f'+{len(pills) - 3}', size = 10, weight = FontWeight.BOLD),
                            right = 2,
                            bottom = 2
                        )
                    )

                date_container = Container(
                    content = Text(str(day) if day else '', size = calendar_txt),
                    alignment = alignment.center,
                    padding = padding.all(0),
                    margin = margin.all(0),
                )

                markers_container = Container(
                    expand = True,
                    padding = padding.all(0),
                    margin = margin.all(0),
                    content = Stack(
                        expand = True,
                        controls = markers
                    )
                )

                cell_content = Column(
                    spacing = 0, 
                    tight = True,
                    controls = [date_container, markers_container]
                )

                cells.append(
                    Container(
                        width = cell_width, 
                        height = row_height,
                        padding = padding.all(0),
                        margin = margin.all(0),
                        border = border.only(
                            bottom = border.BorderSide(1, unit_color_dark)
                        ),
                        content = cell_content,
                        on_click = (lambda e, d = day: self.open_day_dialog(d)) if pills else None
                    )
                )
            rows.append(Row(spacing = 0, tight = True, controls = cells))
        self.calendar.content.controls = rows

    def open_day_dialog(self, day):
        pass
    
    # Functions to go one month forward or back
    def prev_month(self, e):
        if self.month == 1:
            self.month, self.year = 12, self.year - 1
        else:
            self.month -= 1
        self.month_header.value = f"{calendar.month_name[self.month]} {self.year}"
        self._generate_calendar()
        self.update()

    def next_month(self, e):
        if self.month == 12:
            self.month, self.year = 1, self.year + 1
        else:
            self.month += 1
        self.month_header.value = f"{calendar.month_name[self.month]} {self.year}"
        self._generate_calendar()
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
                            on_click = lambda e: self.save_medicine()
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

    def save_medicine(self):
        pill_name = self.medname_field.value
        pill_qty = self.qty_field.value
        # date = self.date_picker.value.strftime('%Y-%m-%d')
        pill_date = self.selected_date.value
        pill_note = self.note_field.value

        if pill_name and pill_qty and pill_date:
            save_pill_database(self.user_uid, self.token, pill_name, pill_qty, pill_date, pill_note)
            self.form.open = False
            self.page.snack_bar = SnackBar(Text('Medicine saved'))
            self.page.snack_bar.open = True
            self.page.update()
        else:
            self.page.snack_bar = SnackBar(Text('Please, fill all fields'))
            self.page.snack_bar.open = True
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
            
        


