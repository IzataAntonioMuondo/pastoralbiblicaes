from flet import *
import calendar # built-in python calen library
import datetime

# some constants

CELL_SIZE = (28, 28)
CELL_BG_SIZE = 'white10'
TO_BG_COLOR = 'teal600'

# let's start first with the actual calen control. we'll tackle the UI a bit and focus heavy on the logic
class SetCalendar(UserControl):
    def __init__(self, update_callback, start_year=datetime.date.today().year):
        # we'll need a few class instances up here first
        # this widget will display the12 months of year 2023 . But an additional instance can be added to display other years as well
        self.current_year = start_year # the current year
        self.current_day = datetime.date.today().day

        self.m1 = datetime.date.today().month # current month
        self.m2 = self.m1 + 1 # the second month, needed for the calen module
        self.current_month = self.m1
        self.click_count: list = [] # for tracking clicks
        self.long_press_count: list = [] # same as above

        self.current_color = 'blue'

        self.selected_date = any
        self.update_callback = update_callback

        self.calendar_grid = Column(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )

        self.locate_button = TextButton(
            content=Text("Localizar Data", size=8, color=colors.BLACK),
            on_click=self.locate_date,
            style=ButtonStyle(
                shape={"": RoundedRectangleBorder(radius=6)},
                bgcolor={"": "teal600"},
            ), 
        )

        # Add a new TextField and confirmation button
        self.input_field_locate = TextField(label='',
            value=f'{self.current_day}/{self.current_month}/{self.current_year}',
            color=colors.BLACK,
            width=100,
            height=28,
            text_size=12,
        )
        self.confirm_button_locate = IconButton(
            icon=icons.SEARCH,
            icon_color=colors.BLACK,
            on_click=self.on_click_confirm_button_locate
        )
        self.input_row_locate = Row(
            [Text('                     '), self.input_field_locate, self.confirm_button_locate],
            alignment=MainAxisAlignment.CENTER,
            #spacing=5            
        )

        self.input_row_locate_date = Row(
            [self.input_field_locate, self.locate_button],
            alignment=MainAxisAlignment.CENTER,
            #spacing=5
        )

        self.build()
        self.output = Text()
        self.output_date = TextField(disabled=True, width=150)

        super().__init__()
    def output_date_label(self, label):
        if label == 1:
            self.output_date = TextField(label='Data de nascimento',disabled=True, width=150)
            value = self.output_date
            return value
        elif label == 2:
            self.output_date = TextField(label='Data da promessa',disabled=True, width=150)
            value = self.output_date
            return value


    

    def locate_date(self, e):
        date_str = self.input_field_locate.value
        try:
            date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
            self.current_month = date_obj.month
            self.current_day = date_obj.day
            self.current_year = date_obj.year
            self.build()
            self.calendar_grid.update()
            self.selected_date = date_obj.date()
            self.selected_date = self.selected_date.strftime('%d/%m/%Y')  # Atualiza a data selecionada
            self.update()
        except ValueError:
            print('Formato de data inválido. Use dd/mm/yyyy.')
            return
   
    def on_click_confirm_button_locate(self, e):
        self.locate_date(e)

    # first, let's create the ability to paginate the months
    def _change_month(self, delta):
        # recall the stored the current month + months above as self.m1 and self.m2
        # we can use the max and min to make sure the numbers stay between 1 and 13, as per the calendar library
        # the below now keeps m1 between 1 and 12, and m2 between 2 and 13.
        self.m1 = min(max(1, self.m1 + delta), 12)
        self.m2 = min(max(2, self.m2 + delta), 13)
        
        # we need to create a new calendar varaible
        new_calendar = self.create_month_calendar(self.current_year)
        self.calendar_grid = new_calendar
        self.update() # this should update the calendar  

    # finally, we can keep adding more functions to make the widget more complex. Let's highlight the container when it's clicked
    def one_click_date(self, e):
        # if i want to change the text title to the highlighted click, we can also do this... but it'll requere a third button.
        
        if self.selected_date is not None:
            e.control.bgcolor = None
            self.selected_date = None
            self.update_callback = self.selected_date  # Limpa a data selecionada na classe OpenCalendarButton
            self.output_date.value = ''
            self.output_date.update()
            e.control.value = ""  # Limpa a data selecionada
            e.control.update()
            self.update()
            
        else:
            e.control.bgcolor = colors.BLUE_600
            e.control.update()
            self.selected_date = e.control.data
            self.selected_date = self.selected_date.strftime('%d/%m/%Y')  # Atualiza a data selecionada
            self.output_date.value = f'{self.selected_date}'
            self.output_date.update()
            self.update_callback = self.selected_date  # Atualiza a data selecionada na classe OpenCalendarButton
            
            self.update()
    # Adicione este método para atualizar a data selecionada na classe OpenCalendarButton
    def update_selected_date(self, selected_date):
        self.selected_date = selected_date

    def get_selected_date(self):
        return self.selected_date

    def long_click_date(self, e):
        # now for multiple dates
        # we can set this up so that a user click two dates and it'll highlight all the dates in between.
        # 1. save the two clicks to a list
        print("Long click date called")
        self.long_press_count.append(e.control.data)
        # 2. check to see if there are indeed 2 clicks
        if len(self.long_press_count) == 2:
            # 3. set two dates by unpacking the list
            date1, date2 = self.long_press_count
            print(date1)
            print(date2)
            print(self.long_press_count)
            # 4. get the absoluted distance between them
            delta = abs(date1 - date2)
            # now click to see if it's past selection or future
            #if date1 < date2:
            dates = [date1 + datetime.timedelta(days=x) for x in range(delta.days + 1)]
            #else:
                #dates = [date2 + datetime.timedelta(days=x) for x in range(delta.days + 1)]

            # 6. we loop over the calendar matrix and color the boxes
            for _ in self.calendar_grid.controls[:]:
                for __ in _.controls[:]:
                    if isinstance(__, Row):
                        for box in __.controls[:]:
                            # 7. here we check to see if the dates list above matches the dates we created for each container's data
                            if box.data in dates:
                                box.bgcolor = colors.BLUE_600
                                box.update()

            self.long_press_count = []

        else:
            pass

    def save_dates(self, e):
        print("Datas Salvas:")
        if self.selected_date is not None:
            formatted_date = self.selected_date
            print(formatted_date)          
            # Adicione uma mensagem de confirmação
            self.output.value = f'Data selecionada: {formatted_date}'
            self.output_date.value = f'{formatted_date}'
            self.output.update()
            self.output_date.update()
        else:
            print("Nenhuma data selecionada.")
    
    # we can now crete the logic for the calen
    def create_month_calendar(self, year):
        self.current_year = year # we gwt the current year
        self.calendar_grid.controls: list = [] # clear the calen grid

        for month in range(self.m1, self.m2):
            # this gets the month name + year
            month_label = Text(
                f'{calendar.month_name[month]} {self.current_year}',
                size=14,
                weight='bold'
            )

            # now we need a month matrix
            #this gets the s of the month as per the year passed in
            month_matrix = calendar.monthcalendar(self.current_year, month)
            month_grid = Column(alignment=MainAxisAlignment.CENTER)
            month_grid.controls.append(
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[month_label]
                )
            )
            month_grid.controls.append(month_label)
            # now lets get the week labels
            # this is in the form of list. compr.
            weekday_labels = [
                Container(
                    width=28,
                    height=28,
                    alignment=alignment.center,
                    content=Text(
                        weekday,
                        size=12,
                        color = colors.BLACK,
                    )
                )
                for weekday in ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
            ]

            # now put the list of week container in row
            weekday_row = Row(controls=weekday_labels)
            month_grid.controls.append(weekday_row)

            # now for the days
            for week in month_matrix:
                week_container = Row()
                for day in week:
                    if day == 0: # if the day grid in the grid is empty
                        day_container = Container(
                            width=28,
                            height=28,
                        )
                    else:
                        day_container = Container(
                            width=28,
                            height=28,
                            border = border.all(0.5, color='black'),
                            alignment=alignment.center,
                            # we need to pass in some additional parameters to the main day cont.
                            data = datetime.date(
                                year=self.current_year,
                                month=month,
                                day=day
                            ),
                            on_click=lambda e: self.one_click_date(e),
                            #on_long_press=lambda e: self.long_click_date(e),
                            animate=400,

                        )
                    day_label = Text(str(day), size=12)

                    # we need to make a secand check here
                    if day ==  0:
                        day_label = None
                    if (
                        day == datetime.date.today().day 
                        and month == datetime.date.today().month
                        and self.current_year == datetime.date.today().year
                    ):
                        day_container.bgcolor = colors.TEAL_700
                    day_container.content = day_label
                    week_container.controls.append(day_container)
                month_grid.controls.append(week_container)


        print(f'{calendar.month_name[month]} {self.current_year}')
        self.calendar_grid.controls.append(month_grid)
        return self.calendar_grid
    
    def build(self):
        return self.create_month_calendar(self.current_year)
    
