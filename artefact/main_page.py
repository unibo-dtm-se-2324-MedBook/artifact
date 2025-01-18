from flet import *

def main(page: Page):
    BG = '#FFFAFA'
    Bir_sin = '#3F888F'
    Vas = '#ABCDEF'

    days_card = Row(
        scroll = 'auto'
    )
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        days_card.controls.append(
            Container(
                bgcolor = '#3F888F',
                width = 100,
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
                        Container(content = Icon(icons.MENU, Colors.BLACK)),
                        Text(value = "MedBook", weight = FontWeight.BOLD, color = 'black'),
                        Container(content = Icon(name = icons.NOTIFICATIONS_OUTLINED, color = Colors.BLACK))
                    ]
                ),
                Text(value = "Schedule"),
                Text(value = 'ADD'),
                
                Container(
                    padding = padding.only(top = 10, bottom = 20),
                    content = days_card
                )
            ]
        )
    )
    
    page_1 = Container(
        bgcolor = Bir_sin,
    )

    page_2 = Row(
        controls=[Container(
            width = 240, 
            height = 450, 
            bgcolor = BG,
            border_radius= 35,
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

app(target = main)
