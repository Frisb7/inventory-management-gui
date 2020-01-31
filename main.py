from tkinter import *
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="",  database="inventory")
db = mydb.cursor()
db.execute("select * from user")
run = 0
if_admin = False
username = ""
ulist = []
plist = []
admin = []
for i in db:
    ulist.append(i[0])
    plist.append(i[1])
    admin.append(i[2])

#user
def check1():
    global run,user,u,p,db,ulist,plist,admin,if_admin,username
    wu = Label(user, text="Wrong username", bg="red", fg="white")
    wp = Label(user, text="Wrong password", bg="red", fg="white")
    u_index = 0
    if u.get() in ulist:
        username = u.get()
        u_index = ulist.index(u.get())
        if p.get() == plist[u_index]:
            if admin[u_index] == 'y':
                if_admin = True
                print("admin : "+u.get())
            else:
                print("not admin : "+u.get())
            user.destroy()
            run = 1
        else:
            wp.grid(row=5, column=1, sticky=NW)
    else:
        wu.grid(row=5, column=1, sticky=NW)
def userwin():
    global user,u,p
    user = Tk()
    user.geometry("200x170+700+300")
    user.minsize(200,170)
    user.maxsize(200,170)
    user.title("Main")
    Label(user).grid()
    l = Label(user, text='LOGIN',font="-size 20") 
    l.grid(row=1, column=1, sticky=NW, padx=4)
    ul = Label(user, text='Username :')
    ul.grid(row=2, sticky=W, padx=4)
    u = Entry(user)
    u.grid(row=2, column=1, sticky=E, pady=4)
    pl = Label(user, text='Password :')
    pl.grid(row=3, sticky=W, padx=4)
    p = Entry(user,show="*")
    p.grid(row=3, column=1, sticky=E, pady=4)
    b = Button(user, text='Login', command=check1)
    b.grid(row=4, column=1, sticky=NW)
    user.mainloop()
userwin()

#inventory
db_inv = mydb.cursor()
db_inv.execute("select * from inventory")
table_inv = []
record_inv = []
for i in db_inv:
    for j in i:
        record_inv.append(j)
    table_inv.append(record_inv)
    record_inv = []
def clear_inv_entry():
    global itm_id,name,stock,avaib,cost
    itm_id.delete(0,END)
    name.delete(0,END)
    stock.delete(0,END)
    avaib.delete(0,END)
    cost.delete(0,END)
def clear_inv_table():
    global frame_table_inv,table_inv
    a = len(table_ser)+1
    for i in range(a):
        for j in range(11):
            Label(frame_table_inv,text="      ",font="-size 10").grid(row=i,column=j)
def data_inv(table_inv):
    global frame_table_inv
    clear_inv_table()
    r = 1
    c = 0
    c1 = 0
    l = ["Iteam No.","Name","Stock","Available","Cost"]
    for i in l:
        Label(frame_table_inv,text=" | ",font="-size 10").grid(row=0,column=c)
        c += 1
        Label(frame_table_inv,text=i,font="-size 10",bg='blue',fg='white').grid(row=0,column=c)
        c += 1
    Label(frame_table_inv,text=" | ",font="-size 10").grid(row=0,column=c)
    c = 1
    for i in table_inv:
        for j in i:
            Label(frame_table_inv,text=j,font="-size 10").grid(row=r,column=c)
            Label(frame_table_inv,text="|",font="-size 10").grid(row=r,column=c1)
            c += 2
            c1 += 2
        Label(frame_table_inv,text="|",font="-size 10").grid(row=r,column=c1)
        c = 1
        c1 = 0
        r += 1
    a = len(table_inv)+1
    for i in range(11):
        for j in range(a,a+10):
            Label(frame_table_inv,text="",font="-size 10").grid(row=j,column=i)
