#Kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition

#KivyMD
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.picker import MDThemePicker
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.datatables import MDDataTable

#Components File
from Component import Database as db

#Load GUI files
Builder.load_file('GUI/main.kv')
Builder.load_file('GUI/edit room.kv')
Builder.load_file('GUI/edit teacher.kv')
Builder.load_file('GUI/add course.kv')
Builder.load_file('GUI/edit course.kv')

#Row Data for Datatables
room_row_data = []
teacher_row_data = []
course_row_data = []
semester_row_data = []

class WindowManager(ScreenManager):
    '''A window manager to manage switching between sceens.'''

class MainScreen(Screen):
    # Sdd new room into database and show it in datatables
    room_no = ObjectProperty()
    room_capacity = ObjectProperty()
    def room_checkbox_click(self, instance, value, type):
        if value == True:
            global room_type
            room_type = type

    def add_room(self):
        conn = db.getConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, capacity, type FROM rooms')
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        id = len(result) + 1
        if not self.room_no.text:
            return False
        name = self.room_no.text
        capacity = self.room_capacity.text
        data = [id, name, capacity, room_type]
        self.insertRoom(data)
        self.ids.room_no.text = ''
        self.ids.room_capacity.text = ''
        self.room_display()

    @staticmethod
    def insertRoom(data):
        conn = db.getConnection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO rooms (id, name, capacity, type) VALUES (?, ?, ?, ?)', data)
        conn.commit()
        conn.close()

    def room_display(self):
        conn = db.getConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT name, capacity, type FROM rooms')
        result = cursor.fetchall()
        conn.close()
        for entry in result:
            name = entry[0]
            capacity = str(entry[1])
            type = entry[2]
            data = (name, capacity, type)
            room_row_data.append(data)

    # Sdd new teacher into database and show it in datatables
    teacher_name = ObjectProperty()
    teacher_dept = ObjectProperty()
    teacher_title = ObjectProperty()

    def add_teacher(self):
        conn = db.getConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, dept, title FROM teachers')
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        id = len(result)+1
        if not self.teacher_name.text:
            return False
        name = self.teacher_name.text
        dept = self.teacher_dept.text
        title = self.teacher_title.text
        data = [id, name, dept, title]
        self.insertTeacher(data)
        self.ids.teacher_name.text = ''
        self.ids.teacher_dept.text = ''
        self.ids.teacher_title.text = ''
        self.room_display()

    @staticmethod
    def insertTeacher(data):
        conn = db.getConnection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO teachers (id, name, dept, title) VALUES (?, ?, ?, ?)', data)
        conn.commit()
        conn.close()

    def teacher_display(self):
        conn = db.getConnection()
        cursor = conn.cursor()
        cursor.execute('SELECT name, dept, title FROM teachers')
        result = cursor.fetchall()
        conn.close()
        for entry in result:
            name = entry[0]
            dept = entry[1]
            title = entry[2]
            data = (name, dept, title)
            teacher_row_data.append(data)

    def delete(self, name):
        conn = db.getConnection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rooms WHERE name = ?', [name])
        conn.commit()
        conn.close()
        MainScreen.room_display(self)

class EditRoom(Screen):
    '''A screen that display the story fleets and all message histories.'''

class EditTeacher(Screen):
    '''A screen that display the story fleets and all message histories.'''

class AddCourse(Screen):
   """jhjh"""

