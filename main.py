import json
import smtplib
import sqlite3
from datetime import timedelta, date, datetime
from os import listdir, getcwd, mkdir
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import urllib.request


def openDB(tableName, query, values=(), commit=False):
    conn = sqlite3.connect(tableName)
    c = conn.cursor()

    if values:
        c.execute(query, values)
    else:
        c.execute(query)

    if commit:
        conn.commit()
    else:
        a = c.fetchall()

        return a


def checkFile():
    a = loadSettings()['table_name'].split('/')[-1]
    if a not in listdir('./Database/'):
        a = loadSettings()
        a['table_name'] = ''
        saveSettings(a)


def mainTable(tableName):
    tName = getcwd() + '/Database/' + tableName

    openDB(tName, """CREATE TABLE log (timeStamp text, subject text, topics text, time integer)""", commit=True)
    openDB(tName, """CREATE TABLE sub_log (sub_short text, subject text)""", commit=True)
    openDB(tName, """CREATE TABLE delete_logs (subject text, topics text, time integer)""", commit=True)


def subjects():
    tableName = fileSettings['table_name']
    if tableName is None or tableName == '':
        mainLabel1.config(text='You Need to select a table.',
                          font=14, bg=color['TABLE_NOT_FND_COLOR'], fg='red')
        mainLabel1.grid(row=0, column=0, sticky=W)
        stateOfBtn(DISABLED)
        main_close()
        resFrame()

    else:
        n_s = {}
        items = openDB(tableName, "SELECT rowid,* FROM sub_log")

        for item in items:
            n_s[item[1]] = item[2]

        return n_s


def stateOfBtn(state):
    newSub.config(state=state)
    inpData.config(state=state)
    viewData.config(state=state)
    checkAct.config(state=state)
    delAct.config(state=state)
    disSub.config(state=state)


def loadSettings():
    return json.load(open('settings.json', 'r'))


def saveSettings(file):
    out_file = open("settings.json", "w")
    json.dump(file, out_file, indent=6)
    out_file.close()


def database():
    New_Table_Window = Toplevel(root, bg=color['MENU_COLORS'])
    New_Table_Window.title('Adding a new table')
    New_Table_Window.geometry('700x200')
    New_Table_Window.after(1, lambda: New_Table_Window.focus_force())

    Label(New_Table_Window, bg=color['MENU_COLORS']).grid(row=0, column=0)
    Label(New_Table_Window, text='  New table name: ', font=(
        text['TEXT_FONT'], 14), bg=color['MENU_COLORS']).grid(row=1, column=0)
    En = Entry(New_Table_Window, width=30, font=12, bg=color['ENTRY_COLOR'])
    En.grid(row=1, column=1, ipady=3)

    lb1 = Label(New_Table_Window)
    radio = IntVar()

    def check():
        out = []
        for temp in listdir('Database'):
            if temp.endswith('.db') and temp.count('.') == 1:
                out.append(temp.replace('.db', '').lower())

        if radio.get() and En.get() != '' and 1 <= len(En.get()) < 16 and En.get().lower() not in out:
            fileSettings['table_name'] = getcwd() + './Database/' + \
                En.get() + '.db'
            saveSettings(fileSettings)
            fName = loadSettings()['table_name'].split(
                '/')[-1].replace('.db', '')
            mainLabel1.config(text=f'  Log  ~  Table Name - {str(fName).ljust(20)}', font=(text['MAIN_HEADING_FONT'], 15, 'bold'),
                              bg=color['BACKGROUND_COLOR'], fg=color['TABLE_TITLE_COLOR'])
            mainLabel1.grid(row=0, column=0, sticky=W)
            stateOfBtn(NORMAL)

    def ok():
        z = [temp.lower() for temp in listdir(
            'Database') if temp.endswith('.db')]

        if len(En.get()) > 16:
            lb1.config(text='Length of the Table should be less than 16', bg=color['MENU_COLORS'], fg=color['RESTRICT_LEN_COLOR'],
                       font=(text['TEXT_FONT'], 14))
            En.delete('0', 'end')

        elif En.get().lower() + '.db' in z:
            lb1.config(text='Guess you need some memory pills 💊💊 ', bg=color['MENU_COLORS'], fg=color['SAME_NAME_COLOR'],
                       font=(text['TEXT_FONT'], 14))
            En.delete('0', 'end')

        elif En.get() != '' and En.get() is not None and len(En.get()) < 16:
            tableName = En.get() + '.db'
            mainTable(tableName)
            lb1.config(text=' ✔ Your New Table has been Added successfully', fg=color["SUCCESS_COLOR"], font=(text['TEXT_FONT'], 14),
                       bg=color['MENU_COLORS'])
            New_Table_Window.after(3000, lambda: New_Table_Window.destroy())

            t = listdir('./Database')
            if not radio.get() and len(t) == 1:
                New_Table_Window.after(2000, lambda: slt_table())

        else:
            lb1.config(text=' ❌ Give the table a name', font=(
                text['TEXT_FONT'], 14), bg=color['MENU_COLORS'], fg=color["ERROR_COLOR"])

        lb1.grid(row=3, column=1, pady=10)
        lb1.after(4000, lambda: lb1.grid_forget())

    bt = Button(New_Table_Window, text=' Ok ',
                command=ok, font=(text['TEXT_FONT'], 9))
    bt.grid(row=1, column=2, padx=10)

    def delOn():
        if En.get() == '':
            New_Table_Window.after(8000, New_Table_Window.destroy)
        else:
            New_Table_Window.after(1000 * 20, New_Table_Window.destroy)

    New_Table_Window.after(10000, delOn)

    c1 = Checkbutton(New_Table_Window, text='Set it as table name', variable=radio, onvalue=1, offvalue=0, command=check,
                     font=(text["TEXT_FONT"], 14), bg=color['MENU_COLORS'])
    c1.grid(row=2, column=1, padx=10, ipady=10)