def add_itm():
    global table_inv,root_inv,db_inv,mydb
    global itm_id,name,stock,avaib,cost
    pri_id = itm_id.get()
    itm_name = name.get()
    itm_stock = stock.get()
    itm_avaib = avaib.get()
    itm_cost = cost.get()
    error1 = False
    error2 = False
    error3 = False
    error4 = False
    if (pri_id == "") or (itm_name == ""):
        Label(root_inv,text='                                                            ',fg='white').place(x=350,y=360)
        Label(root_inv,text='Iteam ID and Name is must',bg='red',fg='white').place(x=350,y=360)
        error1 = True
    else:
        Label(root_inv,text='                                                               ').place(x=350,y=360)
        for i in table_inv:
            if (i[0] == str(pri_id)) or (i[1] == itm_name):
                Label(root_inv,text='                                                    ',fg='white').place(x=350,y=360)
                Label(root_inv,text='Iteam ID and Name must be unique',bg='red',fg='white').place(x=350,y=360)
                error1 = True
            else:
                Label(root_inv,text='                                                   ',fg='white').place(x=350,y=360)
                error1 = False
    if not error1:
        if (len(itm_avaib) > 1) or (len(itm_avaib) == 0):
            Label(root_inv,text='                                                        ',fg='white').place(x=350,y=360)
            Label(root_inv,text='Iteam Availability can only be y/n',bg='red',fg='white').place(x=350,y=360)
            error2 = True
        else:
            Label(root_inv,text='                                                                ').place(x=350,y=360)
            error2 = False
    l = ["1","2","3","4","5","6","7","8","9","0"]
    int_count = 0
    int_stock = 0
    if (not error1) and (not error2):
        if itm_stock != '':
            for i in itm_stock:
                if itm_stock == '':
                    break
                elif i in l:
                    int_count += 1
                else:
                    break
            if len(itm_stock) == int_count:
                error3 = False
            else:
                Label(root_inv,text='Stock and Cost numbers only',bg='red',fg='white').place(x=350,y=360)
                error3 = True
        else:
            itm_stock = 0
            error3 = False
    if (not error1) and (not error2):
        if itm_cost != '':
            for i in itm_cost:
                if itm_cost == '':
                    break
                elif i in l:
                    int_stock += 1
                else:
                    break
            if len(itm_cost) == int_stock:
                error4 = False
            else:
                Label(root_inv,text='Stock and Cost numbers only',bg='red',fg='white').place(x=350,y=360)
                error4 = True
        else:
            itm_cost = 0
            error4 = False
    if (not error1) and (not error2) and (not error3) and (not error4):
        Label(root_inv,text='                                                             ',fg='white').place(x=350,y=360)
        Label(root_inv,text='Product Has been added',bg='green',fg='white').place(x=350,y=360)
        record_inv = [pri_id,itm_name,int(itm_stock),itm_avaib,int(itm_cost)]
        table_inv.append(record_inv)
        query = "insert into inventory values("+"\'"+pri_id+"\'"+","+"\'"+itm_name+"\'"+","+str(itm_stock)+","+"\'"+itm_avaib+"\'"+","+str(itm_cost)+")"
        db_inv.execute(query)
        mydb.commit()
        data_inv(table_inv)
def remove_itm():
    global table_inv,root_inv,db_inv,mydb
    global itm_id,name
    Label(root_inv,text='                                                   ',fg='white').place(x=350,y=360)
    pri_id = itm_id.get()
    itm_name = name.get()
    found = False
    if pri_id == '' or itm_name == '':
        Label(root_inv,text='                                               ',fg='white').place(x=350,y=360)
        Label(root_inv,text='Iteam ID and Name is must',bg='red',fg='white').place(x=350,y=360)
    else:
        for i in table_inv:
            if (i[0] == str(pri_id)) and (i[1] == itm_name):
                found = True
                itm = table_inv.index(i)
                query = "delete from inventory where itm_id = \'"+pri_id+"\' and name = \'"+itm_name+"\'"
                db_inv.execute(query)
                mydb.commit()
                table_inv.pop(itm)
                data_inv(table_inv)
                break
    if found:
        Label(root_inv,text='                                                   ',fg='white').place(x=350,y=360)
        Label(root_inv,text='Product is removed',bg='green',fg='white').place(x=350,y=360)
    else:
        Label(root_inv,text='                                                    ',fg='white').place(x=350,y=360)
        Label(root_inv,text='Product not found',bg='red',fg='white').place(x=350,y=360)