class EditCourse(Screen):
    '''A screen that display the story fleets and all message histories.'''

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class TimeTabler(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "TimeTabler"
        # self.icon = f"{os.environ['CRANE_ROOT']}/assets/images/logo_light.png"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "400"
        MainScreen.room_display(self)
        MainScreen.teacher_display(self)

    def build(self):
        # Window size
        Window.size = (1080, 640)
        Window.left = 160
        Window.top = 80
        # Connect to Database
        if not db.checkSetup():
            db.setup()
        # Datatables for GUI
        self.rooms_data_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=True,
            use_pagination=True,
            # name column, width column
            column_data=[
                ("Room No.", dp(60)),
                ("Capacity", dp(40)),
                ("Type", dp(40)),

            ],
            row_data=room_row_data,
        )
        self.rooms_data_table.bind(on_check_press=self.on_check_press)

        self.teachers_data_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=True,
            use_pagination=True,
            # name column, width column
            column_data=[
                ("Name", dp(50)),
                ("Department", dp(50)),
                ("Title", dp(40)),

            ],
            row_data=teacher_row_data,
        )
        self.teachers_data_table.bind(on_check_press=self.on_check_press)

        self.courses_data_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=True,
            use_pagination=True,
            # name column, width column
            column_data=[
                ("Course Name", dp(60)),
                ("Course Code", dp(20)),
                ("Teachers", dp(70)),
                ("Rooms", dp(40)),
                ("Type", dp(20)),
                ("Hours", dp(20)),
                ("Credit", dp(20)),

            ],
            row_data=[],
        )
        self.courses_data_table.bind(on_check_press=self.on_check_press)

        self.semesters_data_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=True,
            use_pagination=True,
            # name column, width column
            column_data=[
                ("Semester Name", dp(30)),
                ("Department", dp(30)),
                ("Total Student", dp(20)),
                ("Courses", dp(50)),

            ],
            row_data=[],
        )
        self.semesters_data_table.bind(on_check_press=self.on_check_press)

        self.courses_data_table_sem = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=True,
            use_pagination=True,
            # name column, width column
            column_data=[
                ("Course Code", dp(20)),
                ("Teachers", dp(70)),
                ("Type", dp(20)),
                ("Credit", dp(20)),

            ],
            row_data=[],
        )
        # self.courses_data_table.bind(on_check_press=self.on_check_press)

        # Setting Screen Manager
        self.wm = WindowManager(transition=RiseInTransition())
        screens = [
            MainScreen(name='main'), EditRoom(name='edit_room'), EditTeacher(name='edit_teacher'),
            AddCourse(name='add_course'), EditCourse(name='edit_course'),
        ]
        for screen in screens:
            self.wm.add_widget(screen)

        return self.wm


    def on_start(self):
        room_data = self.wm.screens[0].ids['rooms_data']
        room_data.add_widget(self.rooms_data_table)

        teacher_data = self.wm.screens[0].ids['teachers_data']
        teacher_data.add_widget(self.teachers_data_table)

        course_data = self.wm.screens[0].ids['courses_data']
        course_data.add_widget(self.courses_data_table)

        semester_data = self.wm.screens[0].ids['semesters_data']
        semester_data.add_widget(self.semesters_data_table)

        course_data_semester = self.wm.screens[0].ids['courses_data_Semester']
        #course_data_semester.add_widget(self.courses_data_table)

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''
        Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''

    def change_screen(self, screen):
        '''Change screen using the window manager.'''
        self.wm.current = screen
    def theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    alert_dialoge = None
    def show_alert_dialoge(self):
        if not self.alert_dialoge:
            self.alert_dialoge = MDDialog(
                title="WARNING!",
                text="Are You Sure You Want To Delete This File?.",
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.close_dialog
                    ),
                    MDRectangleFlatButton(
                        text="DELETE", on_release=self.delete_dialog(value)
                    ),
                ],
            )
        self.alert_dialoge.open()

    # Click Cancel Button
    def close_dialog(self, obj):
        # Close alert box
        self.alert_dialoge.dismiss()

    # Click the Delete Button
    def delete_dialog(self, name):
        MainScreen.delete(self, name)
        # Close alert box
        self.alert_dialoge.dismiss()

    def on_check_press(self, instance_table, current_row):
        global value
        value = str(current_row[0])
        print(value)


if __name__ == "__main__":
    TimeTabler().run()