def slt_table():
    selectWindow = Toplevel(root, bg=color['MENU_COLORS'])
    selectWindow.title('Select Window')
    selectWindow.geometry('400x300')
    selectWindow.after(1, lambda: selectWindow.focus_force())

    a = listdir('Database')
    out = []
    for temp in a:
        if temp.endswith('.db') and temp.count('.') == 1:
            out.append(temp.replace('.db', ''))

    if len(out) > 0:
        selectWindow.geometry('400x300')
        Label(selectWindow, text='  Select any one of the table ', font=15,
              bg=color['MENU_COLORS'], fg=color['DATABASE_TXT_COLOR']).grid(row=0, column=0)
        radio = IntVar()

        def selection():
            fileSettings['table_name'] = getcwd() + './Database/' + \
                out[radio.get() - 1] + '.db'
            saveSettings(fileSettings)
            fName = loadSettings()['table_name'].split(
                '/')[-1].replace('.db', '')
            mainLabel1.config(text=f' Log  ~  Table Name - {str(fName).ljust(20)}', font=(text['MAIN_HEADING_FONT'], 15, 'bold'),
                              bg=color['BACKGROUND_COLOR'], fg=color['TABLE_TITLE_COLOR'])
            mainLabel1.grid(row=0, column=0, sticky=W)
            stateOfBtn(NORMAL)
            selectWindow.after(1000 * 3, lambda: selectWindow.destroy())

        canvas = Canvas(selectWindow, bg=color['MENU_COLORS'])
        scroll = Scrollbar(selectWindow, orient='vertical',
                           command=canvas.yview, bg=color['MENU_COLORS'])
        r, z = 3, 1

        tTopic = loadSettings()['table_name'].split('/')[-1]

        for temp in range(len(out)):
            label = Radiobutton(canvas, text=out[temp].replace('.db', ''), value=z, variable=radio,
                                command=selection, font=12, bg=color['MENU_COLORS'], fg=color['DATABASE_TXT_COLOR'])

            if out[temp] == tTopic.replace('.db', ''):
                label.select()

            canvas.create_window(0, temp * 50, anchor='nw',
                                 window=label, height=50)
            r, z = r + 1, z + 1
        canvas.configure(scrollregion=canvas.bbox(
            'all'), yscrollcommand=scroll.set)

        canvas.grid(row=1, column=0)
        if z > 6:
            scroll.grid(row=1, column=1, sticky=N + S + W)

        selectWindow.after(1000 * 15, lambda: selectWindow.destroy())

    else:
        selectWindow.geometry('500x200')
        mainLabel1.config(text='You Need to select a table.', font=(text['MAIN_HEADING_FONT'], 15, 'bold'), bg=color['TABLE_NOT_FND_COLOR'],
                          fg=color["ERROR_COLOR"])
        mainLabel1.grid(row=0, column=0, sticky=W)
        Label(selectWindow, text='No table was found in the current Directory', font=(text['TEXT_FONT'], 15, 'bold'), bg=color["MENU_COLORS"],
              fg=color["ERROR_COLOR"]).grid(row=0, column=0, sticky=NW)
        Label(selectWindow, text='Redirecting you to the New Table Window......', bg=color["MENU_COLORS"],
              font=(text['TEXT_FONT'], 15, 'bold')).grid(row=1, column=0, sticky=NW)
        selectWindow.after(3000, lambda: selectWindow.destroy())
        selectWindow.after(2950, database)


def displaySubject():
    main_close()
    result_frame.grid_forget()
    n_s = subjects()

    if len(n_s) > 0:
        tp4.config(text='  These are the subject  ', bg=color["CHILD_COLOR"], font=(
            text["SUB_HEADING_FONT"], 15), justify='center')
        disSubList.delete('0', 'end')
        disSubList.config(width=50, font=(
            text["TEXT_FONT"], 14), bg=color["CHILD_COLOR"])
        tp4.grid(row=0, column=0, ipady=3, ipadx=10)

        disSubList.insert(END, '    ')
        for k, v in n_s.items():
            disSubList.insert(END, f'     {k} : {v}')

        disSubList.grid(row=1, column=0, ipady=len(n_s) + 50)

    else:
        tp2.config(text='   !! No Subject were found !!     ', font=(
            text["ALERT_FONT"], 15, 'bold'), fg=color["ERROR_COLOR"], bg=color["CHILD_COLOR"])
        tp2.grid(row=0, column=0)

    disSubBtn.config(text='X'.center(3), command=close, bg='red')
    # row=0, column=2, sticky=NE, ipadx=15, pady=5
    disSubBtn.grid(row=0, column=2, sticky=NE, ipadx=10, pady=5, ipady=2)


