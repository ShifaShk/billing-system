
from tkinter import *
import random, os, tempfile
import qrcode
from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#FUNCTIONALITY part
from tkinter import messagebox, END

def total():
    # Check if name and phone number are entered
    if not name_entry.get().strip() or not phone_entry.get().strip():
        messagebox.showerror("Error", "Please enter Customer Name and Phone Number.")
        return 

    # Prices of items
    cosmetics_prices = {'Bath Soap': 40, 'Face Cream': 120, 'Face Wash': 100, 'Hair Spray': 150, 'Hair Gel': 130, 'Body Lotion': 180}
    grocery_prices = {'Rice': 50, 'Oil': 140, 'Daal': 100, 'Wheat': 60, 'Sugar': 45, 'Tea': 90}
    cold_drinks_prices = {'Maaza': 30, 'Pepsi': 35, 'Sprite': 40, 'Dew': 35, 'Frooti': 30, 'Coca Cola': 40}

    # Calculate total for cosmetics
    total_cosmetics = sum(int(cosmetics_vars[item].get()) * cosmetics_prices[item] for item in cosmetics_prices)
    total_grocery = sum(int(grocery_vars[item].get()) * grocery_prices[item] for item in grocery_prices)
    total_drinks = sum(int(cold_drinks_vars[item].get()) * cold_drinks_prices[item] for item in cold_drinks_prices)

    # Tax calculation (5% for cosmetics, 3% for groceries, 2% for drinks)
    tax_cosmetics = round(total_cosmetics * 0.05, 2)
    tax_grocery = round(total_grocery * 0.03, 2)
    tax_drinks = round(total_drinks * 0.02, 2)

    # Update the UI
    cosmetic_price_entry.delete(0, END)
    cosmetic_price_entry.insert(0, f'Rs{total_cosmetics}')

    grocery_price_entry.delete(0, END)
    grocery_price_entry.insert(0, f'Rs{total_grocery}')

    drinks_price_entry.delete(0, END)
    drinks_price_entry.insert(0, f'Rs{total_drinks}')

    cosmetic_tax_entry.delete(0, END)
    cosmetic_tax_entry.insert(0, f'Rs{tax_cosmetics}')

    grocery_tax_entry.delete(0, END)
    grocery_tax_entry.insert(0, f'Rs{tax_grocery}')

    drinks_tax_entry.delete(0, END)
    drinks_tax_entry.insert(0, f'Rs{tax_drinks}')

print("Saving bill to:", os.getcwd())

save_path = "D:/billing_system/bills"
if not os.path.exists(save_path):
    os.mkdirs(save_path)
    
def save_bill():
    global bill_number
    bill_number = str(random.randint(10000, 99999))
    file_path = os.path.join(save_path, f"bill_{bill_number}.txt")
    result=messagebox.askyesno("Confirm", "Do you want to save the bill?")
    if result:
        # bill_content = f"Bill No: {bill_number}\nCustomer: {name_entry}\nPhone: {phone_entry}\n"
        bill_content =textarea.get(1.0, "end-1c")
        # file=open(f'bills/ {bill_number}.txt', 'w')
        with open(file_path, "w", encoding="utf-8")as file:
            file.write(bill_content)
            file.close()
            messagebox.showinfo("Sucess", f"bill number:{bill_number} is save successfully")
        print(f"Bill saved at {file_path}")


def print_bill():
    try:
        bill_content = textarea.get(1.0, "end-1c").strip()  # Get the entire text

        if not bill_content:
            messagebox.showerror("Error", "Bill is empty")
            return

        # Create a temporary file
        temp_file = tempfile.mktemp(suffix=".txt")

        # Write bill content to file
        with open(temp_file, "w", encoding="utf-8") as file:
            file.write(bill_content)

        # Print the file
        os.startfile(temp_file, "print")

    except Exception as e:
        messagebox.showerror("Error", f"Error printing bill: {e}")
    