# let's swicth and get to the upper level UI
class DateSetUp(UserControl):
    def __init__(self, cal_grid):
        self.cal_grid = cal_grid # this is the calendar instance
        self.selected_date = cal_grid.selected_date  # Adicione um atributo para armazenar a data selecionada


        # we can create the buttons here
        self.next_btn = BTNPagination('Próximo', lambda e: cal_grid._change_month(1))
        self.save_button = TextButton(
            content=Text("Salvar Datas", size=8, color=colors.BLACK),
            on_click=cal_grid.save_dates,
            style=ButtonStyle(
                shape={"": RoundedRectangleBorder(radius=6)},
                bgcolor={"": "teal600"},
            ), 
        )
        self.prev_btn = BTNPagination('Anterior', lambda e: cal_grid._change_month(-1))

        self.today = Text(
            datetime.date.today().strftime('%b %d, %Y'),
            width=260,
            size=13,
            color=colors.BLACK,
            weight='w400'
        )

        # this will hold the pagination button
        self.btn_container = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                # buttons go in here
                self.prev_btn,
                self.save_button,
                self.next_btn
            ]
        )

        # this container will store  the calendar you see to the right.
        self.calendar = Container(
            width=320,
            height=45,
            bgcolor='#313131',
            border_radius=8,
            animate=300,
            clip_behavior=ClipBehavior.HARD_EDGE,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    #here, we can pass in the actual calendar instance plus the buttons
                    Divider(height=10, color=colors.TRANSPARENT),
                    self.cal_grid,
                    Divider(height=10, color=colors.TRANSPARENT),
                    self.btn_container,
                    Divider(height=10, color=colors.TRANSPARENT),
                    cal_grid.output
                ]
            )
        )
        super().__init__()

    def get_selected_date(self):
        return self.selected_date

        # we need a function to spand the stack to see the calendar
    def _get_calendar(self, e: None):
        if self.calendar.height == 45:
            self.calendar.height = 450
            self.calendar.update()
        else:
            self.calendar.height = 45
            self.calendar.update()

    def build(self):
        return Stack(
            width=320,
            controls=[
                self.calendar, 
                Container(
                    on_click=lambda e: self._get_calendar(e),
                    width=320,
                    height=45,
                    border_radius=8,
                    bgcolor="#313131",
                    padding=padding.only(left=15, right=5),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            self.today,
                            Container(
                                
                                width=32,
                                height=32,
                                border=border.only(left=BorderSide(0.9, 
                                color=colors.GREEN),
                                ),
                                alignment=alignment.center,
                                content=Icon(
                                    name=icons.CALENDAR_MONTH_SHARP, 
                                    size=15,
                                    opacity=0.65
                                    
                                )
                            ), 
                            
                        ]
                    ),    
                ),
                self.cal_grid.input_row_locate,   # Add the input_row here
            ]
        )