def newSubject():
    n_s = subjects()
    tableName = loadSettings()['table_name']
    main_close()
    result_frame.grid_forget()

    tp2.config(text=' Add New Subject', font=(
        text["SUB_HEADING_FONT"], 20, 'bold'), justify='center', bg=color["CHILD_COLOR"], fg=color["TEXT_COLOR"])
    tp2.grid(row=0, column=0, ipady=15)
    nslb1.config(text='Enter the new Subject Name',
                 font=12, bg=color["CHILD_COLOR"])
    nslb2.config(text='Enter the Subject Shortcut Key',
                 font=12, bg=color["CHILD_COLOR"])

    nslb1.grid(row=1, column=0, sticky=NW, pady=10)
    nslb2.grid(row=2, column=0, sticky=NW, pady=5)

    subName.config(textvariable=StringVar(), width=30, borderwidth=2)
    shortSub.config(textvariable=StringVar(), width=30, borderwidth=2)

    subName.grid(row=1, column=1, pady=10, padx=50, sticky=NE, ipady=5)
    shortSub.grid(row=2, column=1, pady=10, padx=50, sticky=NE, ipady=5)

    def delss():
        subName.delete(0, END), shortSub.delete(0, END), lab1.grid_forget()
        lab2.grid_forget(), nslb3.grid_forget(), nsbtn2.config(
            state=NORMAL), stateOfBtn(NORMAL)

    def det():
        a, b = False, False

        if len(subName.get()) <= 18:
            if subName.get() not in n_s.values() and subName.get() != '':
                lab1.config(
                    text=' ✔ ', fg=color["SUCCESS_COLOR"], bg=color["CHILD_COLOR"], font=12)
                a = True
            else:
                if subName.get() == '':
                    lab1.config(text='Subject Name cannot be empty.',
                                fg=color["ERROR_COLOR"], bg=color["CHILD_COLOR"])
                else:
                    lab1.config(text=f'!! {subName.get()} is already used. ', fg=color["ERROR_COLOR"], font=(
                        text["ALERT_FONT"], 14, 'bold'), bg=color["CHILD_COLOR"])
        else:
            lab1.config(text=' Subject Name cannot be greater than 18',
                        fg=color["ERROR_COLOR"], bg=color["CHILD_COLOR"], font=(text["ALERT_FONT"], 14, 'bold'))

        if shortSub.get() not in n_s.keys() and shortSub.get() != '':
            lab2.config(
                text=' ✔ ', bg=color["CHILD_COLOR"], fg=color["SUCCESS_COLOR"], font=12)
            b = True
        else:
            if shortSub.get() == '':
                lab2.config(text='Shortcut Key cannot be empty.', fg=color["ERROR_COLOR"], bg=color["CHILD_COLOR"], font=(
                    text["ALERT_FONT"], 14, 'bold'))
            else:
                lab2.config(text=f'*You have already used this key for {n_s[shortSub.get()]} subject  ', fg=color["ERROR_COLOR"],
                            bg=color["CHILD_COLOR"], font=(text["ALERT_FONT"], 14, 'bold'))

        if not a:
            subName.delete(0, END)
            lab1.after(5000, lambda: lab1.grid_forget())

        if not b:
            shortSub.delete(0, END)
            lab2.after(5000, lambda: lab2.grid_forget())

        if a and b:
            openDB(tableName, "INSERT INTO sub_log VALUES (?,?)",
                   (shortSub.get(), subName.get()), True)

            nslb3.config(text='\t\tYou Data has been Recorded successfully...        ', font=('Yu Mincho', 14, 'bold'),
                         bg=color["CHILD_COLOR"], fg=color["SUCCESS_COLOR"])
            nslb3.grid(row=4, column=0, pady=10, columnspan=3)
            nsbtn2.config(state=DISABLED)
            b1.after(2000, delss)
            stateOfBtn(DISABLED)

        lab1.grid(row=1, column=2, pady=10)
        lab2.grid(row=2, column=2, pady=10)

    nsbtn2.config(text=' Submit ', command=det)
    nsbtn2.grid(row=3, column=0, pady=10, sticky=E)

    nsbtn.config(text=' Close ', command=close)
    nsbtn.grid(row=3, column=1, pady=10)


def add_one():
    tableName = loadSettings()['table_name']
    main_close()
    result_frame.grid_forget()
    n_s = subjects()

    if len(n_s) > 0:

        addDList.delete('0', 'end')
        addDList.config(width=60, font=12, selectmode=MULTIPLE, bd=2, height=8)

        lab1.config(text=' Inserting Data ', font=(text["SUB_HEADING_FONT"], 20, 'bold'), justify='center', bg=color["CHILD_COLOR"],
                    fg=color["TEXT_COLOR"])
        lab1.grid(row=0, column=0)

        aolbl1.config(text=' These are the subjects: ', font=(
            text["HEADING_FONT"], 18, 'bold'), fg=color["TEXT_COLOR"], bg=color["CHILD_COLOR"])
        aolbl1.grid(row=1, column=0, sticky=W)

        sb.config(orient=VERTICAL)
        addDList.config(yscrollcommand=sb.set, font=('Arial', 15))

        if len(n_s) > 9:
            sb.grid(row=2, column=1, sticky=N + S + W)
            sb.config(command=addDList.yview)

        for k, v in n_s.items():
            addDList.insert(END, f'   {k} : {v}, ')

        addDList.grid(row=2, column=0, ipady=20)

        aolb2.config(text='  Subject  ', font=14,
                     bg=color["CHILD_COLOR"], fg=color["TEXT_COLOR"])
        aolb3.config(text='  Topic  ', font=14,
                     bg=color["CHILD_COLOR"], fg=color["TEXT_COLOR"])
        aolb4.config(text='  For how many minutes  ', font=14,
                     bg=color["CHILD_COLOR"], fg=color["TEXT_COLOR"])

        aolb2.grid(row=3, column=0, sticky=NW, pady=15)
        aolb3.grid(row=4, column=0, sticky=NW, pady=10)
        aolb4.grid(row=5, column=0, sticky=NW, pady=10)

        def delstt():
            sub.delete(0, END), topic.delete(
                0, END), time.delete(0, END), tp2.grid_forget()
            tp3.grid_forget(), aolb5.grid_forget(), b1.config(
                state=NORMAL), tp4.grid_forget(), stateOfBtn(NORMAL)

        def det():
            da = False
            db = False
            dc = False

            if sub.get() not in n_s.keys():
                tp2.config(text='* This Subject not found.',
                           fg=color["ERROR_COLOR"], bg=color["CHILD_COLOR"], font=(text["ALERT_FONT"], 14, 'bold'))
            else:
                tp2.config(
                    text='  ✔  ', bg=color["CHILD_COLOR"], fg=color["SUCCESS_COLOR"], font=20)
                da = True

            if time.get().isdigit() and time.get() != '':
                db = True
                tp3.config(
                    text='  ✔  ', bg=color["CHILD_COLOR"], fg=color["SUCCESS_COLOR"], font=20)
            else:
                tp3.config(text=' * The time should be in integer format.',
                           fg=color["ERROR_COLOR"], bg=color["CHILD_COLOR"], font=(text["ALERT_FONT"], 14, 'bold'))

            if len(topic.get()) > 50:
                tp4.config(text=' !! Topic is to large ', fg=color["ERROR_COLOR"], bg=color["CHILD_COLOR"], font=(
                    text["ALERT_FONT"], 14, 'bold'))
            else:
                tp4.config(
                    text='  ✔  ', bg=color["CHILD_COLOR"], fg=color["SUCCESS_COLOR"], font=20)
                dc = True

            if da and db and dc:
                timeStamp = datetime.now().strftime('%d-%m-%y: %H:%M:%S')
                openDB(tableName, "INSERT INTO log VALUES (?,?,?,?)",
                       (timeStamp, n_s[sub.get()], topic.get(), time.get(),), True)
                aolb5.config(text='✔ Your data has been added Successfully.',
                             font=14, bg=color["CHILD_COLOR"], fg=color["SUCCESS_COLOR"])
                aolb5.grid(row=7, column=0, padx=30, pady=10)
                b1.config(state=DISABLED)
                b1.after(2000, delstt)
                stateOfBtn(DISABLED)

            tp2.grid(row=3, column=1)
            tp4.grid(row=4, column=1)
            tp3.grid(row=5, column=1)

        sub.config(textvariable=StringVar(), width=8)
        topic.config(textvariable=StringVar(), width=40)
        time.config(textvariable=StringVar(), width=10)

        sub.grid(row=3, column=0, pady=5, padx=20, ipady=5)
        topic.grid(row=4, column=0, pady=5, padx=20)
        time.grid(row=5, column=0, pady=5, padx=30)

        b1.config(text='Submit', command=det)
        b1.grid(row=6, column=0, padx=30)

    else:
        tp2.config(text='   !!! No Subjects were found !!!   ',
                   bg=color["CHILD_COLOR"], fg=color["ERROR_COLOR"], font=(text["ALERT_FONT"], 15, 'bold'))
        tp2.grid(row=0, column=0)

    aobtn1.config(text='X'.center(3), command=close, bg='red')
    aobtn1.grid(row=0, column=2, sticky=NE, ipadx=10, pady=5, ipady=2)


