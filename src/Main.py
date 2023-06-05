from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from data import DataBase
import ctypes
import sys
try:
    import wmi
except ImportError:
    import pip
    pip.main(['install', 'wmi'])


from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle

KV = """
MDFloatLayout:
    MDBottomNavigation:
        text_color_active: "lightgrey"
    
        MDBottomNavigationItem:
            id: onglet1
            name: "Bots"
            text: "Bots"
            icon: "robot-happy-outline"
                
            AnchorLayout:
                id: bot
"""

class ColorBar(BoxLayout):
    def __init__(self, color, radius = [10,], **kwargs):
        super(ColorBar, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = "48dp"
        self.padding = "4dp"
        self.spacing = "4dp"
        self.color = color

        with self.canvas.before:
            Color(rgba=self.color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MainApp(MDApp,Screen):
    def build(self):
        # Met le theme dark et la couleur en rouge
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.wmi = wmi.WMI()

        # Ajoute tous l'interface au screen Principal
        self.screen = Screen()
        self.app_screen = Builder.load_string(KV)
        self.screen.add_widget(self.app_screen)

        self.db = DataBase("Data.db")
        #self.label = []
        #self.textfield = []
        self.lang = "an"

        # Initialize la base de données
        self.init_data_table = True

        # Crée la Data Table pour la première page
        self.init()

        return self.screen

    def init(self) -> None:
        disk = []
        size = 0
        for disque in self.wmi.Win32_DiskDrive():
            disk.append([disque.Caption, disque.size])
            if len(disque.Caption) > size:
                size = len(disque.Caption)

        self.data_tables = MDDataTable(size_hint=(.9,.7), elevation=3, rows_num=20,column_data=[("Name",size*2),("Size",25)])

        for disque in disk:
            name, size = disque
            self.data_tables.add_row([name, str(int(int(size) / (1024 ** 3))) + ' Go'])

        self.data_tables.bind(on_row_press = self.on_click)
        self.app_screen.ids.bot.add_widget(self.data_tables)

    def on_click(self, *args) -> None:
        table, row = args
        if row.index != 0:
            row.index /= 2

        self.app_screen.ids.bot.remove_widget(self.data_tables)
        


        print()

MainApp().run()