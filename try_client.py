import socket
from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import askstring, askinteger
import json

#-----------------------------------------------------------------------------------------------------#

#create the login window
def top_login():
    global text1, text2, login

    login = Tk()  #the main window
    login.title("Li's library 0.1       Login")
    login.geometry('400x200+600+300')

    Label(login,text = '  User name:',width=15 ,anchor=W).place(x=1,y=10)  #create entry to ask for username and password
    text1 = StringVar()
    text1.set('')
    Entry(login,textvariable = text1,width=30).place(x=120,y=10)
    Label(login,text = '   Password:',width=15,anchor=W).place(x=1,y=50)
    text2 = StringVar()
    text2.set('')
    Entry(login,textvariable = text2,width=30,show='*').place(x=120,y=50)

    Button(login,text ='Sign in',width=15,command=sign_in).place(x=55,y=100)  #create buttons to call functions
    Button(login,text ='Exit',width=15,command=exit).place(x=135,y=150)
    Button(login,text ='Register',width=15,command=top_register).place(x=215,y=100)

    login.mainloop()

#create the register window
def top_register():
    global text3 ,text4,text5, login, ca
    login.destroy()  #close the login window

    ca = Tk()   #the main window
    ca.title("Li's library 0.1  Register")
    ca.geometry('400x200+700+250')

    Label(ca,text = '   name:',width=20,anchor=W).place(x=1,y=10)  #create entry to ask for username and password
    text3 = StringVar()
    text3.set('')
    Entry(ca,textvariable = text3,width=25).place(x=155,y=10)
    Label(ca,text = '   Password:',width=20,anchor=W).place(x=1,y=50)
    text4 = StringVar()
    text4.set('')
    Entry(ca,textvariable = text4,width=25,show='*').place(x=155,y=50)
    Label(ca,text = '   Password again:',width=20,anchor=W).place(x=1,y=90)
    text5 = StringVar()
    text5.set('')
    Entry(ca,textvariable = text5,width=25,show='*').place(x=155,y=90)

    Button(ca,text ='Enter',width=15,command=enter).place(x=55,y=150)  #create buttons to call functions
    Button(ca,text ='Exit',width=15,command=return_login_r).place(x=215,y=150)

    ca.mainloop()

#create the administrator window for librarian to add/check books or print designated records from the database
def top_administrator():
    global login, admin, showbox, current_name
    login.destroy()  #close the login window

    admin = Tk()   #the main window
    admin.title("Li's library 0.1  Administrator_system              Welcome  %s  !"%current_name)
    admin.geometry('1800x900')
    admin.configure(bg='#d3d4cc')

    menubar = Menu(admin)  #create the menu bar, submenu and commands which can call functions
    admin.config(menu = menubar)
    menu1 = Menu(menubar)
    menubar.add_cascade(label = 'add', menu = menu1)
    menu1.add_command(label = 'add item', command = add_item)
    menu1.add_command(label = 'add book', command = add_book)
    menu2 = Menu(menubar)
    menubar.add_cascade(label = 'search', menu = menu2)
    menu2.add_command(label = 'find book - title', command = fb_title)
    menu2.add_command(label = 'find book - author', command = fb_author)
    menu2.add_separator()
    menu2.add_command(label = 'print record', command=record)
    menu3 = Menu(menubar)
    menubar.add_cascade(label = 'exit', menu = menu3)
    menu3.add_command(label = 'exit', command = return_login_a)

    lf1 = LabelFrame(admin,text='add',bg = '#d8caaf')  #create buttons to call functions
    lf1.grid(padx=(30, 30), pady=(30, 0))
    Button(lf1, text='add item', command = add_item,width=50,height=2,bg='#96a48b').grid(padx=80, pady=(30, 0))
    Button(lf1, text='add book', command = add_book,width=50,height=2,bg='#96a48b').grid(padx=80, pady=(40, 50))
    lf2 = LabelFrame(admin,text='find book',bg = '#d8caaf')
    lf2.grid(padx=(30, 30), pady=(40, 0))
    Button(lf2, text='title', command = fb_title,width=50,height=2,bg='#96a48b').grid(padx=80, pady=(30, 0))
    Button(lf2, text='author', command = fb_author,width=50,height=2,bg='#96a48b').grid(padx=80, pady=(40, 50))
    lf3 = LabelFrame(admin,text="book's record",bg = '#d8caaf')
    lf3.grid(padx=(30, 30), pady=(40, 0))
    Button(lf3, text="print record", command=record,width=50,height=2,bg='#96a48b').grid(padx=80, pady=(40, 50))

    lf4 = LabelFrame(admin,text='show box',bg = 'lightyellow')  #create a text box to show information and records
    lf4.grid(row =0,column=1,rowspan=3,padx=(0, 30), pady=(15, 10))
    scrollbar = Scrollbar(lf4)  #create a scroll bar and bind it with the text box
    scrollbar.pack(side=RIGHT,fill='y')
    showbox = Text(lf4,width=112,height=40,bg='ivory')
    showbox.pack(side=RIGHT,fill='y')
    scrollbar.config(command=showbox.yview)
    showbox.config(yscrollcommand=scrollbar.set)

    Label(admin,text ="   Programmering i Python//Nackademin//2018HT//Mengran Li  ", anchor = W, bd = 1,bg='#d3d4cc',
                         relief=SUNKEN).grid(sticky=S+W+E,columnspan=3)  #create a status bar

    admin.mainloop()

