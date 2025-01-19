from flet import *

def main(page: Page):
    BG = '#FFFAFA'
    Bir_sin = '#3F888F'
    Vas = '#ABCDEF'

    def shrink(e):
        page_2.controls[0].width = 100
        page_2.controls[0].scale = transform.Scale(0.8, alignment=alignment.center_right)
        page_2.controls[0].border_radius = border_radius.only(top_left=35, top_right=0, bottom_left=35, bottom_right=0)
        page_2.update()

    def restore(e):
        page_2.controls[0].width = 240
        page_2.controls[0].border_radius = 35
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
    
    page_1 = Container(
        width = 240, 
        height = 450,
        bgcolor = Bir_sin,
        border_radius= 35,
        padding = padding.only(top=20, left=20, right=20, bottom=5),
        content = Column(
            controls = [
                Row(
                    alignment="end",
                    controls=[
                        Container(
                            border_radius=25,
                            padding=padding.only(
                                top=13,
                                left=13,
                            ),
                            # height=50,
                            # width=50,
                            border=border.all(color="white", width=1),
                            on_click=lambda e: restore(e),
                            content=Text("<"),
                        )
                    ],
                ),
            ]
        )
    )

    page_2 = Row(
        alignment='end',
        controls=[Container(
            width = 240, 
            height = 450, 
            bgcolor = BG,
            border_radius= 35,
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
        width = 240, 
        height = 450, 
        bgcolor = BG,
        border_radius= 35,
        content=Stack(
            controls=[page_1, page_2]
        )
    )
    page.add(container)

    #page.on_route_change = route_change
    #page.go(page.route)

app(target = main)
