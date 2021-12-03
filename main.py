# Sets the window size
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

# Imports the module sqlite3 and re
import sqlite3
import re

# Imports the necessary kivy and kivymd modules
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.toast.kivytoast import toast
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineListItem
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivymd.utils import asynckivy
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from datetime import date, datetime

# Empty lists for storage and indexing purposes
user_key = []
index_hashtag = []
task_name_detail_list = []
task_tag_list = ['important']
task_tag_list2 = []
task_tag_list3 = []
task_due_list = []
task_time_list = []
task_card_color = []
task_title = []
task_info = []
index_task = []
edit_task = []

# Class to show the login screen
class LoginScreen(Screen):
    # Method to get the email and password from the user and use the database to verify the input
    def do_login(self, usernametext, passwordtext):

        useri = usernametext
        passwd = passwordtext
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS accounts(id_num integer PRIMARY KEY, name VARCHAR(30),lastname VARCHAR(30),emid VARCHAR(40),passwd VARCHAR(30),cpasswd VARCHAR(30))")
        cur.execute("SELECT * FROM accounts")
        cur.fetchall()

        if(len(useri) > 0 and len(passwd) > 0):
            find = ("SELECT * FROM accounts WHERE emid=? AND passwd=?")
            cur.execute(find, [(useri), (passwd)])
            results=cur.fetchall()

            if results:
                for i in results:
                    key = i[0]
                    user_key.append(key)

                    cur.execute("CREATE TABLE IF NOT EXISTS tasks(\
                        task_title VARCHAR(30),\
                        task_info VARCHAR(120),\
                        task_tag VARCHAR(30),\
                        task_due_date DATE,\
                        task_due_date_time TIME,\
                        id_task integer PRIMARY KEY,\
                        id_hashtag integer,\
                        id_user integer)")

                    find = ("SELECT * FROM tasks WHERE id_user=?")
                    cur.execute(find,[(key)])

                    results2 = cur.fetchall()

                    if len(results2) >=1:
                        index_hashtag.append(results2[0][6])
                        print(index_hashtag)

                    self.manager.transition.direction = "left"
                    self.manager.transition.duration = 0.5
                    self.manager.current = "home_screen"

                    return toast('Success. Good day, ' + i[1] + '!')
            else:
                return toast('Please enter correct email and password.')
        else:
            return toast('Please enter email and password.')

        conn.close()

        self.ids['username'].text = ""
        self.ids['password'].text = ""

# Class to show the registration or signup screen
class RegisterScreen(Screen):
    # Method to get the necessary information from the user to create an account
    def do_register(self, firsttext, lasttext, emailtext, passwordtext, copasstext):

        fname = firsttext
        lname = lasttext
        email = emailtext
        password = passwordtext
        conpass = copasstext
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS accounts(id_num integer PRIMARY KEY, name VARCHAR(30),lastname VARCHAR(30),emid VARCHAR(40),passwd VARCHAR(30),cpasswd VARCHAR(30))")
        find = ("SELECT * FROM accounts WHERE emid=?")
        cur.execute(find,[(email)])

        if(len(fname) > 0 and len(lname) > 0 and len(email) > 0 and len(password) > 0 and len(conpass) > 0):
            if cur.fetchall():
                self.manager.transition.direction = "right"
                self.manager.transition.duration = 0.5
                self.manager.current = "login"
                return toast('User is already registered. Please login')
            else:
                cur.fetchall()

                if fname == "":
                    return toast('Enter your first name.')
                elif lname == "":
                    return toast('Enter your last name.')
                elif not re.match("^[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]", email):
                    return toast('Enter an email address.')
                elif not re.match("^[A-Za-z0-9]*$", password):
                    return toast('Enter a password.')
                elif not re.match("^[A-Za-z0-9]*$", password):
                    return toast('Please confirm your password.')
                elif (password==conpass):
                    cur.execute("INSERT INTO accounts(name,lastname,emid,passwd,cpasswd) VALUES(?,?,?,?,?)",(fname,lname,email,password,conpass))
                    cur.execute("SELECT * FROM accounts")

                    cur.execute("CREATE TABLE IF NOT EXISTS hashtags(\
                        id_hashtag integer PRIMARY KEY,\
                        hashtag_name VARCHAR(30),\
                        id_user integer)")

                    find = ("SELECT * FROM accounts WHERE name=? AND emid=?")
                    cur.execute(find, [(fname), (email)])

                    results = cur.fetchall()

                    for i in results:
                        cur.execute("INSERT INTO hashtags(hashtag_name, id_user) VALUES(?,?)", ('yourfirsthashtag', i[0]))
                        cur.execute("SELECT * FROM hashtags")

                    conn.commit()
                    self.manager.transition.direction = "right"
                    self.manager.transition.duration = 0.5
                    self.manager.current = "login_screen"
                    toast('Registration complete. Please login.')
                else:
                    return toast('Please enter the same password.')
        else:
            return toast('Please enter your details.')

        conn.close()

        self.ids['fname'].text = ""
        self.ids['lname'].text = ""
        self.ids['emailid'].text = ""
        self.ids['passwd'].text = ""
        self.ids['cpass'].text = ""