def update_itm():
    global table_inv,root_inv,db_inv,mydb
    global itm_id,name,stock,avaib,cost
    pri_id = itm_id.get()
    itm_name = name.get()
    itm_stock = stock.get()
    itm_avaib = avaib.get()
    itm_cost = cost.get()
    error1 = False
    error2 = False
    error3 = False
    error4 = False
    found = False
    if pri_id == '':
        Label(root_inv,text='                                               ',fg='white').place(x=350,y=360)
        Label(root_inv,text='Iteam ID is needed',bg='red',fg='white').place(x=350,y=360)
    else:
        for i in table_inv:
            if i[0] == pri_id:
                a = table_inv.index(i)
                found = True
    if found:
        if itm_name == '':
            Label(root_inv,text='                                               ',fg='white').place(x=350,y=360)
            Label(root_inv,text='Name cannot be empty',bg='red',fg='white').place(x=350,y=360)
            error1 = True
        else:
            Label(root_inv,text='                                               ',fg='white').place(x=350,y=360)
            error1 = False
        if not error1:
            if (len(itm_avaib) > 1) or (len(itm_avaib) == 0):
                Label(root_inv,text='                                                ',fg='white').place(x=350,y=360)
                Label(root_inv,text='Iteam Availability can only be y/n',bg='red',fg='white').place(x=350,y=360)
                error2 = True
            else:
                Label(root_inv,text='                                                           ').place(x=350,y=360)
                error2 = False
        l = ["1","2","3","4","5","6","7","8","9","0"]
        int_count = 0
        int_stock = 0
        if (not error1) and (not error2):
            if itm_stock != '':
                for i in itm_stock:
                    if itm_stock == '':
                        break
                    elif i in l:
                        int_count += 1
                    else:
                        break
                if len(itm_stock) == int_count:
                    error3 = False
                else:
                    Label(root_inv,text='Stock and Cost numbers only',bg='red',fg='white').place(x=350,y=360)
                    error3 = True
            else:
                itm_stock = 0
                error3 = False
        if (not error1) and (not error2):
            if itm_cost != '':
                for i in itm_cost:
                    if itm_cost == '':
                        break
                    elif i in l:
                        int_stock += 1
                    else:
                        break
                if len(itm_cost) == int_stock:
                    error4 = False
                else:
                    Label(root_inv,text='Stock and Cost numbers only',bg='red',fg='white').place(x=350,y=360)
                    error4 = True
            else:
                itm_cost = 0
                error4 = False
    else:
        Label(root_inv,text='                                               ',fg='white').place(x=350,y=360)
        Label(root_inv,text='Item not found',bg='red',fg='white').place(x=350,y=360)
    if found and (not error1) and (not error2) and (not error3) and (not error4):
        query = "update inventory set name = \'"+itm_name+"\',stock = "+str(itm_stock)+",available = \'"+itm_avaib+"\',cost = "+str(itm_cost)+" where itm_id = \'"+pri_id+"\'"
        db_inv.execute(query)
        mydb.commit()
        table_inv[a] = [pri_id,itm_name,itm_stock,itm_avaib,itm_cost]
        data_inv(table_inv)
def scroll_inv(event):
    global canvas_table
    canvas_table.configure(scrollregion=canvas_table.bbox("all"),width=500,height=250)
def back_inv():
    global root_inv
    root_inv.destroy()
    mainwin()