def send_email():
    email_window = Toplevel()
    email_window.title("Send Email")
    email_window.geometry("500x400")
    
    # Setting same styles as main window
    email_window.configure(bg="DeepPink4")

    # Labels and Entries
    Label(email_window, text="Sender Email:", font=('arial', 12, 'bold'), bg="DeepPink4", fg="wheat1").grid(row=0, column=0, padx=10, pady=5)
    sender_email = Entry(email_window, font=('arial', 12), width=30)
    sender_email.grid(row=0, column=1, padx=10, pady=5)
    sender_email.insert(0, "shaikhshifa052005@gmail.com")  # Fixed sender email
    sender_email.config(state='readonly')

    Label(email_window, text="Password:", font=('arial', 12, 'bold'), bg="DeepPink4", fg="wheat1").grid(row=1, column=0, padx=10, pady=5)
    sender_password = Entry(email_window, font=('arial', 12), width=30, show="*")
    sender_password.grid(row=1, column=1, padx=10, pady=5)
    sender_password.insert(0, "wbko rcyb zuah owma")  # Fixed sender password
    sender_password.config(state='readonly')

    Label(email_window, text="Customer Email:", font=('arial', 12, 'bold'), bg="DeepPink4", fg="wheat1").grid(row=2, column=0, padx=10, pady=5)
    customer_email = Entry(email_window, font=('arial', 12), width=30)
    customer_email.grid(row=2, column=1, padx=10, pady=5)

    Label(email_window, text="Bill Details:", font=('arial', 12, 'bold'), bg="DeepPink4", fg="wheat1").grid(row=3, column=0, padx=10, pady=5)
    # bill_text = textarea.get(1.0, "end-1c")
    bill_text = Text(email_window, font=('arial', 12), width=40, height=10)
    bill_text.grid(row=3, column=1, padx=10, pady=5)
    
    bill_text.insert(END, textarea.get(1.0, "end-1c"))  # You can replace this with actual bill data

    def send_email_action():
        sender = sender_email.get()
        password = sender_password.get()
        recipient = customer_email.get()
        bill_content = bill_text.get("1.0", END)
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, bill_content)
            server.quit()
            Label(email_window, text="Email Sent!", font=('arial', 12, 'bold'), fg="green", bg="DeepPink4").grid(row=5, column=1)
        except Exception as e:
            Label(email_window, text="Failed to send email.", font=('arial', 12, 'bold'), fg="red", bg="DeepPink4").grid(row=5, column=1)
            print(f"Error: {e}")

    # Send Button
    Button(email_window, text="Send", font=('arial', 12, 'bold'), bg='wheat1', fg='DeepPink4', command=send_email_action).grid(row=4, column=1, pady=10)  

    
def search_bill():
    bill_number = bill_entry.get().strip()  # Get bill number input from user

    if not bill_number:  
        messagebox.showwarning("Warning", "Please enter a bill number")
        return

    save_path = "D:/billing_system/bills"  # Ensure this matches the save location
    bill_filename = f"bill_{bill_number}.txt"  # File name format used in save_bill()
    bill_path = os.path.join(save_path, bill_filename)

    # Check if the bill file exists
    if not os.path.exists(bill_path):
        messagebox.showerror("Error", f"Bill number {bill_number} not found!")
        return

    try:
        with open(bill_path, "r", encoding="utf-8") as f:
            bill_content = f.read()

        textarea.delete(1.0, END)  # Clear previous content
        textarea.insert(END, bill_content)  # Display bill content

        messagebox.showinfo("Success", f"Bill {bill_number} loaded successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Error reading the bill: {e}")
            
         
