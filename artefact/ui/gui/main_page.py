from flet import *
import calendar
import datetime as dt
import asyncio
from utils.traits import *
from ui.gui.navigation import NavigationBar
from service.database import save_pill_database, load_medicines_for_user, delete_pill_database
from firebase_admin import auth as firebase_auth

# class MainPage(Container):
class MainPage(UserControl):

    def __init__(self):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)
        
        self.token = ''
        self.user_uid = ''

        # Notification settings
        self.unread_notif = False
        self.notifications = []
        self.btn_notif = IconButton(
            icon = icons.NOTIFICATIONS_OUTLINED,
            icon_size = 25,
            width = 30,
            height = 30,
            padding = padding.all(0),
            alignment = alignment.center,
            icon_color = Colors.BLACK,
            highlight_color ='#FFFAFA',
            on_click = lambda _: self.open_notifications_dialog()
        )

        # Creating a visual for Schedule page
        self.data_by_date = {}
        ## Calendar
        self.today = dt.datetime.today()
        self.year = self.today.year
        self.month = self.today.month

        # Tests with notification dialog
        # day = self.today.day
        # month = calendar.month_name[self.today.month]
        # self.notifications.append({"date": f"{day:02d} {month}", "medicine_name": "Test Pill"})
        # self.notifications.append({"date": f"{day:02d} {month}", "medicine_name": "Test Pill2"})
        # self.notifications.append({"date": f"{day:02d} {month}", "medicine_name": "Test Pill3"})
        # self.notifications.append({"date": f"{day:02d} {month}", "medicine_name": "Test Pill4"})


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
                    padding = padding.only(bottom = 3),
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


    def build(self):
        self.month_header = Text(f'{calendar.month_name[self.month]} {self.year}', size = general_txt_size, italic = True)

        self.token = self.page.session.get("token")
        if self.token:
            self.user_uid = firebase_auth.verify_id_token(self.token)['uid']
            self.data_by_date = load_medicines_for_user(self.user_uid, self.token, self.year, self.month)
            # print('After calling load_medicines_for_user', self.data_by_date)
        else: print('token wasn"t found')
        self._generate_calendar()

        # Combine visual elements of Schedule page
        schedule_content = Container(
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
                            self.btn_notif
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

        # Import navigation
        navigation = NavigationBar(current_page = self.schedule)

        # Combine Navigation + Schedule
        self.content = Container(
            width = base_width, 
            height = base_height, 
            bgcolor = Light_bgcolor,
            border_radius = b_radius,
            expand = True,
            content = Stack(
                controls = [navigation, self.schedule]
            )
        )

        return self.content


    # Open navigation moving the schedule to the right
    def shrink(self, e):
        self.schedule.controls[0].width = 70
        self.schedule.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        self.schedule.controls[0].border_radius = border_radius.only(top_left=35, top_right=0, bottom_left=35, bottom_right=0)
        self.schedule.update()

    # Notifications part
    # did_mount is a life-cycle hook of your UserControl. 
    # It is called automatically by the Flet engine after your control is first built and added to the page (i.e. after build() and the actual rendering)
    def did_mount(self):
        print('did_mount has run')
        self.page.run_task(self._schedule_daily_reminders)
    
    async def _schedule_daily_reminders(self):
        while True:
            now = dt.datetime.now()
            next_run = now.replace(hour = 6, minute = 0, second = 0, microsecond = 0)
            if now >= next_run:
                next_run += dt.timedelta(days = 1)
            
            delay_secs = (next_run - now).total_seconds()
            await asyncio.sleep(delay_secs)

            self.notifications.clear()
            self._handle_daily_reminder()

    # Method will be called when the daily reminder is triggered
    def _handle_daily_reminder(self):
        today = self.today.strftime('%Y-%m-%d')
        day = self.today.day
        month = calendar.month_name[self.today.month]
        pills = load_medicines_for_user(self.user_uid, self.token, self.year, self.month).get(today, [])
        
        if not pills:
            return
        for p in pills:
            self.notifications.append({
                'date': f'{day:02d} {month}',
                'medicine_name': p['medicine_name']
            })

        self.unread_notif = True
        self.btn_notif.icon_color = Colors.RED_900
        self.update()

    def open_notifications_dialog(self):
        notifs = [
            Container(
                content = Column(
                    spacing = 0,
                    controls = [
                        Text(f'Today {n['date']}:', size = general_txt_size),
                        Text(f"don't forget to take {n['medicine_name']}", size = general_txt_size),
                    ]
                ),
                padding = padding.symmetric(vertical = 4, horizontal = 12),
                border = border.all(1, unit_color_dark),
                border_radius = 10
            )
            for n in self.notifications
        ]
        
        notif_dialog = AlertDialog(
            bgcolor = minor_light_bgcolor,
            inset_padding = padding.symmetric(horizontal = 20, vertical = 20),

            title = Text("Notifications", size = 18, text_align = 'center'),
            title_padding = padding.only(top = 20, bottom = 10),

            content_padding = padding.only(top = 0, left = 20, right = 20),
            content = Column(
                spacing = 10,
                controls = [
                    Divider(thickness = 2, color = unit_color_dark),
                    ListView(
                        expand = True,
                        spacing = 10,
                        padding = padding.only(top = 0, bottom = 10), 
                        controls = notifs)
                ]
            ),

            actions = [TextButton(
                content = Text('Close', size = general_txt_size, color = unit_color_dark), 
                on_click = lambda e: self._close_dialog()
            )]
        )
        
        self.unread_notif = False
        self.btn_notif.icon_color = Colors.BLACK

        self.page.dialog = notif_dialog
        notif_dialog.open = True
        self.page.update()
        self.update()


    # Function to close a Dialog of the page    
    def _close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()


    # Functions to go one month forward or back
    def prev_month(self, e):
        if self.month == 1:
            self.month, self.year = 12, self.year - 1
        else:
            self.month -= 1

        if self.token:
            self.data_by_date = load_medicines_for_user(self.user_uid, self.token, self.year, self.month)

        self.month_header.value = f'{calendar.month_name[self.month]} {self.year}'
        self._generate_calendar()
        self.update()

    def next_month(self, e):
        if self.month == 12:
            self.month, self.year = 1, self.year + 1
        else:
            self.month += 1
        
        if self.token:
            self.data_by_date = load_medicines_for_user(self.user_uid, self.token, self.year, self.month)

        self.month_header.value = f'{calendar.month_name[self.month]} {self.year}'
        self._generate_calendar()
        self.update()
    
    # Build the part of calendar with dates and markers
    def _generate_calendar(self):
        print("Keys in data_by_date:", list(self.data_by_date.keys()))
        weeks = calendar.monthcalendar(self.year, self.month)
        rows = []
        row_height = calendar_height / 6
        cell_width = calendar_width  / 7

        for week in weeks:
            cells = []
            for day in week:
                date_key = f'{self.year}-{self.month:02d}-{day:02d}'
                pills = self.data_by_date.get(date_key, [])
                # 
                print('date_key = ', date_key)
                print('Pills = ', pills)
                
                markers = []
                corners = [
                    {"left": 4, "top": 2}, # 4px
                    {"right": 4, "top": 2},
                    {"left": 4, "bottom": 2},
                ]

                for i in range(min(len(pills), 3)):
                    color = (colors.BLUE_ACCENT_200, colors.PURPLE_ACCENT_200, colors.TEAL_ACCENT_200)[i]
                    markers.append(
                        Container(
                            width = 5,
                            height = 5,
                            bgcolor = color,
                            border_radius = 2,
                            **corners[i]
                        )
                    )
                if len(pills) > 3:
                    markers.append(
                        Container(
                            content = Text(f'+{len(pills) - 3}', size = 8, weight = FontWeight.BOLD),
                            right = 4,
                            bottom = 1
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
        date_key = f'{self.year}-{self.month:02d}-{day:02d}'
        pills = self.data_by_date.get(date_key, [])

        list_view = ListView(
            expand = True,
            spacing = 10,
            padding = padding.all(0),
        )
        
        for pill in pills:
            list_view.controls.append(
                Container(
                    width = btn_width,
                    bgcolor = minor_light_bgcolor,
                    border = border.all(1, unit_color_dark),
                    border_radius = 10,
                    padding = padding.all(5),
                    margin = padding.all(0),
                    alignment = alignment.center,
                    content = Text(pill['medicine_name'], size = general_txt_size),
                    on_click = lambda e, p = pill: self._show_med_detail(date_key, p)
                )
            )

        med_list_dialog = AlertDialog(
            bgcolor = minor_light_bgcolor,
            inset_padding = padding.symmetric(horizontal = 20, vertical = 20),
            
            title = Container(
                alignment = alignment.center,
                content = Text(f'{calendar.month_name[self.month]} {day:02d}', size = 18,) # weight = FontWeight.BOLD
            ),
            title_padding = padding.only(top = 20, bottom = 10),

            content_padding = padding.only(top = 0, left = 20, right = 20),
            content = Column(controls = [Divider(thickness = 2, color = unit_color_dark), list_view], spacing = 20),
            actions = [TextButton(
                content = Text('Close', size = general_txt_size, color = unit_color_dark), 
                on_click = lambda e: self._close_dialog()
            )]
        )
        self.page.dialog = med_list_dialog
        med_list_dialog.open = True
        self.page.update()

    def _show_med_detail(self, date_key, pill):
        med_desctiption = AlertDialog(
            bgcolor = minor_light_bgcolor,
            inset_padding = padding.symmetric(horizontal = 20, vertical = 20),

            title = Container(
                alignment = alignment.center,
                content = Text(pill['medicine_name'], size = 18)
            ),
            title_padding = padding.only(top = 20, bottom = 10),

            content_padding = padding.only(top = 0, bottom = 15, left = 20, right = 20),
            content = Column(
                tight = True,
                controls = [
                    Divider(thickness = 2, color = unit_color_dark),
                    Row(controls =[
                        Text('Quantity:', size = general_txt_size, weight = FontWeight.BOLD),
                        Text(f'{pill['quantity']}', size = general_txt_size),
                    ]),
                    Row(
                        vertical_alignment = CrossAxisAlignment.START,
                        controls =[
                            Text('Note:', size = general_txt_size, weight = FontWeight.BOLD),
                            Text(f'{pill['note']}', 
                                size = general_txt_size, 
                                no_wrap=False,
                                overflow="visible",
                                expand=True,
                            ),
                        ]
                    ),
                    Container(
                        alignment = alignment.center, 
                        margin = padding.only(top = 10),   
                        content = TextButton(
                            content=Text('Delete the medicine', size = general_txt_size, color = Colors.WHITE),
                            height = txf_height,
                            style = ButtonStyle(
                                shape = RoundedRectangleBorder(radius=10),
                                bgcolor = Dark_bgcolor,
                            ),
                            on_click = lambda e: self._delete_pill(date_key, pill)
                        )
                    )
                ], 
            ),

            actions = [TextButton(
                content = Text('Close', size = general_txt_size, color = unit_color_dark), 
                on_click = lambda _: self._close_dialog()),
            ]
        )
        self.page.dialog = med_desctiption
        med_desctiption.open = True
        self.page.update()

    def _delete_pill(self, date_key, pill):
        uid = firebase_auth.verify_id_token(self.token)['uid']
        key = pill['key']

        removal = delete_pill_database(uid, self.token, key)

        # Remove the entry locally
        if removal and date_key in self.data_by_date:
            self.data_by_date[date_key] = [i for i in self.data_by_date[date_key] if i["key"] != key]
            
            if not self.data_by_date[date_key]:
                del self.data_by_date[date_key]

        # Close dialog with medicine description
        self.page.dialog.open = False
        self.page.update()

        # Rebuild the calendar and update the UI inside UserControl
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
                            on_click = lambda _: self._close_dialog()
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

    # Functions for DatePicker's working
    def handle_change(self, e):
        self.selected_date.value = e.control.value.strftime('%Y-%m-%d')
        self.page.update()

    def handle_dismissal(self, e):
        self.page.add(Text(f"DatePicker dismissed"))
        
    # Function to save new medicine in database and to show it in the calendar
    def save_medicine(self):
        pill_name = self.medname_field.value
        pill_qty = self.qty_field.value
        pill_date = self.selected_date.value
        pill_note = self.note_field.value

        if pill_name and pill_qty and pill_date:
            new_key = save_pill_database(self.user_uid, self.token, pill_name, pill_qty, pill_date, pill_note)

            self.form.open = False
            self.page.snack_bar = SnackBar(Text('Medicine saved'))
            self.page.snack_bar.open = True
            self.page.update()

            # Update local dictionary and generate the calendar with new medicine
            entry = {
                'key': new_key,
                'medicine_name': pill_name,
                'quantity': pill_qty,
                'note': pill_note
            }
            self.data_by_date.setdefault(pill_date, []).append(entry)
            self._generate_calendar()
            self.update()
        else:
            self.page.snack_bar = SnackBar(Text('Please, fill all fields'))
            self.page.snack_bar.open = True
            self.page.update()


            
        


