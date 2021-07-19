#!/usr/bin/env python
# coding: utf-8

import os, shelve, sqlite3, smtplib
from datetime import timedelta, date, datetime
from os import listdir, getcwd
from tkinter import *
import socket
from tkinter import messagebox
from tkinter import ttk

def mainTable(tableName):
    conn = sqlite3.connect(tableName)
    c = conn.cursor()
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE log (timeStamp text,
                    subject text,
                    topics text,
                    time integer
                   )
                """)

        c.execute("""CREATE TABLE sub_log (
                sub_short text,
                subject text
               )
            """)

        c.execute("""CREATE TABLE delete_logs (
                subject text,
                topics text,
                time integer
               )
            """)

    except Exception as found:
        print(str(found).capitalize())

    conn.commit()
    conn.close()


def database():
    selectWindow = Toplevel(root)
    selectWindow.title('Adding a new table')
    selectWindow.geometry('700x200')
    Label(selectWindow, text='').grid(row=0, column=0)
    Label(selectWindow, text='  New table name: ', font=('Comic Sans MS', 14)).grid(row=1, column=0)
    En = Entry(selectWindow)
    En.grid(row=1, column=1)
    lb1 = Label(selectWindow)

    radio = IntVar()

    def shelOpen():
        shelfFile = shelve.open('file_location')
        vrs = os.getcwd() + '\\' + En.get() + '.db'
        shelfFile['loc'] = vrs
        fName = list(shelfFile.values())[0].split('\\')[-1].replace('.db', '')
        shelfFile.close()
        return fName

    def check():
        if radio.get() and En.get() != '' and 1 <= len(En.get()) < 16 :
            shelOpen()
            stateOfBtN()

    def ok():
        z = [temp for temp in os.listdir() if temp.endswith('.db')]

        if len(En.get()) > 16:
            lb1.config(text='Length of the Table should be less than 16',fg='#EC4D37', font=('Comic Sans MS', 14), bg='white')
            En.delete('0', 'end')

        elif En.get() + '.db' in z:
            lb1.config(text='Guess you need some memory pills 💊💊 ', fg='yellow', font=('Comic Sans MS', 14), bg='white')
            En.delete('0', 'end')

        elif En.get() != '' and En.get() is not None and len(En.get()) < 16:
            tableName = En.get() + '.db'

            mainTable(tableName)

            fName = shelOpen()
            mainlb1.config(text=f'Study Log  ~  Table Name - {fName}', font=('Times New Roman', 15, 'bold'), bg=main_clr,fg='white')
            mainlb1.grid(row=0, column=0, sticky=W)

            lb1.config(text=' ✔ Your New Table has been Added successfully', fg='green', font=('Comic Sans MS', 14), bg='white')
            selectWindow.after(3000, lambda: selectWindow.destroy())
        else:
            lb1.config(text=' ❌ Give the table a name', font=('Comic Sans MS', 14), bg='white', fg='red')

        lb1.grid(row=3, column=1, pady=10)


    bt = Button(selectWindow, text=' Ok ', command=ok, font=('Comic Sans MS', 9))
    bt.grid(row=1, column=2, padx=10)
    
    def delOn():
        if En.get() == '':
            selectWindow.after(8000, selectWindow.destroy)
        else:
            selectWindow.after(1000*20, selectWindow.destroy)
    selectWindow.after(10000, delOn)

    c1 = Checkbutton(selectWindow, text='Set it as table name',variable=radio, onvalue=1, offvalue=0, command=check, font=14)
    c1.grid(row=2,column=1, padx=10,ipady=10)


def tData():
    try:
        oShelve = shelve.open('file_location')
        data = list(oShelve.values())[0]
        oShelve.close()

        for i in os.listdir():
            if i == data.split('\\')[-1]:
                return data

    except:
        mainlb1.config(text=f'Study Log  ~  Table Name ', font=('Times New Roman', 15, 'bold'), bg=main_clr,fg='white')
        mainlb1.grid(row=0, column=0, sticky=W)
        stateOfBtD()

        shell = shelve.open('file_location')
        shell['loc'] = ''
        data = list(shell.values())[0]
        shell.close()

        return data

def slt_table():
    selectWindow = Toplevel(root)
    selectWindow.title('Select Window')
    selectWindow.geometry('400x300')

    a = os.listdir()
    out = []
    for temp in a:
        if temp.endswith('.db') and temp.count('.') == 1:
            out.append(temp.replace('.db', ''))

    if len(out) > 0:
        selectWindow.geometry('400x300')
        Label(selectWindow, text='Select any one of the table.', font=15).grid(row=0, column=0)
        radio = IntVar()

        def selection():
            shelfFile = shelve.open('file_location')
            vrs = os.getcwd() + '\\' + out[radio.get() - 1] + '.db'
            shelfFile['loc'] = vrs
            shelfFile['loc'] = vrs
            fName = list(shelfFile.values())[0].split('\\')[-1].replace('.db', '')
            mainlb1.config(text=f'Study Log  ~  Table Name - {fName}', font=('Times New Roman', 15, 'bold'), bg=main_clr,fg='white')
            mainlb1.grid(row=0, column=0, sticky=W)
            shelfFile.close()

            stateOfBtN()

        canvas = Canvas(selectWindow)
        scroll = Scrollbar(selectWindow, orient='vertical', command=canvas.yview)
        r, z = 3, 1
        
        tTopic = tData()
        tTopic = tTopic.split('\\')[-1].replace('.db','')

        for temp in range(len(out)):
            
            if out[temp] == tTopic.replace('.db',''):
                label = Radiobutton(canvas, text=out[temp].replace('.db', ''), value=z, variable=radio, command=selection,
                                    font=12)
                label.select()

            else:
                label = Radiobutton(canvas, text=out[temp].replace('.db', ''), value=z, variable=radio, command=selection,
                                    font=12)

            canvas.create_window(0, temp * 50, anchor='nw', window=label, height=50)
            r, z = r + 1, z + 1
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll.set)

        canvas.grid(row=1, column=0)
        if z > 6:
            scroll.grid(row=1, column=1, sticky=N + S + W)
        secs = 1 * 20
        selectWindow.after(1000 * secs, lambda: selectWindow.destroy())

    else:
        selectWindow.geometry('500x200')
        mainlb1.config(text=f'Study Log  ~  Table Name ', font=('Times New Roman', 15, 'bold'), bg=main_clr,fg='white')
        mainlb1.grid(row=0, column=0, sticky=W)
        Label(selectWindow, text='No table was found in the current Directory', font=('Comic Sans MS', 15, 'bold'), fg='red').grid(row=0, column=0,sticky=NW)
        Label(selectWindow, text='Redirecting you to the New Table Window......',font=('Comic Sans MS', 15, 'bold')).grid(row=1, column=0, sticky=NW)
        selectWindow.after(3000, lambda: selectWindow.destroy())

        selectWindow.after(2950, database)

def Help():
    helpWindow = Toplevel(root)
    helpWindow.title(' Help ')
    helpWindow.geometry('500x300')
    Label(helpWindow, text='Work in Progress..........', justify='center', font = ('Comic Sans MS',20,'bold')).grid(row=0,column=0)
    helpWindow.after(10000, helpWindow.destroy)
    pass

def connect():
    IPaddress = socket.gethostbyname(socket.gethostname())
    return IPaddress != "127.0.0.1"

def send_feedback(name, email_id, comment):
    smtp_object = smtplib.SMTP('smtp.gmail.com',587)
    smtp_object.ehlo()
    smtp_object.starttls()

    email = 'youremail@test.com'
    passoword = 'yourpassowordhere'
    smtp_object.login(email,passoword)
    from_address = email
    subject = 'Customer FeedBack'
    name = name.replace(' ','_')
    comment = comment.replace(' ','_')
    message = 'Name:_' + name + '<<::>>Email_Address:_' + email_id + '<<::>>Comment:_'+ comment

    Body=f"""Subject:{subject}

    {message}
    """
    smtp_object.sendmail(from_address,from_address,Body)
    smtp_object.quit()

def feedback():

    fback_window = Toplevel(root)
    fback_window.title(" FeedBack Window ")
    fback_window.geometry('550x400')

    Label(fback_window, text = ' FeedBack Form ', justify='center', font = ('Comic Sans MS',20,'bold')).grid(row=0,column=1)
    Label(fback_window, text = ' Name ', font=('Comic Sans MS', 14)).grid(row=1, column=0, padx = 10, pady=10)
    Label(fback_window, text = ' Email Address ', font=('Comic Sans MS', 14)).grid(row=2, column=0, padx =10, pady=10)
    Label(fback_window, text = ' Comment ', font=('Comic Sans MS', 14)).grid(row=3, column=0, padx=10, pady=10)

    name = StringVar(); email_id = StringVar()
    n = Entry(fback_window, textvariable = name, width=30)
    e = Entry(fback_window, textvariable = email_id, width=30)

    n.grid(row=1,column=1,pady=10, ipady=5)
    e.grid(row=2, column=1, pady = 10, ipady=5)

    c = Text(fback_window, height = 10, width=40)
    c.grid(row=3, column= 1, pady=15, padx=5, columnspan = 2)

    n.insert(0, 'Your Name')
    e.insert(0, 'user_@domain.com')
    c.insert('1.0',' // Your comment.')

    def submit():
        comment = c.get("1.0", END)
 
        if connect():
            send_feedback(name.get(), email_id.get(), comment)
            messagebox.showinfo('Feedback Window', 'Your feedback has been submitted.')
            fback_window.after(1000, fback_window.destroy)
        else:
            messagebox.showerror("Connection Error", " Check your Internet Connection. ")

    b1 = Button(fback_window, text = ' Submit ', command = submit)
    b1.grid(row=4, column=1)
    fback_window.after(1000  * 60 * 4, fback_window.destroy)

    
def stateOfBtN():
    newSub.config(state=NORMAL)
    inpData.config(state=NORMAL)
    viewData.config(state=NORMAL)
    checAct.config(state=NORMAL)
    delAct.config(state=NORMAL)
    disSub.config(state=NORMAL)

def stateOfBtD():
    newSub.config(state=DISABLED)
    inpData.config(state=DISABLED)
    viewData.config(state=DISABLED)
    checAct.config(state=DISABLED)
    delAct.config(state=DISABLED)
    disSub.config(state=DISABLED)


def subjects():
    tableName = tData()
    if tableName == None or tableName == '':
        mainlb1.config(text='You Need to select a table.', font=14, bg='#CCF381', fg='red')  
        mainlb1.grid(row=0, column=0, sticky=W)
        stateOfBtD()
        main_close()
        resFrame()

    n_s = {}
    conn = sqlite3.connect(tableName)
    c = conn.cursor()

    c.execute("SELECT rowid,* FROM sub_log")
    items = c.fetchall()

    for item in items:
        n_s[item[1]] = item[2]

    conn.commit()
    conn.close()

    return n_s


def displaySubject():
    main_close()
    result_frame.grid_forget()
    tableName = tData()
    n_s = subjects()

    if len(n_s) > 0:
        disSubList.delete('0', 'end')
        disSubList.config(width=50, font=12)
        disSubList.insert(END, '  These are the subject')

        for k, v in n_s.items():
            disSubList.insert(END, f'     {k} : {v}')

        disSubList.grid(row=0, column=1, ipady=len(n_s) + 50)

    else:
        tp2.config(text='   !! No Subject were found !!     ', font=('Bahnschrift', 14, 'bold'), fg='red', bg='white')
        tp2.grid(row=0, column=0)

    def disSubClose():
        main_close()
        resFrame()

    disSubBtn.config(text=' X ', command=disSubClose, bg='red')
    disSubBtn.grid(row=0, column=2, sticky=N, ipadx=15,pady=5)


def newSubject():
    n_s = subjects()
    tableName = tData()
    main_close()
    result_frame.grid_forget()

    tp2.config(text='\tAdd New Subject', font=('Bahnschrift SemiLight',15,'bold'), bg='white', fg='black')
    tp2.grid(row=0,column=0)
    nslb1.config(text='Enter the new Subject Name', font=12, bg='white')
    nslb2.config(text='Enter the Subject Shortcut Key', font=12, bg='white')

    nslb1.grid(row=1, column=0, sticky=NW, pady=10)
    nslb2.grid(row=2, column=0,sticky=NW,pady=5)

    subName.config(textvariable=StringVar(), width=30, borderwidth=2)
    shortSub.config(textvariable=StringVar(), width=30, borderwidth=2)

    subName.grid(row=1, column=1, pady=10, padx=50, sticky=NE)
    shortSub.grid(row=2, column=1, pady=10, padx=50, sticky=NE)

    def delss():
        subName.delete(0,END), shortSub.delete(0,END), lab1.grid_forget()
        lab2.grid_forget(), nslb3.grid_forget(), nsbtn2.config(state=NORMAL)

    def det():
        a,b = False,False

        if len(subName.get()) <= 12:
            
            if subName.get() not in n_s.values() and subName.get() != '':
                lab1.config(text=' ✔ ', fg='green', bg='white', font=12)
                a = True
            else:
                if subName.get() == '':
                    lab1.config(text='Subject Name cannot be empty.', fg='red', bg='white')
                else:
                    lab1.config(text=f'!! {subName.get()} is already used. ', fg='red', bg='white')

            if shortSub.get() not in n_s.keys() and shortSub.get() != '':
                lab2.config(text=' ✔ ', bg='white', fg='green', font=12)
                b = True
            else:
                if shortSub.get() == '':
                    lab2.config(text='Shortcut Key cannot be empty.',fg='red', bg='white')
                else:
                    lab2.config(text=f'*You have already used this key for {n_s[shortSub.get()]} subject  ', fg='red', bg='white')

            if a and b:
                conn = sqlite3.connect(tableName)
                c = conn.cursor()
                c.execute("INSERT INTO sub_log VALUES (?,?)", (shortSub.get(), subName.get()))
                conn.commit()
                conn.close()

                nslb3.config(text='\t\tYou Data has been Recorded successfully...        ', font=('Yu Mincho', 14, 'bold'), bg='white', fg='black')
                nslb3.grid(row=4, column=0, pady=10, columnspan=3)
                nsbtn2.config(state=DISABLED)
                b1.after(2000, delss)

        else:
            lab1.config(text=' Subject Name cannot be greater than 12', fg='red', bg='white',font=14)

        lab1.grid(row=1, column=2, pady=10)
        lab2.grid(row=2, column=2, pady=10)

    nsbtn2.config(text=' Submit ', command=det)
    nsbtn2.grid(row=3, column=0, pady=10, sticky=E)

    def newSubClose():
        main_close()
        resFrame()

    nsbtn.config(text=' Close ', command=newSubClose)
    nsbtn.grid(row=3, column=1, pady=10)


def add_one():
    tableName = tData()
    main_close()
    result_frame.grid_forget()
    n_s = subjects()

    if len(n_s) > 0:
        
        addDList.delete('0', 'end')
        addDList.config(width=60, font=12,selectmode=MULTIPLE, bd=2, height=8)
        
        lab1.config(text=' Inserting Data ', font=('Lucida Console', 20, 'bold'), justify='center',bg='white',fg='black')
        lab1.grid(row=0, column=0)

        aolbl1.config(text=' These are the subjects: ', font=('SimSon',18,'bold'), bg='white', fg='black')
        aolbl1.grid(row=1, column=0, sticky=W)

        sb.config(orient=VERTICAL)
        addDList.config(yscrollcommand=sb.set, font=('Arial', 15,))
        
        if len(n_s) > 9:
            sb.grid(row=2, column=1, sticky=N + S + W)
            sb.config(command=addDList.yview)

        for k, v in n_s.items():
            addDList.insert(END, f'   {k} : {v}, ')

        addDList.grid(row=2, column=0,ipady=20)

        aolb2.config(text='  Subject  ', font=14, bg='white', fg='black')
        aolb3.config(text='  Topic  ', font=14, bg='white', fg='black')
        aolb4.config(text='  For how many minutes  ', font=14, bg='white', fg='black')

        aolb2.grid(row=3, column=0, sticky=NW, pady=15)
        aolb3.grid(row=4, column=0, sticky=NW, pady=10)
        aolb4.grid(row=5, column=0, sticky=NW, pady=10)

        def delstt():
            sub.delete(0,END), topic.delete(0,END), time.delete(0,END), tp2.grid_forget()
            tp3.grid_forget(), aolb5.grid_forget(), b1.config(state=NORMAL)

        def det():
            da = False
            db = False

            if sub.get() not in n_s.keys():
                tp2.config(text='* This Subject not found. You need to add it ', fg='red', font=2,bg='white')
            else:
                tp2.config(text='  ✔  ', bg='white', fg='green', font=20)
                da = True

            if time.get().isdigit() and time.get() != '':
                db = True
                tp3.config(text='  ✔  ', bg='white', fg='green', font=20)
            else:
                tp3.config(text=' * The time should be in integer format.', fg='red', font=1, bg='white')

            if da and db:
                timeStamp = datetime.now().strftime('%d-%m-%y: %H:%M:%S')
                conn = sqlite3.connect(tableName)
                c = conn.cursor()
                c.execute("INSERT INTO log VALUES (?,?,?,?)", (timeStamp, n_s[sub.get()], topic.get(), time.get(),))
                conn.commit()

                conn.close()

                aolb5.config(text='✔ Your data has been added succesfully.', font=14, bg='white',fg='black')
                aolb5.grid(row=7, column=0, padx=30, pady=10)
                b1.config(state=DISABLED)
                b1.after(2000, delstt)
            tp2.grid(row=3, column=1)
            tp3.grid(row=5, column=1)

        sub.config(textvariable=StringVar(), width=20)
        topic.config(textvariable=StringVar(), width=40)
        time.config(textvariable=StringVar(), width=10)

        sub.grid(row=3, column=0, pady=5, padx=20)
        topic.grid(row=4, column=0, pady=5, padx=20)
        time.grid(row=5, column=0, pady=5, padx=30)

        b1.config(text='Submit', command=det)
        b1.grid(row=6, column=0, padx=30)

    else:
        tp2.config(text='No Subjects were found !!!', font=('Bahnschrift', 15, 'bold'), bg='white', fg='red')
        tp2.grid(row=0, column=0)

    def addSubClose():
        main_close()
        resFrame()

    aobtn1.config(text=' X ', command=addSubClose,bg='red')
    aobtn1.grid(row=0, column=1, padx=30,ipady=5,ipadx=10,pady=10)



def show_data():
    subjects()
    tableName = tData()
    main_close()

    result_frame.grid_forget()

    connection = sqlite3.connect(tableName)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM log")
    items = cursor.fetchall()

    if len(items) > 0:
        listBox.delete(*listBox.get_children())
        sb.config(orient=VERTICAL)

        style = ttk.Style()

        # Data
        style.configure("mystyle.Treeview",
                font=('Calibri', 15),
                fieldbackground='white'
                )

        style.theme_use("default")
        style.map('Treeview',background=[('selected','black')])
        style.map('Treeview.Heading', font=[(None, 16)])
        
        lab1.config(text="Table Data", font=("Arial",20), bg='white')
        lab1.grid(row=0, columnspan=3)
    
        listBox.config(show='headings',style="mystyle.Treeview", height=30)
        listBox["column"] = ('TimeStamp', 'Subject', 'Time', 'Topic')

        listBox.column("TimeStamp", width=185)
        listBox.column("Subject", width=150)
        listBox.column("Time", width=80)
        listBox.column("Topic", width=420)
        listBox['show'] = 'headings'
        listBox.column("#3", stretch=True)
        listBox.grid(row=1, column=2)

        cols = ('TimeStamp', 'Subject', 'Time', 'Topic')
        for col in cols:
            listBox.heading(col,text=col)

        # Adding Strips
        listBox.tag_configure('odd', background='white', font=('Calibri', 14))
        listBox.tag_configure('even', background='light green',font=('Calibri', 14))
        count = 0

        for tstamp, subject, topic, time in items:
            if count % 2 == 0:
                listBox.insert("","end",values=(tstamp.center(25), subject.center(15), str(time).center(16), (topic).ljust(10)), tags=('even',))
            else:
                listBox.insert("","end",values=(tstamp.center(25), subject.center(15), str(time).center(16), (topic).ljust(10)), tags=('odd',))
            count += 1

        listBox.config(yscrollcommand=sb.set)
        sb.config(command=listBox.yview)

        if count >= 30:
            sb.grid(row=1,column=3, sticky=N+W+S, padx=15, pady = 10)
    else:
        aslb1.config(text='!!! No Data was found. !!! ', font=('SimSun', 15), bg='white', fg='red')
        aslb1.grid(row=0, column=0)

    def showDClose():
        main_close()
        resFrame()

    vdbtn.config(text=' X ', command=showDClose, bg='red')
    vdbtn.grid(row=0, column=3)


def date_range(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

def oReturn():
    o = []
    start_dt = date(2021, 1, 1)
    end_dt = date(2030, 12, 31)

    for dt in date_range(start_dt, end_dt):
        o.append(dt.strftime("%d-%m-%y"))
    return o

def activitySearch():
    tableName = tData()
    main_close()
    result_frame.grid_forget()
    n_s = subjects()

    conn = sqlite3.connect(tableName)
    c = conn.cursor()

    c.execute("SELECT * FROM log")
    items = c.fetchall()
    entered_date.delete(0,END)
    aslb1.config(text='')

    if len(items) > 0:
        aslb1.config(text='\t\tActivity Search', font=('Lucida Console', 20, 'bold'), justify='center',bg='white', fg='black')
        aslb2.config(text='', bg='white')
        aslb3.config(text=' Enter the Date here (To get Today\'s Activity Enter nothing) ', font=('Bahnschrift Light SemiCondensed', 15), bg='white', fg='black')

        entered_date.config(width=30)

        aslb1.grid(row=0, column=0)
        aslb2.grid(row=1, column=0, columnspan=3)
        aslb3.grid(row=2, column=0, sticky=NW, pady=5)

        entered_date.grid(row=2, column=2, ipady=5, padx=10)
        entered_date.insert(0, '  Enter Date in \'dd-mm\' format. ')

        sb.config(orient=HORIZONTAL, width=20)
        sb2.config(orient=VERTICAL, width=20)

        def search():
            yr = datetime.now().strftime('-%y')

            ed = entered_date.get()

            if entered_date.get() == '':
                ed = datetime.now().strftime('%d-%m-%y')
            elif len(ed) == 5: 
                ed = ed + yr

            out = []
            
            for k, v in n_s.items():
                res = [k]
                for j in items:
                    if (j[0][:8] == ed) and j[1] == v:
                        res.append(j[2])
                out.append(res)
            t = True

            actSList.delete('0', 'end')
            actSList.config(width=50, font=('Bahnschrift Light', 14), xscrollcommand=sb.set, height=15)
            actSList.config(width=50, font=('Bahnschrift Light', 14), yscrollcommand=sb2.set, height=15)

            i = 1
            m = 0
            for temp in out:
                if len(temp) > 1:
                    x = ", ".join(temp[1:])
                    actSList.insert(END, f'  In {n_s[temp[0]]} :')
                    actSList.insert(END, f'    {x}.')
                    actSList.insert(END,"\n")
                    t = False
                    i +=1

                    if m < len(x): m = len(x)

            sb.config(command=actSList.xview)
            sb2.config(command=actSList.yview)

            if t:
                actSList.grid_forget(), sb.grid_forget(), sb2.grid_forget()
                
                if ed in oReturn():
                    lab3.config(text=f'Looks like you have not done anything on {ed}', font=('Bahnschrift Light', 14), fg='black')
                else:
                    if t:
                        lab3.config(text='Enter the date in \'dd-mm-yy\' format', font=('Bahnschrift Light', 14), fg='black')

                lab3.grid(row=5, column=0, sticky=N + W + S)
            
            else:
                lab3.grid_forget()

                if m > 50:
                    sb.grid(row=3, column=0, sticky=W+E)

                if i > 6:
                    sb2.grid(row=5,column=1,stick=N+W+S)

                actSList.grid(row=5, column=0, pady=5)

            conn.close()

        asbtn1.config(text='Search', command=search)
        asbtn1.grid(row=2, column=4, padx=10)

    else:
        aslb1.config(text='You need to Add Data To View Your Activity.', font=('SimSun', 15))
        aslb1.grid(row=0, column=0)

    def actSerClose():
        main_close()
        resFrame()

    asbtn.config(text=' X ', command=actSerClose, bg='red')
    asbtn.grid(row=0, column=5, padx=10,pady=5)

def Updatesub():
    table_name = tData()
    conn = sqlite3.connect(table_name)
    c  = conn.cursor()
    c.execute("SELECT rowid,* FROM sub_log")
    Rid = [i[0] for i in c.fetchall()]
    for i in range(len(Rid)):
        c.execute("UPDATE sub_log SET rowid = (?) WHERE rowid = (?)", (i+1, Rid[i]))
    conn.commit()
    conn.close()

def updateTable():
    table_name = tData()
    conn = sqlite3.connect(table_name)
    c = conn.cursor()
    c.execute("SELECT rowid,* FROM log")
    Rowid  = [i[0] for i in c.fetchall()]
    for i in range(len(Rowid)):
        c.execute("UPDATE log SET rowid=(?) WHERE rowid=(?)",(i+1, Rowid[i]))
    conn.commit()
    conn.close()

def DelSubRow():
    tableName = tData()
    main_close()
    result_frame.grid_forget()
    t = False
    n_s = subjects()

    if len(n_s):
        des.config(textvariable=StringVar(), width=5)
        tp2.config(text = '           Delete Subject/Row Data.', font=('Lucida Console', 20, 'bold'), justify='center',bg='white',fg='black')
        tp2.grid(row=0, column=0)
        delsrlb.config(text='Do you want to delete the Subject(s) or Row(r) : ', font=('Comic Sans MS',14), fg='black', bg='white')
        

        delsrlb.grid(row=1, column=0, sticky=NW, padx=10, pady=10)
        des.grid(row=1, column=1)
        Updatesub()
        updateTable()

        def ok():
            if des.get() == 's':
                conn = sqlite3.connect(tableName)
                c = conn.cursor()
                c.execute("SELECT rowid, * FROM sub_log")
                a = c.fetchall()
                
                c.close()

                sb.config(orient=VERTICAL)
                
                delrlist1.delete('0', 'end')
                delrlist1.config(yscrollcommand=sb.set, width=40, font=12)
                delslb.config(text='Select rowid of the subject you want to remove', font=8, bg='white')

                delslb.grid(row=2, column=0, sticky=NW, pady=10)

                for data in range(len(a)):
                    delrlist1.insert(END, f'  RowId = {a[data][0]} : {a[data][2]}')

                if data > 9:
                    sb.grid(row=3, column=1, sticky=N + S + W)

                delrlist1.grid(row=3, column=0, sticky=NW)
                sb.config(command=delrlist1.yview)

                r = 3

                delrid.config(text='\tRowid?? ', font=('Bahnschrift SemiLight',12), bg='white')
                delrid.grid(row=r + 1, column=0, stick=NW, pady=20)
                Id.grid(row=r + 1, column=0,pady=20)

                def OKK():
                    conn = sqlite3.connect(tableName)
                    c = conn.cursor()
                    c.execute("SELECT sub_short FROM sub_log WHERE rowid = (?)", (Id.get(),))
                    items = c.fetchall()
                    n_s = subjects()
                    dellb3.grid_forget(),dellb.grid_forget(),dellb2.grid_forget()

                    try:
                        tp4.grid_forget()
                        s = n_s[items[0][0]]
                        c.execute("SELECT rowid,topics FROM log WHERE subject = (?)", (s,))
                        a = c.fetchall()
                        conn.close()
                        sub = '\n'.join([i[1] for i in a])
                        rid = [i[0] for i in a]

                        l = False
                        if len([i[1] for i in a]) > 0:
                            dellb.config(text=f' In {s}, these topics will be removed: ', font=('Bahnschrift SemiLight',14), fg='black', bg='white')

                            dellb2.config(text=f'{sub}', font=('Book Antiqua',12))
                            dellb2.grid(row=r + 3, column=0, sticky=W)
                        else:
                            l = True
                            dellb.config(text=f' Do you want to remove Subject {s}', font=('Bahnschrift SemiLight',14), fg='black', bg='white')

                        dellb.grid(row=r + 2, column=0, sticky=NW, pady=10)
                        def yes():
                            conn = sqlite3.connect(tableName)
                            c = conn.cursor()
                            c.execute("DELETE from sub_log WHERE rowid = (?)", (str(Id.get()),))

                            for i in rid:
                                c.execute("DELETE from log WHERE rowid = (?)", (str(i),))
                            conn.commit()

                            if l: dellb3.config(text=f' {s} is removed. ',font=('Simsun',15), bg='white')
                            else: dellb3.config(text=f' {s} is removed along with its topics.', font=('SimSun',15), bg='white')

                            dellb3.grid(row=r + 6, column=0)

                            conn.close()

                        def no():
                            close()

                        dely.config(text='Yes', command=yes)
                        deln.config(text='No', command=no)

                        dely.grid(row=r + 4, column=0, pady=10)
                        deln.grid(row=r + 4, column=0, sticky=NE, pady=10)

                    except Exception as e:
                        print(e)
                        dellb.grid_forget(),dellb2.grid_forget(),dellb3.grid_forget(),dely.grid_forget(),deln.grid_forget()
                        tp4.config(text=f'The Subject is not defined.', font=('Bahnschrift', 14, 'bold'), bg='white')
                        tp4.grid(row=9, column=0)

                delbtn.config(text='OK', command=OKK)
                delbtn.grid(row=r + 1, column=0, sticky=E, pady=20)

            elif des.get() == 'r':
                
                n_s = subjects()
                result_frame.grid_forget()
                result_frame.config(fg='white')

                dellb.config(text=f'Which Subject do you want to remove', font=('Comic Sans MS',14), bg='white', fg='black')
                dellb.grid(row=2, column=0, pady=10, sticky=NW)

                n = 120

                delrlist3.delete('0', 'end')
                delrlist3.config(yscrollcommand=sb.set, width=30, font=5, height=7)

                for k, v in n_s.items():
                    delrlist3.insert(END, f'  {k} : {v}')

                if len(n_s) > 7:
                    sb.grid(row=3, column=2, sticky=N + S + W)

                delrlist3.grid(row=3, column=0, ipady=5, sticky=N + W)
                sb.config(command=delrlist3.yview)

                dellb2.config(text=' Subject: ', font=3)
                dellb2.grid(row=4, column=0, pady=5, sticky=NW, padx=30)
                subj.grid(row=4, column=0, padx=20)

                def ok_row():
                    if subj.get() in n_s.keys():
                        n = 120
                        lab1.grid_forget()
                        delrlist4.delete('0', 'end')
                        delrlist4.config(yscrollcommand=sb2.set, width=50, font=10, height=5)

                        delslb.config(text=f' For {n_s[subj.get()]}', font=8,bg='white')
                        delslb.grid(row=5, column=0, sticky=N + W)
                        sb2.config(command=delrlist4.yview)

                        connection = sqlite3.connect(tableName)
                        c = connection.cursor()
                        c.execute("SELECT rowid,* FROM log WHERE subject = (?)", (n_s[subj.get()],))

                        a = c.fetchall()
                        forward = False

                        if len(a) > 5:
                            sb2.grid(row=6, column=1, sticky=N + S + W)

                        if len(a) > 0:
                            for i in a:
                                delrlist4.insert(END, f' Rowid: {i[0]}, Topic: {i[3]}')
                                forward = True
                        else:
                            Id.grid_forget(), delrid.grid_forget(),delbtn4.grid_forget(), dellb3.grid_forget()
                            dellb4.grid_forget(),dely.grid_forget(),deln.grid_forget(),sb2.grid_forget()

                            delrlist4.insert(END, f'No Topic entry was found for {n_s[subj.get()]}')

                        delrlist4.grid(row=6, column=0, sticky=NW)

                        if forward:
                            items = a
                            delrid.config(text='Rowid?? ', font = ('Bahnschrift SemiLight',12))
                            delrid.grid(row=7, column=0, sticky=N + W, pady=15)
                            Id.grid(row=7, column=0, pady=15)

                            def OOOk():
                                dellb4.config(text='')
                                if Id.get() in [str(i[0]) for i in items]:
                                    c.execute("SELECT rowid, topics, time FROM log WHERE rowid = (?)", (Id.get(),))
                                    item = c.fetchall()[0]
                                    dellb3.config(text=f'Remove {item[1]} ?? ', font=6)
                                    dellb3.grid(row=8, column=0, sticky=NW, pady=15)

                                    def yes():
                                        c.execute("DELETE from log WHERE rowid = (?)", (Id.get(),))
                                        c.execute("INSERT INTO delete_logs VALUES (?,?,?)", (subj.get(), item[1], item[2]))
                                        connection.commit()
                                        connection.close()

                                        dellb4.config(text=f'{item[1]} has been removed.', font=('Bahnschrift', 15, 'bold'),bg='white')
                                        dellb4.grid(row=9, column=0)

                                    dely.config(text='Yes', command=yes)
                                    deln.config(text='No', command=close)

                                    dely.grid(row=8, column=1, pady=15, sticky=W)
                                    deln.grid(row=8, column=2,  pady=15)

                                else:
                                    dellb3.grid_forget(), dely.grid_forget(), deln.grid_forget()
                                    dellb4.config(text=f'Rowid {Id.get()} is not in {n_s[subj.get()]} subject.')
                                    dellb4.grid(row=8, column=0)

                            delbtn4.config(text='Ok', command=OOOk)
                            delbtn4.grid(row=7, column=1, pady=15)
                    else:
                        delrlist4.grid_forget(), delslb.grid_forget(),delrid.grid_forget(),Id.grid_forget(), delbtn4.grid_forget()
                        dellb3.grid_forget(), dely.grid_forget(), deln.grid_forget(), dellb4.grid_forget(), sb2.grid_forget()
                        lab1.config(text = 'Subject Not Found', font=('Bahnschrift', 15, 'bold') )
                        lab1.grid(row=7,column=0,pady=30)

                delrbtn.config(text='Ok', command=ok_row)
                delrbtn.grid(row=4, column=1, sticky=S + W)

        delsub.config(text=' Ok ', command=ok)
        delsub.grid(row=1, column=2, padx=30)

    else:
        tp4.config(text='You have to add subject in order to delete it.', font=('Bahnschrift', 14, 'bold'),fg='red',bg='white')
        tp4.grid(row=0, column=0, sticky=N)
        t = True

    def close():
        main_close()
        resFrame()

    nslb1.config(text='     ',font=15, bg='white')
    nslb1.grid(row=0, column=3)
    delcl.config(text=' X ', command=close, bg='red', fg='white')

    delcl.grid(row=0, column=4, sticky=NW)


def main_close():
    dely.grid_forget(), deln.grid_forget(), dellb3.grid_forget(), dellb.grid_forget(), dellb2.grid_forget(),
    des.grid_forget(), delsrlb.grid_forget(), delbtn.grid_forget(), delsub.grid_forget(), delcl.grid_forget(),
    sb.grid_forget(), delslb.grid_forget(), delrlist1.grid_forget(), Id.grid_forget(), tp4.grid_forget(),
    delrid.grid_forget(), delrbtn.grid_forget(), dellb4.grid_forget(), delrlist3.grid_forget()
    delrlist4.grid_forget(), subj.grid_forget(), sb2.grid_forget(), delbtn4.grid_forget(), showDList.grid_forget()

    aslb1.grid_forget(), aslb2.grid_forget(), aslb3.grid_forget(), entered_date.grid_forget()
    actSList.grid_forget(), lab3.grid_forget(), asbtn.grid_forget(), asbtn1.grid_forget(), sb.grid_forget()

    sb.grid_forget(), vdbtn.grid_forget()

    disSubBtn.grid_forget()

    nslb1.grid_forget(), nslb2.grid_forget(), nslb3.grid_forget(), subName.grid_forget(), shortSub.grid_forget()
    lab1.grid_forget(), lab2.grid_forget(), nsbtn.grid_forget(), nsbtn2.grid_forget()

    aolbl1.grid_forget(), aolb2.grid_forget(), aolb3.grid_forget(), aolb4.grid_forget()
    aolb5.grid_forget(), tp2.grid_forget(), tp3.grid_forget(), sub.grid_forget(), topic.grid_forget()
    time.grid_forget(), b1.grid_forget(), aobtn1.grid_forget(), addDList.grid_forget(), disSubList.grid_forget()

    listBox.grid_forget()

def resFrame():
    result_frame.config(text=f'This is the Result Area.', font=('Times New Roman', 14, 'bold'), borderwidth=2,
                            width=70, height=30, relief=GROOVE, fg='black')

    result_frame.grid(row=1, column=3)


comment = ''

root = Tk()
root.title('Study Log')
w, h = 1200, 800
root.geometry(f'{w}x{h}')

color = '#FBEAEB'
main_clr = '#1D1B1B'
btn_clr = '#F79862' 

menubar = Menu(root, borderwidth=3, bg="#20232A")
menubar.add_command(label=' New Table ', command=database)
menubar.add_command(label=' Select Table ', command=slt_table)
menubar.add_command(label=' Help ', command=Help)
menubar.add_command(label=' FeedBack ', command=feedback)
menubar.add_command(label='Close', command=root.quit)

root.config(menu=menubar, relief=GROOVE, bg=main_clr)

f1 = Frame(root, bg='white', borderwidth=3, width=700, height=600, relief=SUNKEN)
f1.grid(row=2, column=6, rowspan=50, padx=20, columnspan=3)

result_frame = Label(f1, text=f'This is the Result Area.', font=('Times New Roman', 14, 'bold'), borderwidth=2,
                     width=70, height=30, relief=GROOVE, bg='#F9D342')

result_frame.grid(row=2, column=3)

newSub = Button(root, text='Add a New Subject', command=newSubject, bg=btn_clr)
inpData = Button(root, text='Inserting Data', command=add_one, bg=btn_clr)
viewData = Button(root, text='To view the entire Data', command=show_data, bg=btn_clr)
checAct = Button(root, text='Check Activity', command=activitySearch, bg=btn_clr)
delAct = Button(root, text='To Delete Subject or Row From the Data', command=DelSubRow, bg=btn_clr)
disSub = Button(root, text='Display the Subjects', command=displaySubject, bg=btn_clr)

mainlb1 = Label(root)

try:
    tTopic = tData().split("\\")[-1].replace(".db", "")
except:
    tTopic = ''

if tTopic != '':
    mainlb1.config(text=f'  Study Log   ~ Table Name - {tTopic}', font=('Times New Roman', 15, 'bold'), bg=main_clr, fg='#FFFFFF')
else:
    mainlb1.config(text='You Need to select a table.', font=14, bg='#CCF381', fg='red')
    stateOfBtD()

mainlb1.grid(row=0, column=0, sticky=W, columnspan=3)


i = 2
newSub.grid(row=i + 0, column=0, sticky=NW, pady=10,padx=10)  # Done
inpData.grid(row=i + 1, column=0, sticky=NW, pady=5,padx=10)  # Done
viewData.grid(row=i + 2, column=0, sticky=NW, pady=5,padx=10)  # Done
checAct.grid(row=i + 3, column=0, sticky=NW, pady=5,padx=10)  # Done
delAct.grid(row=i + 4, column=0, sticky=NW, pady=5,padx=10)  # Done
disSub.grid(row=i + 5, column=0, sticky=NW, pady=5,padx=10)  # Done



tp2 = Label(f1); tp3 = Label(f1); tp4 = Label(f1); lab1 = Label(f1); lab2 = Label(f1); lab3 = Label(f1)
delsrlb = Label(f1); dellb = Label(f1); dellb2 = Label(f1); delslb = Label(f1); delrid = Label(f1);dellb4 = Label(f1)
dellb3 = Label(f1); aslb1 = Label(f1); aslb2 = Label(f1); aslb3 = Label(f1); nslb1 = Label(f1); nslb2 = Label(f1)
nslb3 = Label(f1); aolbl1 = Label(f1); aolb2 = Label(f1); aolb3 = Label(f1); aolb4 = Label(f1); aolb5 = Label(f1)

delrlist4 = Listbox(f1); delrlist1 = Listbox(f1); delrlist3 = Listbox(f1); myList = Listbox(f1); disSubList = Listbox(f1)
addDList = Listbox(f1); actSList = Listbox(f1); showDList = Listbox(f1)

listBox= ttk.Treeview(f1)

sb = Scrollbar(f1); sb2 = Scrollbar(f1)

Id = Entry(f1); subj = Entry(f1); des = Entry(f1); entered_date = Entry(f1); subName = Entry(f1); shortSub = Entry(f1)
Id = Entry(f1); subj = Entry(f1); des = Entry(f1); entered_date = Entry(f1); subName = Entry(f1); shortSub = Entry(f1)
sub = Entry(f1); topic = Entry(f1); time = Entry(f1)

dely = Button(f1); deln = Button(f1); delrbtn = Button(f1); delbtn = Button(f1); delbtn4 = Button(f1); delsub = Button(f1)
delcl = Button(f1); asbtn = Button(f1); asbtn1 = Button(f1); vdbtn = Button(f1); disSubBtn = Button(f1);nsbtn = Button(f1)
nsbtn2 = Button(f1); b1 = Button(f1); aobtn1 = Button(f1)

root.mainloop()
