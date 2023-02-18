from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.toast import toast

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
import matplotlib.pyplot as plt

from firebaseAuth import FirebaseAuth
from datetime import datetime
from collections import Counter
import calendar
import numpy as np
import pyrebase
import os

Config.set('graphics', 'multisamples', '0')

Window.size = (450, 740)

kv_string = """ 
# This is the multiline string used for the kivy builder language
# Used for designing the ui of the app

ScreenManager: # Manages the different screens

    #Vendor screens
    LoginScreen:
        id: login_screen
        name: "login_screen"
    SignupScreen:
        id: signup_screen
        name: "signup_screen"
    VendorScreen:
        id: vendor_screen
        name: "vendor_screen"

    #User screens
    MainScreen:
        id: main_screen
        name: "main_screen"
    MainMenuScreen:
        id: main_menu_screen
        name: "main_menu_screen"
    SideMenuScreen:
        id: side_menu_screen
        name: "side_menu_screen"
    StatsScreen:
        id:stats_screen
        name: "stats_screen"

# Screens

<LoginScreen>: # Log in screen
    BoxLayout:
        size: root.width, root.height
        padding:25

        MDCard:
            radius: 50
            elevation: 20

            BoxLayout:
                orientation: "vertical"
                padding: 25

                MDLabel:
                    text: "Login Page"
                    halign: "center"
                    height: 80
                    size_hint: 1, 0.3

                MDTextField:
                    id: login_email_input
                    hint_text: "Email"
                    height: 80
                    width: self.parent.width-70
                    size_hint: 1, 0.1
                    pos_hint: {"center_x":0.5}

                MDTextField:
                    id: login_password_input
                    hint_text: "Password"
                    password: True     
                    height: 80
                    size_hint: 1, 0.1
                    pos_hint: {"center_x":0.5}

                BoxLayout:
                    size_hint: 1, 0.3
                    orientation: "vertical"

                    MDFillRoundFlatButton:
                        text: "Sign In"
                        pos_hint: {"center_x":0.5}
                        size_hint_x: 1
                        on_release:
                            app.firebaseAuth.login(self, login_email_input.text, login_password_input.text)
                    MDLabel:
                        text: "Or"
                        height: 80
                        size_hint_y: None
                        halign: "center"

                    MDFillRoundFlatButton:
                        text: "Sign Up"
                        width: self.parent.width
                        size_hint_x: 1
                        pos_hint: {"center_x":0.5}
                        on_release: 
                            app.root.current = "signup_screen"

<SignupScreen>: #Sign up screen
    BoxLayout:
        size: root.width, root.height
        padding:25

        MDCard:
            radius: 50
            elevation: 20

            BoxLayout:
                orientation: "vertical"
                padding: 25

                MDLabel:
                    text: "Signup Page"
                    halign: "center"
                    size_hint: 1, 0.3
                    height: 80

                MDTextField:
                    id: signup_fullname_input

                    size_hint: None, 0.1
                    height: 80
                    width: self.parent.width-70
                    pos_hint: {"center_x":0.5}

                    hint_text: "Full Name as per NRIC"
                    helper_text: "This field is required"
                    helper_text_mode: "on_focus"

                MDTextField:
                    id: signup_email_input

                    height: 80
                    width: self.parent.width-70
                    pos_hint: {"center_x":0.5}
                    size_hint: None, 0.1

                    hint_text: "Email"
                    helper_text: "This field is required"
                    helper_text_mode: "on_focus"

                MDTextField:
                    id: signup_password_input
                    password: True

                    size_hint: None, 0.1
                    height: 80
                    width: self.parent.width-70
                    pos_hint: {"center_x":0.5}

                    hint_text: "Password"
                    helper_text: "This field is required"
                    helper_text_mode: "on_focus"

                MDTextField:
                    id: signup_confirmpassword_input
                    password: True

                    height: 80
                    size_hint: None, 0.1
                    width: self.parent.width-70

                    hint_text: "Confirm Password"
                    helper_text: "This field is required"
                    helper_text_mode: "on_focus"

                BoxLayout:
                    orientation: "vertical"
                    size_hint: 1, 0.3

                    MDFillRoundFlatButton:
                        id: sign_up_button
                        text: "Sign Up"

                        pos_hint: {"center_x":0.5}
                        width: self.parent.width

                        on_release:
                            root.manager.transition.direction = 'right'
                            app.firebaseAuth.signup(self, signup_fullname_input.text, signup_email_input.text, signup_password_input.text, signup_confirmpassword_input.text)

                    MDLabel:
                        text: "Or"
                        size_hint_y: None
                        height: 80
                        halign: "center"

                    MDFillRoundFlatButton:
                        id: back_to_login_button
                        text: "Back to Login"

                        width: self.parent.width
                        pos_hint: {"center_x":0.5}

                        on_release: 
                            app.root.current = "login_screen"
                            root.manager.transition.direction = 'right'


<VendorScreen>: # Vendor screen
    MDNavigationLayout: 
        ScreenManager:
            Screen:
                MDBottomNavigation:
                    MDBottomNavigationItem:
                        text: 'Dashboard'
                        name: 'HomeScreen'
                        icon: 'home'

                        BoxLayout:
                            orientation: "vertical"

                            MDToolbar:
                                title: 'Dashboard'
                                elevation: 8
                                left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]


                            ScrollView:

                                BoxLayout:
                                    padding: 50
                                    spacing: 20
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height

                                    MDCard:
                                        elevation: 10
                                        padding: 30
                                        size_hint: (1,None)
                                        height: self.minimum_height*12
                                        radius: 50

                                        BoxLayout:
                                            id: earnings_graph
                                            orientation: "vertical"
                                            pos_hint: {"center_x":0.5}

                                    MDCard:
                                        elevation: 10
                                        padding: 30
                                        size_hint: (1,None)
                                        height: self.minimum_height*12
                                        radius: 50

                                        BoxLayout:
                                            id: sides_graph
                                            orientation: "vertical"
                                            pos_hint: {"center_x":0.5}

                                    MDCard:
                                        elevation: 10
                                        padding: 30
                                        size_hint: (1,None)
                                        height: self.minimum_height*12
                                        radius: 50

                                        BoxLayout:
                                            id: main_graph
                                            orientation: "vertical"
                                            pos_hint: {"center_x":0.5}

                                    MDCard:
                                        elevation: 10
                                        padding: 40
                                        size_hint: (1,None)
                                        height: 400
                                        radius: 50

                                        BoxLayout:
                                            spacing: 12
                                            orientation: "vertical"
                                            pos_hint: {"center_x":0.5}

                                            MDLabel:
                                                halign: "left"
                                                font_style: "H5"
                                                bold: True
                                                #adaptive_height: True
                                                text: "More Data"

                                            MDFillRoundFlatButton:
                                                text:"Daily Data"
                                                pos_hint:{"center x": 0.5}
                                                on_release:
                                                    app.statsDailyScreen()


                                            MDFillRoundFlatButton:
                                                text:"Monthly Data"
                                                pos_hint:{"center x": 0.5}
                                                on_release:
                                                    app.statsMonthlyScreen()

                                            MDFillRoundFlatButton:
                                                text:"Yearly Data"
                                                pos_hint:{"center x": 0.5}
                                                on_release:
                                                    app.statsYearlyScreen()

                    MDBottomNavigationItem:
                        text: 'Orders'
                        name: 'OrdersScreen'
                        icon: 'food'

                        BoxLayout:
                            orientation: "vertical"

                            MDToolbar:
                                title: 'Menu'
                                elevation: 8
                                left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

                            ScrollView:  

                                BoxLayout:
                                    padding: 50
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: self.minimum_height

                                    MDLabel:
                                        height: 80
                                        font_style: "H5"
                                        size_hint_y: None
                                        bold: True
                                        text: "Orders"

                                    MDList: 
                                        spacing: 20
                                        id: order_listboii

                    MDBottomNavigationItem:
                        text: 'Menu'
                        name: 'MenuScreen'
                        icon: 'menu'

                        BoxLayout:
                            orientation: 'vertical'

                            MDToolbar:
                                title: 'Menu'
                                elevation: 8
                                right_action_items: [['plus',lambda x: app.item_add()]]
                                left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

                            ScrollView:  

                                BoxLayout:
                                    padding: 50
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: self.minimum_height

                                    MDLabel:
                                        height: 80
                                        font_style: "H5"
                                        size_hint_y: None
                                        bold: True
                                        text: "Main Dishes"

                                    MDList:
                                        spacing: 20
                                        id: main_listboii

                                    MDLabel:
                                        height: 80
                                        font_style: "H5"
                                        size_hint_y: None
                                        bold: True
                                        text: "Side Dishes"

                                    MDList:
                                        spacing: 20
                                        id: side_listboii

        MDNavigationDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: 'vertical'
                spacing: '8dp'
                padding: '8dp'

                ScrollView:

                    MDList:

                        OneLineIconListItem:
                            on_release: 
                                root.manager.transition.direction = 'right'
                                app.firebaseAuth.logout(self)

                            text: 'Logout'
                            IconLeftWidget:
                                icon: 'logout'

<StatsScreen>: # Vendor statistics screen
    BoxLayout:
        orientation: "vertical"
        MDToolbar:
            title: "Main Dishes"
            elevation: 10
            left_action_items:
                [['arrow-left', lambda x: app.stats_screen_change()]]

        BoxLayout:
            id : datatable
            orientation: "vertical"
            spacing: 20       

<MainScreen>: # User main screen (Written by Kai Jun)
    MDNavigationLayout:
        ScreenManager:
            Screen:
                MDBottomNavigation  
                    MDBottomNavigationItem:
                        name: 'Menu'
                        text: 'Menu'
                        icon: 'food'

                        BoxLayout:
                            orientation: 'vertical'

                            MDToolbar:
                                title: 'Menu'
                                elevation: 8
                                left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

                            ScrollView:

                                BoxLayout:
                                    id: stallsid
                                    padding: 50
                                    spacing: 20
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height*11
                                


                    
                    
                    MDBottomNavigationItem:
                        name: 'Order'
                        text: 'My Orders'
                        icon: 'cart'

                        BoxLayout:
                            orientation: 'vertical'

                            MDToolbar:
                                title: 'My Orders'
                                elevation: 8
                                left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

                            ScrollView:

                                BoxLayout:
                                    id: ordersid
                                    padding: 50
                                    spacing: 20
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: self.minimum_height*12
                                        
                                        

                                
                                    

                    MDBottomNavigationItem:
                        name: 'Profile'
                        text: 'Profile'
                        icon: 'account'

                        BoxLayout:
                            orientation: 'vertical'

                            MDToolbar:
                                title: 'Profile'
                                elevation: 8
                                left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

                            ScrollView:
                                do_scroll_y: True

                                BoxLayout:
                                    height: self.minimum_height
                                    size_hint_y: None
                                    orientation: "vertical"
                                    padding: 40

                                    MDCard:
                                        radius: 50
                                        elevation: 10
                                        size_hint_y: None
                                        pos_hint: {"center x": 0.5, "center y": 0.5}
                                        height: self.minimum_height

                                        BoxLayout:
                                            orientation: "vertical"
                                            padding: 50
                                            height: self.minimum_height
                                            size_hint_y: None
                                            pos_hint: {"center_x": 0.5, "center_y": 0.5}

                                            MDLabel:
                                                id: name_label
                                                text: "Name"
                                                font_style: "H6"
                                                bold: True
                                                size_hint_y: None
                                                height: 80

                                            MDLabel:
                                                id: name_var
                                                text: "Name"
                                                bold: False
                                                font_style: "Subtitle1"
                                                size_hint_y: None
                                                height: 80

                                            MDLabel:
                                                id: email_label
                                                text: "Email"
                                                font_style: "H6"
                                                bold: True
                                                height: 80
                                                size_hint_y: None

                                            MDLabel:
                                                id: email_var
                                                text: "Email"
                                                font_style:"Subtitle1"
                                                bold: False
                                                height: 80
                                                size_hint_y: None

        MDNavigationDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: 'vertical'
                spacing: '8dp'
                padding: '8dp'

                ScrollView:
                    MDList:
                        OneLineIconListItem:
                            on_release: 
                                root.manager.transition.direction = 'right'
                                app.firebaseAuth.logout(self)
                            text: 'Logout'
                            IconLeftWidget:
                                icon: 'logout'

<MainMenuScreen>: #User menu screen (Written by Kai Jun)
    BoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: "Main Dishes"
            elevation: 10
            left_action_items:
                [['arrow-left', lambda x: app.go_back_to_menu()]] 

        ScrollView:

            BoxLayout:
                padding: 50
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    height: 80
                    font_style: "H5"
                    size_hint_y: None
                    bold: True
                    text: "Main Dishes Available"

                MDList:
                    spacing: 30
                    id: mainmenuid      


<SideMenuScreen>: # User sides selecting screen (Written by Kai Jun)
    BoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: "Side Dishes"
            elevation: 10
            left_action_items:
                [['arrow-left', lambda x: app.go_back_to_mains()]] 

        ScrollView:

            BoxLayout:
                padding: 50
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    height: 80
                    font_style: "H5"
                    size_hint_y: None
                    bold: True
                    text: "Side Dishes Available"

                MDList:
                    spacing: 30
                    id: sidesmenuid

        MDCard:
            orientation: "vertical"
            padding: 25
            radius: 50
            elevation: 10

            BoxLayout:
                id: orderpreview
                orientation: "vertical"
                padding: 10
                adaptive_height: True
                adaptive_width: True
                adaptive_size: True         


# Screen Widgets

<SidesCheckBox>: # MDCheckBox (Written by Kai Jun)
    size_hint: None, None
    size: "60dp", "60dp"
    pos_hint: {"right":1}
    on_active: 
        app.checkbox_state(*args)

<OrderButton>: # MDFillRoundFlatButton (Written by Kai Jun)
    text:"   Place Order    "
    pos_hint:{"right": 1}
    on_release:
        app.place_order()

<MainMenuOrder>: # MDFillRoundFlatButton (Written by Kai Jun)
    text:"     Select     "
    pos_hint:{"right": 0.95}
    on_release: 
        app.on_main_click(root)

<MainMenuButton>: # MDFillRoundFlatButton (Written by Kai Jun)
    text:"Browse Menu"
    pos_hint:{"right": 0.95}
    on_release: 
        app.on_stall_click(self.parent.children[3].text)

<Content>: #MDBoxLayout
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height

    MDTextField:
        id: item
        hint_text: 'Item name'
        height: 80
        width: self.parent.width
        pos_hint: {"center_x":0.5}        
        helper_text: "This field is required"
        helper_text_mode: "on_focus"

    MDTextField:
        id: price
        hint_text: 'Item price'
        height: 80
        width: self.parent.width
        pos_hint: {"center_x":0.5}        
        helper_text: "This field is required"
        helper_text_mode: "on_focus"

    MDFillRoundFlatButton:
        id: dish_type
        size_hint_x: 1
        text: "Dish Type"
        on_release:
            app.menu.open()

<MenuMainDeleteButton>: # MDFillRoundFlatButton
    text: "Delete"
    pos_hint: {"right": 0.95}
    on_release:
        app.get_menu_main_name(root)

<MenuSideDeleteButton>: # MDFillRoundFlatButton
    text: "Delete"
    pos_hint: {"right": 0.95}
    on_release:
        app.get_menu_side_name(root)

<delete>: #MDFillRoundFlatButton
    text: 'Complete'
    on_release: app.remove_widget(root)
"""