# Class to show the forgot password option
class ForgotScreen(Screen):
    # Method to get the user email, new password, and verification password
    def do_reset(self, reemailtext, pastext, repastext):

        reemail = reemailtext
        paste = pastext
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS accounts(id_num integer PRIMARY KEY, name VARCHAR(30),lastname VARCHAR(30),emid VARCHAR(40),passwd VARCHAR(30),cpasswd VARCHAR(30))")
        cur.execute("SELECT * FROM accounts")

        find = ("SELECT * FROM accounts WHERE emid=? ")
        cur.execute(find, [(reemail)])

        results = cur.fetchall()

        if(len(reemail)>0):
            if results:
                if paste == repastext:
                    if paste == "" and repastext == "":
                        return toast('Enter a new password.')
                    else:
                        cur.execute('UPDATE accounts SET passwd=? WHERE emid=?', (paste, reemail))
                        conn.commit()
                        for element in results:
                            self.manager.transition.direction = "right"
                            self.manager.transition.duration = 0.5
                            self.manager.current = "login_screen"
                            return toast('Your password has been updated. Please login.')
                else:
                    return toast('Please confirm your new password correctly.')
            else:
                return toast('Please enter your registered email.')
        else:
            return toast('Please enter an email address.')

        conn.close()
        self.ids['reemail'].text = ""
        self.ids['pas'].text = ""
        self.ids['repas'].text = ""

# Class to form and show the contents of the delete hashtag dialog box
class DeleteHashtag(BoxLayout):
    # Method to delete a hashtag with error handling
    def delete_hashtag(self):

        id_u = user_key[-1]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        find = ("SELECT * FROM hashtags WHERE id_user=? ")
        cur.execute(find, [(id_u)])
        results = cur.fetchall()

        if len(index_hashtag) == 0:
            toast('No hashtag available.')
        elif len(results) == 1:
            toast('You can\'t delete all the hashtag.')
        else:
            hashtag_id = index_hashtag[-1]

            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()        

            delete1 = "DELETE FROM tasks WHERE id_hashtag=" + str(hashtag_id)
            delete2 = "DELETE FROM hashtags WHERE id_hashtag=" + str(hashtag_id)
            cur.execute(delete1)
            cur.execute(delete2)
            conn.commit()
            conn.close()
            toast('Hashtag deleted.')

# Class to form and show the components in the dialog box of edit hashtag
class EditHashtag(BoxLayout):
    # Method to get the hashtag input from the user
    def edit_hashtag(self, user_hashtag):
        
        id_u = user_key[-1]
        hashtag = user_hashtag.lower()

        if len(index_hashtag) == 0:
            toast('No available hashtag.')
        else:
            if hashtag == "":
                toast('Please enter a new hashtag name.')
            else:
                hashtag_id = index_hashtag[-1]
                conn = sqlite3.connect("mybase.db")
                cur = conn.cursor()

                find = ("SELECT * FROM hashtags WHERE hashtag_name=? AND id_user=?")
                cur.execute(find, [(hashtag), (id_u)])

                if(len(hashtag)>0):
                    if cur.fetchall():
                        self.ids['edit_hashtag'].text = ""
                        return toast('Hashtag already exist. Try again.')
                    else:
                        find = ("SELECT * FROM hashtags WHERE id_hashtag=? ")
                        cur.execute(find, [(hashtag_id)])
                        results = cur.fetchall()
                        if(len(hashtag)>0):
                            if results:
                                cur.execute('UPDATE hashtags SET hashtag_name=? WHERE id_hashtag = ?', (hashtag, hashtag_id))
                                conn.commit()
                                conn.close()
                                self.ids['edit_hashtag'].text = ""
                                return toast('The hashtag has been updated. Please refresh.')
                        else:
                            return toast('Please enter a new hashtag name to edit.')

