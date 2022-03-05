from tkinter import Tk, Label, StringVar, OptionMenu, Entry, Text, Scrollbar, RIGHT, Y, Listbox, YES, Button, mainloop, \
    END, Frame, messagebox, TclError
import bitlyshortener
from bitlyshortener.exc import RequestError, ArgsError, ShortenerError
import time
from datetime import date, datetime
import klembord

# Main Window
master = Tk()
app_width = 800
app_height = 600
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
master.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')  # main window start in the center of the screen
master.title('High Sev Escalation App --Version 3.5')

status = ["New",
          "New/Resolved",
          "Updated",
          "Ongoing",
          "On Hold",
          "Resolved",
          "Re-occurring",
          "Re-occurring/Resolved",
          "Canceled"]

severity = ["A", "B"]

affecting_system = ["all", "Live Dealer", "TNGQuickfire", "MGP SW", "QF2", "Sempris", "TEG0", "TEG1", "TEG2", "TEG3",
                    "TEG4", "TEG6"]

tier = ["N/A", "Tier_1", "Tier_2"]

operator = ["all", "TEG1", "GT", "TEG2", "BBIN_CNY", "TEG3", "JuGaming(A)",
            "TEG4", "JuGamingA(6)", "JuGamingA(12)", "JuGamingA(18)", "JuGamingA(25)",
            "JuGamingA(28)", "TEG6", "Oriental_Game", "OG", "TEG0", "Power_Asia", "infini88",
            "Asia888", "ambtw", "topusd3", "TOP_USD2",
            "Poseidon", "TH1GAMES", "TOP_USD(GAMA)", "UEG", "inplaymatrix", "GplayG", "MGP SW", "AMBSW",
            "AMBGAMESSW", "pay4dsw",
            "Sempris", "W88", "Wild_Treasure", "188bet", "Asiabet", "Solid_Gaming", "GSD", "Foxnos", "M88",
            "Asian_Logic", "VWIN", "SBO"]

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
                 "Juan Gilpin (+886 909948943)"
                 "Ran Alkalay",
                 "Arik Klein",
                 "Jamil Saab",
                 "Yaacov Pines"]

crisis_manager = ["Abri Liebenberg (+61 432823087)",
                  "Matt Cheng (+886 932075280)",
                  "Matthew Geoghegan (+886 905249541)",
                  "Bartosz Lewandowski (+886 978705232)",
                  "Jeff Huang (+886 933308768)",
                  "Jill Shen (+886 903438345)",
                  "Frank Hsu (+886 972211756)",
                  "Juan Gilpin (+886 909948943)",
                  "Ran Alkalay",
                  "Arik Klein",
                  "Jamil Saab",
                  "Yaacov Pines"]


# Status Dropdown Menu
status_label = Label(master, text="Status").place(x=0, y=0)
status_variable = StringVar(master)
status_variable.set(status[0])  # default value
status_options = OptionMenu(master, status_variable, *status)
status_options.place(y=15, x=0)


def resolved_checker():
    if status_variable.get() == "Resolved" or status_variable.get() == "New/Resolved" or \
            status_variable.get() == "Re-occurring/Resolved":
        return str(year2_str.get()) + "-" + str(month2_str.get()) + "-" + str(day2_str.get()) + " " + \
               str(end_time.get()) + " " + "(GMT+8)"
    else:
        return "N/A"


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
name_entry_box = Entry(master, textvariable=name, width=42).place(x=0, y=120, height=25)

# Tier
tier_label = Label(master, text="Tier").place(x=0, y=175)
tier_variable = StringVar(master)
tier_variable.set(tier[0])  # default value
tier_options = OptionMenu(master, tier_variable, *tier)
tier_options.place(y=193, x=0)

# Start Time
start_time_label = Label(master, text="Date & Start Time (GMT+8):").place(x=0, y=305)
start_time = StringVar()
start_time.set("10:30")
start_time_entry_box = Entry(master, textvariable=start_time, width=0).place(x=100, y=325, height=25)

# End Time
end_time_label = Label(master, text="Date & Now/End Time (GMT+8):").place(x=0, y=355)
end_time = StringVar()
end_time.set("11:30")
end_time_entry_box = Entry(master, textvariable=end_time, width=0).place(x=100, y=375, height=25)


