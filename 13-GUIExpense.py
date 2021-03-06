#GUIExpense.py

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#########CSV##########
import csv

#Comma-separated values: CSV

def WritetoCSV(ep):
    with open('allexpense.csv','a',newline='',encoding='utf-8') as file:
        # 'a' = append (เพิ่มได้เรื่อยๆ) , 'w' = replace (ทับไฟล์เดิม)
        fw = csv.writer(file) # fw คือ file writer
        # ep = ['ไก่',300]
        fw.writerow(ep)

    #print('บันทึกรายการ...')

def ReadCSV():
    with open('allexpense.csv',newline='',encoding='utf-8') as file:
        #fr = file reader
        fr = csv.reader(file)
        #print(list(fr))
        data = list(fr)
    return data

########MAIN GUI########

GUI = Tk()
GUI.title('Income & Expense : โปรแรมบัญชี รายรับ-รายจ่าย')
width = 1024
height = 768
screen_width = GUI.winfo_screenwidth()
screen_height = GUI.winfo_screenheight()
x = (screen_width/1) - (width/1)
y = (screen_height/1) - (height/1)
GUI.geometry("%dx%d+%d+%d" % (width, height, x, y))
GUI.resizable(1, 1)
GUI.state('zoomed')
####################################################################

try:
    GUI.iconbitmap('wallet.ico')
except:
    pass

menubar = Menu(GUI)
GUI.config(menu=menubar)

filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Exit - (F4)',command=GUI.quit)
#command= lambda: GUI.destroy()
GUI.bind('<F4>',lambda x: GUI.destroy())

## helpmenu
import webbrowser

def About():
    url = 'https://www.uncle-engineer.com'
    webbrowser.open(url)

from tkinter import messagebox as msb

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About', command=About)
helpmenu.add_command(label='Donate',command=lambda: msb.showinfo('Donate','เลขบัญชี: 700 258 444\nธนาคารกรุงไทย'))
#command=lambda: msb.showinfo('Donate','เลขบัญชี: 700 258 444\nธนาคารกรุงไทย')


from tkinter.ttk import Notebook

Tab = Notebook(GUI)
Tab.pack(fill=BOTH, expand=1)

T1 = Frame(Tab)
T2 = Frame(Tab)
T3 = Frame(Tab)

icon_expense = PhotoImage(file='cart.png')
icon_income = PhotoImage(file='money.png')
icon_dashboard = PhotoImage(file='dashboard.png')

Tab.add(T1,text='รายจ่าย',image=icon_expense,compound='top')
Tab.add(T2,text='รายรับ',image=icon_income,compound='top')
Tab.add(T3,text='สรุปผล',image=icon_dashboard,compound='top')


####################Expense######################

FONT1 = ('Tahoma',15)
FONT2 = ('Tahoma',15,'bold')

#-------------Lable/Button/Style----------------------------------------------------------

Font = ('Tahoma',10)
TKFont = ttk.Style()
TKFont.configure('TButton', font=('Tahoma', 10))
ttk.Style().configure("TButton",relief="GROOVE",background="white")
TKFont.configure('TButton', foreground='#000000',background="white")

# v_expense ใช้สำหรับเก็บค่าที่ user พิมพ์
v_expense = StringVar()

# E1 คือช่องกรอกข้อมูล
lbtitle = ttk.Label(T1,text='โปรแรมบัญชี รายรับ-รายจ่าย', font=('Tahoma',15))
lbtitle.pack(side=TOP, padx=5,pady=5)


L = ttk.Label(T1,text='กรุณากรอกรายจ่าย', font=('Tahoma',10))
L.pack(padx=5,pady=5) #หัวข้อบนช่องกรอก
E1 = ttk.Entry(T1,textvariable=v_expense, font=('Tahoma',10), width=20)
E1.pack(padx=5,pady=5)

# v_expense ใช้สำหรับเก็บค่าที่ user พิมพ์
v_price = StringVar()

# E1 คือช่องกรอกข้อมูล
L = ttk.Label(T1,text='ค่าใช้จ่าย (บาท)', font=('Tahoma',10))
L.pack(padx=5,pady=5) #หัวข้อบนช่องกรอก
E2 = ttk.Entry(T1,textvariable=v_price, font=('Tahoma',10), width=20)
E2.pack(padx=5,pady=5)


# SaveExpense คือฟังชั่นเมื่อมีการกดปุ่ม ฟังชั่นนี้จะทำงาน
from datetime import datetime #เวลา

