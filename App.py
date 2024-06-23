from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.label import Label
import random
from kivy.uix.boxlayout import BoxLayout
from tabulate import tabulate
from kivy.uix.textinput import TextInput
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from itertools import cycle
from kivy.animation import Animation 

KV= '''
Manager:
    Main:
    HomeScreen:
    FirstScreen:
<Main>:
    name: "Main"
    
    Label:
        text: 'TimeTable Generator'
        font_size: 48
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        color: 0, 0, 0, 1  
        size_hint_y: None
        height: 50
        color: 54/255, 82/255, 173/255, 1
    MDRectangleFlatButton:
        text: '====>'
        font_size: 52
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        md_bg_color: 0.5, 0.7, 0.9, 1
        on_press: root.manager.current = "HomeScreen"
<HomeScreen>:
    name: "HomeScreen"
    MDRectangleFlatButton:
        text: 'Get Started'
        id: start
        font_size: 36
        pos_hint: {'center_x': 0.5, 'center_y': -1}
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        md_bg_color: 0.5, 0.7, 0.9, 1
        on_press: root.manager.current = "FirstScreen"
    Image:
        id: image
        source: "C:\\My_Data\\Career\\Time Table generator\\WhatsApp_Image_2024-01-27_at_12.49.49_688b4dc8-removebg-preview.png"
        pos_hint:{'center_x':0.5,'center_y':1}
        size: (150,100)
             
<FirstScreen>:
    
    name : "FirstScreen"
    Label:
        text: 'TimeTable'
        font_size: 48
        #font_name: 'E:/Career/Time Table generator/PlayfairDisplay-Italic-VariableFont_wght.ttf'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        color: 0, 0, 0, 1  
        size_hint_y: None
        height: 50
        color: 54/255, 82/255, 173/255, 1
    MDRectangleFlatButton:
        text: '<back'
        pos_hint:{'center_x':0.06,'center_y':0.95}
        on_press:root.manager.current= 'HomeScreen'
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1 
        md_bg_color: 0.5, 0.7, 0.9, 1  
        size:(10,10)
    MDRectangleFlatButton:
        text: 'Generate'
        id: Gen
        font_size: 20
        pos_hint:{'center_x':0.5,'center_y':0.05}
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1  
        md_bg_color: 0.1, 0.5, 0.7, 1 
        on_press:root.generate_timetable(self)
    
    '''
class Main(Screen):
    pass
class SharedData:
    subjects = []
    teachers = []
    
class HomeScreen(Screen):
    '''
    def set_font(self):
        LabelBase.register(name="WorkSans", fn_regular="C:/Users/DELL/Desktop/Time Table generator/WorkSans-SemiBold.ttf")
        self.theme_cls.font_styles.update({"WorkSans": ["WorkSans", 0, False, 0.8]})'''
    
        
    def on_pre_enter(self, *args):
        self.animate_button()
        self.animate_picture()
    def animate_button(self):
        button = self.ids.start
        anim = Animation(pos_hint={'center_y': 0.1}, height=50, duration=1)  # Example animation, adjust as needed
        anim.start(button)
    def animate_picture(self):
        image = self.ids.image
        anim = Animation(
            pos_hint={'center_y': 0.6},
            size=(150, 100),
            duration=1,
        )
        anim.start(image)

class FirstScreen(Screen):
    time_slots = ["Monday 9am-10am", "Tuesday 10am-11am", "Wednesday 11:30am-12:30pm", "Thursday 12:30pm-1:30pm", "Friday 2:30pm-3:30pm","Day 3:30pm-4:30pm","Day No_Class","Day No_Class","Day No_Class"]
    subject_teacher_mapping = {
            "MATH": "Mr. N.C.Sabarad",
            "OS": "Mrs. Avanti Patil",
            "DSA": "Mr. G.Deshpande",
            "DDCO": "Prof. Kiran Itagi",
            "C++": "Mrs. Sonam B",
            "DSA-Lab":"Mr. G.Deshpande",
            "DDCO-Lab":"Prof. Kiran Itagi",
            "OS-Lab":"Mrs. Avanti Patil",
            "Data Analytics":"Mr. Vaibhav"
        }
    #print("Original subject_teacher_mapping:", subject_teacher_mapping)
    subjects = ["MATH",
                        "OS",
                        "DSA",
                        "DDCO",
                        "C++",
                        "DSA-Lab",
                        "DDCO-Lab",
                        "OS-Lab",
                        "Data Analytics"]
    professors = ["Mr. N.C.Sabarad",
                           "Mrs. Avanti Patil",
                           "Mr. G.Deshpande",
                           "Prof. Kiran Itagi",
                           "Mrs. Sonam B",
                           "Mr. G.Deshpande",
                           "Prof. Kiran Itagi",
                           "Mrs. Avanti Patil",
                           "Mr. Vaibhav"]
    classrooms = ["Room:101", "Room:102", "Room:103", "Room:104","Room:105", "Room:106", "Room:107", "Room:108","Room:109"]
    days= ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        self.days_label = Label(text='TimeTable', halign='center', font_size='20sp')
        self.timetable_table = MDDataTable(
            size_hint=(0.5, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0,
            check=False,
            column_data=[
                ("Classroom", dp(30)),
                ("Subject", dp(30)),
                ("Professor", dp(30)),
                ("Time", dp(30)),
            ],
            row_data=[]
        )
        self.add_widget(self.timetable_table)
        
    def on_pre_enter(self, *args):
        # Animate the timetable_table opacity
        anim = Animation(opacity=1, duration=0.7)
        anim.start(self.timetable_table)

    def generate_timetable(self, instance):
        button = self.ids.Gen
        anim = Animation(opacity=1, duration=1)  # Example animation, adjust as needed
        anim.start(button)
        timetable = self._generate_timetable()
        self.display_timetable(timetable)

    def _generate_timetable(self):
        timetable = {}

        for day in self.time_slots:
            shuffled_time_slots = random.sample(self.time_slots, len(self.time_slots))

            for subject in self.subjects:
                time_slot = f"{day.split()[0]} {shuffled_time_slots.pop().split()[1]}"
                professor = self.subject_teacher_mapping.get(subject, random.choice(self.professors))
                classroom = f"Room: {self.subjects.index(subject) + 101}"

                timetable[(subject, time_slot)] = {"professor": professor, "classroom": classroom}
                

        return timetable


    def display_timetable(self, timetable):
        timetable_data = []
        for (subject, time_slot), info in timetable.items():
            _, day = time_slot.split()
            timetable_data.append((info['classroom'], subject,  info['professor'], day))

        self.timetable_table.row_data = timetable_data
        
    def back_to_home_screen(self, instance):
        self.manager.current = 'HomeScreen'

class Manager(ScreenManager):
    pass
class YourApp(MDApp):
    def build(self): 
        return Builder.load_string(KV)
    
    
if __name__ == '__main__':
    YourApp().run()
