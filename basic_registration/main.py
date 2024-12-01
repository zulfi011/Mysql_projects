import tkinter as tk
from tkinter import *
import pymysql
from dotenv import load_dotenv
import os


class Managment:
    def __init__(self,root,conn,cursor):
        self.conn = conn
        self.curosr = cursor
        self.root = root
        self.root.title('app')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        banner = Label(self.root,text='Registration Managment System',justify='center',relief='solid',background='lightblue',fg='red',font=("TkDefaultFont",40),bd=5)
        banner.pack(side='top',fill='both')

        self.main_frame = Frame(self.root,bg='lightblue',bd=2,relief='solid',width=450,height=600)
        self.main_frame.pack(side='top',pady=20)

        signup_btn = Button(self.main_frame,text='Sign up',bg='white',bd=2,relief='solid',font=("TkDefaultFont",15),command=self.signup,height=2,width=20)
        signup_btn.grid(row=0,column=0,pady=70)
        login_btn = Button(self.main_frame,text='Login',bg='white',font=("TkDefaultFont",15),border=2,relief='solid',command=self.login,height=2,width=20)
        login_btn.grid(row=1,column=0,padx=100)
        close = Button(self.main_frame,text='Close',bg='white',font=("TkDefaultFont",15),bd=2,relief='solid',height=2,width=20,command=lambda: self.root.destroy())
        close.grid(row=2,column=0,pady=70)
    

        # ============== signup section  ===================
    def signup(self):
        self.main_frame.pack_forget()
        signup_frame = Frame(self.root,bg='lightblue',width=450,height=600,bd=2,relief='solid')
        signup_frame.grid_propagate(False)
        signup_frame.pack(side='top',pady=20)

        user_label = Label(signup_frame,text="user name : ",bg='lightblue',font=("TkDefaultFont",20),padx=40)
        user_label.grid(row=0,column=0,pady=30)
        user_entry = Entry(signup_frame,state='normal')
        user_entry.grid(row=0,column=1)
        pwd_label = Label(signup_frame,text="password : ",bg='lightblue',font=("TkDefaultFont",20),padx=40)
        pwd_label.grid(row=1,column=0)
        pwd_entry = Entry(signup_frame,state='normal')
        pwd_entry.grid(row=1,column=1)
        pwd_comfirm = Label(signup_frame,text="confirm password : ",wraplength=150,bg='lightblue',font=("TkDefaultFont",20),padx=40)
        pwd_comfirm.grid(row=2,column=0)
        confirm_entry = Entry(signup_frame,state='normal')
        confirm_entry.grid(row=2,column=1,pady=40)

        get_signin_values = Button(signup_frame,text="Ok",bg="white",font=("TkDefaultFont",15),bd=2,relief='solid',command=lambda:self.insert_into_db(user_entry,pwd_entry,confirm_entry,signup_frame),width=10,height=1).grid(row=3,column=0,pady=50)
        get_back = Button(signup_frame,text="Cancel",bg="white",font=("TkDefaultFont",15),bd=2,relief='solid',command=lambda:self.go_back(signup_frame),width=10,height=1).grid(row=3,column=1)

    def insert_into_db(self,user,pwd,confirm,frame):
        user_val = user.get()
        pwd_val = pwd.get()
        confirm_val = confirm.get()
        if user_val and pwd_val and confirm_val:
            try:
                if pwd_val == confirm_val:
                    insert_query = "INSERT INTO signup(user_name,password) VALUES (%s,%s)"
                    data = (user_val,pwd_val)
                    self.curosr.execute(insert_query,data)
                    self.conn.commit()
                    user.delete(0,tk.END)
                    pwd.delete(0,tk.END)
                    confirm.delete(0,tk.END)
                    message = Message(frame,text=f"{user_val} saved as a user!!!",bg="lightblue",font=("TkDefaultFont",12),bd=2,relief='solid',justify='center',width=450,pady=10)
                    message.grid(row=0,column=0,columnspan=2,sticky='n')
                    self.root.after(1000,lambda:message.grid_forget())
                else:
                    message = Message(frame,text="plz confirm password!!!",bg="lightblue",font=("TkDefaultFont",12),bd=2,relief='solid',justify='center',width=450,pady=10)
                    message.grid(row=0,column=0,columnspan=2,sticky='n')
                    self.root.after(1000,lambda:message.grid_forget())
            except Exception as e:
                print(e)
                message = Message(frame,text="user already exists!!!",bg="lightblue",font=("TkDefaultFont",12),bd=2,relief='solid',justify='center',width=450,pady=10)
                message.grid(row=0,column=0,columnspan=2,sticky='n')
                self.root.after(1000,lambda:message.grid_forget())
        else:
            message = Message(frame,text="fill all the fields!!!",bg="lightblue",font=("TkDefaultFont",12),bd=2,relief='solid',justify='center',width=450,pady=10)
            message.grid(row=0,column=0,columnspan=2,sticky='n')
            self.root.after(1000,lambda:message.grid_forget())
    

    # ========================  login section  ===========================
    def login(self):
        self.main_frame.pack_forget()
        login_frame = Frame(self.root,bg='lightblue',width=450,height=600,bd=2,relief='solid')
        login_frame.grid_propagate(False)
        login_frame.pack(side='top',pady=20)

        user_label = Label(login_frame,text="user name : ",bg='lightblue',font=("TkDefaultFont",20),padx=40)
        user_label.grid(row=0,column=0,pady=30)
        user_entry = Entry(login_frame,state='normal')
        user_entry.grid(row=0,column=1)
        pwd_label = Label(login_frame,text="password : ",bg='lightblue',font=("TkDefaultFont",20),padx=40)
        pwd_label.grid(row=1,column=0)
        pwd_entry = Entry(login_frame,state='normal')
        pwd_entry.grid(row=1,column=1)

        get_login_values = Button(login_frame,text="Ok",bg="white",font=("TkDefaultFont",15),bd=2,relief='solid',command=lambda:self.login_from_db(user_entry,pwd_entry,login_frame),width=10,height=1).grid(row=2,column=0,pady=50)
        get_back = Button(login_frame,text="Cancel",bg="white",font=("TkDefaultFont",15),bd=2,relief='solid',command=lambda:self.go_back(login_frame),width=10,height=1).grid(row=2,column=1)

    def login_from_db(self,user,pwd,frame):
        user_val = user.get()
        pwd_val = pwd.get()
        if user_val and pwd_val:
            try:
                user_read_query = "SELECT user_name FROM signup WHERE user_name = %s"
                cursor.execute(user_read_query, user_val)
                user_read = cursor.fetchone()
                if not user_read:
                    message = Message(frame,text="no such user!!!",bg="lightblue",font=("TkDefaultFont",12),bd=2,relief='solid',justify='center',width=450,pady=10)
                    message.grid(row=0,column=0,columnspan=2,sticky='n')
                    self.root.after(1000,lambda:message.grid_forget())
                else:
                    pwd_read_query = "SELECT user_name,password FROM signup WHERE user_name=%s AND password = %s"
                    cursor.execute(pwd_read_query, (user_val,pwd_val))
                    pwd_read = cursor.fetchone()
                    if pwd_read:
                        frame.pack_forget()
                        welcome_frame = Frame(self.root,bg='lightblue',bd=2,relief='solid',width=450,height=600)
                        welcome_frame.pack_propagate(False)
                        welcome_frame.pack(side='top',pady=20)
                        wel_label = Label(welcome_frame,text=f"welcome \n{user_read[0]}",font=("TkDefaultFont",25),fg="red",bg='lightblue',justify='center').pack(pady=70,side='top')
                        wel_button = Button(welcome_frame,text="Go Back",bg="white",font=("TkDefaultFont",15),bd=2,relief='solid',command=lambda:self.go_to_login(frame,welcome_frame),width=10,height=1).pack(side='top')
                    else:
                        message = Message(frame,text="wrong password!!!",bg="lightblue",font=("TkDefaultFont",12),bd=2,relief='solid',justify='center',width=450,pady=10)
                        message.grid(row=0,column=0,columnspan=2,sticky='n')
                        self.root.after(1000,lambda:message.grid_forget())
            except Exception as e:
                print(e)
        else:
            message = Message(frame,text="fill all the fields!!!",bg="lightblue",font=("TkDefaultFont",12),bd=2,relief='solid',justify='center',width=450,pady=10)
            message.grid(row=0,column=0,columnspan=2,sticky='n')
            self.root.after(1000,lambda:message.grid_forget())


    # go back button
    def go_back(self,frame):
        frame.pack_forget()
        self.main_frame.pack(side='top',pady=20)
    def go_to_login(self,log_frame,wel_frame):
        wel_frame.pack_forget()
        log_frame.pack(side='top',pady=20)


            

# database 
try:
    load_dotenv()
    DB_CONFIG = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    conn = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    cursor = conn.cursor()
    root = tk.Tk()
    manage = Managment(root,conn,cursor)
    root.mainloop()
except Exception as e:
            print("couldn't connect database",e)
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
