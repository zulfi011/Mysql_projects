import tkinter as tk
from tkinter import *
from tkinter import messagebox,ttk
import pymysql
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


class Managment:
    def __init__(self,root,conn,cursor):
        self.conn = conn
        self.cursor = cursor
        self.root = root
        self.root.title("app")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        main_label = Label(self.root,text="Library Managment",bg="lightgreen",fg="blue",bd=5,relief='groove',font=("Ariel",40,"bold"))
        main_label.pack(side="top",fill="both")

        # ----- button frame -----
        btn_frame = Frame(self.root,bg='lightblue',bd=3,relief='groove',width=350,height=500)
        btn_frame.pack_propagate(False)
        btn_frame.pack(side='left',padx=70)
        user_btn = Button(btn_frame,text='user',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',command=lambda:self.make_choice(0),width=20,height=1)
        user_btn.pack(side='top',pady=10)
        book_btn = Button(btn_frame,text='book',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',command=lambda:self.make_choice(1),width=20,height=1)
        book_btn.pack(side='top',pady=10)
        borrow_btn = Button(btn_frame,text='borrow book',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',command=self.borrow_book,width=20,height=1)
        borrow_btn.pack(side='top',pady=10)
        return_btn = Button(btn_frame,text='return book',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',command=self.return_book,width=20,height=1)
        return_btn.pack(side='top',pady=10)
        search_btn = Button(btn_frame,text='search',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',command=lambda:self.make_choice(2),width=20,height=1)
        search_btn.pack(side='top',pady=10)
        show_btn = Button(btn_frame,text='show all',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',command=lambda:self.make_choice(3),width=20,height=1)
        show_btn.pack(side='top',pady=10)
        close_btn = Button(btn_frame,text='close',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',command=lambda:self.root.destroy(),width=20,height=1)
        close_btn.pack(side='top',pady=10)

        # ----- info data frame -----
        data_frame = Frame(self.root,bg='lightblue',bd=3,relief='groove',width=800,height=500)
        data_frame.pack_propagate(False)
        data_frame.pack(side='left')
        x_scrol = tk.Scrollbar(data_frame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")
        y_scrol = tk.Scrollbar(data_frame, orient="vertical")
        y_scrol.pack(side="right", fill="y")
        self.table = ttk.Treeview(data_frame,xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set)
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        self.table.pack(fill='both',expand=True)


    # ----------------- tab choice frame  ---------------------
    def make_choice(self,choice):
        text = ""
        if choice==0:
            text = "user"
        elif choice==1:
            text = "book"
        elif choice==2:
            text = "search"
        else:
            text = "show"

        choice_frame = Frame(self.root,bg='lightgreen',bd=3,relief='groove')
        choice_frame.place(x=500,y=90,width=350,height=300)

        btn_one = Button(choice_frame,text=f'add {text}',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',width=20,height=1)
        btn_one.pack(side='top',pady=10)
        btn_two = Button(choice_frame,text=f'remove {text}',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',width=20,height=1)
        btn_two.pack(side='top',pady=10)
        close_btn = Button(choice_frame,text='close',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',command=lambda:choice_frame.destroy(),width=20,height=1)
        close_btn.pack(side='top',pady=10)

        if text=="user":
            btn_one.config(command=self.add_usr)
            btn_two.config(command=lambda:self.remove_usr_book(True))
        elif text=="book":
            btn_one.config(command=self.add_book)
            btn_two.config(command=lambda:self.remove_usr_book(False))
        elif text=="search":
            btn_one.config(text="search user")
            btn_two.config(text="search book")
            btn_one.config(command=self.search_usr)
            btn_two.config(command=self.search_book)
        else:
            btn_one.config(text="all user")
            btn_two.config(text="all book")
            btn_one.config(command=lambda:self.show_all(0,choice_frame))
            btn_two.config(command=lambda:self.show_all(1,choice_frame))
            close_btn.config(text="borrowing history",command=lambda:self.show_all(2,choice_frame))
            new_close = Button(choice_frame,text='close',bg='silver',bd=2,relief='groove',font=('Arial',20,'bold'),fg='blue',command=lambda:choice_frame.destroy(),width=20,height=1)
            new_close.pack(side='top',pady=10)


    # --------- user ---------------
    def add_usr(self):
        local_frame = Frame(self.root,bg='lightgreen',bd=3,relief='groove')
        local_frame.grid_propagate(False)
        local_frame.place(x=500,y=90,width=350,height=300)
        
        name_label= Label(local_frame,text="Name :",font=('Arial',20,'bold'),bg='lightgreen')
        name_label.grid(row=0,column=0,pady=20,padx=30)
        name_entry = Entry(local_frame,bg='white',state='normal',textvariable=StringVar())
        name_entry.grid(row=0,column=1,pady=20,padx=10)
        
        email_label= Label(local_frame,text="Email :",font=('Arial',20,'bold'),bg='lightgreen')
        email_label.grid(row=1,column=0,pady=20,padx=30)
        email_entry = Entry(local_frame,bg='white',state='normal',textvariable=StringVar())
        email_entry.grid(row=1,column=1,pady=20,padx=10)

        btn_frame = Frame(local_frame,bg='lightgreen',width=300,height=100)
        btn_frame.pack_propagate(False)
        btn_frame.grid(row=2,column=0,columnspan=2)
        get_value_btn = Button(btn_frame,text="Add",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:self.add_usr_into_db(name_entry,email_entry),height=1,width=10)
        get_value_btn.pack(side='left')
        close_btn = Button(btn_frame,text="Close",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:local_frame.destroy(),height=1,width=10)
        close_btn.pack(side='right')

    def add_usr_into_db(self,name,email):
        name_val = (name.get()).capitalize()
        email_val = email.get()
        print(name_val,email_val)
        if name_val and email_val:
            try:
                insert_query = "INSERT INTO user_table(name,email) VALUES (%s,%s)"
                data = (name_val,email_val)
                self.cursor.execute(insert_query,data)
                self.conn.commit()
                name.delete(0,tk.END)
                email.delete(0,tk.END)
                messagebox.showinfo("",f"{name_val} added as a user")
            except pymysql.MySQLError as e:
                print(e)
                messagebox.showinfo("",f"{name_val} user already exists")
        else:
            messagebox.showinfo("","plz fill all the fields")
  

    # ----------- book --------------
    def add_book(self):
        local_frame = Frame(self.root,bg='lightgreen',bd=3,relief='groove')
        local_frame.grid_propagate(False)
        local_frame.place(x=500,y=90,width=450,height=500)
        
        title_label= Label(local_frame,text="Title :",font=('Arial',20,'bold'),bg='lightgreen')
        title_label.grid(row=0,column=0,pady=20,padx=30)
        title_entry = Entry(local_frame,bg='white',state='normal',textvariable=StringVar())
        title_entry.grid(row=0,column=1,pady=20,padx=10)
        
        author_label= Label(local_frame,text="Author :",font=('Arial',20,'bold'),bg='lightgreen')
        author_label.grid(row=1,column=0,pady=20,padx=30)
        author_entry = Entry(local_frame,bg='white',state='normal',textvariable=StringVar())
        author_entry.grid(row=1,column=1,pady=20,padx=10)

        genre_label= Label(local_frame,text="Genre :",font=('Arial',20,'bold'),bg='lightgreen')
        genre_label.grid(row=2,column=0,pady=20,padx=30)
        genre_entry = Entry(local_frame,bg='white',state='normal',textvariable=StringVar())
        genre_entry.grid(row=2,column=1,pady=20,padx=10)

        available_label= Label(local_frame,text="Available :",font=('Arial',20,'bold'),bg='lightgreen')
        available_label.grid(row=3,column=0,pady=20,padx=30)
        available_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        available_entry.grid(row=3,column=1,pady=20,padx=10)

        total_label= Label(local_frame,text="Total :",font=('Arial',20,'bold'),bg='lightgreen')
        total_label.grid(row=4,column=0,pady=20,padx=30)
        total_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        total_entry.grid(row=4,column=1,pady=20,padx=10)

        btn_frame = Frame(local_frame,bg='lightgreen',width=300,height=100)
        btn_frame.pack_propagate(False)
        btn_frame.grid(row=5,column=0,columnspan=2)
        get_value_btn = Button(btn_frame,text="Add",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:self.add_book_into_db(title_entry,author_entry,genre_entry,available_entry,total_entry),height=1,width=10)
        get_value_btn.pack(side='left')
        close_btn = Button(btn_frame,text="Close",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:local_frame.destroy(),height=1,width=10)
        close_btn.pack(side='right')

    def add_book_into_db(self,title,author,genre,available,total):
        title_val = (title.get()).capitalize()
        author_val = (author.get()).capitalize()
        genre_val = (genre.get()).capitalize()
        available_val = available.get()
        total_val = total.get()
        if title_val and author_val and genre_val:
            if available_val <= total_val:
                try:
                    insert_query = "INSERT INTO books_table(title,author,genre,available_copies,total_copies) VALUES (%s,%s,%s,%s,%s)"
                    data = (title_val,author_val,genre_val,available_val,total_val)
                    self.cursor.execute(insert_query,data)
                    self.conn.commit()
                    title.delete(0,tk.END)
                    author.delete(0,tk.END)
                    genre.delete(0,tk.END)
                    available.delete(0,tk.END)
                    total.delete(0,tk.END)
                    messagebox.showinfo("",f"{title_val} added into books")
                except pymysql.MySQLError as e:
                    messagebox.showinfo("",f"{title_val} book already exists")
            else:
                messagebox.showinfo("","available cannot be greater than total")
        else:
            messagebox.showinfo("","plz fill all the fields")


    # ----------- same functions for removing usr and book  ----------------
    def remove_usr_book(self,usr_book):
        local_frame = Frame(self.root,bg='lightgreen',bd=3,relief='groove')
        local_frame.grid_propagate(False)
        local_frame.place(x=500,y=90,width=350,height=300)
        
        id_label= Label(local_frame,text="Id :",font=('Arial',20,'bold'),bg='lightgreen')
        id_label.grid(row=0,column=0,pady=20,padx=40)
        id_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        id_entry.grid(row=0,column=1,pady=20,padx=20)

        btn_frame = Frame(local_frame,bg='lightgreen',width=300,height=100)
        btn_frame.pack_propagate(False)
        btn_frame.grid(row=2,column=0,columnspan=2)
        get_value_btn = Button(btn_frame,text="Remove",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:self.remove_from_db(id_entry,usr_book),height=1,width=10)
        get_value_btn.pack(side='left')
        close_btn = Button(btn_frame,text="Close",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:local_frame.destroy(),height=1,width=10)
        close_btn.pack(side='right')
        
    def remove_from_db(self,ids,usr_book):
        id_val = ids.get()
        table = ""
        if usr_book:
            table = "user_table"
        else:
            table = "books_table"
        if id_val:
            try:
                all_ids = f"SELECT id FROM {table} WHERE "+ "id=(%s)"
                search_val = (id_val)
                self.cursor.execute(all_ids,search_val)
                row = self.cursor.fetchall()
                print(row)
                if row:
                    delete_query = f"DELETE FROM {table} WHERE " "id=(%s)"
                    data = (id_val)
                    self.cursor.execute(delete_query,data)
                    self.conn.commit()
                    ids.delete(0,tk.END)
                    messagebox.showinfo("",f"{id_val} deleted")
                else:
                    messagebox.showinfo("",f"{id_val} no such id")
            except pymysql.MySQLError as e:
                print(e)
        else:
            messagebox.showinfo("","plz fill the fields")

    
    # -----------------  borrow book ---------------
    def borrow_book(self):
        local_frame = Frame(self.root,bg='lightgreen',bd=3,relief='groove')
        local_frame.grid_propagate(False)
        local_frame.place(x=500,y=90,width=450,height=500)
        
        usr_label= Label(local_frame,text="User Id :",font=('Arial',20,'bold'),bg='lightgreen')
        usr_label.grid(row=0,column=0,pady=20,padx=30)
        usr_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        usr_entry.grid(row=0,column=1,pady=20,padx=10)
        
        book_label= Label(local_frame,text="Book Id :",font=('Arial',20,'bold'),bg='lightgreen')
        book_label.grid(row=1,column=0,pady=20,padx=30)
        book_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        book_entry.grid(row=1,column=1,pady=20,padx=10)

        borrow_label= Label(local_frame,text="Borrow\nDate :",font=('Arial',20,'bold'),bg='lightgreen')
        borrow_label.grid(row=2,column=0,pady=20,padx=30)
        borrow_entry = Entry(local_frame,bg='white',state='normal')
        borrow_entry.grid(row=2,column=1,pady=20,padx=10)
        borrow_entry.insert(0,"today : "+datetime.now().strftime("%d-%m-%Y"))
        
        borrow_days_label= Label(local_frame,text="For Days :",font=('Arial',20,'bold'),bg='lightgreen')
        borrow_days_label.grid(row=3,column=0,pady=20,padx=30)
        borrow_days_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        borrow_days_entry.grid(row=3,column=1,pady=20,padx=10)

        btn_frame = Frame(local_frame,bg='lightgreen',width=300,height=100)
        btn_frame.pack_propagate(False)
        btn_frame.grid(row=5,column=0,columnspan=2)
        get_value_btn = Button(btn_frame,text="Borrow",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:self.borrow_into_db(usr_entry,book_entry,borrow_days_entry),height=1,width=10)
        get_value_btn.pack(side='left')
        close_btn = Button(btn_frame,text="Close",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:local_frame.destroy(),height=1,width=10)
        close_btn.pack(side='right')

    def borrow_into_db(self,usr,book,days):
        usr_id,book_id = int(usr.get()),int(book.get())
        g_days = int(days.get())
        days_val = datetime.now() + timedelta(days=g_days)
        if usr_id>0 and book_id>0 and g_days>0:
            try:
                ava_books = "SELECT available_copies FROM books_table WHERE id=%s"
                ava_data = (book_id)
                self.cursor.execute(ava_books,ava_data)
                ava = self.cursor.fetchone()
                try:
                    borrow_his = "SELECT count(id) FROM borrow_return_table WHERE user_id=%s and book_id=%s and status=%s"
                    borrow_data = (usr_id,book_id,"borrowed")
                    self.cursor.execute(borrow_his,borrow_data)
                    borrow_data = self.cursor.fetchone()
                    print(borrow_data)
                    if borrow_data[0]==0:
                        if ava[0]>0:
                            insert_query = "INSERT INTO borrow_return_table(user_id,book_id,due_date,status) VALUES (%s,%s,%s,%s)"
                            data = (usr_id,book_id,days_val,"borrowed")
                            self.cursor.execute(insert_query,data)
                            self.conn.commit()
                            self.update_revelant_tb(usr_id,book_id,True)
                            usr.delete(0,tk.END)
                            book.delete(0,tk.END)
                            days.delete(0,tk.END)
                            messagebox.showinfo("",f"book borrowed")
                        else:
                            messagebox.showinfo("","out of stock")
                    else:
                        messagebox.showinfo("","user already borrowed this book")
                except Exception as e:
                    messagebox.showinfo("","user already borrowed this book")
            except pymysql.MySQLError as e:
                print(e)
                messagebox.showinfo("",f"no user or book by that id")
        else:
            messagebox.showinfo("","plz fill all the fields")
    

    # ---------- return book --------------------
    def return_book(self):
        local_frame = Frame(self.root,bg='lightgreen',bd=3,relief='groove')
        local_frame.grid_propagate(False)
        local_frame.place(x=500,y=90,width=450,height=500)
        
        usr_label= Label(local_frame,text="User Id :",font=('Arial',20,'bold'),bg='lightgreen')
        usr_label.grid(row=0,column=0,pady=20,padx=30)
        usr_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        usr_entry.grid(row=0,column=1,pady=20,padx=10)
        
        book_label= Label(local_frame,text="Book Id :",font=('Arial',20,'bold'),bg='lightgreen')
        book_label.grid(row=1,column=0,pady=20,padx=30)
        book_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        book_entry.grid(row=1,column=1,pady=20,padx=10)

        btn_frame = Frame(local_frame,bg='lightgreen',width=300,height=100)
        btn_frame.pack_propagate(False)
        btn_frame.grid(row=5,column=0,columnspan=2)
        get_value_btn = Button(btn_frame,text="Return",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:self.return_into_db(usr_entry,book_entry),height=1,width=10)
        get_value_btn.pack(side='left')
        close_btn = Button(btn_frame,text="Close",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:local_frame.destroy(),height=1,width=10)
        close_btn.pack(side='right')
    
    def return_into_db(self,usr,book):
        usr_id,book_id = int(usr.get()),int(book.get())
        if usr_id>0 and book_id>0:
            try:
                select_query = "SELECT count(id) from borrow_return_table where user_id=%s and book_id=%s and status=%s"
                sel_val = (usr_id,book_id,"borrowed")
                self.cursor.execute(select_query,sel_val)
                id_count = self.cursor.fetchone()
                select_query = "SELECT books_borrowed from user_table where id=%s"
                sel_val = (usr_id)
                self.cursor.execute(select_query,sel_val)
                no_of_books = self.cursor.fetchone()
                if id_count[0]>0 and no_of_books[0]>0:
                    update_query = "UPDATE borrow_return_table set status=%s where user_id=%s and book_id=%s"
                    data = ("returned",usr_id,book_id)
                    self.cursor.execute(update_query,data)
                    self.conn.commit()
                    self.update_revelant_tb(usr_id,book_id,False)
                    usr.delete(0,tk.END)
                    book.delete(0,tk.END)
                    messagebox.showinfo("",f"{usr_id} returned the book")
                else:
                    messagebox.showinfo("","no one of this data has borrowed any book")
            except Exception as e:
                print(e)
        else:
            messagebox.showinfo("","fill all the fillds")

    # ----------- same function for updating borrowing or returning tables ---------
    def update_revelant_tb(self,usr_id,book_id,from_borrow):
        try:
            get_usr = "SELECT books_borrowed FROM user_table WHERE id=%s"
            usr_val = (usr_id)
            self.cursor.execute(get_usr,usr_val)
            usr_val = self.cursor.fetchone()
            get_ava_book = "SELECT available_copies FROM books_table WHERE id=%s"
            ava_val = (book_id)
            self.cursor.execute(get_ava_book,ava_val)
            ava_val = self.cursor.fetchone()
            up_ava,up_usr = 0,0
            if from_borrow:
                up_ava = ava_val[0]-1
                up_usr = usr_val[0]+1
            else:
                up_ava = ava_val[0]+1
                up_usr = usr_val[0]-1
            update_books = "UPDATE books_table SET available_copies=%s WHERE id=%s"
            up_val = (up_ava,book_id)
            self.cursor.execute(update_books,up_val)
            self.conn.commit()
            update_usr = "UPDATE user_table SET books_borrowed=%s WHERE id=%s"
            up_val = (up_usr,usr_id)
            self.cursor.execute(update_usr,up_val)
            self.conn.commit()
        except Exception as e:
            print(e)

    # -------------- search section ---------------------- 
    def search_usr(self):
        local_frame = Frame(self.root,bg='lightgreen',bd=3,relief='groove')
        local_frame.grid_propagate(False)
        local_frame.place(x=500,y=90,width=450,height=500)
        
        id_label= Label(local_frame,text="By Id :",font=('Arial',20,'bold'),bg='lightgreen')
        id_label.grid(row=0,column=0,pady=20,padx=30)
        id_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        id_entry.grid(row=0,column=1,pady=20,padx=10)
        
        name_label= Label(local_frame,text="By Name :" ,font=('Arial',20,'bold'),bg='lightgreen')
        name_label.grid(row=1,column=0,pady=20,padx=30)
        name_entry = Entry(local_frame,bg='white',state='normal',textvariable=StringVar())
        name_entry.grid(row=1,column=1,pady=20,padx=10)

        btn_frame = Frame(local_frame,bg='lightgreen',width=300,height=100)
        btn_frame.pack_propagate(False)
        btn_frame.grid(row=3,column=0,columnspan=2)
        get_value_btn = Button(btn_frame,text="search",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:self.search_usr_db(id_entry,name_entry,local_frame),height=1,width=10)
        get_value_btn.pack(side='left')
        close_btn = Button(btn_frame,text="Close",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:local_frame.destroy(),height=1,width=10)
        close_btn.pack(side='right')
    def search_usr_db(self,ids,name,frame):
        id_value = int(ids.get())
        name_value = name.get()
        query = "SELECT * FROM user_table WHERE"
        conditions = []
        if id_value != 0:
            conditions.append(f"id={id_value}")
        if name_value != "":
            conditions.append(f"name='{name_value}'")

        if conditions:
            query += " " + " AND ".join(conditions)
        else:
            query = "" 
        print("Query:", query)
        if query != "":
            self.table.config(columns=("id","user_name","email","books_borrowed"))
            self.table.heading("id", text="Id")
            self.table.heading("user_name", text="Name")
            self.table.heading("email", text="Email")
            self.table.heading("books_borrowed", text="Books Borrowed")
            self.table["show"] = "headings"
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                if rows:
                    self.table.delete(*self.table.get_children())
                    for row in rows:
                        self.table.insert('',tk.END,values=row)
                frame.destroy()
            except Exception as e:
                print(e)


    def search_book(self):
        local_frame = Frame(self.root,bg='lightgreen',bd=3,relief='groove')
        local_frame.grid_propagate(False)
        local_frame.place(x=500,y=90,width=450,height=500)
        
        id_label= Label(local_frame,text="By Id :",font=('Arial',20,'bold'),bg='lightgreen')
        id_label.grid(row=0,column=0,pady=20,padx=30)
        id_entry = Entry(local_frame,bg='white',state='normal',textvariable=IntVar())
        id_entry.grid(row=0,column=1,pady=20,padx=10)

        title_label= Label(local_frame,text="By Title :",font=('Arial',20,'bold'),bg='lightgreen')
        title_label.grid(row=1,column=0,pady=20,padx=30)
        title_entry = Entry(local_frame,bg='white',state='normal',textvariable=StringVar())
        title_entry.grid(row=1,column=1,pady=20,padx=10)
        
        author_label= Label(local_frame,text="By Author :",font=('Arial',20,'bold'),bg='lightgreen')
        author_label.grid(row=2,column=0,pady=20,padx=30)
        author_entry = Entry(local_frame,bg='white',state='normal',textvariable=StringVar())
        author_entry.grid(row=2,column=1,pady=20,padx=10)

        genre_label= Label(local_frame,text="By Genre :",font=('Arial',20,'bold'),bg='lightgreen')
        genre_label.grid(row=3,column=0,pady=20,padx=30)
        genre_entry = Entry(local_frame,bg='white',state='normal',textvariable=StringVar())
        genre_entry.grid(row=3,column=1,pady=20,padx=10)


        btn_frame = Frame(local_frame,bg='lightgreen',width=300,height=100)
        btn_frame.pack_propagate(False)
        btn_frame.grid(row=4,column=0,columnspan=2)
        get_value_btn = Button(btn_frame,text="Search",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:self.search_book_db(id_entry,title_entry,author_entry,genre_entry,local_frame),height=1,width=10)
        get_value_btn.pack(side='left')
        close_btn = Button(btn_frame,text="Close",bg='lightblue',bd=3,relief='groove',font=('Arial',15,'bold'),command=lambda:local_frame.destroy(),height=1,width=10)
        close_btn.pack(side='right')
    def search_book_db(self,ids,title,author,genre,frame):
        id_val,title_val,author_val,genre_val = int(ids.get()),title.get(),author.get(),genre.get()
        query = "SELECT * FROM books_table WHERE"
        conditions = []
        if id_val != 0:
            conditions.append(f"id={id_val}")
        if title_val != "":
            conditions.append(f"title='{title_val}'")
        if author_val != "":
            conditions.append(f"author='{author_val}'")
        if genre_val != "":
            conditions.append(f"genre='{genre_val}'")
        if conditions:
            query += " " + " AND ".join(conditions)
        else:
            query = "" 
        print("Query:", query)
        if query != "":
            self.table.config(columns=("id","title","author","genre","available_copies","total_copies"))
            self.table.heading("id", text="Id")
            self.table.heading("title", text="Title")
            self.table.heading("author", text="Author")
            self.table.heading("genre", text="Genre")
            self.table.heading("available_copies", text="Available\nCopies")
            self.table.heading("total_copies", text="Total\nCopies")
            self.table["show"] = "headings"
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                if rows:
                    self.table.delete(*self.table.get_children())
                    for row in rows:
                        self.table.insert('',tk.END,values=row)
                frame.destroy()
            except Exception as e:
                print(e)
    
    def show_all(self,choice,frame):
        content = tuple()
        use_table  = ""
        if choice==0:
            content = ('id','name','email','books_borrowed')
            self.table.config(columns=content)
            use_table = "user_table"
        elif choice==1:    
            content =('id','title','author','genre','available_copies','total_copies')
            self.table.config(columns=content)
            use_table = "books_table"
        elif choice==2:
            content = ('id','user_id','book_id','borrow_date','due_date','status')
            self.table.config(columns=content)
            use_table = "borrow_return_table"
        for con in content:
            self.table.heading(con,text=con)
        self.table["show"] = "headings"
        try:
            query = "SELECT * FROM "+use_table
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            if rows:
                self.table.delete(*self.table.get_children())
                for row in rows:
                    self.table.insert('',tk.END,values=row)
        except Exception as e:
            print(e)

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