def bill():
    global bill_number
    # Generate a random bill number
    bill_number = str(random.randint(10000, 99999))
    bill_entry.delete(0, END)
    bill_entry.insert(0, bill_number)

    # Check if name and phone number are entered
    if not name_entry.get().strip() or not phone_entry.get().strip():
        messagebox.showerror("Error", "Please enter Customer Name and Phone Number.")
        return 

    customer_name = name_entry.get().strip()
    phone_number = phone_entry.get().strip()

    # Prices of items
    cosmetics_prices = {'Bath Soap': 40, 'Face Cream': 120, 'Face Wash': 100, 'Hair Spray': 150, 'Hair Gel': 130, 'Body Lotion': 180}
    grocery_prices = {'Rice': 50, 'Oil': 140, 'Daal': 100, 'Wheat': 60, 'Sugar': 45, 'Tea': 90}
    cold_drinks_prices = {'Maaza': 30, 'Pepsi': 35, 'Sprite': 40, 'Dew': 35, 'Frooti': 30, 'Coca Cola': 40}

    # Calculate total for cosmetics, grocery, and drinks
    total_cosmetics = sum(int(cosmetics_vars[item].get()) * cosmetics_prices[item] for item in cosmetics_prices)
    total_grocery = sum(int(grocery_vars[item].get()) * grocery_prices[item] for item in grocery_prices)
    total_drinks = sum(int(cold_drinks_vars[item].get()) * cold_drinks_prices[item] for item in cold_drinks_prices)

    # Tax calculation (5% for cosmetics, 3% for groceries, 2% for drinks)
    tax_cosmetics = round(total_cosmetics * 0.05, 2)
    tax_grocery = round(total_grocery * 0.03, 2)
    tax_drinks = round(total_drinks * 0.02, 2)

    grand_total = total_cosmetics + total_grocery + total_drinks + tax_cosmetics + tax_grocery + tax_drinks

    #  Display in Bill Area
    textarea.delete('1.0', END)
    textarea.insert(END, f"\n===== Bill Summary =====\n")
    textarea.insert(END, f"Bill Number: {bill_number}\n")
    textarea.insert(END, f"Customer Name: {customer_name}\n")
    textarea.insert(END, f"Phone Number: {phone_number}\n")
    textarea.insert(END, f"---------------------------------\n")
    textarea.insert(END, f"Product Name\tQuantity\tPrice\n")
    textarea.insert(END, f"---------------------------------\n")

    # Add purchased items
    for item in cosmetics_prices:
        quantity = int(cosmetics_vars[item].get())
        if quantity > 0:
            price = quantity * cosmetics_prices[item]
            textarea.insert(END, f"{item}\t{quantity}\tRs{price}\n")

    for item in grocery_prices:
        quantity = int(grocery_vars[item].get())
        if quantity > 0:
            price = quantity * grocery_prices[item]
            textarea.insert(END, f"{item}\t{quantity}\tRs{price}\n")

    for item in cold_drinks_prices:
        quantity = int(cold_drinks_vars[item].get())
        if quantity > 0:
            price = quantity * cold_drinks_prices[item]
            textarea.insert(END, f"{item}\t{quantity}\tRs{price}\n")

    textarea.insert(END, f"---------------------------------\n")
    textarea.insert(END, f"Subtotal:\tRs{total_cosmetics + total_grocery + total_drinks}\n")
    textarea.insert(END, f"Tax (Cosmetics 5%): Rs{tax_cosmetics}\n")
    textarea.insert(END, f"Tax (Grocery 3%): Rs{tax_grocery}\n")
    textarea.insert(END, f"Tax (Drinks 2%): Rs{tax_drinks}\n")
    textarea.insert(END, f"---------------------------------\n")
    textarea.insert(END, f"Grand Total:\tRs{grand_total}\n")
    textarea.insert(END, f"---------------------------------\n")
    textarea.insert(END, f"Thank you for shopping with us!\n")
    save_bill()
    # Generate QR Code with Bill Details
    bill_data = f"Bill No: {bill_number}\nName: {customer_name}\nPhone: {phone_number}\nTotal: Rs{grand_total}"
    qr = qrcode.make(bill_data)
    qr.save("bill_qr.png")

    # Display QR Code in GUI
    qr_image = Image.open("bill_qr.png")
    qr_image = qr_image.resize((150, 150))  # Resize QR code
    qr_tk = ImageTk.PhotoImage(qr_image)

    qr_label.config(image=qr_tk)
    qr_label.image = qr_tk  # Keep reference

    

 
def clear():
    # Clear customer details
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    bill_entry.delete(0, END)

    # Reset product quantity entries to '0'
    for entry in cosmetics_vars.values():
        entry.delete(0, END)
        entry.insert(0, '0')

    for entry in grocery_vars.values():
        entry.delete(0, END)
        entry.insert(0, '0')

    for entry in cold_drinks_vars.values():
        entry.delete(0, END)
        entry.insert(0, '0')

    # Clear price and tax fields
    cosmetic_price_entry.delete(0, END)
    grocery_price_entry.delete(0, END)
    drinks_price_entry.delete(0, END)

    cosmetic_tax_entry.delete(0, END)
    grocery_tax_entry.delete(0, END)
    drinks_tax_entry.delete(0, END)

    # Clear the bill area
    textarea.delete('1.0', END)

    
 
#GUI part 
root = Tk()
root.title("Billing System")
root.geometry('1270x685')
root.iconbitmap("icon.ico")
root.configure(bg='DeepPink4')
qr_label = Label(root)
qr_label.place(x=700, y=400)
# Heading Label
headingLabel = Label(root, text='Billing System', font=('times new roman', 30, 'bold'), bg='DeepPink4', fg='wheat1', bd=12,  relief=GROOVE)
headingLabel.pack(fill=X)

# Customer Details Frame
customer_frame = Frame(root, bd=8, relief=GROOVE, bg='DeepPink4')
customer_frame.pack(fill=X, pady=5)

