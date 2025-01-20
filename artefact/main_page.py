from flet import *
from utils.traits import *

def main(page: Page):


    def shrink(e):
        page_2.controls[0].width = 80
        page_2.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        page_2.controls[0].border_radius = border_radius.only(top_left=35, top_right=0, bottom_left=35, bottom_right=0)
        page_2.update()

    def restore(e):
        page_2.controls[0].width = base_width
        page_2.controls[0].border_radius = b_radius
        page_2.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        page_2.update()

    #pages = {
        #'/':View(
            #'/',
                #[
                    #container
                #]
            #),
        #'/add_pills':View(
            #'/add_pills',
                #[
                    #add_pills
                #]
            #)
    #}



    #def route_change(route):
        #page.views.clear()
        #page.views.append(
            #View(
                #'/',
                #[
                    #container
                #]
            #)
        #)

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

    first_page_contents = Container(
        content = Column(
            controls=[
                Row(
                    alignment = 'spaceBetween',
                    controls=[
                        Container(
                            on_click=lambda e: shrink(e),
                            content = Icon(icons.MENU, Colors.BLACK)),
                        Text(value = "MedBook", weight = FontWeight.BOLD, color = 'black'),
                        Container(content = Icon(name = icons.NOTIFICATIONS_OUTLINED, color = Colors.BLACK))
                    ]
                ),
                
                
                Row(
                    alignment="center",
                    controls=[
                        Text(value = "Schedule")
                    ]
                    
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
                    padding = padding.only(bottom = 20),
                    content = days_card
                ),
                Container(height = 10),

            ]
        )
    )
    
    def go_to_page():
        pass

    page_1 = Container(
        bgcolor = Dark_bgcolor,
        border_radius= b_radius,
        padding = padding.only(top=20, left=20, right=20, bottom=5),
        content = Column(controls = [
            Row(
                controls=[IconButton(icon=Icons.KEYBOARD_RETURN, icon_color='white', on_click=lambda e: restore(e), icon_size=20, highlight_color ='#FFFAFA')],
            ),
            Container(
                padding = padding.only(left=15),
                content= Text("Your portable\nmedical card", size=15, weight="bold", color='white')
            ),

            Container(height=10),
            Row(controls=[
                TextButton(
                    on_click=go_to_page(),
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
                    on_click=go_to_page(),
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
                    on_click=go_to_page(),
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
                    on_click=go_to_page(),
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
                    on_click=go_to_page(),
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

    page_2 = Row(
        alignment='end',
        controls=[Container(
            width = base_width, 
            height = base_height, 
            bgcolor = Light_bgcolor,
            border_radius= b_radius,
            animate = animation.Animation(600, AnimationCurve.DECELERATE),
            animate_scale=animation.Animation(400, curve="decelerate"),
            padding = padding.only(top=20, left=20, right=20, bottom=5),
            content = Column(
                controls=[
                    first_page_contents
                ]
            )
        )]
    )

    container = Container(
        width = base_width, 
        height = base_height, 
        bgcolor = Light_bgcolor,
        border_radius= b_radius,
        content=Stack(
            controls=[page_1, page_2]
        )
    )
    page.add(container)

    #page.on_route_change = route_change
    #page.go(page.route)

app(target = main)
