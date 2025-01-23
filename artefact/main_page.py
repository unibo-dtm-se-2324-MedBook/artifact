from flet import *
from utils.traits import *

class MainPage(Container):

    def __init__(self, page: Page):
        super().__init__()
        self.expand = True
        self.offset = transform.Offset(0,0,)
        self.page = page

        days_card = Row(scroll = 'auto')
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            days_card.controls.append(
                Container(
                    bgcolor = '#3F888F',
                    width = 80,
                    height = 40,
                    border_radius = 15,
                    padding = 10,
                    content = Text(day, color = '#FFFAFA', text_align = 'center')
                )
            )

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
                        on_click=self.go_to_page,
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
                        on_click= self.go_to_page,
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
                        on_click= self.go_to_page,
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
                        on_click= self.go_to_page,
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
                        on_click= self.go_to_page,
                        content = Row(controls = [
                            Icon(icons.EXIT_TO_APP, color="white60"),
                            Text("Exit",
                                size=15,
                                weight=FontWeight.W_300,
                                color="white",
                                font_family="poppins"
                            )
                        ])
                    )
                ])
            ])
        )

        schedule_content = Container(
            content = Column(
                controls=[
                    Row(
                        alignment = 'spaceBetween',
                        controls=[
                            Container(
                                on_click= self.shrink,
                                content = Icon(icons.MENU, Colors.BLACK)),
                            Text(value = "MedBook", weight = FontWeight.BOLD, color = 'black'),
                            Container(padding= padding.only(right = 16), content = Icon(name = icons.NOTIFICATIONS_OUTLINED, color = Colors.BLACK))
                        ]
                    ),
                    Row(
                        alignment="center",
                        controls=[Text(value = "Schedule")]
                    ),
                    #Container(height = 10),
                    #Row(
                        #alignment = 'center',
                        #controls = [
                            #FilledButton("Add new pills", icon="add", bgcolor = '#3F888F', on_click = lambda _: page.go('/add_pills'))
                        #]
                    #),
                    #Container(height = 5),
                    Text(value = "DAYS"),
                    Container(
                        padding = padding.only(bottom = 20, right= 16),
                        content = days_card
                    ),
                    Container(height = 10),
                ]
            )
        )

        self.schedule = content = Row(
            alignment='end',
            controls=[Container(
                width = base_width, 
                height = base_height, 
                bgcolor = Light_bgcolor,
                border_radius= b_radius,
                animate = animation.Animation(600, AnimationCurve.DECELERATE),
                animate_scale=animation.Animation(400, curve="decelerate"),
                padding = padding.only(top=15, left=20, right=20, bottom=5),
                content = Column(controls=[schedule_content])
            )]
        )

        self.content = Container(
            width = base_width, 
            height = base_height, 
            bgcolor = Light_bgcolor,
            border_radius= b_radius,
            expand = True,
            content=Stack(
                controls=[self.navig, self.schedule]
            )
        )
    
    def shrink(self, e):
        self.schedule.controls[0].width = 70
        self.schedule.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        self.schedule.controls[0].border_radius = border_radius.only(top_left=35, top_right=0, bottom_left=35, bottom_right=0)
        self.schedule.update()

    def restore(self, e):
        self.schedule.controls[0].width = base_width
        self.schedule.controls[0].border_radius = b_radius
        self.schedule.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        self.schedule.update()


    #############
    def go_to_page(self, e):
            pass


