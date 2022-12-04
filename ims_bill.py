from tkinter import *
from tkinter import messagebox,ttk
import math,random
import pymysql
from datetime import datetime

class Bill_App:
    def __init__(self,root):
        global F3
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Billing Software")
        bg_color="#074463"
        title=Label(self.root,bd=12,relief=GROOVE,bg=bg_color,fg="white",text="Billing Software",font=("monospace",30,"bold"),pady=2).pack(fill=X)

        #=============Variables==================#
        #=========Search Field=============#
        self.search_item_no=StringVar()
        self.search_item_no.set("")

        #========Item Details============#
        self.item_no=StringVar()
        self.item_name=StringVar()
        self.item_price=IntVar()
        self.item_quantity=IntVar()
        self.item_quantity.set(1)
        self.item_color = StringVar()
        self.item_guage = StringVar()
        my_colors = []
        #===========Customer===========#
        self.c_id = StringVar()
        self.c_name=StringVar()
        self.c_phon=StringVar()
        self.bill_no=StringVar()
        self.color_options = StringVar()
        self.search_bill=StringVar()
        self.bill_type = StringVar()
        self.bill_type.set(0)
        self.c_name.set("")
        self.c_phon.set("")
        self.bill_book = IntVar()
        self.bill_book.set(1)
        self.bill_no.set(1)
        self.color_options.set("Select Color: ")

        #=========Creating Menus for project=======================

        main_menu=Menu(self.root)
        self.root.config(menu=main_menu)

        fileMenu=Menu(main_menu)
        main_menu.add_cascade(label="File",menu=fileMenu)
        fileMenu.add_command(label="Stock Section", command=self.openStock)
        fileMenu.add_command(label="Customer Section", command=self.openCustomerDetails)
        fileMenu.add_command(label="Daily Expenses", command=self.openDE)
        fileMenu.add_command(label="Orders", command=self.openOrders)
        fileMenu.add_command(label="Raw Materials",command=self.RawMaterial)
        fileMenu.add_command(label="Employees",command=self.openEmployee)
        fileMenu.add_command(label="Payouts",command=self.openPayouts)
        fileMenu.add_command(label="Exit", command=exit)

        #==========Menu ends here===================================

        ##-------------Customer Detail Frame-------------##
        F1=LabelFrame(self.root,bd=10,relief=GROOVE, text="Customer Details",font=("monospace",10,"bold"),fg="gold",bg=bg_color)
        F1.place(x=0,y=80,relwidth=1)

        cname_lbl=Label(F1,bg=bg_color,fg="white",text="Customer Name",font=("monospace",18,"bold")).grid(row=0,column=0,padx=20,pady=5)
        cname_txt=Entry(F1,textvariable=self.c_name,width=20,font=("monospace",10,"bold"),bd=7,relief=SUNKEN).grid(row=0,column=1,pady=5,padx=10)

        cphn_lbl=Label(F1,bg=bg_color,fg="white",text="Phone No.",font=("monospace",18,"bold")).grid(row=0,column=2,padx=20,pady=5)
        cphn_lbl=Entry(F1,textvariable=self.c_phon,width=20,font=("monospace",10,"bold"),bd=7,relief=SUNKEN).grid(row=0,column=3,pady=5,padx=10)

        c_bill_lbl=Label(F1,bg=bg_color,fg="white",text="Bill No.",font=("monospace",18,"bold")).grid(row=0,column=4,padx=20,pady=5)
        c_bill_lbl=Entry(F1,textvariable=self.search_bill,width=20,font=("monospace",10,"bold"),bd=7,relief=SUNKEN).grid(row=0,column=5,pady=5,padx=10)

        bill_btn=Button(F1,text="Search",command=self.find_bill,width=10,bd=7,font="arial 15 bold").grid(row=0,column=6,padx=20,pady=10)

        #============Search Items===============#

        F2=LabelFrame(self.root,bd=10,relief=GROOVE, text="Search Items",font=("monospace",15,"bold"),fg="gold",bg=bg_color)
        F2.place(y=160,width=325,height=380)

        item_no_lbl=Label(F2,text="Item No.",font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=0,column=0,padx=0,pady=10,sticky="w")
        item_no_txt=Entry(F2,width=10,textvariable=self.search_item_no,font=("monospace",16,"bold"),bd=5,relief=SUNKEN).grid(row=0,column=1,padx=10,pady=10)

        #Button for search using item no.
        search_no_btn=Button(F2,command=self.search_item,bg="black",text="Search",fg="Black",pady=15,width=11,bd=5,font="arial 15 bold").grid(row=1,column=1,padx=5,pady=5)

        #============Item Details===============#

        F3=LabelFrame(self.root,bd=10,relief=GROOVE, text="Item Details",font=("monospace",15,"bold"),fg="gold",bg=bg_color)
        F3.place(x=340,y=160,width=325,height=380)

        # g1_lbl=Label(F3,text="Item No:",font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=0,column=0,padx=0,pady=10,sticky="w")
        # g1_txt=Label(F3,textvariable=self.item_no,font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=0,column=1,padx=10,pady=10,stick="w")

        g2_lbl=Label(F3,text="Item Name:",font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=0,column=0,padx=0,pady=10,sticky="w")
        g2_txt=Label(F3,textvariable=self.item_name,font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=0,column=1,padx=10,pady=10,stick="w")

        g3_lbl=Label(F3,text="Price:",font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=1,column=0,padx=0,pady=10,sticky="w")
        g3_txt=Label(F3,textvariable=self.item_price,font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=1,column=1,padx=10,pady=10,stick="w")

        g4_lbl=Label(F3,text="Color:",font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=2,column=0,padx=0,pady=10,sticky="w")

        g5_lbl=Label(F3,text="Guage:",font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=3,column=0,padx=0,pady=10,sticky="w")
        g5_txt=Label(F3,textvariable=self.item_guage,font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=3,column=1,padx=10,pady=10,stick="w")

        item_qty_lbl=Label(F3,text="Item Quantity: ",font=("monospace",16,"bold"),bg=bg_color,fg="lightgreen").grid(row=4,column=0,padx=0,pady=10,sticky="w")
        item_qty_txt=Entry(F3,width=10,textvariable=self.item_quantity,font=("monospace",16,"bold"),bd=5,relief=SUNKEN).grid(row=4,column=1,padx=10,pady=10)

        search_name_btn=Button(F3,command=self.add_item,bg="black",text="Add",fg="Black",pady=15,width=11,bd=5,font="arial 15 bold").grid(row=5,column=1,padx=5,pady=5)


        #============Shopping Cart===============#

        F4=LabelFrame(self.root,bd=10,relief=GROOVE, text="Shopping Cart",font=("monospace",15,"bold"),fg="gold",bg=bg_color)
        F4.place(x=680,y=160,width=325,height=380)

        scroll_x=Scrollbar(F4,orient=HORIZONTAL)
        scroll_y=Scrollbar(F4,orient=VERTICAL)
        self.Stock_Table=ttk.Treeview(F4, column=("item_no","item_name","qty","price","color","guage"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Stock_Table.xview)
        scroll_y.config(command=self.Stock_Table.yview)

        self.Stock_Table.heading("item_no",text="Item No")
        self.Stock_Table.heading("item_name",text="Item Name")
        self.Stock_Table.heading("qty",text="Qty")
        self.Stock_Table.heading("price",text="Price")
        self.Stock_Table.heading("color",text="Color")
        self.Stock_Table.heading("guage",text="Guage")
        self.Stock_Table['show']='headings'
        self.Stock_Table.column("item_no",width=30)
        self.Stock_Table.column("item_name",width=140)
        self.Stock_Table.column("qty",width=30)
        self.Stock_Table.column("price",width=20)
        self.Stock_Table.column("color",width=20)
        self.Stock_Table.column("guage",width=20)
        self.Stock_Table.pack(fill=BOTH,expand=1)
        self.Stock_Table.bind("<ButtonRelease-1>",self.work_on_focus)

        #=================Bill Area==================#

        F5=LabelFrame(self.root,bd=10,relief=GROOVE)
        F5.place(x=1010,y=160,width=340,height=380)
        bill_title=Label(F5,text="Bill Area",font="arial 15 bold", bd=7,relief=GROOVE).pack(fill=X)

        scrol_y=Scrollbar(F5,orient=VERTICAL)
        self.txtarea=Text(F5,yscrollcommand=scrol_y.set)

        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH,expand=1)

        #================Bottom Frame================#
        F6=LabelFrame(self.root,bd=10,relief=GROOVE,text="Registered Customers",font=("monospace",15,"bold"),bg=bg_color,fg="gold")
        F6.place(x=0,y=545,relwidth=1,height=140)

        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        cur.execute(f"select customer_name from registered_customers")
        rows=cur.fetchall()
        if len(rows) > 0:
            my_list = [r for r, in rows] 
            print(my_list)
            self.options = StringVar()
            self.options.set("")
            lbl_options=Label(F6,bg=bg_color,fg="white",text="Select Customer:",font=("monospace",15,"bold")).grid(row=0,column=0,padx=20,pady=1,sticky="w")
            self.option_field = OptionMenu(F6, self.options, *my_list, command=self.displayCustomer)
            self.option_field.grid(row=0,column=1)
            self.option_field['width'] = 20

        # m1_lbl=Label(F6,bg=bg_color,fg="white",text="Total Cosmetics Price",font=("monospace",15,"bold")).grid(row=0,column=0,padx=20,pady=1,sticky="w")
        # m1_txt=Entry(F6,width=18,font="arial 10 bold",bd=7,relief=SUNKEN).grid(row=0,column=1,padx=10,pady=1)

        # m2_lbl=Label(F6,bg=bg_color,fg="white",text="Total Grocery Price",font=("monospace",15,"bold")).grid(row=1,column=0,padx=20,pady=1,sticky="w")
        # m2_txt=Entry(F6,width=18,font="arial 10 bold",bd=7,relief=SUNKEN).grid(row=1,column=1,padx=10,pady=1)

        # m3_lbl=Label(F6,bg=bg_color,fg="white",text="Total Drinks Price",font=("monospace",15,"bold")).grid(row=2,column=0,padx=20,pady=1,sticky="w")
        # m3_txt=Entry(F6,width=18,font="arial 10 bold",bd=7,relief=SUNKEN).grid(row=2,column=1,padx=10,pady=1)

        # c1_lbl=Label(F6,bg=bg_color,fg="white",text="Cosmetics Tax",font=("monospace",15,"bold")).grid(row=0,column=2,padx=20,pady=1,sticky="w")
        # c1_txt=Entry(F6,width=18,font="arial 10 bold",bd=7,relief=SUNKEN).grid(row=0,column=3,padx=10,pady=1)

        # c2_lbl=Label(F6,bg=bg_color,fg="white",text="Grocery Tax",font=("monospace",15,"bold")).grid(row=1,column=2,padx=20,pady=1,sticky="w")
        # c2_txt=Entry(F6,width=18,font="arial 10 bold",bd=7,relief=SUNKEN).grid(row=1,column=3,padx=10,pady=1)

        # c3_lbl=Label(F6,bg=bg_color,fg="white",text="Drinks Tax",font=("monospace",15,"bold")).grid(row=2,column=2,padx=20,pady=1,sticky="w")
        # c3_txt=Entry(F6,width=18,font="arial 10 bold",bd=7,relief=SUNKEN).grid(row=2,column=3,padx=10,pady=1)


        btn_F=Frame(F6,bd=7,relief=GROOVE)
        btn_F.place(x=670,width=625,height=105)

        total_btn=Button(btn_F,command=self.find_bill,bg="black",text="Total",fg="Black",pady=15,width=11,bd=5,font="arial 15 bold").grid(row=0,column=0,padx=5,pady=5)
        GBill_btn=Button(btn_F,command=self.bill_area,bg="Blue",text="Generate Bill",fg="Black",pady=15,width=15,bd=5,font="arial 15 bold").grid(row=0,column=1,padx=5,pady=5)
        Clear_btn=Button(btn_F,command=self.clear,bg="Blue",text="Clear",fg="Black",pady=15,width=11,bd=5,font="arial 15 bold").grid(row=0,column=2,padx=5,pady=5)
        Exit_btn=Button(btn_F,command=self.root.destroy,bg="Blue",text="Exit",fg="Black",pady=15,width=11,bd=5,font="arial 15 bold").grid(row=0,column=3,padx=5,pady=5)
        self.welcome_bill()


    #===============New functions==============

    def search_item(self):
        if self.search_item_no.get()=="":
            messagebox.showerror("Error","No input entered")
            return
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        cur.execute(f"select * from stocks where item_no='{self.search_item_no.get()}'")
        rows=cur.fetchall()
        if len(rows)==0:
            messagebox.showinfo("Alert","No Item found")
        for row in rows:
            self.item_no.set(row[5])
            self.item_name.set(row[0])
            self.item_quantity.set(1)
            self.item_price.set(row[2])
            self.item_guage.set(row[4])
            self.color_fetch()
        con.commit()
        con.close()

    def color_fetch(self):
        global F3
        try:
            if self.item_name.get() != '':
                print("doing")
                con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
                cur=con.cursor()
                cur.execute(f"select color from stocks where name='{self.item_name.get()}' and guage = {self.item_guage.get()}")
                color_rows=cur.fetchall()
                my_colors = [r for r, in color_rows]
                self.color_options.set("")
                self.color_option_field = OptionMenu(F3, self.color_options, *my_colors, command=self.update_color)
                self.color_option_field.grid(row=2,column=1)
                self.color_option_field['width'] = 10
                con.commit()
                con.close()
        except Exception as e:
            print(e)

    def update_color(self, value):
        self.item_color.set(value)

    def add_item(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        cur.execute(f"select * from stocks where item_no={self.item_no.get()}")
        rows=cur.fetchall()
        available_quantity=rows[0][2]

        listOfEntriesInTreeView=self.Stock_Table.get_children()
        for each in listOfEntriesInTreeView:
            if int(self.Stock_Table.item(each)['values'][0])==int(self.item_no.get()):
                new_quantity=int(self.Stock_Table.item(each)['values'][2])+int(self.item_quantity.get())
                if new_quantity<available_quantity or new_quantity==available_quantity:
                    self.Stock_Table.detach(each)
                    new_item=(self.item_no.get(),self.item_name.get(),new_quantity,self.item_price.get()*new_quantity)
                    self.Stock_Table.insert('',END, values=new_item)
                    return
                else:
                    messagebox.showinfo("Alert","Available quantity is less.")
                    return
        if int(self.item_quantity.get())<available_quantity or int(self.item_quantity.get())==available_quantity:
            new_item=(self.item_no.get(),self.item_name.get(),self.item_quantity.get(),self.item_price.get()*self.item_quantity.get())
            self.Stock_Table.insert('',END, values=new_item)

    def bill_area(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        total=0
        if self.c_phon.get()=='' or self.c_name.get()=='':
            messagebox.showinfo("Alert","Enter Customer details first")
            return

        elif self.calculateItemInCart()==0:
            messagebox.showinfo("Alert","Add items to cart")
            return

        self.welcome_bill()
        listOfEntriesInTreeView=self.Stock_Table.get_children()
        i=1

        cur.execute(f"select * from registered_customers where customer_name='{self.c_name.get()}' and customer_contact={self.c_phon.get()}")
        rows=cur.fetchall()
        if len(rows)!=0:
            customer_id=rows[0][0]
            self.bill_type.set(1)
        else:
            self.bill_type.set(0)
            customer_id=random.randint(1,1000)
            cur.execute(f"insert into customer values ({customer_id},'{self.c_name.get()}',{self.c_phon.get()})")
            con.commit()

        for each in listOfEntriesInTreeView:
            statement=f"insert into sales_stocks values ({self.bill_no.get()},{self.Stock_Table.item(each)['values'][0]},{self.Stock_Table.item(each)['values'][2]})"
            cur.execute(statement)
            con.commit()
            statement=f"update stocks set qty=qty-{self.Stock_Table.item(each)['values'][2]} where item_no={self.Stock_Table.item(each)['values'][0]}"
            cur.execute(statement)
            con.commit()
            total=total+int(self.Stock_Table.item(each)['values'][3])
            self.txtarea.insert(END,f"\n{i}\t{self.Stock_Table.item(each)['values'][1]}\t\t     {self.Stock_Table.item(each)['values'][2]}\t {self.Stock_Table.item(each)['values'][3]}")
            self.Stock_Table.detach(each)
            i=i+1
        self.txtarea.insert(END,f"\n=======================================")
        self.txtarea.insert(END,f"\n\t\t     Subtotal Rs. {total}")
        self.txtarea.insert(END,f"\n\t\t     Sales Tax Rs. {0.10*total}")
        self.txtarea.insert(END,"\n---------------------------------------")
        self.txtarea.insert(END,f"\n\t\t\tTotal Rs.  {total+0.10*total}")
        self.txtarea.insert(END,"\n---------------------------------------")
        self.txtarea.insert(END,"\n\n\n\n\n\n\n\n\n-----------Thanks for shopping------------")
        self.save_bill()

        #==============Save the bill to database================

        statement=f"insert into sales_bill values ({self.bill_no.get()},'{datetime.today().strftime('%Y-%m-%d')}',{total+0.1*total},{customer_id},{self.bill_type.get()}) "
        cur.execute(statement)
        con.commit()
        con.close()

    def save_bill(self):
        self.bill_data=self.txtarea.get('1.0',END)
        f1=open("generated_bill/"+self.bill_no.get()+".txt","w")
        f1.write(self.bill_data)
        f1.close()
        messagebox.showinfo("Saved",f"Bill No. :{self.bill_no.get()} saved Successfully.")

    def welcome_bill(self):
        self.txtarea.delete('1.0',END)
        self.txtarea.insert(END,"\tWelcome to Meta Cables")
        self.txtarea.insert(END,f"\n Bill Number: {self.bill_no.get()}")
        self.txtarea.insert(END,f"\n Customer Name: {self.c_name.get()}")
        self.txtarea.insert(END,f"\n Phone Number: {self.c_phon.get()}")
        self.txtarea.insert(END,f"\n=======================================")
        self.txtarea.insert(END,f"\nS.No  \tItem Name\t\t   Qty \tPrice")
        self.txtarea.insert(END,f"\n=======================================")

    def calculateItemInCart(self):
        listOfEntriesInTreeView=self.Stock_Table.get_children()
        i=0
        for each in listOfEntriesInTreeView:
            i=i+1
        return (i)

    def work_on_focus(self,ev):
        cursor_row=self.Stock_Table.focus()
        contents=self.Stock_Table.item(cursor_row)
        row=contents['values']
        self.item_no.set(row[5])
        self.item_name.set(row[0])
        self.item_quantity.set(row[1])
        self.item_price.set(row[2])
        self.item_color.set(row[3])
        self.item_guage.set(row[4])

    def clear(self):
        self.Stock_Table.delete(*self.Stock_Table.get_children())
        self.item_no.set("")
        self.item_name.set("")
        self.item_price.set(0)
        self.item_quantity.set(1)
        self.item_color.set("")
        self.item_guage.set("")
        self.c_name.set("")
        self.c_phon.set("")
        self.bill_no.set(str(random.randint(1000,9999)))
        self.welcome_bill()

    def find_bill(self):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        cur.execute(f"select * from sales_bill where inv_id={self.search_bill.get()}")
        rows=cur.fetchall()
        if len(rows)==0:
            messagebox.showinfo("Not Found",f"Bill No. :{self.search_bill.get()} not found.")
            return
        inv_date=rows[0][1]
        inv_amount=rows[0][2]
        inv_id=rows[0][0]
        cur.execute(f"select * from customer where customer_id={rows[0][3]}")
        rows=cur.fetchall()
        c_name=rows[0][1]
        c_phone=rows[0][2]
        self.txtarea.delete('1.0',END)
        self.txtarea.delete('1.0',END)
        self.txtarea.insert(END,"\tWelcome to Meta Cables")
        self.txtarea.insert(END,f"\n Bill Number: {self.bill_book}{inv_id}")
        self.txtarea.insert(END,f"\n Bill Date: {inv_date}")
        self.txtarea.insert(END,f"\n Customer Name: {c_name}")
        self.txtarea.insert(END,f"\n Phone Number: {c_phone}")
        self.txtarea.insert(END,f"\n=======================================")
        self.txtarea.insert(END,f"\nS.No  \tItem Name\t\t   Qty \tPrice")
        self.txtarea.insert(END,f"\n=======================================")

        cur.execute(f"select * from sales_stocks where inv_id={inv_id}")
        rows=cur.fetchall()
        i=1
        total=0
        for row in rows:
            cur.execute(f"select * from stocks where item_no={row[1]}")
            temp=cur.fetchall()
            self.txtarea.insert(END,f"\n{i}\t{temp[0][1]}\t\t     {row[2]}\t {temp[0][3]}")
            total=total+row[2]*temp[0][3]
            i=i+1
        self.txtarea.insert(END,f"\n=======================================")
        self.txtarea.insert(END,f"\n\t\t     Subtotal Rs. {total}")
        self.txtarea.insert(END,f"\n\t\t     Sales Tax Rs. {0.10*total}")
        self.txtarea.insert(END,"\n---------------------------------------")
        self.txtarea.insert(END,f"\n\t\t\tTotal Rs.  {total+0.10*total}")
        self.txtarea.insert(END,"\n---------------------------------------")
        self.txtarea.insert(END,"\n\n\n\n\n\n\n\n\n-----------Thanks for shopping------------")

    # def showOption(self):
    #     con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
    #     cur=con.cursor()
    #     cur.execute(f"select customer_name from registered_customers")
    #     rows=cur.fetchall()
    #     if len(rows) > 0:
    #         my_list = [r for r, in rows] 
    #         self.options = StringVar(my_list)
    #         self.options.set(self.my_list[0])
    #         om1 = OptionMenu(my_list, self.options, *my_list)
    #         om1.grid(row=2,column=5)

    def displayCustomer(self, option):
        con=pymysql.connect(host="localhost",user="ryzon",password="zain0980",database="ims")
        cur=con.cursor()
        cur.execute(f"select * from registered_customers where customer_name='{option}' limit 1")
        rows=cur.fetchall()
        if len(rows) > 0:
            for row in rows:
                self.c_id.set(row[0])
                self.c_name.set(row[1])
                self.c_phon.set(row[2])



    def openStock(self):
        from ims_stock import Stock
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Stock(self.root)
    
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
        self.root = Raw(self.root)
    
    def openOrders(self):
        from mms_orders import Order
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root=Order(self.root)

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