#create the user window for customers to borrow/return books and check loans etc.
def top_user():
    global login, user, showbox, current_name
    login.destroy()  #close the login window

    user = Tk()   #the main window
    user.title("Li's library 0.1  user_system              Welcome  %s  !"%current_name)
    user.geometry('1800x900')
    user.configure(bg='steel blue')

    menubar = Menu(user)  #create the menu bar, submenu and commands which can call functions
    user.config(menu = menubar)
    menu1 = Menu(menubar)
    menubar.add_cascade(label = 'search', menu = menu1)
    menu1.add_command(label = 'find book - title', command = fb_title)
    menu1.add_command(label = 'find book - author', command = fb_author)
    menu2 = Menu(menubar)
    menubar.add_cascade(label = 'operate', menu = menu2)
    menu2.add_command(label = 'borrow book', command = borrow_book)
    menu2.add_command(label = 'return book', command = return_book)
    menu3 = Menu(menubar)
    menubar.add_cascade(label = 'my page', menu = menu3)
    menu3.add_command(label = 'my loans', command = check_loans)
    menu4 = Menu(menubar)
    menubar.add_cascade(label = 'exit', menu = menu4)
    menu4.add_command(label = 'exit', command = return_login_u)

    lf1 = LabelFrame(user,text='borrow/return',bg = 'light steel blue')  #create buttons to call functions
    lf1.grid(padx=(30, 30), pady=(30, 0))
    Button(lf1, text='borrow book', command = borrow_book,width=50,height=2,bg='steel blue').grid(padx=80, pady=(30, 0))
    Button(lf1, text='return book', command = return_book,width=50,height=2,bg='steel blue').grid(padx=80, pady=(40, 50))
    lf2 = LabelFrame(user,text='find book',bg = 'light steel blue')
    lf2.grid(padx=(30, 30), pady=(40, 0))
    Button(lf2, text='title', command = fb_title,width=50,height=2,bg='steel blue').grid(padx=80, pady=(30, 0))
    Button(lf2, text='author', command = fb_author,width=50,height=2,bg='steel blue').grid(padx=80, pady=(40, 50))
    lf3 = LabelFrame(user,text="check my loans",bg = 'light steel blue')
    lf3.grid(padx=(30, 30), pady=(40, 0))
    Button(lf3, text="print my loans", command=check_loans,width=50,height=2,bg='steel blue').grid(padx=80, pady=(40, 50))

    lf4 = LabelFrame(user,text='show box',bg = 'light steel blue')  #create a text box to show information and records
    lf4.grid(row =0,column=1,rowspan=3,padx=(0, 30), pady=(15, 10))
    scrollbar = Scrollbar(lf4)  #create a scroll bar and bind it with the text box
    scrollbar.pack(side=RIGHT,fill='y')
    showbox = Text(lf4,width=112,height=40,bg='light steel blue')
    showbox.pack(side=RIGHT,fill='y')
    scrollbar.config(command=showbox.yview)
    showbox.config(yscrollcommand=scrollbar.set)

    Label(user,text ="   Programmering i Python//Nackademin//2018HT//Mengran Li  ", anchor = W, bd = 1,bg='steel blue',
                            relief=SUNKEN).grid(sticky=S+W+E,columnspan=3)  #create a status bar

    user.mainloop()