# Giving the screens a screen class
class LoginScreen(Screen):
    pass


class SignupScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class MainMenuScreen(Screen):
    pass


class SideMenuScreen(Screen):
    pass


class VendorScreen(Screen):
    pass


class StatsScreen(Screen):
    pass


# Giving screen widgets their widget classes
class Card(MDCard):
    pass


class Content(MDBoxLayout):
    pass


class delete(MDFillRoundFlatButton):
    pass


class MainMenuButton(MDFillRoundFlatButton):
    pass


class MainMenuOrder(MDFillRoundFlatButton):
    pass


class SidesCheckBox(MDCheckbox):
    pass


class MenuMainDeleteButton(MDFillRoundFlatButton):
    pass


class MenuSideDeleteButton(MDFillRoundFlatButton):
    pass


class OrderButton(MDFillRoundFlatButton):
    pass


class ScreenManager1(ScreenManager):
    pass


class SSTOrder(MDApp):  # Code for the app
    # Load menu items
    main_list = []
    main_cost_list = []
    side_list = []
    side_cost_list = []

    # Dummy data
    stallrid = 0
    selected_sides_cost = 0
    selected_sides = ["No sides selected"]



    # Stall email
    stall_emails = []
    stall_names = []

    selected_stall_email = ""
    selected_stall_name = ""

    selected_main = ""
    selected_main_cost = 0

    # Pyrebase configurations, so as to be able to connect to the database
    config = {
        "apiKey": "AIzaSyCfVmGyN1xEckRMQOpwyOdJuD2OjXHWM8Y",
        "authDomain": "coursework-app-9f20c.firebaseapp.com",
        "databaseURL": "https://coursework-app-9f20c-default-rtdb.asia-southeast1.firebasedatabase.app/",
        "storageBucket": "gs://coursework-app-9f20c.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()  # To be used for database functions
    auth = firebase.auth()  # To be used for authentication functions

    # Get user data from login_data.txt
    try:
        with open("login_data.txt", "r") as f:
            data = f.readlines()
            text_email = data[0].strip().replace('.', ',')
            text_password = data[1].strip()
            text_bool = data[2].strip()
            # Check if log in data is vendor or user
            if text_bool == 'False':
                text_name = db.child("users").child(text_email.replace(".", ",")).child("Info").get().val()["fullname"]
            else:
                pass
    except Exception as e:
        print(e)
        text_email = ""
        text_password = ""
        text_bool = ""
        text_name = ""

    def __init__(self, **kwargs):  # Initialisation of app
        self.title = "SSTOrder"
        super().__init__(**kwargs)

        # Dialog box for confirmation of order
        self.order_dialog = MDDialog(title="Confirmation",
                                     radius=[50],
                                     text="Are you sure you want to place your order?",
                                     buttons=[MDFlatButton(text="Cancel",
                                                           on_release=self.close_order_confirmation_dialog),
                                              MDFlatButton(text="Confirm!",
                                                           on_release=self.confirm_order_confirmation_dialog)])

    # Written by Jun Seng
    def build(self):  # Building the App's code
        self.root = Builder.load_string(kv_string)  # Loading the multiline string
        self.firebaseAuth = FirebaseAuth
        FirebaseAuth.login_current_user(self)

        if self.text_bool == "True":

            if self.text_email != "":
                # Loading statistics screen for vendors
                Clock.schedule_once(self.dataScreen, 1)
                self.dataSreen_clock = Clock.schedule_interval(self.dataScreen, 10)

                # Refresh pending orders for vendors
                self.refresh_vendor_pending_orders()
                self.refresh_pending_orders_clock = Clock.schedule_interval(self.refresh_vendor_pending_orders, 10)


                # Statistics
                self.get_stats()
                self.get_stats_clock = Clock.schedule_interval(self.get_stats, 10)
                Clock.start_clock()

            # Load menu for vendors
            self.load_items()

        else:
            # Instantiate user orders
            if self.text_email != "":
                self.load_user_orders()
                self.clock1 = Clock.schedule_interval(self.load_user_orders, 10)
                print("bruh")
                Clock.start_clock()

            # Instantiate order preview
            self.orderpreview()

            # Instantiate ordering screens
            self.load_user_stalls()

            # Load account info
            self.load_profile()

    # Written by Jun Seng
    def go_back_to_menu(self):  # Function for going back to the user main screen (Written by Kai Jun)
        self.root.transition.direction = "right"
        self.root.current = "main_screen"

        self.selected_stall_email = ""

        self.selected_main = ""
        self.selected_main_cost = 0

    # Written by Jun Seng
    def after_ordering(self):  # Function for after confirmation of order (Written by Kai Jun)

        self.root.transition.direction = "right"
        self.root.current = "main_screen"

        self.selected_stall_email = ""

        self.selected_sides = ["No sides selected"]
        self.selected_sides_cost = 0

        self.selected_main = ""
        self.selected_main_cost = 0

        self.order_dialog.dismiss()
        toast("Order Placed!")

    # Written by Jun Seng
    def go_back_to_mains(self):  # Function for going back to user menu screen (Written by Kai Jun)
        self.root.transition.direction = "right"
        self.root.current = "main_menu_screen"

        self.selected_sides = ["No sides selected"]
        self.selected_sides_cost = 0

    # Written by Jun Seng
    def load_profile(self):  # Load user profile, namecard
        self.root.ids.main_screen.ids.name_var.text = self.text_name
        self.root.ids.main_screen.ids.email_var.text = self.text_email.replace(",", ".")

    # Written by Kai Jun, edited by Jun Seng
    def checkbox_state(self, checkbox,
                       value):  # Function for adding functionality to checkbox for sides menu (Written by Kai Jun)

        if value:
            self.selected_sides.append(str(checkbox.parent.children[1].children[1].text))

            self.selected_sides_cost += float(str(checkbox.parent.children[1].children[0].text).replace("Cost: $", ""))
        else:
            self.selected_sides.pop(-1)
            if len(self.selected_sides) == 0:
                self.selected_sides = ["No sides selected"]
                self.selected_sides_cost -= float(
                    str(checkbox.parent.children[1].children[0].text).replace("Cost: $", ""))
            else:
                self.selected_sides_cost -= float(
                    str(checkbox.parent.children[1].children[0].text).replace("Cost: $", ""))

        self.orderpreview()

    # Written by Kai Jun, edited by Jun Seng and Ying Xuan
    def load_user_stalls(self, *args):  # Function for loading the stalls (Written by Kai Jun)

        stall_info = []

        self.root.ids.main_screen.ids.stallsid.clear_widgets()
        self.stall_emails = self.db.child("vendors").shallow().get().val()

        self.stall_emails = list(self.stall_emails)

        for email in self.stall_emails:
            stall_info.append(self.db.child("vendors").child(email).child("StallInfo").get().val())

        for i in range(len(self.stall_emails)):
            stall_name = stall_info[i]["Name"]
            self.stall_names.append(stall_info[i]["Name"])
            stall_description = stall_info[i]["Description"]

            stall_card = MDCard(orientation="vertical",
                                padding=50,
                                radius=[50],
                                elevation=10)

            stall_boxlayout = BoxLayout(orientation='vertical',
                                        pos_hint={'center_x': 0.5},
                                        spacing=30)

            id_label = MDLabel(text=str(i),
                               height=0,
                               font_style="Overline",
                               text_color=[1, 1, 1, 1],
                               theme_text_color="Custom")

            name_label = MDLabel(text=stall_name,
                                 font_style="H6",
                                 halign="left")

            description_label = MDLabel(text=stall_description,
                                        font_style="Subtitle2",
                                        halign="left")

            stall_boxlayout.add_widget(id_label)
            stall_boxlayout.add_widget(name_label)
            stall_boxlayout.add_widget(description_label)
            stall_boxlayout.add_widget(MainMenuButton())
            stall_card.add_widget(stall_boxlayout)

            self.root.ids.main_screen.ids.stallsid.add_widget(stall_card)
        pass

    # Written by Kai Jun, edited by Jun Seng and Ying Xuan
    def load_user_mains(self):  # Function for loading the main dishes for the stall selected (Written by Kai Jun)
        self.root.ids.main_menu_screen.ids.mainmenuid.clear_widgets()

        stall_mains = self.db.child("vendors").child(self.selected_stall_email).child("Menu").child(
            "Main").shallow().get().val()

        stall_mains = list(stall_mains)

        for i in range(len(stall_mains)):
            main_name = stall_mains[i]
            main_cost = "{:.2f}".format(float(
                self.db.child("vendors").child(self.selected_stall_email).child("Menu").child("Main").child(
                    main_name).child(
                    "Cost").get().val()))

            main_card = MDCard(orientation='vertical',
                               pos_hint={'center_x': .5, 'center_y': .7},
                               size_hint=(.9, None),
                               padding=30,
                               elevation=10,
                               radius=[50])

            main_boxlayout = BoxLayout(spacing='20',
                                       orientation='vertical',
                                       size_hint_y=None,
                                       pos_hint={'center_x': 0.5, "center_y": 0.5})

            name_label = MDLabel(text=main_name,
                                 bold=True,
                                 font_style='H6',
                                 adaptive_height=True)

            cost_label = MDLabel(text="Cost: $" + str(main_cost),
                                 bold=False,
                                 font_style='Subtitle1',
                                 adaptive_height=True)

            main_boxlayout.add_widget(name_label)
            main_boxlayout.add_widget(cost_label)
            main_boxlayout.add_widget(MainMenuOrder())
            main_card.add_widget(main_boxlayout)
            main_card.height = main_card.height * 2.6

            self.root.ids.main_menu_screen.ids.mainmenuid.add_widget(main_card)

        pass

    # Written by Kai Jun, edited by Jun Seng and Ying Xuan
    def load_user_sides(self):  # Function for loading the sides for the stall selected (Written by Kai Jun)

        self.orderpreview()

        self.root.ids.side_menu_screen.ids.sidesmenuid.clear_widgets()

        stall_sides = self.db.child("vendors").child(self.selected_stall_email).child("Menu").child(
            "Sides").shallow().get().val()

        stall_sides = list(stall_sides)

        for i in range(len(stall_sides)):
            side_name = stall_sides[i]
            side_cost = "{:.2f}".format(float(
                self.db.child("vendors").child(self.selected_stall_email).child("Menu").child("Sides").child(
                    side_name).child(
                    "Cost").get().val()))

            side_card = MDCard(orientation='vertical',
                               pos_hint={'center_x': .5, 'center_y': .7},
                               size_hint=(.9, None),
                               padding=30,
                               elevation=10,
                               radius=[50])

            side_boxlayout = BoxLayout(spacing='20',
                                       orientation='vertical',
                                       size_hint_y=None,
                                       pos_hint={'center_x': 0.5, "center_y": 0.5})

            hori_box = BoxLayout(spacing='20',
                                 orientation='horizontal',
                                 size_hint_y=None,
                                 pos_hint={'center_x': 0.5, "center_y": 0.5})

            side_name = MDLabel(text=side_name,
                                bold=True,
                                font_style='H6',
                                adaptive_height=True)

            side_cost = MDLabel(text="Cost: $" + str(side_cost),
                                bold=False,
                                font_style='Subtitle1',
                                adaptive_height=True)

            side_boxlayout.add_widget(side_name)
            side_boxlayout.add_widget(side_cost)
            hori_box.add_widget(side_boxlayout)
            hori_box.add_widget(SidesCheckBox())
            side_card.add_widget(hori_box)
            side_card.height = side_card.height * 1.8

            self.root.ids.side_menu_screen.ids.sidesmenuid.add_widget(side_card)
        pass

    # Written by Jun Seng
    def on_stall_click(self, stall_id):  # Function for getting stall id for selected stall
        self.root.transition.direction = "left"
        self.selected_stall_email = self.stall_emails[int(stall_id)]
        self.selected_stall_name = self.stall_names[int(stall_id)]
        self.load_user_mains()
        self.root.current = "main_menu_screen"
        pass

    # Written by Jun Seng
    def on_main_click(self, obj):  # Function for getting data for selected main dish
        self.root.transition.direction = "left"
        self.selected_main = obj.parent.children[2].text
        self.selected_main_cost = float((obj.parent.children[1].text).replace("Cost: $", ""))
        self.load_user_sides()
        self.root.current = "side_menu_screen"
        pass

    # Written by Kai Jun, edited by Jun Seng and Ying Xuan
    def orderpreview(self):  # Preview of order at sides menu screen (Written by Kai Jun)
        self.root.ids.side_menu_screen.ids.orderpreview.clear_widgets()

        mainlabel = MDLabel(text="Main: " + self.selected_main,
                            halign="left")

        self.root.ids.side_menu_screen.ids.orderpreview.add_widget(mainlabel)
        if len(self.selected_sides) == 1:
            sideslabel = MDLabel(text="- " + str(self.selected_sides[0]),
                                 halign="left")
            self.root.ids.side_menu_screen.ids.orderpreview.add_widget(sideslabel)
        else:
            for i in range(len(self.selected_sides) - 1):
                sideslabel = MDLabel(text="- " + str(self.selected_sides[i + 1]),
                                     halign="left")
                self.root.ids.side_menu_screen.ids.orderpreview.add_widget(sideslabel)

        costlabel = MDLabel(
            text="Total Cost: $" + str("{:.2f}".format(self.selected_sides_cost + self.selected_main_cost)),
            halign="right")

        self.root.ids.side_menu_screen.ids.orderpreview.add_widget(costlabel)
        self.root.ids.side_menu_screen.ids.orderpreview.add_widget(OrderButton())

    # Written by Kai Jun, edited by Jun Seng
    def close_order_confirmation_dialog(self, *args):  # Function for closing dialog confirming orders
        self.order_dialog.dismiss()

    # Written by Kai Jun, edited by Jun Seng
    def place_order(self):  # Function for opening dialog confirming order
        self.order_dialog.open()

    # Written by Kai Jun, edited by Jun Seng
    def confirm_order_confirmation_dialog(self,
                                          obj):  # Function for the functionality of the dialog confirming of order

        timestamp = datetime.now().strftime("%d,%m,%Y %H,%M,%S")
        self.selected_sides.pop(0)
        strsidesnames = ",".join(self.selected_sides)
        if len(strsidesnames) == 0:
            strsidesnames = "No sides selected"

        totalcost = float("{:.2f}".format(self.selected_main_cost + self.selected_sides_cost))

        # Writing to database (User)
        userorderdata = {"Stall Name": self.selected_stall_name,
                         "Main": self.selected_main, "Sides": strsidesnames, "Status": "Incomplete",
                         "Total Cost": totalcost}

        self.db.child("users").child(self.text_email).child("Orders").child(timestamp).set(userorderdata)

        # Writing to database (Vendor)
        vendororderdata = {"Customer": self.db.child("users").child(self.text_email).child("Info").child("fullname").get().val(),
                           "Customer Email": self.text_email, "Main": self.selected_main,
                           "Sides": strsidesnames,
                           "Total Cost": totalcost}
        self.db.child("vendors").child(self.selected_stall_email).child("Pending").child(timestamp).set(vendororderdata)

        self.after_ordering()

    # Written by Jun Seng
    def get_menu_main_name(self, obj):  # Removes selected main and removes it from database and app

        main_name = obj.parent.children[2].text

        self.db.child("vendors").child(self.text_email).child("Menu").child("Main").child(main_name).remove()
        App.get_running_app().root.ids.vendor_screen.ids.main_listboii.remove_widget(obj.parent.parent)
        pass

    # Written by Jun Seng
    def get_menu_side_name(self, obj):  # Removes selected side and removes it from database and app
        side_name = obj.parent.children[2].text

        self.db.child("vendors").child(self.text_email).child("Menu").child("Sides").child(side_name).remove()
        App.get_running_app().root.ids.vendor_screen.ids.side_listboii.remove_widget(obj.parent.parent)
        pass

    # Written by Jun Seng, Kai Jun and Ying Xuan
    def load_user_orders(self, *args):  # Function for loading the orders of the user (Written by Kai Jun)

        # clear list before loading
        self.root.ids.main_screen.ids.ordersid.clear_widgets()

        # gets the list of data
        getorderdata = self.db.child("users").child(self.text_email).child("Orders").shallow().get().val()
        getorderdata = list(getorderdata)
        templatedata = list(getorderdata).pop(-1)

        # iterate through the entire list
        for i in range(1, len(getorderdata)):

            # reformat data
            timestamp = str(getorderdata[-1 - i])
            getorderkey = str(getorderdata[-1 - i]).split()
            date = str(getorderkey[0]).replace(",", "/")
            time = str(getorderkey[1]).replace(",", ":")

            # get timestamp
            getordervalue = self.db.child("users").child(self.text_email).child("Orders").child(timestamp).get().val()
            print(getordervalue.keys())

            stallnameval = getordervalue["Stall Name"]
            mainval = getordervalue["Main"]
            sidesval = getordervalue["Sides"]
            sidesval = sidesval.split(",")
            statusval = getordervalue["Status"]
            costval = getordervalue["Total Cost"]

            # add widgets for the items in the list
            ordercard = MDCard(orientation="vertical",
                               padding=50,
                               radius=[50],
                               elevation=10)

            boxlayout = BoxLayout(orientation='vertical',
                                  pos_hint={'center_x': 0.5})

            stalllabel = MDLabel(text=stallnameval,
                                 halign="left",
                                 font_style="H6")

            mainlabel = MDLabel(text=mainval,
                                halign="left",
                                font_style="Body1")

            statuslabel = MDLabel(text="Order Status: " + statusval,
                                  halign="right",
                                  font_style="Subtitle2")

            costlabel = MDLabel(text="Total Cost: $" + str("{:.2f}".format(costval)),
                                halign="right",
                                font_style="Subtitle2")

            timelabel = MDLabel(text="Time Ordered: " + date + " " + time,
                                halign="right",
                                font_style="Caption")

            # add widgets to the boxlayout
            boxlayout.add_widget(stalllabel)
            boxlayout.add_widget(mainlabel)

            # iterate through sides
            for i in sidesval:
                sideslabel = MDLabel(text="- " + str(i),
                                     halign="left",
                                     font_style="Body2"
                                     )
                boxlayout.add_widget(sideslabel)

            # add widgets to the boxlayout
            boxlayout.add_widget(statuslabel)
            boxlayout.add_widget(costlabel)
            boxlayout.add_widget(timelabel)
            ordercard.add_widget(boxlayout)
            ordercard.height = ordercard.minimum_height*2.6

            # add widget to the list in the screen
            self.root.ids.main_screen.ids.ordersid.add_widget(ordercard)

        # timestamp = str(templatedata)
        # getorderkey = str(templatedata).split()
        # date = str(getorderkey[0]).replace(",", "/")
        # time = str(getorderkey[1]).replace(",", ":")
        #
        # getordervalue = self.db.child("users").child(self.text_email).child("Orders").child(timestamp).get().val()
        # stallnameval = getordervalue["Stall Name"]
        # mainval = getordervalue["Main"]
        # sidesval = getordervalue["Sides"]
        # statusval = getordervalue["Status"]
        # costval = getordervalue["Total Cost"]
        #
        # # adds widgets for the items in the list
        # ordercard = MDCard(orientation="vertical",
        #                   padding=20,
        #                   radius=[50],
        #                   elevation=10)
        #
        # boxlayout = BoxLayout(orientation='vertical',
        #                      pos_hint={'center_x': 0.5})
        #
        # stalllabel = MDLabel(text=stallnameval,
        #                     halign="left",
        #                     font_style="H6")
        #
        # sidesval2 = MDLabel(text=stallnameval,
        #                   halign="left",
        #                   font_style="Body2")
        #
        # mainlabel = MDLabel(text=mainval,
        #                    halign="left",
        #                    font_style="Body1")
        #
        # statuslabel = MDLabel(text="Order Status: " + statusval,
        #                      halign="right",
        #                      font_style="Subtitle2")
        #
        # costlabel = MDLabel(text="Total Cost: $" + str("{:.2f}".format(costval)),
        #                    halign="right",
        #                    font_style="Subtitle2")
        #
        # timelabel = MDLabel(text="Time Ordered: " + date + " " + time,
        #                    halign="right",
        #                    font_style="Caption")
        #
        # # add widgets to the boxlayout
        # boxlayout.add_widget(stalllabel)
        # boxlayout.add_widget(mainlabel)
        # boxlayout.add_widget(sidesval2)
        # boxlayout.add_widget(statuslabel)
        # boxlayout.add_widget(costlabel)
        # boxlayout.add_widget(timelabel)
        # ordercard.add_widget(boxlayout)



        # add widgets to the list in the screen
        # self.root.ids.main_screen.ids.ordersid.add_widget(ordercard)

    # Written by Jun Seng
    def close_dialog(self, *args):  # Closing dialog box for adding new menu item
        self.dialog.dismiss()

    # Written by Jun Seng, edited by Kai Jun and Ying Xuan
    def load_orders(self):  # Load orders to vendor screens

        App.get_running_app().root.ids.vendor_screen.ids.order_listboii.clear_widgets()

        # Menu part
        menu1 = self.db.child('vendors').child(self.text_email).child('Pending').get()
        lst = []
        try:

            # iterate through menu items and append to list
            for food in menu1.each():
                path = self.db.child('vendors').child(self.text_email).child('Pending').child(food.key()).get().val()
                lst.append(list(path.items()))

            lst = [dict(i) for i in lst]
            for i in range(len(lst)):
                # reformat time
                lst[i]['Time'] = lst[i]['Time'].replace(',', ':')
                lst[i]['Time'] = lst[i]['Time'].replace(':', '/', 2)

            for i in range(len(lst)):
                # add widgets for the items
                order_card = MDCard(orientation='vertical',
                                    pos_hint={'center_x': .5, 'center_y': .7},
                                    size_hint=(.9, None),
                                    padding=30,
                                    radius=[50])
                order_boxlayout = MDBoxLayout(spacing='5',
                                              orientation='vertical',
                                              pos_hint={'center_x': 0.5, "center_y": 0.5})

                order_buyer_label = MDLabel(text=lst[i]['Buyer'],
                                            bold=True,
                                            halign="left",
                                            font_style='H6',
                                            adaptive_height=True)

                order_boxlayout.add_widget(order_buyer_label)

                try:
                    mainFood = MDLabel(text=list(lst[i]['Main'].keys())[0],
                                       halign="left")
                    order_boxlayout.add_widget(mainFood)
                except KeyError:
                    pass
                try:
                    for side in lst[i]['Sides']:
                        sideFood = MDLabel(text='   - ' + side,
                                           adaptive_height=True)
                        order_boxlayout.add_widget(sideFood)
                except KeyError:
                    # prevent crashes
                    pass
                else:
                    pass

                totalCost = MDLabel(text='$' + format(lst[i]['TotalCost'], '.2f'), )

                # add widgets to order box layout
                order_boxlayout.add_widget(totalCost)
                order_boxlayout.add_widget(delete())
                order_boxlayout.add_widget(MDLabel(text=lst[i]['Time'],
                                                   halign="left",
                                                   adaptive_height=True))

                order_card.add_widget(order_boxlayout)

                # changes height to make design correct
                order_card.height = order_card.height * 2.6

                # add widgets to the items
                App.get_running_app().root.ids.vendor_screen.ids.order_listboii.add_widget(order_card)
        except:
            pass

    # Written by Jun Seng, edited by Kai Jun and Ying Xuan
    def load_items(self):  # Load menu items to update list
        app = App.get_running_app()
        # Clears data in main and sides screen
        app.root.ids.vendor_screen.ids.main_listboii.clear_widgets()
        app.root.ids.vendor_screen.ids.side_listboii.clear_widgets()

        # Get data from database
        all_main = self.db.child("vendors").child(self.text_email).child("Menu").child("Main").get()
        all_sides = self.db.child("vendors").child(self.text_email).child("Menu").child("Sides").get()

        try:
            # loop through list and add values to their respective lists
            for main in all_main.each():
                self.main_list.append(main.key())
                self.main_cost_list.append(main.val()["Cost"])

        except Exception as e:
            print(e)

            # this means that the list is empty or there are no orders
            self.main_list = []
            self.main_cost_list = []

        try:
            for side in all_sides.each():
                self.side_list.append(side.key())
                self.side_cost_list.append(side.val()["Cost"])

        except Exception as e:
            print(e)
            self.side_list = []
            self.side_cost_list = []

        if self.main_list != []:

            # iterates through every object in main list
            for i in range(len(self.main_list)):
                # add widgets to the main list
                main_card = MDCard(orientation='vertical',
                                   pos_hint={'center_x': .5, 'center_y': .7},
                                   size_hint=(.9, None),
                                   elevation=10,
                                   padding=30,
                                   radius=[50])

                main_boxlayout = MDBoxLayout(spacing='20',
                                             orientation='vertical',
                                             size_hint_y=None,
                                             pos_hint={'center_x': 0.5, "center_y": 0.5})

                main_name_label = MDLabel(text=str(self.main_list[i]),
                                          bold=True,
                                          font_style='H6',
                                          adaptive_height=True)

                main_cost_label = MDLabel(text=str("Cost: $" + "{:.2f}".format(self.main_cost_list[i])),
                                          halign="left",
                                          bold=False,
                                          font_style='Subtitle1',
                                          adaptive_height=True)

                delete_main_button = MDFillRoundFlatButton(text="Delete",
                                                           on_release=self.get_menu_main_name,
                                                           size_hint_x=1)

                # adding object to list
                main_boxlayout.add_widget(main_name_label)
                main_boxlayout.add_widget(main_cost_label)
                main_boxlayout.add_widget(delete_main_button)
                main_card.add_widget(main_boxlayout)

                # changes height
                main_card.height = main_card.height * 2.6
                app.root.ids["vendor_screen"].ids["main_listboii"].add_widget(main_card)

        if self.side_list != []:
            # iterates through every object in the side list
            for j in range(len(self.side_list)):
                # add widgets to the side list
                side_card = MDCard(orientation='vertical',
                                   pos_hint={'center_x': .5, 'center_y': .7},
                                   size_hint=(.9, None),
                                   padding=30,
                                   radius=[50])

                side_boxlayout = MDBoxLayout(spacing='20',
                                             orientation='vertical',
                                             size_hint=(1, None),
                                             pos_hint={'center_x': 0.5, "center_y": 0.5})

                side_name_label = MDLabel(text=str(self.side_list[j]),
                                          bold=True,
                                          font_style='H6',
                                          adaptive_height=True)

                side_cost_label = MDLabel(text=str("Cost: $" + "{:.2f}".format(self.side_cost_list[j])),
                                          halign="left",
                                          bold=False,
                                          font_style='Subtitle1',
                                          adaptive_height=True)

                delete_side_button = MDFillRoundFlatButton(text="Delete",
                                                           on_release=self.get_menu_side_name)

                # add widget to side list
                side_boxlayout.add_widget(side_name_label)
                side_boxlayout.add_widget(side_cost_label)
                side_boxlayout.add_widget(delete_side_button)
                side_card.add_widget(side_boxlayout)
                side_card.height = side_card.height * 2.6
                app.root.ids["vendor_screen"].ids["side_listboii"].add_widget(side_card)

    # Refreshes graphs
    # Written by Ying Xuan, edited by Kai Jun and Jun Seng
    def dataScreen(self, *args):
        # Clears previous graphs
        self.root.ids.vendor_screen.ids.earnings_graph.clear_widgets()
        self.root.ids.vendor_screen.ids.main_graph.clear_widgets()
        self.root.ids.vendor_screen.ids.sides_graph.clear_widgets()

        list1 = []
        list2 = []

        all_users = FirebaseAuth.db.child("users").get()
        for user in all_users.each():
            list1.append(user.key())

        all_vendors = FirebaseAuth.db.child("vendors").get()
        for vendor in all_vendors.each():
            list2.append(vendor.key())
        # Get stats data from database
        if self.text_email in list2:
            barGraphData = self.db.child('vendors').child(self.text_email).child('Stats').child('Daily').get()
            bar_data = {}
            items = []

            # Adds date for each data in barGraphData
            for item in barGraphData.each():
                items.append(item.key())

            # Adds graph only if there is no dummy data (only happens when there are no orders at all)
            if items == ['99,99,9999']:
                self.root.ids.vendor_screen.ids.earnings_graph.add_widget(MDLabel(text='No Data',
                                                                                  font_style="H5",
                                                                                  halign="center",
                                                                                  bold=True))
                self.root.ids.vendor_screen.ids.main_graph.add_widget(MDLabel(text='No Data',
                                                                              font_style="H5",
                                                                              halign="center",
                                                                              bold=True))
                self.root.ids.vendor_screen.ids.sides_graph.add_widget(MDLabel(text='No Data',
                                                                               font_style="H5",
                                                                               halign="center",
                                                                               bold=True))
            else:
                # Code for creating the bar plot
                for date in barGraphData.each()[-7:]:
                    bar_data[date.key()] = date.val()['Total Cost']['Cost']

                days = list(bar_data.keys())
                if '99,99,9999' in days:
                    days.remove('99,99,9999')

                for i in range(len(days)):
                    day = (calendar.day_name[datetime.strptime(days[i].replace(',', ' '), '%d %m %Y').weekday()])
                    days[i].replace(' ', '/')
                    days[i] += '\n' + day

                price = list(bar_data.values())

                plt.figure(figsize=(10, 5))

                plt.bar(days, price,
                        color='teal',
                        width=0.5)

                # Adds more ticks on y-axis
                plt.yticks(np.arange(0, max(price) + 1, 2.0))
                plt.xlabel("Past 7 Days")
                plt.ylabel("Total Earnings Daily / $")
                plt.title("Earnings Past 7 days")
                for i in range(len(price)):
                    plt.text(i, price[i], price[i], ha='center', va='bottom')
                self.root.ids.vendor_screen.ids.earnings_graph.add_widget(MDLabel(height=80,
                                                                                  font_style="H5",
                                                                                  size_hint_y=None,
                                                                                  bold=True,
                                                                                  text="Total Earnings (Past Week)"))

                # Adds bar graph to card
                self.root.ids.vendor_screen.ids.earnings_graph.add_widget(FigureCanvas(plt.gcf()))

                # Main dish pie chart
                mainPieData = barGraphData.each()[-1].val()['Main']
                mains = list(mainPieData.keys())
                num1 = list(mainPieData.values())
                fig = plt.figure(figsize=(10, 8))
                plt.pie(num1, labels=mains, autopct='%1.1f%%')
                plt.title('Main dishes sold today')

                # plt.axis('equal')
                self.root.ids.vendor_screen.ids.main_graph.add_widget(MDLabel(height=80,
                                                                              font_style="H5",
                                                                              size_hint_y=None,
                                                                              bold=True,
                                                                              text="Main Dish Graph (For Today)"))

                # Adds main dish pie chart to card
                self.root.ids.vendor_screen.ids.main_graph.add_widget(FigureCanvas(plt.gcf()))

                # Side dish pie chart
                sidesPieData = barGraphData.each()[-1].val()['Sides']
                sides = list(sidesPieData.keys())
                num2 = list(sidesPieData.values())
                fig = plt.figure(figsize=(10, 8))
                plt.pie(num2, labels=sides, autopct='%1.1f%%')
                plt.title('Side dishes sold today')
                self.root.ids.vendor_screen.ids.sides_graph.add_widget(MDLabel(height=80,
                                                                               font_style="H5",
                                                                               size_hint_y=None,
                                                                               bold=True,
                                                                               text="Side Dish Graph (For Today)"))

                # Adds side dish pie chart to card
                self.root.ids.vendor_screen.ids.sides_graph.add_widget(FigureCanvas(plt.gcf()))
        else:
            pass

    # Written by Jun Seng
    def item_add(self):

        # Add new menu item dialog
        self.dialog = MDDialog(title='Item details', type='custom',
                               content_cls=Content(),
                               buttons=[MDFlatButton(text='Cancel', on_release=
                               self.close_dialog),
                                        MDFlatButton(text='Add!', on_release=self.add_item_to_list)])

        # Dropdown menu to select dish type when creating new menu item
        self.menu = MDDropdownMenu(
            size_hint=(1, None),
            items=[{"viewclass": "OneLineListItem", "text": "Main Dish",
                    "on_release": lambda x=f"Main Dish": self.menu_callback(x)},
                   {"viewclass": "OneLineListItem", "text": "Side Dish",
                    "on_release": lambda x=f"Side Dish": self.menu_callback(x)}],
            caller=self.dialog.content_cls.ids.dish_type,
            width_mult=2)

        self.dialog.open()

    # Written by Jun Seng
    def menu_callback(self, text_item):
        self.dialog.content_cls.ids.dish_type.text = text_item
        self.menu.dismiss()

    # Written by Jun Seng
    def add_item_to_list(self, obj):

        app = App.get_running_app()

        def check_float(number):
            try:
                float(number)
                return True
            except ValueError:
                return False

        with open("login_data.txt", "r") as f:
            data = f.readlines()
            vendor_email = data[0].strip().replace(".", ",")

        # Validation
        if ((self.dialog.content_cls.ids["item"].text).strip() == ""):
            toast("Item name cannot be empty!")
            return

        if ((self.dialog.content_cls.ids["price"].text).strip() == ""):
            toast("Price cannot be empty")
            return

        if not (check_float(self.dialog.content_cls.ids["price"].text)):
            toast("Price needs to be a number!")
            return

        if self.dialog.content_cls.ids.dish_type.text == "Dish Type":
            toast("Dish type needs to selected!")
            return

        menu_cost = float(self.dialog.content_cls.ids["price"].text)
        item_name = self.dialog.content_cls.ids["item"].text.strip().title()

        # Adds accordingly to dish type chosen
        if self.dialog.content_cls.ids.dish_type.text == "Main Dish":
            dish = "Main"

            main_card = MDCard(orientation='vertical',
                               pos_hint={'center_x': .5, 'center_y': .7},
                               size_hint=(.9, None),
                               padding=30,
                               radius=[50])

            main_boxlayout = MDBoxLayout(spacing='5',
                                         orientation='vertical',
                                         size_hint_y=None,
                                         pos_hint={'center_x': 0.5, "center_y": 0.5})

            main_name_label = MDLabel(text=str(item_name),
                                      bold=True,
                                      font_style='H6',
                                      adaptive_height=True)

            main_cost_label = MDLabel(text=str("Cost: $" + "{:.2f}".format(menu_cost)),
                                      halign="left",
                                      adaptive_height=True)

            delete_main_button = MDFillRoundFlatButton(text="Delete",
                                                       on_release=self.get_menu_main_name)

            # Adds item to menu screen
            main_boxlayout.add_widget(main_name_label)
            main_boxlayout.add_widget(main_cost_label)
            main_boxlayout.add_widget(delete_main_button)
            main_card.add_widget(main_boxlayout)
            main_card.height = main_card.height * 2.4
            app.root.ids["vendor_screen"].ids["main_listboii"].add_widget(main_card)

            self.main_list.append(item_name)
            self.main_cost_list.append(menu_cost)
        else:
            dish = "Sides"

            side_card = MDCard(orientation='vertical',
                               pos_hint={'center_x': .5, 'center_y': .7},
                               size_hint=(.9, None),
                               # height=350,
                               padding=30,
                               radius=[50])

            side_boxlayout = MDBoxLayout(spacing='5',
                                         orientation='vertical',
                                         pos_hint={'center_x': 0.5})

            side_name_label = MDLabel(text=str(item_name),
                                      bold=True,
                                      font_style='H6')

            side_cost_label = MDLabel(text=str(menu_cost),
                                      bold=True,
                                      font_style='H6')

            delete_side_button = MDFillRoundFlatButton(text="Delete",
                                                       on_release=self.get_menu_side_name)

            # Adds item to menu screen
            side_boxlayout.add_widget(side_name_label)
            side_boxlayout.add_widget(side_cost_label)
            side_boxlayout.add_widget(delete_side_button)
            side_card.add_widget(side_boxlayout)
            app.root.ids["vendor_screen"].ids["side_listboii"].add_widget(side_card)

            self.side_list.append(item_name)
            self.side_cost_list.append(menu_cost)

        # Adds the item added to database
        self.db.child("vendors").child(self.text_email).child("Menu").child(dish).child(item_name.title()).set(
            {"Cost": menu_cost})
        self.dialog.dismiss()

    # Written by Ying Xuan, edited by Jun Seng and Kai Jun
    def remove_widget(self, obj):  # removes the order widget from the vendor pending orders section

        # removes the parent of the parent of the object being casted into the argument
        self.root.get_screen('vendor_screen').ids.order_listboii.remove_widget(obj.parent.parent)
        # makes sure that the date is in the correct format
        times = obj.parent.children[0].text.replace(':', ',').replace('/', ',')

        # finds the name of the widget about to be deleted
        user = obj.parent.children[-2].text.lower()

        # changes pending order in database to completed instead of pending
        self.db.child("users").child(user.replace(".", ",")).child('Orders').child(times).child("Status").set(
            "Completed")
        try:
            menu_items1 = dict(
                self.db.child('vendors').child(self.text_email).child('Pending').child(times).get().val())
            self.db.child('vendors').child(self.text_email).child('Completed').child(times).set(menu_items1)
        except TypeError:
            # makes sure that errors do not crash the app
            pass

        # remove the object from the database
        self.db.child('vendors').child(self.text_email).child('Pending').child(times).remove()

    # Written by Jun Seng, edited by Kai Jun and Ying Xuan
    def remove_item(self, obj, section_string):  # Remove item from main or side menu for vendor
        if section_string == "Main":
            # finds position of main dish object to be deleted
            indexboi = self.main_list.index(obj.text)

            # remove object from the list in the screen
            self.root.ids["vendor_screen"].ids["main_listboii"].remove_widget(obj)

            # remove the objects from the arrays
            self.main_list.pop(indexboi)
            self.main_cost_list.pop(indexboi)
        else:
            # finds position of main dish object to be deleted
            indexboi = self.side_list.index(obj.text)

            # remove object frmo the list in the screen
            self.root.ids.vendor_screen.ids.side_listboii.remove_widget(obj)

            # remove the objects from the arrays
            self.side_list.pop(indexboi)
            self.side_cost_list.pop(indexboi)

        # remove the object from the database
        self.db.child("vendors").child(self.text_email).child('Menu').child(section_string).child(obj.text).remove()

    # Written by Ying Xuan, edited by Jun Seng and Kai Jun
    def refresh_vendor_pending_orders(self, *args):  # Refresh vendor pending orders
        list1 = []
        list2 = []

        all_users = FirebaseAuth.db.child("users").get()
        for user in all_users.each():
            list1.append(user.key())

        all_vendors = FirebaseAuth.db.child("vendors").get()
        for vendor in all_vendors.each():
            list2.append(vendor.key())
        # Get stats data from database
        if self.text_email in list2:

            # makes sure that the lists are empty before adding more widgets upon loading
            self.root.ids.vendor_screen.ids.order_listboii.clear_widgets()

            # get a list of dictionaries of user objects from the databse
            menu1 = self.db.child('vendors').child(self.text_email).child('Pending').get()

            # declare arrays in the function (scope is limited so it can only be used in this function)
            lst = []
            times = []

            # iterate through every object in the pending section and adds them to the arrays
            for food in menu1.each():
                path = self.db.child('vendors').child(self.text_email).child('Pending').child(food.key()).get().val()
                times.append(food.key())
                lst.append(list(path.items()))

            # convert a dictionary into an array
            lst = [dict(i) for i in lst[:-1]]

            # iterate through the list and reformats the time
            for i in range(len(lst)):
                lst[i]['Time'] = times[i]
                lst[i]['Time'] = lst[i]['Time'].replace(',', ':')
                lst[i]['Time'] = lst[i]['Time'].replace(':', '/', 2)

            # iterate through the list and adds the individual orders in the form of a gui into the list
            for i in range(len(lst)):
                card = MDCard(orientation='vertical',
                              pos_hint={'center_x': .5, 'center_y': .7},
                              size_hint=(.9, None),
                              padding=30,
                              radius=[50],
                              elevation=10)

                boxlayout_card = MDBoxLayout(spacing='12',
                                             orientation='vertical',
                                             pos_hint={'center_x': 0.6}
                                             )

                user_title = MDLabel(text=lst[i]['Customer'],
                                     bold=True,
                                     font_style='H6',
                                     adaptive_height=True
                                     )

                boxlayout_card.add_widget(user_title)
                user_email = MDLabel(text=lst[i]['Customer Email'].replace(",","."),
                                     font_style='Overline',
                                     adaptive_height=True,
                                     )

                # add widgets to the boxlayout
                boxlayout_card.add_widget(user_email)

                try:
                    mainFood = MDLabel(text=lst[i]['Main'])
                    boxlayout_card.add_widget(mainFood)
                except KeyError:
                    # makes sure that errors do not cause crashes
                    pass

                try:
                    for side in lst[i]['Sides'].split(','):
                        sideFood = MDLabel(text='   - ' + side)

                        # adds widgets to the boxlayout
                        boxlayout_card.add_widget(sideFood)
                except KeyError:
                    # makes sure that errors do not cause crashes
                    pass
                else:
                    # makes sure that errors do not cause crashes
                    pass

                # reformat the cost to 2dp and create a label object
                totalCost = MDLabel(text='$' + format(lst[i]['Total Cost'], '.2f'), )

                # add widgets to boxlayout
                boxlayout_card.add_widget(totalCost)
                boxlayout_card.add_widget(delete())
                boxlayout_card.add_widget(MDLabel(text=lst[i]['Time'],
                                                  font_style='Overline',
                                                  pos_hint={'right': 1.55}))

                # add boxlayout to the card
                card.add_widget(boxlayout_card)

                # makes sure that the height for the card is correct
                card.height = len([i.height for i in boxlayout_card.children]) * 62

                # ultimately adds the card object into the lsit in the ui
                self.root.ids.vendor_screen.ids.order_listboii.add_widget(card)
        else:
            pass

    # Function updates data under the 'Stats' node in database so that it can be used for the graphs
    # Written by Ying Xuan
    def get_stats(self, *args):
        try:
            # get completed orders from database in the form of dictionary objects
            data = self.db.child('vendors').child(self.text_email).child('Completed').get()

            # declare the stat dictionary
            stat = {}

            # iterate through every object in the dictionary
            for items in data.each()[:-1]:
                # adds order data to dictionary
                stat[items.key()[:10]] = {'Main': {}, 'Sides': {}, 'Total Cost': {'Cost': 0}}

            # iterates through every object in the dictionary
            for items in data.each()[:-1]:

                # accumulates the number of main dishes sold
                if items.val()['Main'] in stat[items.key()[:10]]['Main']:

                    # increase the number of main dishes sold in the dictionary
                    stat[items.key()[:10]]['Main'][items.val()['Main']] += 1

                else:

                    # changes main dishes sold to 1
                    stat[items.key()[:10]]['Main'][items.val()['Main']] = 1

                # makes sure that the sides are individual
                sides = items.val()['Sides'].split(',')

                # iterate through the new sides
                for i in sides:
                    if i in stat[items.key()[:10]]['Sides']:

                        stat[items.key()[:10]]['Sides'][i] += 1

                    else:
                        stat[items.key()[:10]]['Sides'][i] = 1
                if 'Total Cost' in stat[items.key()[:10]]:
                    stat[items.key()[:10]]['Total Cost']['Cost'] += items.val()['Total Cost']
                else:
                    stat[items.key()[:10]]['Total Cost']['Cost'] = items.val()['Total Cost']
        except TypeError:
            pass
        else:
            # Counter() to allow addition of dictionaries
            mainMonthly = Counter()
            sideMonthly = Counter()
            costMonthly = Counter()
            # Formating the data from 'stat'
            for key in stat:
                if key[3:] in mainMonthly:
                    mainMonthly[key[3:]] += Counter(stat[key]['Main'])
                else:
                    mainMonthly[key[3:]] = Counter(stat[key]['Main'])
                if key[3:] in sideMonthly:
                    sideMonthly[key[3:]] += Counter(stat[key]['Sides'])
                else:
                    sideMonthly[key[3:]] = Counter(stat[key]['Sides'])
                if key[3:] in costMonthly:
                    costMonthly[key[3:]] += Counter(stat[key]['Total Cost'])
                else:
                    costMonthly[key[3:]] = Counter(stat[key]['Total Cost'])

            # Counter() to allow addition of dictionaries
            mainYearly = Counter()
            sideYearly = Counter()
            costYearly = Counter()
            # Formating the data from 'stat'
            for key in mainMonthly:
                if key[3:] in mainYearly:
                    mainYearly[key[3:]] += mainMonthly[key]
                else:
                    mainYearly[key[3:]] = mainMonthly[key]
                if key[3:] in sideYearly:
                    sideYearly[key[3:]] += sideMonthly[key]
                else:
                    sideYearly[key[3:]] = sideMonthly[key]
                if key[3:] in costYearly:
                    costYearly[key[3:]] += costMonthly[key]
                else:
                    costYearly[key[3:]] = costMonthly[key]

            # Change back to dictionary
            mainMonthly = dict(mainMonthly)
            sideMonthly = dict(sideMonthly)
            costMonthly = dict(costMonthly)
            mainYearly = dict(mainYearly)
            sideYearly = dict(sideYearly)
            costYearly = dict(costYearly)

            for key in mainMonthly:
                mainMonthly[key] = dict(mainMonthly[key])
            for key in sideMonthly:
                sideMonthly[key] = dict(sideMonthly[key])
            for key in costMonthly:
                costMonthly[key] = dict(costMonthly[key])
            for key in mainYearly:
                mainYearly[key] = dict(mainYearly[key])
            for key in sideYearly:
                sideYearly[key] = dict(sideYearly[key])
            for key in costYearly:
                costYearly[key] = dict(costYearly[key])
            month = {}
            year = {}
            # Formating data received
            for key in mainMonthly:
                month[key] = {'Main': mainMonthly[key], 'Sides': sideMonthly[key], 'Total Cost': costMonthly[key]}
            for key in mainYearly:
                year[key] = {'Main': mainYearly[key], 'Sides': sideYearly[key], 'Total Cost': costYearly[key]}

            # Set data only if 'stat' is not empty
            if stat == {}:
                pass
            else:
                self.db.child('vendors').child(self.text_email).child('Stats').child('Monthly').set(month)
                self.db.child('vendors').child(self.text_email).child('Stats').child('Yearly').set(year)
                self.db.child('vendors').child(self.text_email).child('Stats').child('Daily').set(stat)

    # Function to retrieve data from database, the functions dailyData, monthlyData, yearlyData require this function for it to work
    # Written by Ying Xuan
    def getData(self):
        try:
            # Get Completed orders from database
            data = self.db.child('vendors').child(self.text_email).child('Completed').get()
            stat = {}
            # Formating the data received
            for items in data.each()[:-1]:
                stat[items.key()[:10]] = {'Main': {}, 'Sides': {}, 'Total Cost': {'Cost': 0}}
            for items in data.each()[:-1]:
                if items.val()['Main'] in stat[items.key()[:10]]['Main']:
                    stat[items.key()[:10]]['Main'][items.val()['Main']] += 1
                else:
                    stat[items.key()[:10]]['Main'][items.val()['Main']] = 1
                sides = items.val()['Sides'].split(',')
                for i in sides:
                    if i in stat[items.key()[:10]]['Sides']:
                        stat[items.key()[:10]]['Sides'][i] += 1
                    else:
                        stat[items.key()[:10]]['Sides'][i] = 1
                if 'Total Cost' in stat[items.key()[:10]]:
                    stat[items.key()[:10]]['Total Cost']['Cost'] += items.val()['Total Cost']
                else:
                    stat[items.key()[:10]]['Total Cost']['Cost'] = items.val()['Total Cost']
        except TypeError as e:
            pass
        else:
            # Counter() to allow addition of dictionaries
            mainMonthly = Counter()
            sideMonthly = Counter()
            costMonthly = Counter()
            # Formating the data from 'stat'
            for key in stat:
                if key[3:] in mainMonthly:
                    mainMonthly[key[3:]] += Counter(stat[key]['Main'])
                else:
                    mainMonthly[key[3:]] = Counter(stat[key]['Main'])
                if key[3:] in sideMonthly:
                    sideMonthly[key[3:]] += Counter(stat[key]['Sides'])
                else:
                    sideMonthly[key[3:]] = Counter(stat[key]['Sides'])
                if key[3:] in costMonthly:
                    costMonthly[key[3:]] += Counter(stat[key]['Total Cost'])
                else:
                    costMonthly[key[3:]] = Counter(stat[key]['Total Cost'])

            # Counter() to allow addition of dictionaries
            mainYearly = Counter()
            sideYearly = Counter()
            costYearly = Counter()
            # Formating the data from 'stat'
            for key in mainMonthly:
                if key[3:] in mainYearly:
                    mainYearly[key[3:]] += mainMonthly[key]
                else:
                    mainYearly[key[3:]] = mainMonthly[key]
                if key[3:] in sideYearly:
                    sideYearly[key[3:]] += sideMonthly[key]
                else:
                    sideYearly[key[3:]] = sideMonthly[key]
                if key[3:] in costYearly:
                    costYearly[key[3:]] += costMonthly[key]
                else:
                    costYearly[key[3:]] = costMonthly[key]

            # Change back to dictionary
            mainMonthly = dict(mainMonthly)
            sideMonthly = dict(sideMonthly)
            costMonthly = dict(costMonthly)
            mainYearly = dict(mainYearly)
            sideYearly = dict(sideYearly)
            costYearly = dict(costYearly)

            for key in mainMonthly:
                mainMonthly[key] = dict(mainMonthly[key])
            for key in sideMonthly:
                sideMonthly[key] = dict(sideMonthly[key])
            for key in costMonthly:
                costMonthly[key] = dict(costMonthly[key])
            for key in mainYearly:
                mainYearly[key] = dict(mainYearly[key])
            for key in sideYearly:
                sideYearly[key] = dict(sideYearly[key])
            for key in costYearly:
                costYearly[key] = dict(costYearly[key])
            month = {}
            year = {}
            # Formating data received
            for key in mainMonthly:
                month[key] = {'Main': mainMonthly[key], 'Sides': sideMonthly[key], 'Total Cost': costMonthly[key]}
            for key in mainYearly:
                year[key] = {'Main': mainYearly[key], 'Sides': sideYearly[key], 'Total Cost': costYearly[key]}
            # Returns data for use in statsDailyScreen, statsMonthlyScreen and statsYearlyScreen
            return year, mainMonthly, sideMonthly, costMonthly, mainYearly, sideYearly, costYearly, stat

    # Written by Kai Jun
    def stats_screen_change(self):
        self.root.transition.direction = "right"
        self.root.current = "vendor_screen"

    # 'Daily Button'
    # Runs after pressing the 'Daily' button
    # Needs year
    # Written by Ying Xuan
    def statsDailyScreen(self):  # Add daily datatable to screen when button pressed
        self.root.transition.direction = "left"
        self.root.current = "stats_screen"
        # Clears previous datatable
        self.root.ids.stats_screen.ids.datatable.clear_widgets()
        data = self.getData()
        # Creates column data for datatable
        column = [['Date', 50], ['Total Earnings', 30]]
        for years in data[0]:
            for key in data[0][years]['Main']:
                column.append([key, 30])
            for key in data[0][years]['Sides']:
                column.append([key, 30])
        column = [tuple(i) for i in column]
        row = []
        # Creates row data for datatable
        for key in data[7]:
            date = [key.replace(',', '/'), '${0:.2f}'.format(data[7][key]['Total Cost']['Cost'])]
            food = {**data[7][key]['Main'], **data[7][key]['Sides']}
            for i in range(len(column[2:])):
                date.append(0)
                for j in range(len(list(food))):
                    if column[i + 2][0] == list(food)[j]:
                        date[i + 2] = list(food.values())[j]
            row.append(tuple(date))
        row.append(tuple([''] * len(column)))
        dailyDataTable = MDDataTable(
            size_hint=(1, 0.6),
            column_data=column,
            row_data=row
        )
        # Add datatable
        self.root.ids.stats_screen.ids.datatable.add_widget(dailyDataTable)

    # 'Monthly' Button
    # Runs after pressing the 'Monthly' button
    # Needs year, costMonthly, sideMonthly, mainMonthly

    # Written by Ying Xuan
    def statsMonthlyScreen(self):  # Add monthly datatable to screen when button pressed
        self.root.transition.direction = "left"
        self.root.current = "stats_screen"
        # Clears previous datatable
        self.root.ids.stats_screen.ids.datatable.clear_widgets()
        data = self.getData()
        # Create column data fro datatable
        column = [['Month', 40], ['Total Earnings', 30]]
        for years in data[0]:
            for key in data[0][years]['Main']:
                column.append([key, 30])
            for key in data[0][years]['Sides']:
                column.append([key, 30])
        column = [tuple(i) for i in column]
        row = []
        # Create row data for datatable
        for key in data[2]:
            month = [key.replace(',', '/'), '${0:.2f}'.format(data[3][key]['Cost'])]
            food = {**data[1][key], **data[2][key]}
            for i in range(len(column[2:])):
                month.append(0)
                for j in range(len(list(food))):
                    if column[i + 2][0] == list(food)[j]:
                        month[i + 2] = list(food.values())[j]
            row.append(tuple(month))
        row.append(tuple([''] * len(column)))
        monthlyDataTable = MDDataTable(
            size_hint=(1, 0.6),
            column_data=column,
            row_data=row
        )
        # Add datatable
        self.root.ids.stats_screen.ids.datatable.add_widget(monthlyDataTable)

    # 'Yearly' button
    # Runs after pressing the 'Yearly' button
    # Needs year, costYearly, sideYearly, mainYearly
    # Written by Ying Xuan
    def statsYearlyScreen(self):  # Add yearly datatable to screen when button pressed
        self.root.transition.direction = "left"
        self.root.current = "stats_screen"
        # Clears previous datatable
        self.root.ids.stats_screen.ids.datatable.clear_widgets()
        data = self.getData()
        # Creating column data for datatable
        column = [['Month', 40], ['Total Earnings', 30]]
        for years in data[0]:
            for key in data[0][years]['Main']:
                column.append([key, 30])
            for key in data[0][years]['Sides']:
                column.append([key, 30])
        column = [tuple(i) for i in column]
        row = []
        # Creating row data for datatable
        for key in data[5]:
            _year = [key.replace(',', '/'), '${0:.2f}'.format(data[6][key]['Cost'])]
            food = {**data[4][key], **data[5][key]}
            for i in range(len(column[2:])):
                _year.append(0)
                for j in range(len(list(food))):
                    if column[i + 2][0] == list(food)[j]:
                        _year[i + 2] = list(food.values())[j]
            row.append(tuple(_year))
        row.append(tuple([''] * len(column)))
        yearlyDataTable = MDDataTable(
            size_hint=(1, 0.6),
            column_data=column,
            row_data=row
        )
        # Add datatable
        self.root.ids.stats_screen.ids.datatable.add_widget(yearlyDataTable)


if __name__ == "__main__":
    SSTOrder().run()