def show_data():
    tableName = loadSettings()['table_name']
    main_close()
    result_frame.grid_forget()

    items = openDB(tableName, "SELECT * FROM log")

    if len(items) > 0:
        listBox.delete(*listBox.get_children())
        sb.config(orient=VERTICAL)

        style = ttk.Style()

        style.configure("mystyle.Treeview", font=(
            text["SUB_HEADING_FONT"], 15))

        style.theme_use("default")
        style.map('Treeview', background=[('selected', 'black')])
        style.map('Treeview.Heading', font=[(None, 16)])

        lab1.config(text="Table Data", font=(
            text["SUB_HEADING_FONT"], 20), justify='center', bg=color["CHILD_COLOR"], fg=color["TEXT_COLOR"])
        lab1.grid(row=0, columnspan=3)

        listBox.config(show='headings', style="mystyle.Treeview", height=30)
        listBox["column"] = ('TimeStamp', 'Subject', 'Time', 'Topic')

        listBox.column("TimeStamp", width=185)
        listBox.column("Subject", width=160)
        listBox.column("Time", width=80)
        listBox.column("Topic", width=420)

        listBox.grid(row=1, column=2)

        cols = ('TimeStamp', 'Subject', 'Time', 'Topic')
        for col in cols:
            listBox.heading(col, text=col)

        listBox.tag_configure(
            'odd', background=color["STRIP_COL_ODD"], font=(text["TEXT_FONT"], 12))
        listBox.tag_configure(
            'even', background=color["STRIP_COL_EVN"], font=(text["TEXT_FONT"], 12))
        count = 0

        for tstamp, subject, topic, time in items:
            tag = 'odd'
            if count % 2 == 0:
                tag = 'even'

            listBox.insert("", "end", values=(tstamp.center(25), subject.center(15), str(time).center(16), topic.ljust(10)),
                           tags=(tag,), iid=count)

            count += 1

        listBox.config(yscrollcommand=sb.set)
        sb.config(command=listBox.yview)

        if count >= 30:
            sb.grid(row=1, column=4, sticky=N + W + S, padx=15, pady=10)
    else:
        aslb1.config(text='!!! No Data was found. !!!   ',
                     bg=color["CHILD_COLOR"], fg=color["ERROR_COLOR"], font=(text["ALERT_FONT"], 15, 'bold'))
        aslb1.grid(row=0, column=0)

    vdbtn.config(text='X'.center(3), command=close, bg='red')
    # row=0, column=3, padx=10, pady=10, ipady=5, ipadx=5
    vdbtn.grid(row=0, column=3, sticky=NE, ipadx=10, pady=10, ipady=2)