# Class to form and show the components in the dialog box of add hashtag
class AddHashtag(BoxLayout):
    # Method to get the hashtag input from the user
    def add_hashtag(self, user_hashtag):
        
        hashtag = user_hashtag.lower()
        id_u = user_key[-1]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS hashtags(\
            id_hashtag integer PRIMARY KEY,\
            hashtag_name VARCHAR(30),\
            id_user integer)")

        find = ("SELECT * FROM hashtags WHERE hashtag_name=? AND id_user=?")
        cur.execute(find, [(hashtag), (id_u)])
        
        if(len(hashtag)>0):
            if cur.fetchall():
                self.ids['task_hashtag'].text = ""
                return toast('Hashtag already exist.')
            else:
                cur.execute("INSERT INTO hashtags(hashtag_name, id_user) VALUES(?,?)", (hashtag, id_u,))
                cur.execute("SELECT * FROM hashtags")
                conn.commit()
                self.ids['task_hashtag'].text = ""
                return toast('Hashtag Added.')
        elif hashtag == "":
            return toast('Please enter a hashtag.')

        conn.close()

# Class to form and show the components in the dialog box of add task
class AddTask(BoxLayout):
    # Method to check what checkbox is active to get the tag of task
    def on_checkbox_active(self, checkbox, value):

        if value:
            task_tag_list.append('important')
        else:
            task_tag_list.append('normal')
    # Method to save the entered due date of task from the user
    def on_save(self, instance, value, date_range):

        date = value
        task_due_list.append(date)
        self.get_due_date()
    # Method to cancel the imported data
    def on_cancel(self, instance, value):

        pass
    # Method to show the kivymd default date picker
    def show_date_picker(self):

        date_dialog = MDDatePicker(primary_color=get_color_from_hex("#C69C6D"),
                                    accent_color=get_color_from_hex("#F3EBE2"),
                                    selector_color=get_color_from_hex("#C6826D"),
                                    text_toolbar_color=get_color_from_hex("#C69C6D"),
                                    text_color=("#C69C6D"),
                                    text_current_color=get_color_from_hex("#e93f39"),
                                    input_field_background_color=(1, 1, 1, 0.2),
                                    input_field_text_color=get_color_from_hex("#C69C6D"),
                                    text_button_color=get_color_from_hex("#C69C6D"),
                                    font_name="segoeui.ttf",
                                    min_date=date.today(),max_date=datetime.strptime("2025:05:30", '%Y:%m:%d').date())
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    # Method to return the entered due date by the user
    def get_due_date(self):

        months = ['January','February','March','April','May','June','July','August','September','October','November','December']

        if task_due_list == []:
            set_date = 'No Task Due Date Set'
        else:
            date = str(task_due_list[-1])[5:7]
            
            if date[0] == '1':
                set_date = months[int(date) - 1] + ' ' + str(task_due_list[-1])[8:10]
            else:
                set_date = months[int(date[1]) - 1] + ' ' + str(task_due_list[-1])[8:10]


        current_date = self.ids["duedate"].text = f"{set_date}"
        return current_date
    # Method to return the entered due time by the user
    def get_due_time(self):
    
        if task_time_list == []:
            set_time = 'No Task Due Date Time Set'
        else:
            time = str(task_time_list[-1])
            time2 = datetime.strptime(time, "%H:%M:%S")
            set_time = time2.strftime("%I:%M %p")
        
        current_time = self.ids["duetime"].text = f"{set_time}"
        return current_time
    # Method to show the kivymd default time picker
    def show_time_picker(self):

        time_dialog = MDTimePicker(primary_color=get_color_from_hex("#C69C6D"),
                                    accent_color=get_color_from_hex("#F3EBE2"),
                                    text_color=("#C69C6D"),
                                    input_field_text_color=get_color_from_hex("#FFFFFF"),
                                    selector_color=get_color_from_hex("#C6826D"),
                                    text_button_color=get_color_from_hex("#FFFFFF"),
                                    font_name="segoeui.ttf")
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    # Method to return the entered due time by the user
    def get_time(self, instance, time):

        task_time_list.append(time)
        self.get_due_time()
    # Method to return the entered task details from the user and save it on the data base
    def get_task(self, title, info):

        id_u = user_key[-1]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        if len(index_hashtag) == 0:
            toast('No hashtag available. Add one to add a task.')
        else:
            hashtag_id = index_hashtag[-1]

            title = title
            info = info
            tag = task_tag_list[-1]

            if len(task_due_list) == 0:
                due_date = ""
            else:
                due_date = str(task_due_list[-1])

            if len(task_time_list) == 0:
                due_date_time = ""
            else:       
                due_date_time = str(task_time_list[-1])

            if title == "":
                return toast('Please enter a Task Name.')
            elif info == "":
                return toast('Please enter the Task Detail.')
            elif due_date == "":
                return toast('Please set a Task Due Date.')            
            elif due_date_time == "":
                return toast('Please set a Task Due Date Time.')
            else:
                cur.execute("CREATE TABLE IF NOT EXISTS tasks(\
                    task_title VARCHAR(30),\
                    task_info VARCHAR(120),\
                    task_tag VARCHAR(30),\
                    task_due_date DATE,\
                    task_due_date_time TIME,\
                    id_task integer PRIMARY KEY,\
                    id_hashtag integer,\
                    id_user integer)")

                cur.execute("INSERT INTO tasks(task_title, task_info, task_tag, task_due_date, task_due_date_time, id_hashtag, id_user) VALUES(?,?,?,?,?,?,?)", (title, info, tag, due_date, due_date_time, hashtag_id, id_u,))
                cur.execute("SELECT * FROM tasks")
                conn.commit()

                task_due_list.clear()
                task_tag_list.clear()
                task_tag_list.append('important')
                task_time_list.clear()

                self.ids['importantc'].active = True
                self.ids['duedate'].text = 'No Task Due Date Set'
                self.ids['duetime'].text = 'No Task Due Date Time Set'

                toast('Task Added.')

            conn.close()

        self.ids['task_name'].text = ""
        self.ids['task_details'].text = ""

