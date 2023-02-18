import re
import pyrebase
from kivymd.toast import toast
from kivy.app import App
from kivy.clock import Clock

class FirebaseAuth:

    config = {
        "apiKey": "AIzaSyCfVmGyN1xEckRMQOpwyOdJuD2OjXHWM8Y",
        "authDomain": "coursework-app-9f20c.firebaseapp.com",
        "databaseURL": "https://coursework-app-9f20c-default-rtdb.asia-southeast1.firebasedatabase.app/",
        "storageBucket": "gs://coursework-app-9f20c.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()

    #Written by Jun Seng
    def logout(self):

        app = App.get_running_app()

        FirebaseAuth.auth.current_user = None

        f = open('login_data.txt', 'r+')
        f.truncate(0)

        app.root.current = "login_screen"
        toast("Logged out successfully!")

        if app.text_bool=="True":
            app.dataScreen_clock.cancel()
            app.refresh_vendor_pending_orders_clock.cancel()
            app.get_stats_clock.cancel()
        else:
            app.clock1.cancel()

        app.main_list = []
        app.main_cost_list = []
        app.side_list = []
        app.side_cost_list = []

        # Dummy data
        app.stallrid = 0

        app.selected_sides_cost = 0
        app.selected_sides = ["No sides selected"]

        # Stall email
        app.stall_emails = []
        app.stall_names = []

        app.selected_stall_email = ""
        app.selected_stall_name = ""

        app.selected_main = ""
        app.selected_main_cost = 0

    #Written by Jun Seng
    def signup(self, sfullname, semail, spassword, confirmpassword):

        app = App.get_running_app()

        try:
            user_list = []
            vendor_list = []

            all_users = FirebaseAuth.db.child("users").get()
            for user in all_users.each():
                user_list.append(user.key())

            all_vendors = FirebaseAuth.db.child("vendors").get()
            for vendor in all_vendors.each():
                vendor_list.append(vendor.key())

        except:
            user_list = []
            vendor_list = []

        if (sfullname==""):
            toast("Name cannot be empty!")
            return

        if ("‎" in sfullname):
            toast("Name must contain only proper characters!")
            return

        if (semail==""):
            toast("Email cannot be empty!")
            return

        if ("‎" in semail):
            toast("Email must contain only proper characters!")
            return

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", semail):
            toast("Email is invalid!")
            return

        if (spassword==""):
            toast("Password cannot be empty!")
            return

        if ("‎" in spassword==""):
            toast("Password must only contain proper characters!")
            return

        if (confirmpassword==""):
            toast("Password cannot be empty!")
            return

        if (" " in spassword):
            toast("Password cannot contain whitespaces!")
            return

        if (spassword!=confirmpassword):
            toast("Passwords do not match!")
            return
        if (len(spassword)<6):
            toast("Password needs to be at least 6 characters long!")
            return

        if (" " in spassword):
            toast("Password should not contain whitespaces!")
            return

        if (semail.replace(".",",") in vendor_list):
            app.root.manager.transition.direction = "left"
            app.root.current = "login_screen"
            return

        if (semail.replace(".",",") in user_list):
            app.root.ids["signup_screen"].ids["error_label"].text = "Email already exists!"
            return

        signup_name = sfullname.strip().title()
        signup_email = semail.strip().lower()
        signup_password = spassword.strip()

        default_payload = {"fullname": signup_name, "password": signup_password}
        orders = {"Main": "(Main Order)", "Sides": "(Sides)", "Stall Name": "(Stall Name)", "Status": "(Order Status)", "Total Cost": 0}

        FirebaseAuth.auth.create_user_with_email_and_password(signup_email, signup_password)
        FirebaseAuth.db.child("users").child(signup_email.replace(".", ",")).child("Info").set(default_payload)
        FirebaseAuth.db.child("users").child(signup_email.replace(".", ",")).child("Orders").child("99,99,9999 24,00,00").set(orders)

        app.root.current = "login_screen"
        app.root.ids["signup_screen"].ids["signup_fullname_input"].text = ""
        app.root.ids["signup_screen"].ids["signup_email_input"].text = ""
        app.root.ids["signup_screen"].ids["signup_password_input"].text = ""
        app.root.ids["signup_screen"].ids["signup_confirmpassword_input"].text = ""
        toast("Please sign in :D")

    #Written by Jun Seng
    def login(self, lemail, lpassword):

        app = App.get_running_app()

        try:
            user_list = []
            vendor_list = []
            all_users = FirebaseAuth.db.child("users").get()

            for user in all_users.each():
                user_list.append(user.key())
            print(user_list)

            all_vendors = FirebaseAuth.db.child("vendors").get()
            for vendor in all_vendors.each():
                vendor_list.append(vendor.key())

        except:
            user_list = []
            vendor_list = []

        if (lemail==""):
            toast("Email cannot be empty!")
            return

        if ("‎" in lemail):
            toast("Email must only contain proper characters!")
            return

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", lemail):
            toast("Email is invalid!")
            return

        if (" " in lemail):
            toast("Email cannot contain whitespaces!")
            return

        if ((lemail.replace(".", ",") in vendor_list)==False) and ((lemail.replace(".", ",") in user_list)==False):
            toast("Account does not exist, sign up!")
            return

        if (lpassword == ""):
            toast("Password cannot be empty!")
            return

        if (" " in lpassword):
            toast("Password cannot contain whitespaces!")
            return

        if ("‎" in lpassword==""):
            toast("Password must only contain proper characters!")
            return

        login_email = lemail.strip().lower()
        login_password = lpassword.strip()

        try:


            FirebaseAuth.auth.sign_in_with_email_and_password(login_email, login_password)

            if (login_email.replace(".",",") in vendor_list):
                app.root.current = "vendor_screen"

                with open("login_data.txt", "w") as f:
                    f.write(lemail + "\n")
                    f.write(lpassword + "\n")
                    f.write("True" + "\n")

                with open("login_data.txt", "r") as f:
                    data = f.readlines()
                    print(data)
                    app.text_email = data[0].strip().replace('.', ',')
                    app.text_password = data[1].strip()
                    app.text_bool = data[2].strip()
                toast("Logged in Successfully! :D")

            else:
                app.root.current = "main_screen"
                app.root.ids.main_screen.ids.name_var.text = \
                app.root.ids.main_screen.ids.email_var.text = login_email

                with open("login_data.txt", "w") as f:
                    f.write(lemail + "\n")
                    f.write(lpassword + "\n")
                    f.write("False" + "\n")

                with open("login_data.txt", "r") as f:
                    data = f.readlines()
                    print(data)
                    app.text_email = data[0].strip().replace('.', ',')
                    app.text_password = data[1].strip()
                    app.text_bool = data[2].strip()

                    app.text_name = app.db.child("users").child(app.text_email.replace(".", ",")).child("Info").get().val()[
                            "fullname"]
                toast("Logged in Successfully! :D")

            app.root.ids["login_screen"].ids["login_email_input"].text = ""
            app.root.ids["login_screen"].ids["login_password_input"].text = ""

            if app.text_bool == "True":
                # Do vendor functions here

                # Load vendor
                app.load_items()
                # self.update_donut_graph()
                # Clock.schedule_interval(self.update_donut_graph, 10)

                Clock.schedule_once(app.dataScreen, 1)
                app.dataScreen_clock = Clock.schedule_interval(app.dataScreen, 10)
                

                # Refresh pending orders for vendor screen
                app.refresh_vendor_pending_orders()
                app.refresh_vendor_pending_orders_clock = Clock.schedule_interval(app.refresh_vendor_pending_orders, 10)

                # Statistics
                app.get_stats()
                # self.dailyData()
                # self.monthlyData()
                # self.yearlyData()

                app.get_stats_clock = Clock.schedule_interval(app.get_stats, 10)
                Clock.start_clock()
                # Clock.schedule_interval(self.dailyData, 10)
                # Clock.schedule_interval(self.monthlyData, 10)
                # Clock.schedule_interval(self.yearlyData, 10)




            else:
                # Do user functions here

                # Instantiate user orders
                app.load_user_orders()
                app.clock1 = Clock.schedule_interval(app.load_user_orders, 10)
                Clock.start_clock()

                # Instantiate order preview
                app.orderpreview()

                # Instantiate ordering screens
                app.load_user_stalls()

                # Load account info
                app.load_profile()

        except Exception as e:
            print(e)
            toast("Incorrect password!")
            return

    #Written by Jun Seng
    def login_current_user(self):

        app = App.get_running_app()

        try:
            with open("login_data.txt", "r") as f:
                data = f.readlines()
                data_email = data[0].strip()
                data_password = data[1].strip()
                data_bool = data[2].strip()

                FirebaseAuth.auth.sign_in_with_email_and_password(data_email, data_password)

                if (data_bool=="True"):
                    app.root.current = "vendor_screen"
                    toast("Logged in Successfully! :D")
                else:
                    app.root.current = "main_screen"
                    toast("Logged in Successfully! :D")

        except Exception as a:
            print(a)
            pass