def inventory_win():
    global root_inv,canvas_table,frame_table_inv,main
    global itm_id,name,stock,avaib,cost
    main.destroy()
    root_inv=Tk()
    root_inv.wm_geometry("%dx%d+%d+%d" % (600, 400, 450, 150))
    main_frame=Frame(root_inv,relief=GROOVE,width=150,height=100,bd=1)
    main_frame.place(x=50,y=10)
    canvas_table=Canvas(main_frame)
    frame_table_inv=Frame(canvas_table)
    myscrollbar=Scrollbar(main_frame,orient="vertical",command=canvas_table.yview)
    canvas_table.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right",fill="y")
    canvas_table.pack(side="left")
    canvas_table.create_window((0,0),window=frame_table_inv,anchor='nw')
    frame_table_inv.bind("<Configure>",scroll_inv)
    data_inv(table_inv)
    Label(root_inv,text="ID:",font="-size 10").place(x=40,y=280)
    itm_id = Entry(root_inv)
    itm_id.place(x=70,y=280)
    Label(root_inv,text="Name:",font="-size 10").place(x=210,y=280)
    name = Entry(root_inv)
    name.place(x=260,y=280)
    Label(root_inv,text="Stock:",font="-size 10").place(x=400,y=280)
    stock = Entry(root_inv)
    stock.place(x=450,y=280)
    Label(root_inv,text="Available(y/n):",font="-size 10").place(x=40,y=320)
    avaib = Entry(root_inv)
    avaib.place(x=135,y=320)
    Label(root_inv,text="Cost:",font="-size 10").place(x=280,y=320)
    cost = Entry(root_inv)
    cost.place(x=320,y=320)
    add_itm_b = Button(root_inv,text="Add Iteam",command=add_itm)
    add_itm_b.place(x=40,y=360)
    remove_itm_b = Button(root_inv,text="Remove Iteam",command=remove_itm)
    remove_itm_b.place(x=115,y=360)
    update_itm_b = Button(root_inv,text="Update Iteam",command=update_itm)
    update_itm_b.place(x=210,y=360)
    clear_b = Button(root_inv,text="Clear",command=clear_inv_entry)
    clear_b.place(x=300,y=360)
    back_inv_b = Button(root_inv,text="Back",command=back_inv)
    back_inv_b.place(x=550,y=360)
    root_inv.mainloop()

#search
db_ser = mydb.cursor()
db_ser.execute("select * from inventory")
table_ser = []
record_ser = []
for i in db_ser:
    for j in i:
        record_ser.append(j)
    table_ser.append(record_ser)
    record_ser = []
def clear():
    global frame_table_ser,table_ser
    a = len(table_ser)+1
    for i in range(a):
        for j in range(11):
            Label(frame_table_ser,text="       ",font="-size 10").grid(row=i,column=j)
def data_ser(table_ser):
    clear()
    global frame_table_ser
    a = len(table_ser)
    r = 1
    c = 0
    c1 = 0
    l = ["Iteam No.","Name","Stock","Available","Cost"]
    for i in l:
        Label(frame_table_ser,text=" | ",font="-size 10").grid(row=0,column=c)
        c += 1
        Label(frame_table_ser,text=i,font="-size 10",bg='blue',fg='white').grid(row=0,column=c)
        c += 1
    Label(frame_table_ser,text=" | ",font="-size 10").grid(row=0,column=c)
    c = 1
    for i in table_ser:
        for j in i:
            Label(frame_table_ser,text=j,font="-size 10").grid(row=r,column=c)
            Label(frame_table_ser,text="|",font="-size 10").grid(row=r,column=c1)
            c += 2
            c1 += 2
        Label(frame_table_ser,text="|",font="-size 10").grid(row=r,column=c1)
        c = 1
        c1 = 0
        r += 1
def check_ser():
    global table_ser,frame_table_ser,itm_id,availabe_ser,canvas_table
    itm_id_entry = itm_id.get()
    avaib = availabe_ser.get()
    new_table_ser = []
    if (itm_id_entry == "") and (avaib == ""):
        data_ser(table_ser)
    else:
        if itm_id_entry == "":
            for i in table_ser:
                if i[3]=='y':
                    new_table_ser.append(i)
            data_ser(new_table_ser)
        else:
            for i in table_ser:
                if i[0] == itm_id_entry:
                    new_table_ser.append(i)
            data_ser(new_table_ser)