Label(customer_frame, text="Customer Details", font=('times new roman', 15, 'bold'), bg='DeepPink4', fg='wheat1').grid(row=0, columnspan=3)
Label(customer_frame, text="Name", font=('arail', 12, 'bold'), bg='DeepPink4', fg='white').grid(row=1, column=0, padx=10)
name_entry = Entry(customer_frame, font=('arail', 12), width=20)
name_entry.grid(row=1, column=1, padx=10)

Label(customer_frame, text="Phone Number", font=('arail', 12, 'bold'), bg='DeepPink4', fg='white').grid(row=1, column=2, padx=10)
phone_entry = Entry(customer_frame, font=('arail', 12), width=20)
phone_entry.grid(row=1, column=3, padx=10)

Label(customer_frame, text="Bill Number", font=('arail', 12, 'bold'), bg='DeepPink4', fg='white').grid(row=1, column=4, padx=10)
bill_entry = Entry(customer_frame, font=('arail', 12), width=20)
bill_entry.grid(row=1, column=5, padx=10)

search=Button(customer_frame, text='SEARCH', font=('arail', 12, 'bold'), bg='gray', fg='DeepPink4', command=search_bill).grid(row=1, column=6, padx=10)

# Product Frames
product_frame = Frame(root) #, bd=8, relief=GROOVE, bg='DeepPink4')
product_frame.pack()#fill=X)

# Cosmetics Section
cosmetics_frame = LabelFrame(product_frame, text="Cosmetics", font=('times new roman', 15, 'bold'), bg='DeepPink4', fg='wheat1', relief=GROOVE, bd=8)
cosmetics_frame.grid(row=0, column=0 )# padx=10)

cosmetics_items = ['Bath Soap', 'Face Cream', 'Face Wash', 'Hair Spray', 'Hair Gel', 'Body Lotion']
cosmetics_vars = {}
for i, item in enumerate(cosmetics_items):
    Label(cosmetics_frame, text=item, font=('times new roman', 15, 'bold'), bg='DeepPink4', fg='white', width=10, bd=5).grid(row=i, column=0, sticky='w', pady=9)
    cosmetics_vars[item] = Entry(cosmetics_frame, width=5, font=('times new roman', 15, 'bold'), bd=5)
    cosmetics_vars[item].grid(row=i, column=1)
    cosmetics_vars[item].insert(0, '0')


# Grocery Section
grocery_frame = LabelFrame(product_frame, text="Grocery", font=('times new roman', 15, 'bold'), bg='DeepPink4', fg='wheat1', relief=GROOVE, bd=8)
grocery_frame.grid(row=0, column=1, padx=10)

grocery_items = ['Rice', 'Oil', 'Daal', 'Wheat', 'Sugar', 'Tea']
grocery_vars = {}
for i, item in enumerate(grocery_items):
    Label(grocery_frame, text=item, font=('times new roman', 15, 'bold'), bg='DeepPink4', fg='white', width=10, bd=5).grid(row=i, column=0, sticky='w', pady=9)
    grocery_vars[item] = Entry(grocery_frame, width=5, font=('times new roman', 15, 'bold'), bd=5)
    grocery_vars[item].grid(row=i, column=1)
    grocery_vars[item].insert(0, '0')

# Cold Drinks Section
cold_drink_frame = LabelFrame(product_frame, text="Cold Drinks", font=('times new roman', 15, 'bold'), bg='DeepPink4', fg='wheat1', relief=GROOVE, bd=8)
cold_drink_frame.grid(row=0, column=2)

cold_drinks = ['Maaza', 'Pepsi', 'Sprite', 'Dew', 'Frooti', 'Coca Cola']
cold_drinks_vars = {}
for i, item in enumerate(cold_drinks):
    Label(cold_drink_frame, text=item, font=('times new roman', 15, 'bold'), bg='DeepPink4', fg='white', width=10, bd=5).grid(row=i, column=0, sticky='w', pady=9, padx=10)
    cold_drinks_vars[item] = Entry(cold_drink_frame, width=5,  font=('times new roman', 15, 'bold'), bd=5)
    cold_drinks_vars[item].grid(row=i, column=1)
    cold_drinks_vars[item].insert(0, '0')


bill_frame= Frame(product_frame,bd=8, relief=GROOVE)
bill_frame.grid(row=0, column=3, padx=10)

billarealabel = Label(bill_frame, text='Bill Area', font=('times new roman', 15, 'bold'),bd=7, relief=GROOVE, bg='DeepPink4', fg='wheat1')
billarealabel.pack(fill=X)