# Class to show and form the components of the dialog box edit task
class EditTask(BoxLayout):
    # Clears the input and data in the dialog box after using
    def on_leave(self):

        task_time_list.clear()
        task_tag_list2.clear()
        task_tag_list3.clear()
    # Returns the new tag of the task
    def get_check(self):

        id = edit_task[-1]

        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()
        find = ("SELECT * FROM tasks WHERE id_task=? ")
        cur.execute(find, [(id)])
        results = cur.fetchall()

        for i in results:
            return i[2]
    # Returns the new task name of the task
    def get_task_name(self):

        id = edit_task[-1]

        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()
        find = ("SELECT * FROM tasks WHERE id_task=? ")
        cur.execute(find, [(id)])
        results = cur.fetchall()

        for i in results:
            return i[0]
    # Returns the new task details of the task
    def get_task_details(self):
    
        id = edit_task[-1]

        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()
        find = ("SELECT * FROM tasks WHERE id_task=? ")
        cur.execute(find, [(id)])
        results = cur.fetchall()

        for i in results:
            return i[1]
    # Adds an element in task_tag_list2 to indicate that the task tag is changed to important
    def on_checkbox_active1(self, checkbox, value):

        if value:
            task_tag_list2.append('important')
    # Adds an element in task_tag_list2 to indicate that the task tag is changed to normal
    def on_checkbox_active2(self, checkbox, value):
    
        if value:
            task_tag_list2.append('normal')
    # Method to sava the new entered date from user
    def on_save(self, instance, value, date_range):

        date = value
        task_due_list.clear()
        task_due_list.append(date)
        self.get_due_date()
    # Method to cancel saving the newly added data by the user
    def on_cancel(self, instance, value):

        pass
    # Method to show the date picker from kivymd
    def show_date_picker(self):

        date_dialog = MDDatePicker(primary_color=get_color_from_hex("#C69C6D"),
                                    accent_color=get_color_from_hex("#F3EBE2"),
                                    selector_color=get_color_from_hex("#C6826D"),
                                    text_toolbar_color=get_color_from_hex("#C69C6D"),
                                    text_color=("#C69C6D"),
                                    text_current_color=get_color_from_hex("#e93f39"),
                                    input_field_background_color=(1, 1, 1, 0.2),
                                    input_field_text_color=get_color_from_hex("#C69C6D"),
                                    text_button_color=get_color_from_hex("#C69C6D"),
                                    font_name="segoeui.ttf",
                                    min_date=date.today(),max_date=datetime.strptime("2025:05:30", '%Y:%m:%d').date())
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    # Method to get the new due date from the user
    def get_due_date(self):

        months = ['January','February','March','April','May','June','July','August','September','October','November','December']

        if len(task_due_list) > 0:
            date = str(task_due_list[-1])[5:7]
            
            if date[0] == '1':
                set_date = months[int(date) - 1] + ' ' + str(task_due_list[-1])[8:10]
            else:
                set_date = months[int(date[1]) - 1] + ' ' + str(task_due_list[-1])[8:10]
        else:
            id = edit_task[-1]

            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()
            find = ("SELECT * FROM tasks WHERE id_task=? ")
            cur.execute(find, [(id)])
            results = cur.fetchall()

            for i in results:
                date = i[3]
                
                if date[5] == '1':
                    set_date = months[int(date[4:6]) - 1] + ' ' + str(date[8:])
                else:
                    set_date = months[int(date[6]) - 1] + ' ' + str(date[8:])

        current_date = self.ids["duedate"].text = f"{set_date}"
        return current_date
    # Method to get the new due time from the user
    def get_due_time(self):

        if len(task_time_list) > 0:
            time = str(task_time_list[-1])
            time2 = datetime.strptime(time, "%H:%M:%S")
            set_time = time2.strftime("%I:%M %p")
        else:
            id = edit_task[-1]

            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()
            find = ("SELECT * FROM tasks WHERE id_task=? ")
            cur.execute(find, [(id)])
            results = cur.fetchall()

            for i in results:
                time = i[4]
                time2 = datetime.strptime(time, "%H:%M:%S")
                set_time = time2.strftime("%I:%M %p")

        current_time = self.ids["duetime"].text = f"{set_time}"
        return current_time
    # Method to show the time picker from kivymd
    def show_time_picker(self):

        time_dialog = MDTimePicker(primary_color=get_color_from_hex("#C69C6D"),
                                    accent_color=get_color_from_hex("#F3EBE2"),
                                    text_color=("#C69C6D"),
                                    input_field_text_color=get_color_from_hex("#FFFFFF"),
                                    selector_color=get_color_from_hex("#C6826D"),
                                    text_button_color=get_color_from_hex("#FFFFFF"),
                                    font_name="segoeui.ttf")
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    # Method to get save the new due time from the user
    def get_time(self, instance, time):

        task_time_list.append(time)
        self.get_due_time()
    # Method to get all the new data entered by the user and update in the data base
    def get_task(self, title, info):

        id_u = edit_task[-1]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        if len(index_hashtag) == 0:
            toast('No hashtag available. Add one to add a task.')
        else:
            hashtag_id = index_hashtag[-1]

            title = title
            info = info

            if len(task_tag_list2) == 0:
                id = edit_task[-1]

                conn = sqlite3.connect("mybase.db")
                cur = conn.cursor()
                find = ("SELECT * FROM tasks WHERE id_task=? ")
                cur.execute(find, [(id)])
                results = cur.fetchall()

                for i in results:
                    tag = i[2]
            else:
                tag = task_tag_list2[-1]

            if len(task_due_list) == 0 and len(edit_task) > 0:
                
                id = edit_task[-1]

                conn = sqlite3.connect("mybase.db")
                cur = conn.cursor()
                find = ("SELECT * FROM tasks WHERE id_task=? ")
                cur.execute(find, [(id)])
                results = cur.fetchall()

                for i in results:
                    due_date = str(i[3])
            else:
                due_date = str(task_due_list[-1])

            if len(task_time_list) == 0 and len(edit_task) > 0:

                id = edit_task[-1]

                conn = sqlite3.connect("mybase.db")
                cur = conn.cursor()
                find = ("SELECT * FROM tasks WHERE id_task=? ")
                cur.execute(find, [(id)])
                results = cur.fetchall()

                for i in results:
                    due_date_time = str(i[4])
            else:       
                due_date_time = str(task_time_list[-1])

            if title == "":
                return toast('Please enter a Task Name.')
            elif tag == "":
                return toast('Please set if the task is important or normal.')
            elif info == "":
                return toast('Please enter the Task Detail.')
            elif due_date == "":
                return toast('Please set a Task Due Date.')            
            elif due_date_time == "":
                return toast('Please set a Task Due Date Time.')
            else:
                update_task = "UPDATE tasks SET task_title=?, task_info=?, task_tag=?, task_due_date=?, task_due_date_time=? WHERE id_hashtag=? AND id_task=?"
                update_values = (title, info, tag, due_date, due_date_time, hashtag_id, id_u)
                cur.execute(update_task, update_values)
                conn.commit()
                task_time_list.clear()
                task_due_list.clear()
                task_tag_list2.clear()

                toast('Task Updated. Please refresh.')

                conn.close()