def date_range(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


def oReturn():
    o = []
    start_dt = date(2010, 1, 1)
    end_dt = date(2030, 12, 31)

    for dt in date_range(start_dt, end_dt):
        o.append(dt.strftime("%d-%m-%y"))
    return o


def activitySearch():
    tableName = loadSettings()['table_name']
    main_close()
    result_frame.grid_forget()
    n_s = subjects()

    items = openDB(tableName, "SELECT * FROM log")
    entered_date.delete(0, END)
    aslb1.config(text='')

    if len(items) > 0:
        aslb1.config(text='\t\tActivity Search', font=(
            text["SUB_HEADING_FONT"], 20, 'bold'), justify='center', bg=color["CHILD_COLOR"], fg=color["TEXT_COLOR"])
        aslb2.config(text='', bg=color["CHILD_COLOR"])
        aslb3.config(text=' Enter the Date here (To get Today\'s Activity Enter nothing) ', font=(
            text["HEADING_FONT"], 12, 'bold'), bg=color["CHILD_COLOR"], fg=color["TEXT_COLOR"])
        tp4.config(text='   ', bg=color["CHILD_COLOR"])
        entered_date.config(width=12, font=10)

        aslb1.grid(row=0, column=0)
        aslb2.grid(row=1, column=0, columnspan=3)
        aslb3.grid(row=2, column=0, sticky=NW, pady=5)
        tp4.grid(row=3, column=0, columnspan=3, ipady=5)

        entered_date.config(font=(text["TEXT_FONT"]), width=13)
        entered_date.grid(row=2, column=2, ipady=5, padx=10)
        atemp = " 'dd-mm' format "
        entered_date.insert(0, atemp)

        sb.config(orient=HORIZONTAL, width=20)
        sb2.config(orient=VERTICAL, width=20)

        # aslb3.after(5000, lambda :aslb3.config(text=' Enter the Date here '))
        def search():
            yr = datetime.now().strftime('-%y')
            ed = entered_date.get()
            if ed in ['', atemp]:
                entered_date.delete(0, END)
                entered_date.insert(0, str(datetime.now().strftime("%d-%m")))
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
            actSList.config(width=60, font=(text["TEXT_FONT"], 14), yscrollcommand=sb2.set, xscrollcommand=sb.set,
                            height=15)

            i = 1
            m = 0
            for temp in out:
                if len(temp) > 1:
                    x = ", ".join(temp[1:])
                    actSList.insert(END, f'  In {n_s[temp[0]]} :')
                    actSList.insert(END, f'    {x}.')
                    actSList.insert(END, "\n")
                    t = False
                    i += 1

                    if m < len(x):
                        m = len(x)

            sb.config(command=actSList.xview)
            sb2.config(command=actSList.yview)

            if t:
                actSList.grid_forget(), sb.grid_forget(), sb2.grid_forget()

                if ed in oReturn():
                    lab3.config(text=f'Looks like you have not done anything on {ed}', font=(text["ALERT_FONT"], 14),
                                fg=color["TEXT_COLOR"], bg=color["CHILD_COLOR"])
                else:
                    if t:
                        lab3.config(text="Enter the date in dd-mm-yy format", font=(text["ALERT_FONT"], 14),
                                    fg=color["TEXT_COLOR"], bg=color["CHILD_COLOR"])

                lab3.grid(row=5, column=0, sticky=N + W + S)

            else:
                lab3.grid_forget()

                if m > 80:  # for horizontal
                    sb.grid(row=3, column=0, sticky=W + E)

                if i > 6:  # for vertical
                    sb2.grid(row=5, column=1, stick=N + W + S)

                actSList.grid(row=5, column=0, ipady=30, ipadx=10)

        asbtn1.config(text='Search', command=search)
        asbtn1.grid(row=2, column=4, padx=10)

    else:
        aslb1.config(text='You need to Add Data To View Your Activity   ', font=(
            text["ALERT_FONT"], 15, 'bold'), bg=color["CHILD_COLOR"], fg=color["ERROR_COLOR"])
        aslb1.grid(row=0, column=0)

    asbtn.config(text='X'.center(3), command=close, bg='red')
    asbtn.grid(row=0, column=5, sticky=NE, ipadx=10, pady=5, ipady=2)


def UpdateSubject():
    tableName = loadSettings()['table_name']
    items = openDB(tableName, "SELECT rowid,* FROM sub_log")

    Rid = [i[0] for i in items]
    for i in range(len(Rid)):
        openDB(tableName, "UPDATE sub_log SET rowid = (?) WHERE rowid = (?)",
               (i + 1, Rid[i]), True)


def updateTable():
    tableName = loadSettings()['table_name']
    items = openDB(tableName, "SELECT rowid,* FROM log")
    Rowid = [i[0] for i in items]

    for i in range(len(Rowid)):
        openDB(tableName, "UPDATE log SET rowid=(?) WHERE rowid=(?)",
               (i + 1, Rowid[i]), True)


def DelSubRow():
    tableName = loadSettings()['table_name']
    main_close()
    result_frame.grid_forget()
    n_s = subjects()

    if len(n_s):
        des.config(textvariable=StringVar(), width=5)
        tp2.config(text='Delete Subject/Row Data.'.rjust(10), font=(
            text["SUB_HEADING_FONT"], 20, 'bold'), justify='center', bg=color["CHILD_COLOR"], fg=color["TEXT_COLOR"])
        delsrlb.config(text='Do you want to delete the Subject(s) or Row(r) : ', font=(
            text['TEXT_FONT'], 14), fg=color["TEXT_COLOR"], bg=color["CHILD_COLOR"])

        tp2.grid(row=0, column=0, sticky=N)
        delsrlb.grid(row=1, column=0, sticky=NW, padx=10)
        des.grid(row=1, column=1)

        UpdateSubject()
        updateTable()

        def ok():
            if des.get() == 's':
                a = openDB(tableName, "SELECT rowid, * FROM sub_log")

                sb.config(orient=VERTICAL)
                delrlist1.delete('0', 'end')
                delrlist1.config(yscrollcommand=sb.set, width=40, font=12)
                delslb.config(
                    text='Select rowid of the subject you want to remove', font=8, bg=color["CHILD_COLOR"])

                delslb.grid(row=2, column=0, sticky=NW, pady=10)

                for data in range(len(a)):
                    delrlist1.insert(
                        END, f'  RowId = {a[data][0]} : {a[data][2]}')

                data = len(a)-1
                if data > 9:
                    sb.grid(row=3, column=1, sticky=N + S + W)

                delrlist1.grid(row=3, column=0, sticky=NW)
                sb.config(command=delrlist1.yview)

                r = 3

                delrid.config(text='\tRowid?? ', font=(
                    'Bahnschrift SemiLight', 12), bg=color["CHILD_COLOR"])
                delrid.grid(row=r + 1, column=0, stick=NW, pady=20)
                Id.grid(row=r + 1, column=0, pady=20)

                def OKK():
                    items = openDB(
                        tableName, "SELECT sub_short FROM sub_log WHERE rowid = (?)", (Id.get(),))
                    n_s = subjects()
                    dellb3.grid_forget(), dellb.grid_forget(), dellb2.grid_forget()

                    try:
                        tp4.grid_forget()
                        s = n_s[items[0][0]]
                        a = openDB(
                            tableName, "SELECT rowid,topics FROM log WHERE subject = (?)", (s,))

                        sub = '\n'.join([str(i[1]).ljust(80) for i in a])
                        rid = [i[0] for i in a]

                        temp2 = False
                        if len([i[1] for i in a]) > 0:
                            dellb.config(text=f' In {s}, these topics will be removed: ',
                                         font=('Bahnschrift SemiLight', 14), fg=color["TEXT_COLOR"], bg=color["CHILD_COLOR"])

                            dellb2.config(text=f'{sub}', font=(
                                'Book Antiqua', 12), bg=color["CHILD_COLOR"])
                            dellb2.grid(row=r + 3, column=0, sticky=SW)
                        else:
                            temp2 = True
                            dellb.config(text=f' Do you want to remove Subject {s}', font=('Bahnschrift SemiLight', 14),
                                         fg='red', bg=color["CHILD_COLOR"])

                        dellb.grid(row=r + 2, column=0, sticky=NW, pady=10)

                        def close_grid():
                            dellb2.grid_forget()
                            dellb.grid_forget()
                            dely.grid_forget()
                            deln.grid_forget()
                            dellb3.grid_forget()
                            tp4.after(1000, ok)
                            Id.delete(0, END)

                        def yes():
                            openDB(
                                tableName, "DELETE from sub_log WHERE rowid = (?)", (str(Id.get()),), True)

                            for i in rid:
                                openDB(
                                    tableName, "DELETE from log WHERE rowid = (?)", (str(i),), True)

                            if temp2:
                                dellb3.config(text=f' {s} is removed. ', font=(
                                    'Simsun', 15), bg=color["CHILD_COLOR"])
                            else:
                                dellb3.config(text=f' {s} is removed along with its topics.', font=('SimSun', 15),
                                              bg=color["CHILD_COLOR"])

                            dellb3.grid(row=r + 6, column=0)

                            tp4.after(3000, lambda: close_grid())

                        dely.config(text='Yes', command=yes)
                        deln.config(text='No', command=close)

                        dely.grid(row=r + 4, column=0, pady=10)
                        deln.grid(row=r + 4, column=0, sticky=NE, pady=10)

                    except:
                        dellb.grid_forget(), dellb2.grid_forget(), dellb3.grid_forget(
                        ), dely.grid_forget(), deln.grid_forget()
                        tp4.config(text=f'The Subject is not defined.', font=(
                            'Bahnschrift', 14, 'bold'), bg=color["CHILD_COLOR"])
                        tp4.grid(row=9, column=0)

                delbtn.config(text='OK', command=OKK)
                delbtn.grid(row=r + 1, column=0, sticky=E, pady=20)

            elif des.get() == 'r':
                n_s = subjects()
                result_frame.grid_forget()
                result_frame.config(fg=color["RES_ME_COLOR"])

                dellb.config(text=f'Which Subject do you want to remove', font=(text['TEXT_FONT'], 14), bg=color["CHILD_COLOR"],
                             fg=color["TEXT_COLOR"])
                dellb.grid(row=2, column=0, pady=10, sticky=NW)

                delrlist3.delete('0', 'end')
                delrlist3.config(yscrollcommand=sb.set,
                                 width=30, font=5, height=7)

                for k, v in n_s.items():
                    delrlist3.insert(END, f'  {k} : {v}')

                if len(n_s) > 7:
                    sb.grid(row=3, column=2, sticky=N + S + W)

                delrlist3.grid(row=3, column=0, ipady=5, sticky=N + W)
                sb.config(command=delrlist3.yview)

                dellb2.config(text='Subject: '.rjust(
                    15), font=3, bg=color["CHILD_COLOR"])
                dellb2.grid(row=4, column=0, sticky=NW, padx=30, pady=20)
                subj.grid(row=4, column=0, ipady=3, pady=20)

                def ok_row():
                    if subj.get() in n_s.keys():
                        lab1.grid_forget()
                        delrlist4.delete('0', 'end')
                        delrlist4.config(yscrollcommand=sb2.set,
                                         width=50, font=10, height=5)

                        delslb.config(text=f' For {n_s[subj.get()]}', font=(
                            text["TEXT_FONT"], 14), bg=color["CHILD_COLOR"])
                        delslb.grid(row=5, column=0, sticky=N + W)
                        sb2.config(command=delrlist4.yview)

                        a = openDB(
                            tableName, "SELECT rowid,* FROM log WHERE subject = (?)", (n_s[subj.get()],))

                        if len(a) > 5:
                            sb2.grid(row=6, column=1, sticky=N + S + W)

                        forward = False
                        if len(a) > 0:
                            for i in a:
                                delrlist4.insert(
                                    END, f' Rowid: {i[0]}, Topic: {i[3]}')
                                forward = True
                        else:
                            Id.grid_forget(), delrid.grid_forget(), delbtn4.grid_forget(), dellb3.grid_forget()
                            dellb4.grid_forget(), dely.grid_forget(), deln.grid_forget(), sb2.grid_forget()

                            delrlist4.insert(
                                END, f'  !! No Topic entry was found !!')

                        delrlist4.grid(row=6, column=0, sticky=NW)

                        if forward:
                            items = a
                            delrid.config(text='Rowid?? '.rjust(15), font=(
                                'Bahnschrift SemiLight', 14), bg=color["CHILD_COLOR"])
                            delrid.grid(row=7, column=0,
                                        sticky=N + W, pady=15, padx=10)
                            Id.grid(row=7, column=0, pady=15)

                            def OOOk():
                                dellb4.config(text='')
                                if Id.get() in [str(i[0]) for i in items]:
                                    item = openDB(
                                        tableName, "SELECT rowid, topics, time FROM log WHERE rowid = (?)", (Id.get(),))[0]
                                    dellb3.config(
                                        text=f'Remove:  {item[1]} ?? ', font=6, bg=color["CHILD_COLOR"], fg='red')
                                    dellb3.grid(row=8, column=0,
                                                sticky=NW, pady=15)

                                    def del_grid():
                                        delrid.grid_forget()
                                        Id.grid_forget()
                                        dellb3.grid_forget()
                                        dely.grid_forget()
                                        deln.grid_forget()
                                        dellb4.grid_forget()
                                        delbtn4.grid_forget()
                                        delrlist4.delete('0', 'end')
                                        tp4.after(1000, ok_row)

                                    def yes():
                                        openDB(
                                            tableName, "DELETE from log WHERE rowid = (?)", (Id.get(),), True)
                                        openDB(tableName, "INSERT INTO delete_logs VALUES (?,?,?)", (subj.get(
                                        ), item[1], item[2]), True)

                                        dellb4.config(text=f'{item[1]} has been removed.'.center(20),
                                                      font=('Bahnschrift', 15, 'bold'), bg=color["CHILD_COLOR"])
                                        dellb4.grid(row=9, column=0)

                                        delbtn4.after(3000, lambda: del_grid())

                                    dely.config(text='Yes', command=yes)
                                    deln.config(text='No', command=close)

                                    dely.grid(row=8, column=1,
                                              pady=15, sticky=W)
                                    deln.grid(row=8, column=2, pady=15)

                                else:
                                    dellb3.grid_forget(), dely.grid_forget(), deln.grid_forget()
                                    dellb4.config(
                                        text=f'Rowid {Id.get()} is not in {n_s[subj.get()]} subject.')
                                    dellb4.grid(row=8, column=0)

                            delbtn4.config(text='Ok', command=OOOk)
                            delbtn4.grid(row=7, column=1, pady=15)
                    else:
                        delrlist4.grid_forget(), delslb.grid_forget(
                        ), delrid.grid_forget(), Id.grid_forget(), delbtn4.grid_forget()
                        dellb3.grid_forget(), dely.grid_forget(), deln.grid_forget(
                        ), dellb4.grid_forget(), sb2.grid_forget()
                        lab1.config(text='Subject Not Found',
                                    font=('Bahnschrift', 15, 'bold'))
                        lab1.grid(row=7, column=0, pady=30)

                delrbtn.config(text='Ok', command=ok_row)
                delrbtn.grid(row=4, column=1, sticky=S + W, pady=20)

        delsub.config(text=' Ok ', command=ok)
        delsub.grid(row=1, column=2, padx=30)

    else:
        tp4.config(text='You have to add subject in order to delete it.', font=(text["ALERT_FONT"], 15, 'bold'), fg=color["ERROR_COLOR"],
                   bg=color["CHILD_COLOR"])
        tp4.grid(row=0, column=0, sticky=N, ipady=10)

    nslb1.config(text='     ', font=15, bg=color["CHILD_COLOR"])
    nslb1.grid(row=0, column=3)
    delcl.config(text='X'.center(3), command=close, bg='red', fg='white')
    delcl.grid(row=0, column=4, sticky=NE, ipadx=10, pady=5, ipady=2)


def main_close():
    dely.grid_forget(), deln.grid_forget(), dellb3.grid_forget(
    ), dellb.grid_forget(), dellb2.grid_forget(),
    des.grid_forget(), delsrlb.grid_forget(), delbtn.grid_forget(
    ), delsub.grid_forget(), delcl.grid_forget(),
    sb.grid_forget(), delslb.grid_forget(), delrlist1.grid_forget(
    ), Id.grid_forget(), tp4.grid_forget(),
    delrid.grid_forget(), delrbtn.grid_forget(
    ), dellb4.grid_forget(), delrlist3.grid_forget()
    delrlist4.grid_forget(), subj.grid_forget(), sb2.grid_forget(
    ), delbtn4.grid_forget(), showDList.grid_forget()

    aslb1.grid_forget(), aslb2.grid_forget(
    ), aslb3.grid_forget(), entered_date.grid_forget()
    actSList.grid_forget(), lab3.grid_forget(
    ), asbtn.grid_forget(), asbtn1.grid_forget(), sb.grid_forget()

    sb.grid_forget(), vdbtn.grid_forget()

    disSubBtn.grid_forget(), listBox.grid_forget()

    nslb1.grid_forget(), nslb2.grid_forget(), nslb3.grid_forget(
    ), subName.grid_forget(), shortSub.grid_forget()
    lab1.grid_forget(), lab2.grid_forget(), nsbtn.grid_forget(), nsbtn2.grid_forget()

    aolbl1.grid_forget(), aolb2.grid_forget(), aolb3.grid_forget(), aolb4.grid_forget()
    aolb5.grid_forget(), tp2.grid_forget(), tp3.grid_forget(
    ), sub.grid_forget(), topic.grid_forget()
    time.grid_forget(), b1.grid_forget(), aobtn1.grid_forget(
    ), addDList.grid_forget(), disSubList.grid_forget()


def connect():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except urllib.error.URLError:
        return False


def send_feedback(name, email_id, message):
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.ehlo()
    smtp_object.starttls()

    email = ''
    password = ''
    smtp_object.login(email, password)
    from_address = email
    subject = 'Customer FeedBack'
    name = name.replace(' ', '_')
    message = message.replace(' ', '_')
    message = 'Name:_' + name + '<<::>>Email_Address:_' + \
        email_id + '<<::>>Comment:_' + message

    Body = f"""Subject:{subject}

    {message}
    """
    smtp_object.sendmail(from_address, from_address, Body)
    smtp_object.quit()


def feedback():
    feedback_window = Toplevel(root, bg=color["MENU_COLORS"])
    feedback_window.title(" FeedBack Window ")
    feedback_window.geometry('550x400')

    Label(feedback_window, text=' FeedBack Form ', justify='center', font=(
        text['TEXT_FONT'], 20, 'bold'), bg=color["MENU_COLORS"]).grid(row=0, column=1)
    Label(feedback_window, text=' Name ', font=(
        text['TEXT_FONT'], 14), bg=color["MENU_COLORS"]).grid(row=1, column=0, padx=10, pady=10)
    Label(feedback_window, text=' Email Address ', font=(
        text['TEXT_FONT'], 14), bg=color["MENU_COLORS"]).grid(row=2, column=0, padx=10, pady=10)
    Label(feedback_window, text=' Comment ', font=(
        text['TEXT_FONT'], 14), bg=color["MENU_COLORS"]).grid(row=3, column=0, padx=10, pady=10)

    name = StringVar()
    email_id = StringVar()
    n = Entry(feedback_window, textvariable=name, width=30)
    e = Entry(feedback_window, textvariable=email_id, width=30)

    n.grid(row=1, column=1, pady=10, ipady=5)
    e.grid(row=2, column=1, pady=10, ipady=5)

    c = Text(feedback_window, height=10, width=40)
    c.grid(row=3, column=1, pady=15, padx=5, columnspan=2)

    n.insert(0, 'Your Name')
    e.insert(0, 'user_@domain.com')
    c.insert('1.0', ' // Your comment.')

    def submit():
        message = c.get("1.0", END)

        if connect():
            send_feedback(name.get(), email_id.get(), message)
            feedback_window.after(500, feedback_window.destroy)
            messagebox.showinfo('Feedback Window',
                                'Your feedback has been submitted.')
        else:
            messagebox.showerror("Connection Error",
                                 " Check your Internet Connection. ")
            feedback_window.after(1, lambda: feedback_window.focus_force())

    button_1 = Button(feedback_window, text=' Submit ', command=submit)
    button_1.grid(row=4, column=1)
    feedback_window.after(1000 * 60 * 4, feedback_window.destroy)


def close():
    main_close()
    resFrame()


def resFrame():
    result_frame.config(text=f'This is the Result Area.', font=(text['MAIN_HEADING_FONT'], 14, 'bold'), borderwidth=2,
                        width=70, height=30, relief=GROOVE, fg='black')

    result_frame.grid(row=1, column=3)


if 'Database' not in listdir(getcwd()):
    mkdir(getcwd() + '/Database/')


checkFile()
fileSettings = loadSettings()
table_name = fileSettings['table_name'].split('/')[-1].replace('.db', '')
color = fileSettings['color']
text = fileSettings['text']


root = Tk()
root.title(' Log  ')
root.attributes('-fullscreen', True)

menu_bar = Menu(root)
menu_bar.add_command(label=' New Table ', command=database)
menu_bar.add_command(label=' Select Table ', command=slt_table)
menu_bar.add_command(label=' FeedBack ', command=feedback)
menu_bar.add_command(label='Close', command=root.quit)

root.config(menu=menu_bar, relief=GROOVE, bg=color['BACKGROUND_COLOR'])

f1 = Frame(root, bg=color["CHILD_COLOR"], borderwidth=3,
           width=700, height=600, relief=SUNKEN)
f1.grid(row=2, column=6, rowspan=50, padx=20, columnspan=3)

result_frame = Label(f1, text=f'This is the Result Area.', font=(
    text['MAIN_HEADING_FONT'], 14, 'bold'), borderwidth=2, width=70, height=30, relief=GROOVE, bg=color['CHILD_COLOR'])
result_frame.grid(row=2, column=3)

newSub = Button(root, text='Add a New Subject',
                command=newSubject, bg=color['MAIN_BTN_COLOR'])
inpData = Button(root, text='Inserting Data',
                 command=add_one, bg=color['MAIN_BTN_COLOR'])
viewData = Button(root, text='To view the entire Data',
                  command=show_data, bg=color['MAIN_BTN_COLOR'])
checkAct = Button(root, text='Check Activity',
                  command=activitySearch, bg=color['MAIN_BTN_COLOR'])
delAct = Button(root, text='To Delete Subject or Row From the Data',
                command=DelSubRow, bg=color['MAIN_BTN_COLOR'])
disSub = Button(root, text='Display the Subjects',
                command=displaySubject, bg=color['MAIN_BTN_COLOR'])

mainLabel1 = Label(root)

if table_name != '':
    mainLabel1.config(text=f'   Log   ~ Table Name - {str(table_name).ljust(20)}', font=(text['MAIN_HEADING_FONT'], 15, 'bold'),
                      bg=color['BACKGROUND_COLOR'], fg=color['TABLE_TITLE_COLOR'])
else:
    mainLabel1.config(text='You Need to select a table.',
                      font=14, bg='#CCF381', fg='red')
    stateOfBtn(DISABLED)

mainLabel1.grid(row=0, column=0, sticky=W, columnspan=3)
newSub.grid(row=2, column=0, sticky=NW, ipady=2, padx=10, pady=8)
inpData.grid(row=3, column=0, sticky=NW, ipady=2, padx=10, pady=8)
viewData.grid(row=4, column=0, sticky=NW, ipady=2, padx=10, pady=8)
checkAct.grid(row=5, column=0, sticky=NW, ipady=2, padx=10, pady=8)
delAct.grid(row=6, column=0, sticky=NW, ipady=2, padx=10, pady=8)
disSub.grid(row=7, column=0, sticky=NW, ipady=2, padx=10, pady=8)

comment = ''
tp2 = Label(f1)
tp3 = Label(f1)
tp4 = Label(f1)
lab1 = Label(f1)
lab2 = Label(f1)
lab3 = Label(f1)
delsrlb = Label(f1)
dellb = Label(f1)
dellb2 = Label(f1)
delslb = Label(f1)
delrid = Label(f1)
dellb4 = Label(f1)
dellb3 = Label(f1)
aslb1 = Label(f1)
aslb2 = Label(f1)
aslb3 = Label(f1)
nslb1 = Label(f1)
nslb2 = Label(f1)
nslb3 = Label(f1)
aolbl1 = Label(f1)
aolb2 = Label(f1)
aolb3 = Label(f1)
aolb4 = Label(f1)
aolb5 = Label(f1)

delrlist4 = Listbox(f1)
delrlist1 = Listbox(f1)
delrlist3 = Listbox(f1)
myList = Listbox(f1)
disSubList = Listbox(f1)
addDList = Listbox(f1)
actSList = Listbox(f1)
showDList = Listbox(f1)

sb = Scrollbar(f1)
sb2 = Scrollbar(f1)

listBox = ttk.Treeview(f1)

f = 10
Id = Entry(f1, width=7, font=f)
subj = Entry(f1, width=10, font=f)
des = Entry(f1, width=30, font=f)
entered_date = Entry(f1, width=30, font=f)
shortSub = Entry(f1, width=30, font=f)
subName = Entry(f1, width=30, font=f)
sub = Entry(f1, width=30, font=f)
topic = Entry(f1, width=30, font=f)
time = Entry(f1, width=30, font=f)

dely = Button(f1)
deln = Button(f1)
delrbtn = Button(f1)
delbtn = Button(f1)
delbtn4 = Button(f1)
delsub = Button(f1)
delcl = Button(f1)
asbtn = Button(f1)
asbtn1 = Button(f1)
vdbtn = Button(f1)
disSubBtn = Button(f1)
nsbtn = Button(f1)
nsbtn2 = Button(f1)
b1 = Button(f1)
aobtn1 = Button(f1)

root.mainloop()
