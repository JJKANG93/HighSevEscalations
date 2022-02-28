from tkinter import *
from tkinter import messagebox
import tkinter as tk
import bitlyshortener
from bitlyshortener import *
from tkcalendar import *

# Bitly Setup
tokens_pool = ['d2375064d1ef535690914f2d2d96d7390b41fb10']  # Use your own API key.
shortener = bitlyshortener.Shortener(tokens=tokens_pool, max_cache_size=256)


master = Tk()

app_width = 800
app_height = 600
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
master.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')  # main window start in the center of the screen
master.title('High Sev Escalation App --Version 1.0')

status = ["New",
          "New/Resolved",
          "Updated",
          "Ongoing",
          "On Hold",
          "Resolved",
          "Re-occurring",
          "Re-occurring/Resolved",
          "Cancelled"]
severity = ["A", "B"]
affecting_system = ["all", "TNGQuickfire", "MGP SW", "QF2", "Sempris", "TEG0", "TEG1", "TEG2", "TEG3", "TEG4", "TEG6"]
tier = ["N/A", "Tier_1", "Tier_2"]
operator = ["all", "TEG1", "GT", "TEG2", "BBIN_CNY", "TEG3", "JuGaming(A)",
            "TEG4", "JuGamingA(6)", "JuGamingA(12)", "JuGamingA(18)", "JuGamingA(25)",
            "JuGamingA(28)", "TEG6", "Oriental_Game", "OG", "TEG0", "Power_Asia", "infini88",
            "Asia888", "ambtw", "topusd3", "TOP_USD2",
            "Poseidon", "TH1GAMES", "TOP_USD(GAMA)", "UEG", "inplaymatrix", "GplayG", "MGP SW", "AMBSW",
            "AMBGAMESSW" "pay4dsw",
            "Sempris", "W88", "Wild_Treasure", "188bet", "Asiabet", "Solid_Gaming", "GSD", "Foxnos", "M88",
            "Asian_Logic", "VWIN", "SBO"]
time_elapsed = []
service_degradation = ["N/A", "25%", "Over 25%", "50%", "Over 50%", "75%", "Over 75%", "100%"]
root_cause = ["N/A", "Internal", "Operator", "Regular Maintenance", "Network", "Internal-3rd Party", "Internal-MG+",
              "Unknown"]
comms_manager = ["Abri Liebenberg (+61 432823087)",
                 "Matt Cheng (+886 932075280)",
                 "Matthew Geoghegan (+886 905249541)",
                 "Bartosz Lewandowski (+886 978705232)",
                 "Jeff Huang (+886 933308768)",
                 "Jill Shen (+886 903438345)",
                 "Frank Hsu (+886 972211756)",
                 "Juan Gilpin (+886 909948943)"]
crisis_manager = ["Abri Liebenberg (+61 432823087)",
                  "Matt Cheng (+886 932075280)",
                  "Matthew Geoghegan (+886 905249541)",
                  "Bartosz Lewandowski (+886 978705232)",
                  "Jeff Huang (+886 933308768)",
                  "Jill Shen (+886 903438345)",
                  "Frank Hsu (+886 972211756)",
                  "Juan Gilpin (+886 909948943)"]

# Status Dropdown Menu
status_label = Label(master, text="Status").place(x=0, y=0)
status_variable = StringVar(master)
status_variable.set(status[0])  # default value
status_options = OptionMenu(master, status_variable, *status)
status_options.place(y=15, x=0)

# Severity Dropdown Menu
severity_label = Label(master, text="Severity").place(x=0, y=45)
severity_variable = StringVar(master)
severity_variable.set(severity[0])  # default value
severity_options = OptionMenu(master, severity_variable, *severity)
severity_options.place(y=65, x=0)

# Escalation Name
name_label = Label(master, text="Escalation Name Here").place(x=0, y=95)
name = StringVar()
name.set("GPM degradation by XX% affecting <xxx>")
name_entry_box = Entry(master, textvariable=name, width=50).place(x=0, y=120, height=25)