# Class to show and form the comopnents of the dialog box task info
class TaskInfo(BoxLayout):
    # Method to add a hashtag based on user input
    def add_hashtag(self, user_hashtag):
        
        hashtag = user_hashtag.lower()
        id_u = user_key[-1]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS hashtags(\
            id_hashtag integer PRIMARY KEY,\
            hashtag_name VARCHAR(30),\
            id_user integer)")

        find = ("SELECT * FROM hashtags WHERE hashtag_name=? ")
        cur.execute(find, [(hashtag)])
        
        if(len(hashtag)>0):
            if cur.fetchall():
                self.ids['task_hashtag'].text = ""
                return toast('Hashtag already exist.')
            else:
                cur.execute("INSERT INTO hashtags(hashtag_name, id_user) VALUES(?,?)", (hashtag, id_u,))
                cur.execute("SELECT * FROM hashtags")
                conn.commit()
                self.ids['task_hashtag'].text = ""
                return toast('Hashtag Added.')
        elif hashtag == "":
            return toast('Please enter a hashtag.')

        conn.close()

# Class to form a one line list item from kivymd
class HashtagsL(OneLineListItem):

    index = NumericProperty()

# Class to form the task card using kivymd
class Card(MDCard):

    title = StringProperty('')
    details = StringProperty('')

