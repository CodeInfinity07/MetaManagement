from tkinter import *
from tkinter import ttk
from random import randint
import pymysql
from ims_bill import Bill_App
from datetime import datetime


class Employee:
    def __init__(self,root):
        self.root=root
        self.root.title("Meta Management System")
        self.root.geometry("1350x700+0+0")

        title=Label(self.root,bd=10,relief=GROOVE,text="Meta Management System",font=("monospace",40,"bold"),bg="yellow",fg="red")
        title.pack(side=TOP,fill=X)

        #===========All Variables==============


        self.employee_id = IntVar()
        self.name=StringVar()
        self.contact=IntVar()

        self.search_by=StringVar()
        self.search_txt=StringVar()

        #=========Creating Menus for project=======================

        main_menu=Menu(self.root)
        self.root.config(menu=main_menu)

        fileMenu=Menu(main_menu)
        main_menu.add_cascade(label="File",menu=fileMenu)
        fileMenu.add_command(label="Bill Section", command=self.openBill)
        fileMenu.add_command(label="Customer Section", command=self.openCustomerDetails)
        fileMenu.add_command(label="Stock Section", command=self.openStock)
        fileMenu.add_command(label="Daily Expenses", command=self.openDE)
        fileMenu.add_command(label="Orders", command=self.openOrders)
        fileMenu.add_command(label="Raw Materials",command=self.RawMaterial)
        fileMenu.add_command(label="Payouts",command=self.openPayouts)
        fileMenu.add_command(label="Exit", command=exit)

        #==========Menu ends here===================================

        #============Stock Entry Frame===============>

        Manage_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="crimson")
        Manage_Frame.place(x=20,y=100,width=450,height=580)

        m_title=Label(Manage_Frame, text="Manage Employees",bg="crimson",fg="white", font=("monospace",30,"bold"))
        m_title.grid(row=0,columnspan=2,pady=20)

        lbl_item_color=Label(Manage_Frame, text="Employee Name:",bg="crimson",fg="white", font=("monospace",20,"bold"))
        lbl_item_color.grid(row=1,column=0,pady=10,padx=20,sticky="w")

        txt_item_color=Entry(Manage_Frame,textvariable=self.name,font=("monospace",10,"bold"),bd=5,relief=GROOVE)
        txt_item_color.grid(row=1,column=1,pady=10,padx=8,sticky="w")

        lbl_item_name=Label(Manage_Frame, text="Employee Contact:",bg="crimson",fg="white", font=("monospace",20,"bold"))
        lbl_item_name.grid(row=2,column=0,pady=10,padx=20,sticky="w")

        txt_item_name=Entry(Manage_Frame,textvariable=self.contact,font=("monospace",10,"bold"),bd=5,relief=GROOVE)
        txt_item_name.grid(row=2,column=1,pady=10,padx=8,sticky="w")
        

        #===========Button Frame=============
        btn_Frame=Frame(Manage_Frame,bd=4,relief=RIDGE,bg="crimson")
        btn_Frame.place(x=8,y=400,width=430)

        Addbtn=Button(btn_Frame,command=self.add_employee,text="Add",width=5).grid(row=0,column=0,padx=8,pady=10)
        updatebtn=Button(btn_Frame,command=self.update_data,text="Update",width=5).grid(row=0,column=1,padx=8,pady=10)
        deletebtn=Button(btn_Frame,command=self.delete_data,text="Delete",width=5).grid(row=0,column=2,padx=8,pady=10)
        Clearbtn=Button(btn_Frame,command=self.clear,text="Clear",width=5).grid(row=0,column=3,padx=8,pady=10)



        # #===========Detail Frame=====================

        Detail_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="crimson")
        Detail_Frame.place(x=500,y=100,width=830,height=580)

        # lbl_Search=Label(Detail_Frame,text="Search By",bg="crimson",fg="white",font=("monospace",20,"bold"))
        # lbl_Search.grid(row=0,column=0,pady=10,padx=20,sticky="w")

        # combo_search=ttk.Combobox(Detail_Frame,textvariable=self.search_by,width=10 ,font=("monospace",13,"bold"),state="readonly")
        # combo_search['values']=("Item No","Item Name")
        # combo_search.grid(row=0,column=1, padx=20,pady=10)

        # txt_Search=Entry(Detail_Frame,textvariable=self.search_txt,width=20,font=("monospace",10,"bold"),bd=5,relief=GROOVE)
        # txt_Search.grid(row=0,column=2,pady=10,padx=20,sticky="w")

        # searchbtn=Button(Detail_Frame,command=self.search_data,text="Search",width=10,pady=5).grid(row=0,column=3,padx=10,pady=10)
        # showallbtn=Button(Detail_Frame,command=self.fetch_date,text="Show All",width=10,pady=5).grid(row=0,column=4,padx=10,pady=10)

        #=============Table Frame===========

        Table_Frame=Frame(Detail_Frame,bd=4,relief=RIDGE,bg="crimson")
        Table_Frame.place(x=10,y=70,width=795,height=490)

        scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
        self.Stock_Table=ttk.Treeview(Table_Frame, column=("id","name","contact_no","date"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Stock_Table.xview)
        scroll_y.config(command=self.Stock_Table.yview)

        self.Stock_Table.heading("id",text="ID") 
        self.Stock_Table.heading("name",text="Name")
        self.Stock_Table.heading("contact_no",text="Contact")
        self.Stock_Table.heading("date",text="Date Joined")
        self.Stock_Table['show']='headings'
        self.Stock_Table.column("id",width=50)
        self.Stock_Table.column("name",width=100)
        self.Stock_Table.column("contact_no",width=100)
        self.Stock_Table.column("date",width=100)
        self.Stock_Table.pack(fill=BOTH,expand=1)
        self.fetch_date()
        self.Stock_Table.bind("<ButtonRelease-1>",self.get_cursor)

    def add_employee(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        statement=f"insert into employee (name,contact_no,date) values ('{self.name.get()}',{self.contact.get()},'{datetime.today().strftime('%Y-%m-%d')}')"
        cur.execute(statement)
        con.commit()
        self.fetch_date()
        self.clear()
        con.close()

    def fetch_date(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        cur.execute("select * from employee")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.Stock_Table.delete(*self.Stock_Table.get_children())
            for row in rows:
                self.Stock_Table.insert('',END, values=row)
            con.commit()
        con.close()

    def clear(self):
        self.employee_id.set(0)
        self.name.set("")
        self.contact.set(0)

    def get_cursor(self,ev):
        cursor_row=self.Stock_Table.focus()
        contents=self.Stock_Table.item(cursor_row)
        row=contents['values']
        self.employee_id.set(row[0])
        self.name.set(row[1])
        self.contact.set(row[2])

    def update_data(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        statement=f"update employee set name='{self.name.get()}', contact_no={self.contact.get()} where id={self.employee_id.get()}"
        cur.execute(statement)
        con.commit()
        self.fetch_date()
        self.clear()
        con.close()

    def delete_data(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        cur.execute(f"delete from employee where id='{self.employee_id.get()}'")
        con.commit()
        con.close()
        self.fetch_date()
        self.clear()

    # def search_data(self):
    #     con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
    #     cur=con.cursor()
    #     if f'{self.search_by.get()}'=='Item No':
    #         statement=f"select * from stocks where item_no='{self.search_txt.get()}'"
    #     else:
    #         statement=f"select * from stocks where name='{self.search_txt.get()}'"
    #     cur.execute(statement)
    #     self.Stock_Table.delete(*self.Stock_Table.get_children())
    #     rows=cur.fetchall()
    #     if len(rows)!=0:
    #         self.Stock_Table.delete(*self.Stock_Table.get_children())
    #         for row in rows:
    #             self.Stock_Table.insert('',END, values=row)
    #         con.commit()
    #     con.close()

    def openStock(self):
        from ims_stock import Stock
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Stock(self.root)

    def openBill(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Bill_App(self.root)

    def openCustomerDetails(self):
        from mms_customer import Customer
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Customer(self.root)

    def openDE(self):
        from mms_daily import Daily
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Daily(self.root)

    def openOrders(self):
        from mms_orders import Order
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Order(self.root)

    def RawMaterial(self):
        from mms_raw_materials import Raw
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Raw(self.root)

    def openPayouts(self):
        from payouts import Payout
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Payout(self.root)
    