# Time Elapsed for Hours and Minutes
def elapsed_time(start, end):
    a = datetime.strptime(start, '%H:%M')
    b = datetime.strptime(end, '%H:%M')

    diff = b - a

    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    if hours > 0 and mins > 0:
        return str(hours) + "h " + (str(mins) + "m")
    elif hours > 0:
        return str(hours) + "h"
    elif mins > 0:
        return str(mins) + "m"
    elif mins == 0:
        return str("N/A")
    else:
        pass


# Time Elapsed for Days and Dates
year1_str = StringVar()
year1_str.set(2022)
year1 = Entry(master, textvariable=year1_str, width=0).place(x=0, y=325, height=25)
year1_int = year1

month1_str = StringVar()
month1_str.set("MM")
month1 = Entry(master, textvariable=month1_str, width=0).place(x=40, y=325, height=25)
month1_int = month1

day1_str = StringVar()
day1_str.set("DD")
day1 = Entry(master, textvariable=day1_str, width=0).place(x=70, y=325, height=25)
day1_int = day1

year2_str = StringVar()
year2_str.set(2022)
year2 = Entry(master, textvariable=year2_str, width=0).place(x=0, y=375, height=25)
year_int = year2

month2_str = StringVar()
month2_str.set("MM")
month2 = Entry(master, textvariable=month2_str, width=0).place(x=40, y=375, height=25)
month2_int = month2

day2_str = StringVar()
day2_str.set("DD")
day2 = Entry(master, textvariable=day2_str, width=0).place(x=70, y=375, height=25)
day2_int = day2


# Day difference calculator
def num_of_days(year1, month1, day1, year2, month2, day2):
    date1 = date(year1, month1, day1)
    date2 = date(year2, month2, day2)
    date_diff = (date2 - date1).days
    if date_diff > 0:
        return str(date_diff) + "d"
    else:
        return str("")


# Show Current Time
def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    clock_label = Label(master)
    clock_label.place(x=0, y=260)
    clock_label.config(text="Current Time (GMT+8): \n" + hour + ":" + minute + ":" + second, justify="left")
    clock_label.after(1000, clock)


clock()

# Service Degradation
service_degradation_label = Label(master, text="Service Degradation").place(x=0, y=400)
service_degradation_variable = StringVar(master)
service_degradation_variable.set(service_degradation[0])  # default value
service_degradation_options = OptionMenu(master, service_degradation_variable, *service_degradation)
service_degradation_options.place(y=420, x=0)

# Symptoms
symptoms_label = Label(master, text="Symptoms").place(x=0, y=450)
symptoms = Text(master)
symptoms.insert("3.0", "GPM degradation by XX% affecting <xxx>")
symptoms.place(x=0, y=470, height=100, width=390)