# let's divert quickly and create the buttons for pagination
class BTNPagination(UserControl):
    def __init__(self, txt_name, function):
        self.txt_name = txt_name
        self.function = function
        super().__init__()

    def build(self):
        return IconButton(
            content=Text(self.txt_name, size=8, weight='bold'),
            width=56,
            height=28,
            on_click=self.function,
            style=ButtonStyle(
                shape = {"": RoundedRectangleBorder(radius=6)}, bgcolor={"": 'teal600'}
            )
        )
# main function
class OpenCalendarButton(UserControl):
    def __init__(self, calendar_control, container,  update_callback):
        self.calendar_control = calendar_control
        self.container = container
        #self.cal_grid = SetCalendar()
        self.cal_grid = SetCalendar(update_callback)  # Passe a função de retorno de chamada aqui
        self.update_callback = update_callback
        self.day = datetime.date.day
        self.month = datetime.date.month
        self.year = datetime.date.year 

        self.selected_date_label = Text("", size=12, color=colors.BLACK)
        super().__init__()

    def build(self):
        return Row([
            #self.cal_grid.output_date,
            IconButton(
                icon=icons.CALENDAR_MONTH, tooltip='Calendário: Adicione a data aqui!', 
                on_click=self.open_calendar,
                style=ButtonStyle(
                    shape={"": RoundedRectangleBorder(radius=6)},
                    bgcolor={"": "teal600"},
                ),
            )
        ])

    def open_calendar(self, e):
        # Limpa o conteúdo atual do container
        
        if self.container.content == e.control.data:
            #self.container.content = None
            # Adiciona o controle do calendário ao container
            self.container.content = self.calendar_control
            self.cal_grid.update_selected_date(self.update_callback)  # Atualiza a data selecionada
            #self.day = 
            # Atualiza o container
            self.container.update()
        else:
            self.container.content = None
            # Adiciona o controle do calendário ao container
            #self.container.content = self.calendar_control

            # Atualiza o container
            self.container.update()
        
"""
def main(page: Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.padding = 80

    cal = SetCalendar()
    date = DateSetUp(cal_grid=cal)

    calendar_container = Container()

    open_calendar_button = OpenCalendarButton(date, calendar_container)
    
    page.add(Row(
        alignment=MainAxisAlignment.CENTER,
        controls=[
            open_calendar_button
        ]
    ))

    page.add(calendar_container)

    page.update()

if __name__== "__main__":
    app(target=main)"""