#-----------------------------------------------------------------------------------------------------#

#definit a function to check account and password, then lead users to different windows according to their right
def sign_in():
    global text1 ,text2 ,current_name ,cs
    name = text1.get()
    password = text2.get()
    current_name = name
    try:  #connect to the server
        host,port = socket.gethostname(),9999
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cs:
            cs.connect((host, port))
            msg = 'sign in/%s/%s'%(name,password)  #send message to sever to select command and exchange data
            cs.send(msg.encode('utf-8'))
            msgs = cs.recv(1024).decode('utf8')  #receive message from server
            if msgs == 'matched':
                showinfo('message','Welcome, %s !'%(name))
                msg = 'sign in_pm/%s'%(name)
                cs.send(msg.encode('utf-8'))
                msgs1 = cs.recv(1024).decode('utf8')
                if msgs1 == 'administrator':  #select to enter administrator or user window according to username
                   top_administrator()
                elif msgs1 == 'user':
                   top_user()
            elif msgs == 'fail':
                showerror('error','please enter the right password!')
            elif msgs == 'user is not exist!':
                showerror('error',msgs)
    except ConnectionRefusedError:
        showerror('error','No connection from the server!')

#definit a function to create new account, bur only for users, and add items to the database in server
def enter():
    global text3,text4, text5, ca
    name,password,password1 = text3.get(),text4.get(),text5.get()
    if len(name) == 0 or len(password) == 0 or len(password1) == 0:  #check and confirm the new password
        showerror('error','Fill in completely!')
    elif password != password1:
        showerror('error','please make sure to enter the same password!')
    else:
        try:  #connect with server
            host,port = socket.gethostname(),9999
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cs:
                cs.connect((host, port))
                msg = 'enter/%s/%s'%(name,password)
                cs.send(msg.encode('utf-8'))
                msgs = cs.recv(1024).decode('utf8')
                if msgs == 'create the account successfully!':
                    showinfo('message',msgs)
                    return_login_r()
                else:
                    showerror('error','Username %s is already exist!'%(msgs))
        except ConnectionRefusedError:
            showerror('error','No connection from the server!')

#definit a function to add items
def add_item():
    title = askstring("add item", "please enter the title:")  #ask for information of the item through tkinter.simpledialog module
    author = askstring("add item", "please enter the author:")
    topic = askstring("add item", "please enter the topic:")
    language = askstring("add item", "please enter the language:")
    location = askstring("add item", "please enter the location:")
    msg = 'add_item/%s/%s/%s/%s/%s'%(title,author,topic,language,location)  #send information to sever to write into the database
    cs.send(msg.encode('utf-8'))
    msgs = cs.recv(1024).decode('utf8')
    if msgs =='this item is already exist!':
        showerror('error',msgs)
    elif msgs == 'add item successfully!':
        showinfo('message',msgs)

#create a function to add books
def add_book():
    global showbox, current_name ,cs
    title = askstring("add book", "which book do you want to add?")
    msg = 'add_book/%s'%(title)
    cs.send(msg.encode('utf-8'))
    msgs = cs.recv(2048).decode('utf8')
    if msgs == 'item is not exist, please add the item first!':
        showerror('error',msgs)
    else:
        item_list = json.loads(msgs)  #convert string to list (book list)
        for x in item_list:  #write the book list into text box to show it
            showbox.insert(END,'''bookId: {}, title: {}, author: {}, topic: {}, language: {}, location: {},
                                  total_number: {}, inside_number: {}\n'''.format(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]))
        bookId = askstring("add book", "please enter the bookId:")
        number = askstring("add book", "how many books do you want to add?")
        msg = 'add_book_num/%s/%s/%s/%s'%(bookId,title,number,current_name)
        cs.send(msg.encode('utf-8'))
        showinfo('message','add books successfully!')
        showbox.delete(0.0,END)