# Class to form the detailed task card using kivymd
class Card2(MDCard):
    
    title = StringProperty('')
    title2 = StringProperty('')
    info = StringProperty('')
    details = StringProperty('')
    details_cut = StringProperty('')
    index_color = NumericProperty()
    task_idpk = StringProperty('')

    dialog3 = None
    dialog4 = None
    index = NumericProperty()

    # Method to edit the selected task by getting the required data from the user
    def edit_task(self, title_task, info_task, details_task, id_task):

        edit_task.clear()
        edit_task.append(id_task)

        if not self.dialog4:
                self.dialog4 = MDDialog(
                title = "Edit Task:",
                type = "custom",
                content_cls = EditTask(),
            )
        self.dialog4.open()

    # Method to mark the selected task completed
    def mark_as_done(self):

        task = index_task[-1]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        done = "DELETE FROM tasks WHERE id_task=" + str(task)
        cur.execute(done)
        conn.commit()
        conn.close()
        self.dialog_close()
        toast('Task completed.')

    # Method to form the task dialog using kivymd
    def task_dialog(self, title_task, info_task, details_task, id_task):
        
        if not self.dialog3:
            index_task.append(id_task)
            self.dialog3 = MDDialog(
                title = title_task + ' | ' + info_task,
                text = details_task,
                buttons=[
                    MDFillRoundFlatButton(
                        text="EDIT",
                        theme_text_color = 'Custom',
		                md_bg_color ='#C6826D',
		                text_color = '#F1ECEC',
                        on_release = lambda x:self.edit_task(title_task, info_task, details_task, id_task)),
                    MDFillRoundFlatButton(
                        text="MARK AS DONE",
                        theme_text_color = 'Custom',
		                md_bg_color ='#C6826D',
		                text_color = '#F1ECEC',
                        on_release = lambda x:self.mark_as_done(),
                    ),
                ],
            )
        self.dialog3.open()

    # Method to close the task dialog using kivymd
    def dialog_close(self, *args):
        self.dialog3.dismiss(force=True)

    # Method to close the task dialog using kivymd
    def dialog_close2(self, *args):
        self.dialog4.dismiss(force=True)

# Class to form the cards that contains the FAQ of the application
class Card3(MDCard):
    
    question = StringProperty('')
    answer = StringProperty('')