scrollbar=Scrollbar(bill_frame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)
textarea= Text(bill_frame, height=18, width=55, yscrollcommand=scrollbar.set)
textarea.pack()
scrollbar.config(command=textarea.yview)

# Bottom Menu
menu_frame = LabelFrame(root, text='Bill Menu', font=('times new roman', 13, 'bold'), bd=8, relief=GROOVE, bg='DeepPink4', fg='wheat1')
menu_frame.pack()

cosmetic_price_label= Label(menu_frame, text='Cosmetic Price', font=('times new roman', 13, 'bold'), bg='DeepPink4', fg='white', width=10, bd=5)
cosmetic_price_label.grid(row=0, column=0, pady=6,padx=10)

cosmetic_price_entry = Entry(menu_frame,  width=10,font=('times new roman', 13, 'bold'), bd=5)
cosmetic_price_entry.grid(row=0, column=1, pady=6, padx=10)


grocery_price_label= Label(menu_frame, text='Grocery Price', font=('times new roman', 13, 'bold'), bg='DeepPink4', fg='white', width=10, bd=5)
grocery_price_label.grid(row=1, column=0, pady=6,padx=10)

grocery_price_entry = Entry(menu_frame,  width=10,font=('times new roman', 13, 'bold'), bd=5)
grocery_price_entry.grid(row=1, column=1, pady=6, padx=10)


drinks_price_label= Label(menu_frame, text='Drinks Price', font=('times new roman', 13, 'bold'), bg='DeepPink4', fg='white', width=10, bd=5)
drinks_price_label.grid(row=2, column=0, pady=6,padx=10)

drinks_price_entry = Entry(menu_frame,  width=10,font=('times new roman', 13, 'bold'), bd=5)
drinks_price_entry.grid(row=2, column=1, pady=6, padx=10)



cosmetic_tax_label= Label(menu_frame, text='Cosmetic Tax', font=('times new roman', 13, 'bold'), bg='DeepPink4', fg='white', width=10, bd=5)
cosmetic_tax_label.grid(row=0, column=2, pady=6,padx=10)

cosmetic_tax_entry = Entry(menu_frame,  width=10,font=('times new roman', 13, 'bold'), bd=5)
cosmetic_tax_entry.grid(row=0, column=3, pady=6, padx=10)


grocery_tax_label= Label(menu_frame, text='Grocery Tax', font=('times new roman', 13, 'bold'), bg='DeepPink4', fg='white', width=10, bd=5)
grocery_tax_label.grid(row=1, column=2, pady=6,padx=10)

grocery_tax_entry = Entry(menu_frame,  width=10,font=('times new roman', 13, 'bold'), bd=5)
grocery_tax_entry.grid(row=1, column=3, pady=6, padx=10)


drinks_tax_label= Label(menu_frame, text='Drinks Tax', font=('times new roman', 13, 'bold'), bg='DeepPink4', fg='white', width=10, bd=5)
drinks_tax_label.grid(row=2, column=2, pady=6,padx=10)

drinks_tax_entry = Entry(menu_frame,  width=10,font=('times new roman', 13, 'bold'), bd=5)
drinks_tax_entry.grid(row=2, column=3, pady=6, padx=10)


buttonFrame = Frame(menu_frame, bd=8, relief=GROOVE)
buttonFrame.grid(row=0, column=4, rowspan=3)

totalButton = Button(buttonFrame, text='Total', font=('arial', 16, 'bold'), bg='DeepPink4', fg='wheat1', bd=5, width=8, pady=10, command=total)
totalButton.grid(row=0, column=0, padx=5, pady=20)

billButton = Button(buttonFrame, text='Bill', font=('arial', 16, 'bold'), bg='DeepPink4', fg='wheat1', bd=5, width=8, pady=10, command=bill)
billButton.grid(row=0, column=1, padx=5, pady=20)


emailButton = Button(buttonFrame, text='Email', font=('arial', 16, 'bold'), bg='DeepPink4', fg='wheat1', bd=5, width=8, pady=10, command=send_email)
emailButton.grid(row=0, column=2, padx=5, pady=20)


printButton = Button(buttonFrame, text='Print', font=('arial', 16, 'bold'), bg='DeepPink4', fg='wheat1', bd=5, width=8, pady=10, command=print_bill)
printButton.grid(row=0, column=3, padx=5, pady=20)


clearButton = Button(buttonFrame, text='Clear', font=('arial', 16, 'bold'), bg='DeepPink4', fg='wheat1', bd=5, width=8, pady=10, command=clear)
clearButton.grid(row=0, column=4, padx=5, pady=20)


root.mainloop()