#creat a function to search books, according to title
def fb_title():
    global showbox
    title = askstring("find book", "which book do you want to find?")
    msg = 'fb_title/%s'%(title)
    cs.send(msg.encode('utf-8'))
    msgs = cs.recv(2048).decode('utf8')
    if msgs == 'book is not exist!':
        showerror('error',msgs)
    else:
        showbox.insert(END,msgs)
        showinfo('message','find books successfully!')
        showbox.delete(0.0,END)

#creat a function to search books, according to author
def fb_author():
    global showbox
    author = askstring("find book", "which author do you want to find?")
    msg = 'fb_author/%s'%(author)
    cs.send(msg.encode('utf-8'))
    msgs = cs.recv(2048).decode('utf8')
    if msgs == "this author's book is not exist!":
        showerror('error',msgs)
    else:
        showbox.insert(END,msgs)
        showinfo('message','find books successfully!')
        showbox.delete(0.0,END)

#definit a function to print records of book's change
def record():
    global showbox
    title = askstring("print record", "which book's record do you want to print?")
    msg = 'fb_title/%s'%(title)
    cs.send(msg.encode('utf-8'))
    msgs = cs.recv(2048).decode('utf8')
    if msgs == 'book is not exist!':
        showerror('error',msgs)
    else:
        showbox.insert(END,msgs)
        bookId = askinteger("print record", "please enter the book's id which you want to print!")
        msg = 'record/%d'%(bookId)
        cs.send(msg.encode('utf-8'))
        msgs = cs.recv(2048).decode('utf8')
        if msgs == 'record is not exist!':
            showinfo('message',msgs)
        else:
            showbox.delete(0.0,END)
            showbox.insert(END,msgs)
            showinfo('message','print records successfully!')
        showbox.delete(0.0,END)

#definit a function to borrow books
def borrow_book():
    global showbox, current_name
    title = askstring("borrow book", "which book do you want to borrow?")
    msg = 'fb_title/%s'%(title)
    cs.send(msg.encode('utf-8'))
    msgs = cs.recv(1024).decode('utf8')
    if msgs == 'book is not exist!':
        showerror('error',msgs)
    else:
        showbox.insert(END,msgs)
        bookId = askinteger("borrow book", "please enter the bookId:")
        msg = 'borrow_book/%d/%s/%s'%(bookId,title,current_name)
        cs.send(msg.encode('utf-8'))
        msgs = cs.recv(2048).decode('utf8')
        showinfo('message',msgs)
        showbox.delete(0.0,END)

#definit a function to return books
def return_book():
    global showbox, current_name
    title = askstring("borrow book", "which book do you want to borrow?")
    msg = 'fb_title/%s'%(title)
    cs.send(msg.encode('utf-8'))
    msgs = cs.recv(1024).decode('utf8')
    if msgs == 'book is not exist!':
        showerror('error',msgs)
    else:
        showbox.insert(END,msgs)
        bookId = askinteger("borrow book", "please enter the bookId:")
        msg = 'return_book/%d/%s/%s'%(bookId,title,current_name)
        cs.send(msg.encode('utf-8'))
        msgs = cs.recv(2048).decode('utf8')
        showinfo('message',msgs)
        showbox.delete(0.0,END)

#definit a function to check loans according to username
def check_loans():
    global showbox, current_name
    msg = 'check_loans/%s'%(current_name)
    cs.send(msg.encode('utf-8'))
    msgs = cs.recv(2048).decode('utf8')
    if msgs == "you have not borrowed any book!" or msgs == "you don't have any loan!":
        showinfo('message',msgs)
    else:
        showbox.insert(END,msgs)
        showinfo('message',"please check the list in the show box!")
        showbox.delete(0.0,END)

#definit functions to return login window from other windows
def return_login_r():
    global ca
    ca.destroy()
    top_login()

def return_login_a():
    global admin
    admin.destroy()
    msg = 'over'
    cs.send(msg.encode('utf-8'))
    top_login()

def return_login_u():
    global user
    user.destroy()
    msg = 'over'
    cs.send(msg.encode('utf-8'))
    top_login()

#-----------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    top_login()