# Class to form and show the components in the home screen
class HomeScreen(Screen):

    dialog1 = None
    dialog2 = None
    dialog3 = None
    dialog4 = None
    index = NumericProperty()

    # Method to clear a list and widgets in the homescreen when the user logs out
    def on_leave(self):

        index_hashtag.clear()
        self.ids.container.clear_widgets()
        self.ids.faq.clear_widgets()
        self.ids.hashtag_tasks.clear_widgets()
        self.ids.important_tasks.clear_widgets()

    # Method to delete a hashtag
    def delete_hashtag(self):
    
        id_u = user_key[-1]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        find = ("SELECT * FROM hashtags WHERE id_user=? ")
        cur.execute(find, [(id_u)])
        results = cur.fetchall()

        if len(index_hashtag) == 0:
            toast('No hashtag available.')
        elif len(results) == 1:
            toast('You can\'t delete all the hashtag.')
        else:
            hashtag_id = index_hashtag[-1]

            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()        

            delete1 = "DELETE FROM tasks WHERE id_hashtag=" + str(hashtag_id)
            delete2 = "DELETE FROM hashtags WHERE id_hashtag=" + str(hashtag_id)
            cur.execute(delete1)
            cur.execute(delete2)
            conn.commit()
            conn.close()
            self.dialog_close()
            toast('Hashtag deleted.')

    # Method to close the dialog box
    def dialog_close(self, *args):

        self.dialog4.dismiss(force=True)
        self.callback

    # Method to start and call the layout of the delete hashtag dialog box
    def delete_hashtag_dialog(self):
    
        if not self.dialog4:
            self.dialog4 = MDDialog(
                title="Delete Hashtag",
                text= 'Are you sure you want to delete this hashtag and all of its content?',
                type="custom",
                buttons=[
                    MDFillRoundFlatButton(
                        text="Delete", theme_text_color='Custom', \
                            md_bg_color='#C6826D', text_color='#F1ECEC', \
                            on_release=lambda x: self.delete_hashtag()
                    ),
                ]
            )
        self.dialog4.open() 

    # Method to start and call the layout of the add hashtag dialog box
    def add_hashtag_dialog(self):

        if not self.dialog1:
            self.dialog1 = MDDialog(
                title="Add a Hashtag:",
                type="custom",
                content_cls=AddHashtag(),
            )
        self.dialog1.open() 

    # Method to start and call the layout of the edit hashtag dialog box
    def edit_hashtag_dialog(self):
        
        if not self.dialog3:
            self.dialog3 = MDDialog(
                title = "Edit Hashtag",
                type = "custom",
                content_cls = EditHashtag(),
            )
        self.dialog3.open()

    # Method to start and call the layout of the add hashtag dialog box
    def add_task_dialog(self):
    
        if not self.dialog2:
            self.dialog2 = MDDialog(
                title = "Add a Task:",
                type = "custom",
                content_cls = AddTask(),
            )
        self.dialog2.open()

    # Method to clear the widgets to avoid doubling the showed data from the user
    def refresh_callback(self, *args):

            def refresh_callback(interval):
                
                self.ids.container.clear_widgets()
                self.ids.faq.clear_widgets()
                self.ids.hashtag_tasks.clear_widgets()
                self.ids.important_tasks.clear_widgets()
                
                if self.x == 0:
                    self.x, self.y = 1, 1
                else:
                    self.x, self.y = 0, 0
                self.on_enter()
                self.ids.refresh_layout.refresh_done()

            Clock.schedule_once(refresh_callback, 1)

    # Method that runs and shows the required data from the user when the homescreen is started
    def on_enter(self, *args):

        # Shows the important tasks from the user
        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        id_u = user_key[-1]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS tasks(\
            task_title VARCHAR(30),\
            task_info VARCHAR(120),\
            task_tag VARCHAR(30),\
            task_due_date DATE,\
            task_due_date_time TIME,\
            id_task integer PRIMARY KEY,\
            id_hashtag integer,\
            id_user integer)")
        
        find = ("SELECT * FROM TASKS WHERE task_tag='important' AND id_user=" + str(id_u) + " ORDER BY task_due_date, task_due_date_time ASC")
        cur.execute(find)
        results2 = cur.fetchall()

        for j in results2:
            title_task = j[0]
            if len(title_task) > 20:
                final_title_task = j[0][0:20] + '...'
            else:
                final_title_task = j[0]
            date = j[3][5:7]
            
            if date[0] == '1':
                final_date = months[int(date) - 1] + ' ' + j[3][8:10]
            else:
                final_date = months[int(date[1]) - 1] + ' ' + j[3][8:10]

            time = j[4][0:5]
            time2 = datetime.strptime(time, "%H:%M")
            final_time = time2.strftime("%I:%M %p")

            details_task = 'DUE ON ' + final_date + ' at ' + final_time

            important_list = Card(title=f'{final_title_task}', details=f'{details_task}')
            self.ids.important_tasks.add_widget(important_list)

        # Shows the available hashtags from the user
        find = ("SELECT * FROM hashtags WHERE id_user=?")
        cur.execute(find, [(id_u)])
        results = cur.fetchall()

        for i in results:
            k = i[1]

            self.ids.container.add_widget(HashtagsL(index=i[0],text=f"#{k}", divider=None,\
            theme_text_color='Custom', text_color='#FFFFFF', on_release=self.callback))

        # Shows the FAQ Portion
        faq_cards = [('How to add a hashtag?', 'To add a hashtag, simply click the plus icon in the right side of the word hashtag.'), ('How to add a task?', 'To add a task, simply click the plus icon in the upper right of the center portion of home.'),\
            ('Do I need to add a hashtag before I can add a task?', 'Yes. Tasks will be grouped according to their corresponding hashtag.'), ('How to modify a hashtag?', 'In the upper right of the center portion of home, simply click the edit icon and enter your new hashtag name.'),\
                ('How can I delete a hashtag?', 'Simply click the delete icon in the upper right of the center portion of home.'), ('If I delete a hashtag, will all the task connected to it will also be deleted?', 'Yes. All of tasks added on the hashtag you deleted will also be erased.'),\
                    ('How to view a specific task?', 'Simply click the card of a certain task to expand. By clicking it, a dialog box containing the information of the task you selected will be shown.'), ('How can I mark as done a certain task?', 'Simply click the task and click the MARK AS DONE button in the dialog box.'),\
                        ('How to refresh the app to show newly added task or hashtag?', 'Simply pull down in the center portion of the app or simply click any hashtag on the left panel.')]

        for card in faq_cards:
            faqs = Card3(question=card[0], answer=card[1])
            self.ids.faq.add_widget(faqs)

        # Method to form and show all the available tasks from the user when the user is in homescreen
        async def on_enter():

            if len(index_hashtag) == 0:
                print('No tasks available')
            else:
                id_h = index_hashtag[-1]
                find = ("SELECT * FROM TASKS WHERE id_hashtag=? ORDER BY task_due_date, task_due_date_time ASC")
                cur.execute(find, [(id_h)])
                results = cur.fetchall()

                for i in results:
                    await asynckivy.sleep(0)
                    title_task = i[0]
                    if len(title_task) > 47:
                        final_title_task = i[0][0:47] + '...'
                    else:
                        final_title_task = i[0]

                    info_task = i[1]
                    if len(info_task) > 82:
                        final_info_task = i[1][0:82] + '...'
                    else:
                        final_info_task = i[1]

                    date = i[3][5:7]
                    
                    if date[0] == '1':
                        final_date = months[int(date) - 1] + ' ' + i[3][8:10]
                    else:
                        final_date = months[int(date[1]) - 1] + ' ' + i[3][8:10]

                    time = i[4][0:5]
                    time2 = datetime.strptime(time, "%H:%M")
                    final_time = time2.strftime("%I:%M %p")

                    details_task = 'DUE ON ' + final_date + ' at ' + final_time

                    if i[2] == 'normal':
                        color = 1
                    elif i[2] == 'important':
                        color = 2

                    task_id = i[5]

                    task_list = Card2(title=f'{final_title_task}', title2=f'{title_task}', info=f'{details_task}', details=f'{final_info_task}', details_cut=f'{info_task}', index_color=f'{color}', task_idpk=f'{task_id}')
                    self.ids.hashtag_tasks.add_widget(task_list)
            conn.close()
        asynckivy.start(on_enter())

    # Method like the refresh callback but for the hashtag side to implement real-time task selection and viewing
    def callback(self,instance):

        index_h = instance.index
        index_hashtag.clear()
        index_hashtag.append(index_h)

        self.ids.container.clear_widgets()
        self.ids.faq.clear_widgets()
        self.ids.hashtag_tasks.clear_widgets()
        self.ids.important_tasks.clear_widgets()
        self.on_enter()
        self.hashtag_label()
        
        print(index_h)
        print(index_hashtag)

    # Method to show the clicked hashtag by the user
    def hashtag_label(self):

        if len(index_hashtag) == 0:
            return 'Welcome to CodiPie!'
        else:
            h_index = index_hashtag[-1]
            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()

            find = ("SELECT * FROM hashtags WHERE id_hashtag=?")
            cur.execute(find, [(h_index)])
            results = cur.fetchall()
            print(results)

            if results:
                present_hashtag = '#' + results[0][1]

                clicked_hashtag = self.ids["hash"].text = f"{present_hashtag}"
                return clicked_hashtag
            else:
                return ''

    # Method to show the present date
    def calendar(self):

        months = ['January','February','March','April','May','June','July','August','September','October','November','December']

        todays_date = date.today()

        yy = str(todays_date.year) # year
        mm = months[todays_date.month - 1] # month
        dd = str(todays_date.day) # day

        # display the date
        return mm + ' ' + dd + ',' + ' ' + yy

# These lines of code uses the screen manager from kivy to navigate the app in different screens
screen_manager=ScreenManager()
screen_manager.add_widget(LoginScreen(name = "login_screen"))
screen_manager.add_widget(RegisterScreen(name = "register_screen"))
screen_manager.add_widget(ForgotScreen(name = "forgot_screen"))
screen_manager.add_widget(HomeScreen(name = "home_screen"))

# Class to form the foundation of the whole program which uses MDApp from kivymd
class MyApp(MDApp):

    title = "CodiPie - Organize your tasks"

    # Method to build the foundation of the application's window and icon
    def build(self):
        screen = Builder.load_file("main.kv")
        self.icon = 'codipie_logo_icon.ico'
        self.theme_cls.primary_palette = 'Brown'
        self.theme_cls.primary_hue = "200"  
        return screen

# Starts the application
if __name__ == '__main__':
    MyApp().run()
