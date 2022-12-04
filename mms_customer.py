from tkinter import *
from tkinter import ttk
from random import randint
import pymysql
from ims_bill import Bill_App

class Customer:
    def __init__(self,root):
        self.root=root
        self.root.title("Meta Management System")
        self.root.geometry("1350x700+0+0")

        title=Label(self.root,bd=10,relief=GROOVE,text="Meta Management System",font=("monospace",40,"bold"),bg="yellow",fg="red")
        title.pack(side=TOP,fill=X)

        #===========All Variables==============

        self.customer_id=StringVar()
        self.customer_name = StringVar()
        self.customer_contact=StringVar()
        self.customer_address=StringVar()

        self.search_by=StringVar()
        self.search_txt=StringVar()

        #=========Creating Menus for project=======================

        main_menu=Menu(self.root)
        self.root.config(menu=main_menu)

        fileMenu=Menu(main_menu)
        main_menu.add_cascade(label="File",menu=fileMenu)
        fileMenu.add_command(label="Bill Section", command=self.openBill)
        fileMenu.add_command(label="Stock Section", command=self.openStock)
        fileMenu.add_command(label="Daily Expenses", command=self.openDE)
        fileMenu.add_command(label="Orders", command=self.openOrders)
        fileMenu.add_command(label="Raw Materials",command=self.RawMaterial)
        fileMenu.add_command(label="Employees",command=self.openEmployee)
        fileMenu.add_command(label="Payouts",command=self.openPayouts)
        fileMenu.add_command(label="Exit", command=exit)

        #==========Menu ends here===================================

        #============Stock Entry Frame===============>

        Manage_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="crimson")
        Manage_Frame.place(x=20,y=100,width=450,height=580)

        m_title=Label(Manage_Frame, text="Manage Customers",bg="crimson",fg="white", font=("monospace",30,"bold"))
        m_title.grid(row=0,columnspan=2,pady=20)

        lbl_customer_name=Label(Manage_Frame, text="Customer Name:",bg="crimson",fg="white", font=("monospace",20,"bold"))
        lbl_customer_name.grid(row=1,column=0,pady=10,padx=20,sticky="w")

        txt_customer_name=Entry(Manage_Frame,textvariable=self.customer_name,font=("monospace",10,"bold"),bd=5,relief=GROOVE)
        txt_customer_name.grid(row=1,column=1,pady=10,padx=8,sticky="w")

        lbl_customer_contact=Label(Manage_Frame, text="Customer Contact:",bg="crimson",fg="white", font=("monospace",20,"bold"))
        lbl_customer_contact.grid(row=2,column=0,pady=10,padx=20,sticky="w")

        txt_customer_contact=Entry(Manage_Frame,textvariable=self.customer_contact,font=("monospace",10,"bold"),bd=5,relief=GROOVE)
        txt_customer_contact.grid(row=2,column=1,pady=10,padx=8,sticky="w")

        lbl_customer_address=Label(Manage_Frame, text="Customer Address:",bg="crimson",fg="white", font=("monospace",20,"bold"))
        lbl_customer_address.grid(row=3,column=0,pady=10,padx=20,sticky="w")

        txt_customer_address=Entry(Manage_Frame,textvariable=self.customer_address,font=("monospace",10,"bold"),bd=5,relief=GROOVE)
        txt_customer_address.grid(row=3,column=1,pady=10,padx=8,sticky="w")


        #===========Button Frame=============
        btn_Frame=Frame(Manage_Frame,bd=4,relief=RIDGE,bg="crimson")
        btn_Frame.place(x=8,y=400,width=430)

        Addbtn=Button(btn_Frame,command=self.add_customer,text="Add",width=5).grid(row=0,column=0,padx=8,pady=10)
        updatebtn=Button(btn_Frame,command=self.update_data,text="Update",width=5).grid(row=0,column=1,padx=8,pady=10)
        deletebtn=Button(btn_Frame,command=self.delete_data,text="Delete",width=5).grid(row=0,column=2,padx=8,pady=10)
        # Ordersbtn=Button(btn_Frame,command=self.clear,text="Orders",width=5).grid(row=0,column=3,padx=8,pady=10)



        #===========Detail Frame=====================

        Detail_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="crimson")
        Detail_Frame.place(x=500,y=100,width=830,height=580)

        lbl_Search=Label(Detail_Frame,text="Search By",bg="crimson",fg="white",font=("monospace",20,"bold"))
        lbl_Search.grid(row=0,column=0,pady=10,padx=20,sticky="w")

        combo_search=ttk.Combobox(Detail_Frame,textvariable=self.search_by,width=10 ,font=("monospace",13,"bold"),state="readonly")
        combo_search['values']=("Name","Contact")
        combo_search.grid(row=0,column=1, padx=20,pady=10)

        txt_Search=Entry(Detail_Frame,textvariable=self.search_txt,width=20,font=("monospace",10,"bold"),bd=5,relief=GROOVE)
        txt_Search.grid(row=0,column=2,pady=10,padx=20,sticky="w")

        searchbtn=Button(Detail_Frame,command=self.search_data,text="Search",width=10,pady=5).grid(row=0,column=3,padx=10,pady=10)
        showallbtn=Button(Detail_Frame,command=self.fetch_date,text="Show All",width=10,pady=5).grid(row=0,column=4,padx=10,pady=10)

        #=============Table Frame===========

        Table_Frame=Frame(Detail_Frame,bd=4,relief=RIDGE,bg="crimson")
        Table_Frame.place(x=10,y=70,width=795,height=490)

        scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
        self.Customer_Table=ttk.Treeview(Table_Frame, column=("id","customer_name","customer_contact","customer_address"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Customer_Table.xview)
        scroll_y.config(command=self.Customer_Table.yview)

        self.Customer_Table.heading("id",text="Customer ID")
        self.Customer_Table.heading("customer_name",text="Customer Name")
        self.Customer_Table.heading("customer_contact",text="Customer Contact")
        self.Customer_Table.heading("customer_address",text="Customer Address")
        self.Customer_Table['show']='headings'
        self.Customer_Table.column("id",width=100)
        self.Customer_Table.column("customer_name",width=100)
        self.Customer_Table.column("customer_contact",width=100)
        self.Customer_Table.column("customer_address",width=360)
        self.Customer_Table.pack(fill=BOTH,expand=1)
        self.fetch_date()
        self.Customer_Table.bind("<ButtonRelease-1>",self.get_cursor)

    def add_customer(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        statement=f"insert into registered_customers (customer_name, customer_contact, customer_address) values ('{self.customer_name.get()}','{self.customer_contact.get()}','{self.customer_address.get()}')"
        cur.execute(statement)
        con.commit()
        self.fetch_date()
        self.clear()
        con.close()

    def fetch_date(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        cur.execute("select * from registered_customers")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.Customer_Table.delete(*self.Customer_Table.get_children())
            for row in rows:
                print(row)
                self.Customer_Table.insert('',END, values=row)
            con.commit()
        con.close()

    def clear(self):
        self.customer_name.set("")
        self.customer_contact.set("")
        self.customer_address.set("")

    def get_cursor(self,ev):
        cursor_row=self.Customer_Table.focus()
        contents=self.Customer_Table.item(cursor_row)
        row=contents['values']
        self.customer_id.set(row[0])
        self.customer_name.set(row[1])
        self.customer_contact.set(row[2])
        self.customer_address.set(row[3])

    def update_data(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        statement=f"update registered_customers set customer_name='{self.customer_name.get()}', customer_contact={self.customer_contact.get()}, customer_address='{self.customer_address.get()}' where id={self.customer_id.get()}"
        print(statement)
        cur.execute(statement)
        con.commit()
        self.fetch_date()
        self.clear()
        con.close()

    def delete_data(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        cur.execute(f"delete from registered_customers where id='{self.customer_id.get()}'")
        con.commit()
        con.close()
        self.fetch_date()
        self.clear()

    def search_data(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        if f'{self.search_by.get()}'=='Name':
            statement=f"select * from registered_customers where customer_name='{self.search_txt.get()}'"
        else:
            statement=f"select * from registered_customers where customer_contact='{self.search_txt.get()}'"
        cur.execute(statement)
        self.Customer_Table.delete(*self.Customer_Table.get_children())
        rows=cur.fetchall()
        if len(rows)!=0:
            self.Customer_Table.delete(*self.Customer_Table.get_children())
            for row in rows:
                self.Customer_Table.insert('',END, values=row)
            con.commit()
        con.close()

    def openBill(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Bill_App(self.root)

    def openStock(self):
        from ims_stock import Stock
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Stock(self.root)

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

    def openEmployee(self):
        from employee import Employee
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Employee(self.root)

    def openPayouts(self):
        from payouts import Payout
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Payout(self.root)
