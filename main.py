from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

import sqlite3
import re
import calendar
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.toast.kivytoast import toast
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineListItem, ThreeLineIconListItem, ThreeLineListItem
from kivymd.color_definitions import colors
from datetime import date, datetime
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivymd.utils import asynckivy
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.picker import MDDatePicker, MDTimePicker

user_key = [1]
index_hashtag = [1]
task_name_detail_list = []
task_tag_list = ['important']
task_due_list = []
task_time_list = []
task_card_color = []
task_title = []
task_info = []
index_task = []

class LoginScreen(Screen):

    def do_login(self,usernametext,passwordtext):

        useri = usernametext
        passwd = passwordtext
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS login(userid VARCHAR(40),passwrd VARCHAR(40))")
        cur.execute("INSERT INTO login(userid,passwrd) VALUES(?,?)", (useri,passwd))
        cur.execute("SELECT * FROM accounts")
        cur.fetchall()

        if(len(useri) > 0 and len(passwd) > 0):
            find = ("SELECT * FROM accounts WHERE emid=? AND passwd=?")
            cur.execute(find, [(useri), (passwd)])
            results=cur.fetchall()

            if results:
                for i in results:
                    user_key.append(i[0])
                    self.manager.transition.direction = "left"
                    self.manager.transition.duration = 0.5
                    self.manager.current = "home_screen"
                    print(user_key[0])
                    return toast('Success. Welcome to CodiPie, ' + i[1] + '!')
            else:
                return toast('Please enter correct email and password.')
        else:
            return toast('Please enter email and password.')

        conn.close()

        self.ids['username'].text = ""
        self.ids['password'].text = ""

class RegisterScreen(Screen):
    
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

                if not re.match("^[A-Za-z]*$", fname):
                    return toast('Enter your first name.')
                elif not re.match("^[A-Za-z]*$", lname):
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
                        conn.commit()
                        self.manager.transition.direction = "right"
                        self.manager.transition.duration = 0.5
                        self.manager.current = "login_screen"
                        return toast('Registration complete. Please login.')
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

class ForgotScreen(Screen):
    
    def do_reset(self, reemailtext, pastext, repastext):

        reemail = reemailtext
        paste = pastext
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        find = ("SELECT * FROM accounts WHERE emid=? ")
        cur.execute(find, [(reemail)])
        results = cur.fetchall()
        if(len(reemail)>0):
            if results:
                cur.execute('UPDATE accounts SET passwd=? WHERE emid = ?', (paste,reemail))
                conn.commit()
                for element in results:
                    self.manager.transition.direction = "right"
                    self.manager.transition.duration = 0.5
                    self.manager.current = "login"
                    return toast('Your password has been updated. Please login.')
            else:
                return toast('Please enter your registered email.')
        else:
            return toast('Please enter an email address.')

        conn.close()
        self.ids['reemail'].text = ""
        self.ids['pas'].text = ""
        self.ids['repas'].text = ""

class AddHashtag(BoxLayout):
    
    def add_hashtag(self, user_hashtag):
        
        hashtag = user_hashtag.lower()
        id_u = user_key[0]
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

class AddTask(BoxLayout):

    def on_checkbox_active(self, checkbox, value):

        if value:
            task_tag_list.append('important')
        else:
            task_tag_list.append('normal')

    def on_save(self, instance, value, date_range):

        date = value
        task_due_list.append(date)

    def on_cancel(self, instance, value):

        pass

    def show_date_picker(self):

        date_dialog = MDDatePicker(primary_color=get_color_from_hex("#C69C6D"),
                                    accent_color=get_color_from_hex("#F3EBE2"),
                                    selector_color=get_color_from_hex("#C6826D"),
                                    text_toolbar_color=get_color_from_hex("#cccccc"),
                                    text_color=("#C69C6D"),
                                    text_current_color=get_color_from_hex("#e93f39"),
                                    input_field_background_color=(1, 1, 1, 0.2),
                                    input_field_text_color=get_color_from_hex("#C69C6D"),
                                    text_button_color=get_color_from_hex("#C69C6D"),
                                    font_name="segoeui.ttf",
                                    min_date=date.today(),max_date=datetime.strptime("2025:05:30", '%Y:%m:%d').date())
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

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

    def get_time(self, instance, time):

        task_time_list.append(time)

    def get_task(self, title, info):

        id_u = user_key[0]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

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
        print('Task added.')
        toast('Task Added.')

        conn.close()

        self.ids['task_name'].text = ""
        self.ids['task_details'].text = ""

class TaskInfo(BoxLayout):
    
    def add_hashtag(self, user_hashtag):
        
        hashtag = user_hashtag.lower()
        id_u = user_key[0]
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

class DetailedTaskCard(BoxLayout):

    pass