# Action Taken
action_taken_label = Label(master, text="Action Taken").place(x=550, y=20)
action_taken = Text(master)
action_taken.insert("3.0", "Internal testing showed no errors on our system. "
                           "ITOC is contacting relevant teams. "
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
escalated_by.set("<name> (+886 226 560 700 ext 207)")
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
teams_chat_label = Label(master, text='Shorten to Bitly URL (Needs "https://"): \n '
                                      'Join Microsoft Teams Chat', justify="left").place(x=400, y=505, anchor="w")
bitly_url = StringVar()
bitly_url.set("N/A")
teams_chat_entry_box = Entry(master, textvariable=bitly_url, width=50).place(x=400, y=520, height=25)


# Bitly Setup
def shortener(url):
    url = bitly_url.get()
    tokens_pool = ['d2375064d1ef535690914f2d2d96d7390b41fb10']  # Use your own API key.
    shortener = bitlyshortener.Shortener(tokens=tokens_pool, max_cache_size=256)

    if url == "N/A":
        return url
    elif url != "":
        try:
            return str(','.join(shortener.shorten_urls([bitly_url.get()])))
        except RequestError:
            return str("Invalid URL")
        except ArgsError:
            return str("Invalid URL")
        except ShortenerError:
            return str("Invalid URL")
    else:
        return str("N/A")


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

    yscrollbar = Scrollbar(splash_window)
    yscrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(splash_window, height=10, selectmode='multiple', yscrollcommand=yscrollbar.set)
    yscrollbar.config(command=listbox.yview)

    for item in affecting_system:
        listbox.insert(affecting_system.index(item), item)

    # Creates the list and label inside the window
    def listbox_used(event):
        global items
        items = []
        curselection = listbox.curselection()
        for index in curselection:
            items.append(listbox.get(index))  # Gets current selection from listbox

    listbox.bind("<<ListboxSelect>>", listbox_used)
    listbox.pack(padx=10, pady=10, expand=YES, fill="both")

    def select():
        global af_label
        af_label = Label(af_frame, text=(', '.join(items)), wraplength=240,
                         justify="center")  # Displays current selection
        af_label.pack()
        splash_window.destroy()

    select_button = Button(splash_window, text="Select", command=lambda: select()).pack(pady=0)
    af_label.destroy()

    splash_window.mainloop()


# Affecting System Buttons
af_button = Button(master, text="Affecting System:", command=lambda: select_affecting_system())
af_button.place(y=147, x=0)

# Affecting System Frame
af_frame = Frame(master, width=235, height=80)
af_frame.place(x=150, y=150)


# Select operators from a listbox
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

    yscrollbar = Scrollbar(splash_window)
    yscrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(splash_window, height=10, selectmode='multiple', yscrollcommand=yscrollbar.set)
    yscrollbar.config(command=listbox.yview)

    for item in operator:
        listbox.insert(operator.index(item), item)

    # Creates the list and label inside the window
    def listbox_used(event):
        global op_items
        op_items = []
        curselection = listbox.curselection()
        for index in curselection:
            op_items.append(listbox.get(index))  # Gets current selection from listbox

    listbox.bind("<<ListboxSelect>>", listbox_used)
    listbox.pack(padx=10, pady=10, expand=YES, fill="both")

    def select():
        global op_label
        op_label = Label(op_frame, text=(', '.join(op_items)), wraplength=120, justify="left")
        op_label.pack()
        splash_window.destroy()

    select_button = Button(splash_window, text="Select", command=lambda: select()).pack(pady=0)
    op_label.destroy()

    splash_window.mainloop()


# Operator Buttons
operator_button = Button(master, text="Operators:", command=lambda: select_operators())
operator_button.place(y=230, x=0)

# Operator Frame
op_frame = Frame(master, width=170, height=80)
op_frame.place(x=230, y=230)


def print_template():
    global T
    if shortener(bitly_url) == "Invalid URL":
        messagebox.showinfo('Error', 'Bitly: Invalid URL')
    else:
        try:
            root = Tk()
            root.title("High Sev Escalation")
            T = Text(root, font=('Ariel 10'), height=25, width=80)
            l = Label(root, text="Template")
            l.config(font=("Courier", 14))
            b2 = Button(root, text="Exit", command=root.destroy)
            clipboard_button = Button(root, text="Copy Text", command=lambda: copy())
            l.pack()
            T.pack()
            b2.pack()
            clipboard_button.pack(ipadx=20)

            T.tag_configure('bold', font='Ariel 10 bold')
            TAG_TO_HTML = {
                ('tagon', 'bold'): '<b>',
                ('tagoff', 'bold'): '</b>',
                        }

            def copy():
                klembord.set_with_rich_text('Status', f'<b>Status: </b>{status_variable.get()}'
                                                      f'<br><b>Severity: </b>{severity_variable.get()}'
                                                      f'<br><b>Name: </b>{name.get()}'
                                                      f'<br><b>Affecting System: </b>{", ".join(items)}'
                                                      f'<br><b>Tier: </b>{tier_variable.get()}'
                                                      f'<br><b>Operator: </b>{", ".join(op_items)}'
                                                      f'<br><b>Time Elapsed:</b> {num_of_days(int(year1_str.get()), int(month1_str.get()), int(day1_str.get()), int(year2_str.get()), int(month2_str.get()), int(day2_str.get()))} {elapsed_time(start_time.get(), end_time.get())}'
                                                      f'<br><b>Start Time: </b>{year1_str.get()}-{month1_str.get()}-{day1_str.get()} {start_time.get()} (GMT+8)'
                                                      f'<br><b>End Time: </b>{resolved_checker()}'
                                                      f'<br><b>Service Degradation: </b>{service_degradation_variable.get()}'
                                                      f'<br><b>Symptoms: </b>{symptoms.get("1.0", "end-1c")}'
                                                      f'<br><b>Action Taken: </b>{action_taken.get("1.0", "end-1c")}'
                                                      f'<br><b>Root Cause: </b>{root_cause_variable.get()}'
                                                      f'<br><b>Comms Manager: </b>{comms_manager_variable.get()}'
                                                      f'<br><b>Crisis Manager: </b>{crisis_manager_variable.get()}'
                                                      f'<br><b>Escalated by: </b>{escalated_by.get()}'
                                                      f'<br>'
                                                      f'<br><b>Clik ID: </b>{clik_id.get()}'
                                                      f'<br><b>Customer Ref#: </b>{customer_ref.get()}'
                                                      f'<br>'
                                                      f'<br><b>Join Microsoft Teams Chat: </b>{shortener(bitly_url)}')

            def copy_rich_text(event):
                try:
                    txt = T.get('sel.first', 'sel.last')
                except TclError:
                    # no selection
                    return "break"
                content = T.dump('sel.first', 'sel.last', tag=True, text=True)
                html_text = []
                for key, value, index in content:
                    if key == "text":
                        html_text.append(value)
                    else:
                        html_text.append(TAG_TO_HTML.get((key, value), ''))
                klembord.set_with_rich_text(txt, ''.join(html_text))
                return "break"  # prevent class binding to be triggered

            T.insert("end", "Status: ", "bold")
            T.insert("end", f"{status_variable.get()}\n")
            T.insert("end", "Severity: ", "bold")
            T.insert("end", f"{severity_variable.get()}\n")
            T.insert("end", "Name: ", "bold")
            T.insert("end", f"{name.get()}\n")
            T.insert("end", "Affecting System: ", "bold")
            T.insert("end", f"{', '.join(items)}\n")
            T.insert("end", "Tier: ", "bold")
            T.insert("end", f"{tier_variable.get()}\n")
            T.insert("end", "Operator: ", "bold")
            T.insert("end", f"{', '.join(op_items)}\n")
            T.insert("end", "Time Elapsed: ", "bold")
            T.insert("end", f"{num_of_days(int(year1_str.get()), int(month1_str.get()), int(day1_str.get()), int(year2_str.get()), int(month2_str.get()), int(day2_str.get()))} {elapsed_time(start_time.get(), end_time.get())}\n")
            T.insert("end", "Start Time: ", "bold")
            T.insert("end", f"{year1_str.get()}-{month1_str.get()}-{day1_str.get()} {start_time.get()} (GMT+8)\n")
            T.insert("end", "End Time: ", "bold")
            T.insert("end", f"{resolved_checker()}\n")
            T.insert("end", "Service Degradation: ", "bold")
            T.insert("end", f"{service_degradation_variable.get()}\n")
            T.insert("end", "Symptoms: ", "bold")
            T.insert("end", f"{symptoms.get('1.0','end-1c')}\n")
            T.insert("end", "Action Taken: ", "bold")
            T.insert("end", f"{action_taken.get('1.0', 'end-1c')}\n")
            T.insert("end", "Root Cause: ", "bold")
            T.insert("end", f"{root_cause_variable.get()}\n")
            T.insert("end", "Comms Manager: ", "bold")
            T.insert("end", f"{comms_manager_variable.get()}\n")
            T.insert("end", "Crisis Manager: ", "bold")
            T.insert("end", f"{crisis_manager_variable.get()}\n")
            T.insert("end", "Escalated by: ", "bold")
            T.insert("end", f" {escalated_by.get()}\n\n")
            T.insert("end", "Clik ID: ", "bold")
            T.insert("end", f"{clik_id.get()}\n")
            T.insert("end", "Customer Ref#: ", "bold")
            T.insert("end", f"{customer_ref.get()}\n\n")
            T.insert("end", "Join Microsoft Teams Chat: ", "bold")
            T.insert("end", f"{shortener(bitly_url)}")

        except NameError:
            T.insert(END, f"There is an error! Please check the minimum required fields for an escalation.")
            pass
        except ValueError:
            T.insert(END, 'There is an error! Please check the minimum required fields for an escalation.')
            pass

        mainloop()

print_button = Button(master, text="Print", command=lambda: print_template())
print_button.place(y=0, x=350)

mainloop()