def SaveExpense(event=None):
    if len(v_expense.get() and v_price.get()) == 0:
        messagebox.showinfo("Message", "กรอกข้อมูลของคุณ")
    else:
        exp = v_expense.get()
        pc = float(v_price.get()) # แปลงข้อความเป็นจุดทศนิยม
        # ข้อความเป็นตัวเลขใช้ int() , ข้อความเป็นจุดทศนิยม float() , ตัวเลขหรือจุดทุศนิยมเป็นข้อความ str()
        #print('รายการ: ',exp) # v_expense.get() คือการดึงค่ามาใช้งาน
        #v_result.set('คุณกำลังบันทึกรายการ: ' + exp + ' ราคา: '+ v_price.get() +' บาท')

        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        update_statusbar.set(f'บันทึกรายการ : {exp} ราคา : {pc:,.2f} บาท ... ')

        data = [dt,exp,"%.2f" % pc] #จัดเรียงข้อมูลก่อนเซฟลง csv # ทศนิยม 2 ตำแกน่ง
        WritetoCSV(data) #เรียกฟังชั่นการบันทึกข้อมูล

        #reset ตัวแปร
        v_expense.set('')
        v_price.set('')
        #ทำให้ cursor วิ่งไปหาช่องกรอกตัวแรก
        E1.focus()
        update_table() #อัพเดตตารางทุกครั้งที่มีการเพิ่มรายการใหม่
        CountExpense()
        print('บันทึกรายการ...',dt,exp,"%.2f" % pc)
    

E2.bind('<Return>',SaveExpense) #หากใช้ bind ต้องใส่ event=None ในฟังชั่นด้วย

# B1 คือปุ่มสำหรับกดบันทึก
B1 = ttk.Button(T1,text='บันทึก',command=SaveExpense)
B1.pack(padx=5,pady=5)

#########TABLE###########

F2 = Frame(T1)# F1 คือ เฟรม (white board ติดผนัง)
F2.pack(padx=5,pady=5)

# TAB 2 Treeview Style -----------------------------------------------------------------------------------------
style = ttk.Style()
style.configure("Treeview.Heading", font=('Tahoma', 10,'bold'),foreground="blue" , background = 'yellow')
style.configure("Treeview", font=('Tahoma', 10),rowheight=20)
style.layout("Treeview", [('mystyle.Treeview.treearea', {'sticky': 'news'})]) # Remove the borders


v_allexpense = StringVar()

header = ['วัน-เวลา','รายการ','จำนวนเงิน']

table_expense = ttk.Treeview(F2,column=header,show='headings',height=10)
table_expense.grid(row=0,column=0,ipadx=0,ipady=0,padx=0,pady=0)

table_expense.heading('วัน-เวลา',text='วัน-เวลา')
table_expense.heading('รายการ',text='รายการ')
table_expense.heading('จำนวนเงิน',text='จำนวนเงิน')

vsb = ttk.Scrollbar(F2, orient="vertica", command=table_expense.yview)
vsb.place(x=585, y=0, height=225)
table_expense.configure(yscrollcommand=vsb.set)


F3 = Frame(T1)# F1 คือ เฟรม (white board ติดผนัง)
F3.pack(padx=5,pady=5)


def CountExpense():
    with open('allexpense.csv',newline='',encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            pass
        #print(csv_reader.line_num)
        count = csv_reader.line_num
        v_countexpense.set(f'รายการทั้งหมด : {count} รายการ')

v_countexpense = StringVar()
L2 = ttk.Label(F3,textvariable=v_countexpense,font=('Tahoma',15))
L2.grid(row=0,column=0,ipadx=5,ipady=5,padx=5)


LR1 = ttk.Label(F3,textvariable=v_allexpense,font=('Tahoma',15))
LR1.grid(row=1,column=0,ipadx=5,ipady=5,padx=5)

dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

update_statusbar = StringVar()
update_statusbar.set(f'วันที่ : {dt}') #('Status : Ready')
statusbar = Label(T1, textvariable=update_statusbar, bd=1, relief=SUNKEN, anchor='w',font=('Tahoma',8))
statusbar.pack(side=BOTTOM, fill=X,padx=0,pady=0)

def sum_table():
    allsum = []
    data = ReadCSV()
    for dt in data:
        #dt = [2020-06-27 17:00:03,ข้าว,20.0]
        allsum.append(float(dt[2]))
    v_allexpense.set('รวมรายจ่ายทั้งหมด (บาท) : {:,.2f} บาท'.format(sum(allsum)))


def update_table():
    data = ReadCSV()
    #print(data)
    table_expense.delete(*table_expense.get_children()) 
    #clear ข้อมูลทั้งหมดในตาราง ก่อนการ insert
    for dt in data:
        table_expense.insert('','end',value=dt)
    sum_table()

##Tab3######################################################################

F1T3 = Frame(T3)# F1 คือ เฟรม (white board ติดผนัง)
F1T3.pack(padx=5,pady=5)

LR1 = ttk.Label(F1T3,textvariable=v_allexpense,font=('Tahoma',15))
LR1.grid(row=0,column=1,padx=5,pady=5)

# try / except 
try:
    update_table()
    CountExpense()
except:
    print('ERROR')
GUI.mainloop() # ทำให้โปรแกรมรันได้ตลอดเวลา