# Tier
tier_label = Label(master, text="Tier").place(x=0, y=175)
tier_variable = StringVar(master)
tier_variable.set(tier[0])  # default value
tier_options = OptionMenu(master, tier_variable, *tier)
tier_options.place(y=193, x=0)



# Calendar Date
def grab_date():
    global cal
    splash_window = Toplevel()
    splash_window.title("Select Date")
    screen_width = splash_window.winfo_screenwidth()
    screen_height = splash_window.winfo_screenheight()
    login_width = 300
    login_height = 250
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    splash_window.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')
    cal = Calendar(splash_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack()

    def pick_date():
        global cal_label
        global cal_time
        cal_label = Label(master)
        cal_label.config(text=cal.get_date())
        cal_label.place(x=0, y=333)
        splash_window.destroy()





    def clear_date():
        cal_label.destroy()
    pick_button = Button(splash_window, text="Pick Date", command=lambda: pick_date()).place(x=50, y=200)
    clear_button = Button(splash_window, text="Clear Date", command=lambda: clear_date()).place(x=170, y=200)


date_button = Button(master, text="Start Time: Calendar", command=lambda: grab_date()).place(x=0, y=304)
start_time_label = Label(master)
gmt_label1 = Label(master, text="GMT+8").place(x=132, y=335)
start_time = StringVar()
start_time.set("hh:mm")
start_time_entry_box = Entry(master, textvariable=start_time, width=10).place(x=70, y=335, height=20)
cal_label2 = Label(master)
cal_label2.config(text="____-__-___")
cal_label2.place(x=0, y=333)

# End Time
end_time_label = Label(master, text="End Time:").place(x=0, y=355)
end_time = StringVar()
end_time.set("N/A")
end_time_entry_box = Entry(master, textvariable=end_time, width=50).place(x=0, y=375, height=20)
# gmt_label2 = Label(master, text="GMT+8").place(x=132, y=375)


# Time Elapsed
elapsed_time_label = Label(master, text="Time Elapsed:").place(x=0, y=260)
elapsed_time = StringVar()
elapsed_time.set("N/A")
elapsed_time_entry_box = Entry(master, textvariable=elapsed_time, width=50).place(x=0, y=280, height=25)


# Service Degradation
service_degradation_label = Label(master, text="Service Degradation").place(x=0, y=400)
service_degradation_variable = StringVar(master)
service_degradation_variable.set(service_degradation[0])  # default value
service_degradation_options = OptionMenu(master, service_degradation_variable, *service_degradation)
service_degradation_options.place(y=420, x=0)

# Symptoms
symptoms_label = Label(master, text="Symptoms").place(x=0, y=450)
symptoms = StringVar()
symptoms.set("GPM degradation by XX% affecting <xxx>")
symptoms_entry_box = Entry(master, textvariable=symptoms, width=50).place(x=0, y=470, height=25)

# Action Taken
action_taken_label = Label(master, text="Action Taken").place(x=550, y=20)
action_taken = Text(master)
action_taken.insert("3.0", "Internal testing showed no errors on our system.\n"
                    "ITOC is contacting relevant teams.\n"
                    "ITOC is checking with the operator.")
action_taken.place(x=400, y=40, width=390, height=100)
action_taken.get("1.0", "end-1c")

# Root Cause
root_cause_label = Label(master, text="Root Cause").place(x=400, y=175)
root_cause_variable = StringVar(master)
root_cause_variable.set(root_cause[0])  # default value
root_cause_options = OptionMenu(master, root_cause_variable, *root_cause)
root_cause_options.place(y=193, x=400)

# Comms Manager
comms_manager_label = Label(master, text="Comms Manager").place(x=400, y=250)
comms_manager_variable = StringVar(master)
comms_manager_variable.set(comms_manager[0])  # default value
comms_manager_options = OptionMenu(master, comms_manager_variable, *comms_manager)
comms_manager_options.place(y=270, x=400)

# Crisis Manager
crisis_manager_label = Label(master, text="Crisis Manager").place(x=400, y=300)
crisis_manager_variable = StringVar(master)
crisis_manager_variable.set(crisis_manager[0])  # default value
crisis_manager_options = OptionMenu(master, crisis_manager_variable, *crisis_manager)
crisis_manager_options.place(y=320, x=400)

# Escalated by
escalated_by_label = Label(master, text="Escalated by:").place(x=400, y=350)
escalated_by = StringVar()
escalated_by.set("<name>(+886 226 560 700 ext 207)")
escalated_by_entry_box = Entry(master, textvariable=escalated_by, width=50).place(x=400, y=370, height=25)

# Clik ID
clik_id_label = Label(master, text="Clik ID (ITOC PD) SUPL-XXXX").place(x=400, y=395)
clik_id = StringVar()
clik_id.set("N/A")
clik_id_entry_box = Entry(master, textvariable=clik_id, width=50).place(x=400, y=415, height=25)

# Customer Ref
customer_ref_label = Label(master, text="Customer Ref# (AS Jira) SUPL-XXXX").place(x=400, y=440)
customer_ref = StringVar()
customer_ref.set("N/A")
customer_ref_entry_box = Entry(master, textvariable=customer_ref, width=50).place(x=400, y=460, height=25)

# Teams Chat/Bitly shorten to list
teams_chat_label = Label(master, text='Shorten to Bitly URL (Needs "HTTP/S"): \n Join Microsoft Teams Chat').place(x=400, y=505, anchor="w")
bitly_url = StringVar()
teams_chat_entry_box = Entry(master, textvariable=bitly_url, width=50).place(x=400, y=520, height=25)



def select_affecting_system():
    splash_window = Tk()
    splash_window.title("Select Affecting System")
    screen_width = splash_window.winfo_screenwidth()
    screen_height = splash_window.winfo_screenheight()
    login_width = 300
    login_height = 300
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    splash_window.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')

    # Creates the list and label inside the window
    def listbox_used(event):
        global items
        global af_label
        items = []
        curselection = listbox.curselection()
        for index in curselection:
            items.append(listbox.get(index))  # Gets current selection from listbox
        af_label = Label(master, text=(', '.join(items)))
        af_label.place(y=147, x=150)

    yscrollbar = Scrollbar(splash_window)
    yscrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(splash_window, height=10, selectmode='multiple', yscrollcommand=yscrollbar.set)

    for item in affecting_system:
        listbox.insert(affecting_system.index(item), item)

    listbox.bind("<<ListboxSelect>>", listbox_used)
    listbox.pack(padx=10, pady=10, expand=YES, fill="both")

    yscrollbar.config(command=listbox.yview)

    def close_window():
        splash_window.destroy()

    pick_button = Button(splash_window, text="Select", command=lambda: close_window()).pack(pady=20)


    splash_window.mainloop()


# Overwrites the existing label. Not recommended
def clear_affecting_systems():
    items.clear()
    overwrite_af_label = Label(master, text=('                                    '
                                             '                                    '
                                             '                                    '
                                             '                                    '))
    overwrite_af_label.place(y=147, x=150)


def select_operators():
    splash_window = Tk()
    splash_window.title("Select Affecting System")
    screen_width = splash_window.winfo_screenwidth()
    screen_height = splash_window.winfo_screenheight()
    login_width = 300
    login_height = 300
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    splash_window.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')

    # Creates the list and label inside the window
    def listbox_used(event):
        global op_items
        global op_label
        op_items = []
        curselection = listbox.curselection()
        for index in curselection:
            op_items.append(listbox.get(index))  # Gets current selection from listbox
        op_label = Label(master, text=(', '.join(op_items)))
        op_label.place(y=230, x=110)

    yscrollbar = Scrollbar(splash_window)
    yscrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(splash_window, height=10, selectmode='multiple', yscrollcommand=yscrollbar.set)

    for item in operator:
        listbox.insert(operator.index(item), item)

    listbox.bind("<<ListboxSelect>>", listbox_used)
    listbox.pack(padx=10, pady=10, expand=YES, fill="both")

    yscrollbar.config(command=listbox.yview)

    def close_window():
        splash_window.destroy()

    pick_button = Button(splash_window, text="Select", command=lambda: close_window()).pack(pady=20)

    splash_window.mainloop()


# Overwrites the existing label. Not recommended
def clear_operators():
    op_items.clear()
    overwrite_op_label = Label(master, text=('                                    '
                                             '                                    '
                                             '                                    '
                                             '                                    '
                                             '                                    '
                                             '                                    '
                                             '                                    '
                                             '                                    '))
    overwrite_op_label.place(y=230, x=110)



def print_new():
    def set_bold():
        try:
            T.tag_add('bold', 'sel.first', 'sel.last')
        except Exception as ex:
            # text not selected
            print(ex)

    try:
        final = f"""
Status: {status_variable.get()}
Severity: {severity_variable.get()}
Name: {name.get()}
Affecting System: {', '.join(items)}
Tier: {tier_variable.get()}
Operator: {', '.join(op_items)}
Time Elapsed: {elapsed_time.get()} 
Start Time: {cal.get_date()} {start_time.get()} (GMT+8)
End Time: {end_time.get()} 
Service Degradation: {service_degradation_variable.get()}
Symptoms: {symptoms.get()}
Action Taken: {action_taken.get("1.0", "end-1c")}
Root Cause: {root_cause_variable.get()}
Comms Manager: {comms_manager_variable.get()}
Crisis Manager: {crisis_manager_variable.get()}
Escalated by: {escalated_by.get()}

Clik ID: {clik_id.get()}
Customer Ref#: {customer_ref.get()}

Join Microsoft Teams Chat: N/A

"""
        root = Tk()
        root.geometry("800x500")
        T = Text(root, height=80, width=80)
        l = Label(root, text="Template")
        l.config(font=("Courier", 14))
        b2 = Button(root, text="Exit", command=root.destroy)

        l.pack()
        T.pack()
        b2.pack()

        T.insert(tk.END, final)


    except NameError:
        messagebox.showerror('Error', 'Missing Info.')
        pass

    tk.mainloop()


def print_template():
    try:
        final = f"""
Status: {status_variable.get()}
Severity: {severity_variable.get()}
Name: {name.get()}
Affecting System: {', '.join(items)}
Tier: {tier_variable.get()}
Operator: {', '.join(op_items)}
Time Elapsed: {elapsed_time.get()}
Start Time: {cal.get_date()} {start_time.get()} (GMT+8)
End Time: {end_time.get()} (GMT+8)
Service Degradation: {service_degradation_variable.get()}
Symptoms: {symptoms.get()}
Action Taken: {action_taken.get("1.0", "end-1c")}
Root Cause: {root_cause_variable.get()}
Comms Manager: {comms_manager_variable.get()}
Crisis Manager: {crisis_manager_variable.get()}
Escalated by: {escalated_by.get()}

Clik ID: {clik_id.get()}
Customer Ref#: {customer_ref.get()}

Join Microsoft Teams Chat: {','.join(shortener.shorten_urls([bitly_url.get()]))}

    """
        root = Tk()
        root.geometry("800x500")
        T = Text(root, height=80, width=80)
        l = Label(root, text="Template")
        l.config(font=("Courier", 14))
        b2 = Button(root, text="Exit", command=root.destroy)

        l.pack()
        T.pack()
        b2.pack()
        T.insert(tk.END, final)

    except NameError:
        messagebox.showerror('Error', 'Missing Info')
        pass

    tk.mainloop()

print_button = Button(master, text="Print New", command=lambda: print_new())
print_button.place(y=0, x=300)
print_button = Button(master, text="Print With Teams Chat", command=lambda: print_template())
print_button.place(y=0, x=400)
print_button = Button(master, text="Affecting System", command=lambda: select_affecting_system())
print_button.place(y=147, x=0)
clear_affecting_system_button = Button(master, text="Clear", command=lambda: clear_affecting_systems())
clear_affecting_system_button.place(y=147, x=103)
print_button = Button(master, text="Operators", command=lambda: select_operators())
print_button.place(y=230, x=0)
clear_affecting_system_button = Button(master, text="Clear", command=lambda: clear_operators())
clear_affecting_system_button.place(y=230, x=65)


mainloop()