def scroll_ser(event):
    global canvas_table
    canvas_table.configure(scrollregion=canvas_table.bbox("all"),width=500,height=250)
def back_ser():
    global root_ser
    root_ser.destroy()
    mainwin()
def search_win():
    global root_ser,canvas_table,frame_table_ser,table_ser,itm_id,availabe_ser,main
    main.destroy()
    root_ser=Tk()
    root_ser.wm_geometry("%dx%d+%d+%d" % (600, 400, 450, 150))
    main_frame=Frame(root_ser,relief=GROOVE,width=150,height=100,bd=1)
    main_frame.place(x=50,y=10)
    canvas_table=Canvas(main_frame)
    frame_table_ser=Frame(canvas_table)
    myscrollbar=Scrollbar(main_frame,orient="vertical",command=canvas_table.yview)
    canvas_table.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right",fill="y")
    canvas_table.pack(side="left")
    canvas_table.create_window((0,0),window=frame_table_ser,anchor='nw')
    frame_table_ser.bind("<Configure>",scroll_ser)
    data_ser(table_ser)
    back_ser_b = Button(root_ser,text="Back",command=back_ser)
    back_ser_b.place(x=550,y=350)
    Label(root_ser,text="ID :").place(x=50,y=300)
    itm_id = Entry(root_ser)
    itm_id.place(x=100,y=300)
    Label(root_ser,text="Availabe(y/n) :").place(x=260,y=300)
    availabe_ser = Entry(root_ser)
    availabe_ser.place(x=350,y=300)
    ser_b = Button(root_ser,text="Search",command=check_ser)
    ser_b.place(x=500,y=295)
    root_ser.mainloop()

#user
db_user = mydb.cursor()
db_user.execute("select * from user")
table_user = []
record_user = []
for i in db_user:
    for j in i:
        record_user.append(j)
    table_user.append(record_user)
    record_user = []
def clear_inv_user():
    global frame_table_user,table_inv
    a = len(table_user)+1
    for i in range(a):
        for j in range(11):
            Label(frame_table_user,text="      ",font="-size 10").grid(row=i,column=j)
def data_user(table_user):
    global frame_table_user
    clear_inv_user()
    r = 1
    c = 0
    c1 = 0
    l = ["Username","Password","Admin"]
    for i in l:
        Label(frame_table_user,text=" | ",font="-size 10").grid(row=0,column=c)
        c += 1
        Label(frame_table_user,text=i,font="-size 10",bg='blue',fg='white').grid(row=0,column=c)
        c += 1
    Label(frame_table_user,text=" | ",font="-size 10").grid(row=0,column=c)
    c = 1
    for i in table_user:
        for j in i:
            Label(frame_table_user,text=j,font="-size 10").grid(row=r,column=c)
            Label(frame_table_user,text="|",font="-size 10").grid(row=r,column=c1)
            c += 2
            c1 += 2
        Label(frame_table_user,text="|",font="-size 10").grid(row=r,column=c1)
        c = 1
        c1 = 0
        r += 1
    a = len(table_user)+1
    for i in range(11):
        for j in range(a,a+10):
            Label(frame_table_user,text="",font="-size 10").grid(row=j,column=i)