class HashtagsL(OneLineListItem):

    index = NumericProperty()

class Card(MDCard):

    title = StringProperty('')
    details = StringProperty('')

class Card2(MDCard):
    
    title = StringProperty('')
    title2 = StringProperty('')
    info = StringProperty('')
    details = StringProperty('')
    details_cut = StringProperty('')
    index_color = NumericProperty()
    task_idpk = StringProperty('')

    dialog3 = None
    index = NumericProperty()

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

    def task_dialog(self, title_task, info_task, details_task, id_task):
        
        if not self.dialog3:
            index_task.append(id_task)
            self.dialog3 = MDDialog(
                title = title_task + ' | ' + info_task,
                text = details_task,
                buttons=[
                    MDFillRoundFlatButton(
                        text="MARK AS DONE",
                        theme_text_color = 'Custom',
		                md_bg_color ='#C6826D',
		                text_color = '#F1ECEC',
                        on_release = lambda x:self.mark_as_done(),
                    ),
                ],
                # type = "custom",
                # content_cls=DetailedTaskCard(),
            )
        self.dialog3.open()

    def dialog_close(self, *args):
        self.dialog3.dismiss(force=True)

class HomeScreen(Screen):

    dialog1 = None
    dialog2 = None
    index = NumericProperty()

    def add_hashtag_dialog(self):

        if not self.dialog1:
            self.dialog1 = MDDialog(
                title="Add a Hashtag:",
                type="custom",
                content_cls=AddHashtag(),
            )
        self.dialog1.open() 

    def add_task_dialog(self):
    
        if not self.dialog2:
            self.dialog2 = MDDialog(
                title = "Add a Task:",
                type = "custom",
                content_cls = AddTask(),
            )
        self.dialog2.open()

    def refresh_callback(self, *args):

            def refresh_callback(interval):
                
                self.ids.container.clear_widgets()
                self.ids.hashtag_tasks.clear_widgets()
                self.ids.important_tasks.clear_widgets()
                
                if self.x == 0:
                    self.x, self.y = 1, 1
                else:
                    self.x, self.y = 0, 0
                self.on_enter()
                self.ids.refresh_layout.refresh_done()

            Clock.schedule_once(refresh_callback, 1)

    def on_enter(self, *args):

        months = ['January','February','March','April','May','June','July','August','September','October','November','December']

        # IMPORTANT TASKS SIDE
        id_u = user_key[0]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()
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

        # HASHTAGS SIDE
        find = ("SELECT * FROM hashtags WHERE id_user=" + str(id_u))
        cur.execute(find)
        results = cur.fetchall()

        for i in results:
            k = i[1]

            self.ids.container.add_widget(HashtagsL(index=i[0],text=f"#{k}", divider=None,\
            theme_text_color='Custom', text_color='#FFFFFF', on_release=self.callback))

        async def on_enter():

            id_h = index_hashtag[-1]
            find = ("SELECT * FROM TASKS WHERE id_hashtag=" + str(id_h) + " ORDER BY task_due_date, task_due_date_time ASC")
            cur.execute(find)
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

        asynckivy.start(on_enter())

    def callback(self,instance):

        index_h = instance.index
        index_hashtag.clear()
        index_hashtag.append(index_h)

        self.ids.container.clear_widgets()
        self.ids.hashtag_tasks.clear_widgets()
        self.ids.important_tasks.clear_widgets()
        self.on_enter()
        self.hashtag_label()
        
        print(index_h)
        print(index_hashtag)

    def hashtag_label(self):
        
        h_index = index_hashtag[-1]
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        find = ("SELECT * FROM hashtags WHERE id_hashtag=" + str(h_index))
        cur.execute(find)
        results = cur.fetchall()
        print(results)

        j = results[0][1]

        self.ids.h.clear_widgets()
        return '#' + str(j) 

    def calendar(self):

        months = ['January','February','March','April','May','June','July','August','September','October','November','December']

        todays_date = date.today()

        yy = str(todays_date.year) # year
        mm = months[todays_date.month - 1] # month
        dd = str(todays_date.day) # day

        # display the date
        return mm + ' ' + dd + ',' + ' ' + yy

    def output(self):
        print('k')

screen_manager=ScreenManager()
screen_manager.add_widget(LoginScreen(name = "login_screen"))
screen_manager.add_widget(RegisterScreen(name = "register_screen"))
screen_manager.add_widget(ForgotScreen(name = "forgot_screen"))
screen_manager.add_widget(HomeScreen(name = "home_screen"))

class MyApp(MDApp):
    title="CodiPie - Organize your tasks"

    def build(self):
        screen = Builder.load_file("main.kv")
        self.theme_cls.primary_palette = 'Brown'
        self.theme_cls.primary_hue = "200"  
        return screen

if __name__ == '__main__':
    MyApp().run()