def add_user():
    global username_entry,password_entry,admin_entry
    global table_user,root_user
    username = username_entry.get()
    password = password_entry.get()
    admin = admin_entry.get()
    error1 = False
    error2 = False
    error3 = False
    if username != '':
        for i in table_user:
            if i[0] == username:
                Label(root_user,text='                                     ',fg='white').place(x=350,y=360)
                Label(root_user,text='Username unavailable',bg='red',fg='white').place(x=350,y=360)
                error1 = True
                break
            else:
                Label(root_user,text='                                       ',fg='white').place(x=350,y=360)
                error1 = False
    else:
        Label(root_user,text='                                       ',fg='white').place(x=350,y=360)
        Label(root_user,text='Username cannot be blank',bg='red',fg='white').place(x=350,y=360)
        error1 = True
    if not error1:
        if password == '':
            Label(root_user,text='                                       ',fg='white').place(x=350,y=360)
            Label(root_user,text='Password cannot be blank',bg='red',fg='white').place(x=350,y=360)
            error2 = True
        else:
            Label(root_user,text='                                             ',fg='white').place(x=350,y=360)
            error2 = False
    if (not error1) and (not error2):
        if admin != '':
            if not(admin != 'y' or admin != 'n'):
                Label(root_user,text='                                         ',fg='white').place(x=350,y=360)
                Label(root_user,text='Admin sould be y or n',bg='red',fg='white').place(x=350,y=360)
                error3 = True
            else:
                Label(root_user,text='                                         ',fg='white').place(x=350,y=360)
        else:
            Label(root_user,text='                                             ',fg='white').place(x=350,y=360)
            Label(root_user,text='Admin sould be y or n',bg='red',fg='white').place(x=350,y=360)
            error3 = True
    if (not error1) and (not error2) and (not error3):
        query = "insert into user values(\'"+username+"\',\'"+password+"\',\'"+admin+"\')"
        db_user.execute(query)
        mydb.commit()
        newrecord = [username,password,admin]
        table_user.append(newrecord)
        data_user(table_user)
        Label(root_user,text='                                                ',fg='white').place(x=350,y=360)
        Label(root_user,text='User Added',bg='green',fg='white').place(x=350,y=360)
def remove_user():
    global username_entry,password_entry
    global table_user,root_user
    username = username_entry.get()
    password = password_entry.get()
    found = False
    error = False
    for i in table_user:
        if i[0] == username:
            check_pass = i[1]
            Label(root_user,text='                                              ',fg='white').place(x=350,y=360)
            found = True
            itm = table_user.index(i)
            break
        else:
            Label(root_user,text='                                              ',fg='white').place(x=350,y=360)
            Label(root_user,text='User not found',bg='red',fg='white').place(x=350,y=360)
            found = False
    if found:
        if password == check_pass:
            Label(root_user,text='                                              ',fg='white').place(x=350,y=360)
            error = False
        else:
            Label(root_user,text='                                              ',fg='white').place(x=350,y=360)
            Label(root_user,text='Enter correct password',bg='red',fg='white').place(x=350,y=360)
            error = True
    else:
        error = True
    if found and (not error):
        query = "delete from user where username = \'"+username+"\' and password = \'"+password+"\'"
        db_user.execute(query)
        mydb.commit()
        table_user.pop(itm)
        data_user(table_user)
        Label(root_user,text='                                                ',fg='white').place(x=350,y=360)
        Label(root_user,text='User removed',bg='green',fg='white').place(x=350,y=360)
def update_user():
    global username_entry,password_entry,admin_entry
    global table_user,root_user
    username = username_entry.get()
    password = password_entry.get()
    admin = admin_entry.get()
    error1 = False
    error2 = False
    found = False
    if username != '':
        for i in table_user:
            if i[0] == username:
                Label(root_user,text='                                             ',fg='white').place(x=350,y=360)
                user_indx = table_user.index(i)
                found = True
                break
            else:
                Label(root_user,text='                                             ',fg='white').place(x=350,y=360)
                Label(root_user,text='Username not found',bg='red',fg='white').place(x=350,y=360)
                found = False
    else:
        Label(root_user,text='                                                ',fg='white').place(x=350,y=360)
        Label(root_user,text='Username cant be blank',bg='red',fg='white').place(x=350,y=360)
        found = False
    if found:
        if password != '':
            Label(root_user,text='                                                ',fg='white').place(x=350,y=360)
            error1 = False
        else:
            Label(root_user,text='                                                ',fg='white').place(x=350,y=360)
            Label(root_user,text='Password cant be blank',bg='red',fg='white').place(x=350,y=360)
            error1 = True
    if found and (not error1):
        if admin != '':
            if admin == 'y' or admin == 'n':
                Label(root_user,text='                                              ',fg='white').place(x=350,y=360)
                error2 = False
            else:
                Label(root_user,text='                                              ',fg='white').place(x=350,y=360)
                Label(root_user,text='Admin sould be y or n',bg='red',fg='white').place(x=350,y=360)
                error2 = True
        else:
            Label(root_user,text='                                                ',fg='white').place(x=350,y=360)
            Label(root_user,text='Admin sould be y or n',bg='red',fg='white').place(x=350,y=360)
            error2 = True
    if found and (not error1) and (not error2):
        query = query = "update user set password = \'"+password+"\',admin = \'"+admin+"\' where username = \'"+username+"\'"
        db_user.execute(query)
        mydb.commit()
        table_user[user_indx] = [username,password,admin]
        data_user(table_user)
        Label(root_user,text='                                                ',fg='white').place(x=350,y=360)
        Label(root_user,text='User updated',bg='green',fg='white').place(x=350,y=360)
def scroll_user(event):
    global canvas_table
    canvas_table.configure(scrollregion=canvas_table.bbox("all"),width=500,height=240)
def back_user():
    global root_user
    root_user.destroy()
    mainwin()
def user_win():
    global root_user,canvas_table,frame_table_user,main
    global username_entry,password_entry,admin_entry
    main.destroy()
    root_user=Tk()
    root_user.wm_geometry("%dx%d+%d+%d" % (600, 400, 450, 150))
    main_frame=Frame(root_user,relief=GROOVE,width=150,height=100,bd=1)
    main_frame.place(x=50,y=10)
    canvas_table=Canvas(main_frame)
    frame_table_user=Frame(canvas_table)
    myscrollbar=Scrollbar(main_frame,orient="vertical",command=canvas_table.yview)
    canvas_table.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right",fill="y")
    canvas_table.pack(side="left")
    canvas_table.create_window((0,0),window=frame_table_user,anchor='nw')
    frame_table_user.bind("<Configure>",scroll_user)
    data_user(table_user)
    Label(root_user,text="Username :",font="-size 10").place(x=40,y=280)
    username_entry = Entry(root_user)
    username_entry.place(x=120,y=280)
    Label(root_user,text="Password :",font="-size 10").place(x=260,y=280)
    password_entry = Entry(root_user)
    password_entry.place(x=340,y=280)
    Label(root_user,text="Admin(y/n) :",font="-size 10").place(x=40,y=320)
    admin_entry = Entry(root_user)
    admin_entry.place(x=120,y=320)
    add_user_b = Button(root_user,text="Add User",command=add_user)
    add_user_b.place(x=40,y=360)
    remove_user_b = Button(root_user,text="Remove User",command=remove_user)
    remove_user_b.place(x=115,y=360)
    update_user_b = Button(root_user,text="Update User",command=update_user)
    update_user_b.place(x=210,y=360)
    back_user_b = Button(root_user,text="Back",command=back_user)
    back_user_b.place(x=550,y=350)
    root_user.mainloop()

#main
def mainwin():
    global username,if_admin,main
    main = Tk()
    main.geometry("250x230+690+270")
    main.minsize(200,150)
    exit_y = 170
    if if_admin:
        main.title("Main - " + username + "(admin)")
        user_b = Button(main, text='User', command=user_win)
        user_b.place(x=105,y=130)
    else:
        main.title("Main - " + username)
        exit_y = 130
    Label(main,text="Main Menu",font="-size 20").pack()
    inventory_b = Button(main, text='Inventory', command=inventory_win)
    inventory_b.place(x=95,y=50)
    search_b = Button(main, text='Search', command=search_win)
    search_b.place(x=100,y=90)
    exit_b = Button(main, text='Exit', command=quit)
    exit_b.place(x=107,y=exit_y)
    main.mainloop()
if run == 1:
    mainwin()