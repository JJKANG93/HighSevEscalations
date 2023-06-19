from tkinter import CENTER, Tk, Label, StringVar, OptionMenu, Entry, Text, Scrollbar, RIGHT, Y, Listbox, YES, Button, \
    mainloop, END, Frame, messagebox, TclError, WORD, Menu, font
from tkcalendar import Calendar
import bitlyshortener
from bitlyshortener.exc import RequestError, ArgsError, ShortenerError
import re
from datetime import datetime
import klembord
import json
from jira import JIRA, JIRAError
import psutil
# import smtplib

# Updated History
# 2022/10/28 新增多系統百分比附加, 簡易計算百分比
# 2022/11/09 多import一個模組JIRAError
# 2022/11/09 修復Create Jira ticket. 新增顯示Jira 錯誤訊息
# 2023/03/31 修改Action Taken的內容可在json檔新增修改
# 2023/04/09 新增：Clik ID自動填入、時間日期帶入APP開啟時間、取得當下時間按鈕
# 2023/04/09 移除：持續顯示當下時間，降低佔用資源
# 2023/05/28 增加效能检查psutil
# 2023/06/02 增加倒计时按钮
# 2023/06/13 Bring to front when countdown ends + trigger PD(Hidden)

# Main Window
master = Tk()
app_width = 800
app_height = 600
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
# main window start in the center of the screen
master.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
master.title('High Severity Escalation App --Version 8.4')


# File Menu


def help():
    splash_window = Tk()
    splash_window.title("Help")
    splash_window.winfo_screenwidth()
    splash_window.winfo_screenheight()
    login_width = 300
    login_height = 300
    x = (screen_width /2) - (login_width /2)
    y = (screen_height /2 ) - (login_height /2)
    splash_window.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')

    yscrollbar = Scrollbar(splash_window)
    yscrollbar.pack(side=RIGHT, fill=Y)
    help_box = Text(splash_window, height=120, width=300, undo=True, wrap=WORD)
    help_box.insert("end", "Help\n\n"
                           "1. Time Elapsed is automatically calculated. You just need to fill in the 'Now' time. "
                           "Only resolved escalations will have End Time printed. Time Elapsed 是自動計算的. "
                           "只需要填寫“現在”時間. 只有Resolved才會打印 End Time\n\n"
                           "2. You need to use the Copy button on the print page to copy the bold. You can only copy "
                           "to HTML editors. 您需要使用打印頁面上的複制按鈕來複製粗體. 您只能複製到 HTML 編輯器.\n\n"
                           "3. Bitly API can only do 10 free URLs a month."
                           " You can login to Bitly with our own account. Bitly API 每月只能做 100 個免費 UR."
                           " 您可以使用我們自己的帳戶登錄 Bitly.\n\n"
                           "4. Symptoms will default to escalation name if left blank.如果留空，"
                           "Symptoms將默認為 Escalation Name。 \n\n"
                           "5. Crisis Manager will default to Comms Manager if blank or 'Comms Manager' filled in. "
                           "如果為空白或填寫“Comms Manager”，Crisis Manager 將默認為 Comms Manager. ")
    help_box.pack()


menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)
menu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Help", command=help)
menubar.add_cascade(label="File", menu=filemenu)
master.config(menu=menubar)

# Opening JSON file and put them into a list
status = []
severity = []
affecting_system = []
tier = []
operator = []
service_degradation = []
root_cause = []
comms_manager = []
action_taken_text = []


with open('config.json', 'r', encoding='utf-8') as json_file:
    # with open(r'C:\Users\joyh\OneDrive - Luanta\App\config.json', 'r', encoding='utf-8') as json_file:
    # with open(r'C:\Users\joyh\OneDrive - Luanta\App\config.json') as json_file:
    data = json.load(json_file)

    status_list = list(data.values())
    status.append(status_list[0])

    severity_list = list(data.values())
    severity.append(severity_list[1])

    affecting_system_list = list(data.values())
    affecting_system.append(affecting_system_list[2])

    tier_list = list(data.values())
    tier.append(tier_list[3])

    operator_list = list(data.values())
    operator.append(operator_list[4])

    service_degradation_list = list(data.values())
    service_degradation.append(service_degradation_list[5])

    root_cause_list = list(data.values())
    root_cause.append(root_cause_list[6])

    comms_manager_list = list(data.values())
    comms_manager.append(comms_manager_list[7])

    action_taken = data["action_taken"]
    action_taken_text = "\n".join([str(x) for x in action_taken if x])


# Create another list for the functions to use


def lst_generator(lst1, lst2):
    for x in lst1:
        for y in x:
            lst2.append(y)


status2 = []
lst_generator(status, status2)

severity2 = []
lst_generator(severity, severity2)

affecting_system2 = []
lst_generator(affecting_system, affecting_system2)

tier2 = []
lst_generator(tier, tier2)

operator2 = []
lst_generator(operator, operator2)

service_degradation2 = []
lst_generator(service_degradation, service_degradation2)

root_cause2 = []
lst_generator(root_cause, root_cause2)

comms_manager2 = []
lst_generator(comms_manager, comms_manager2)


# Status Dropdown Menu
status_label = Label(master, text="Status", font=("Ariel", 10, "bold"))
status_label.place(x=0, y=0)
status_variable = StringVar(master)
status_variable.set(status2[0])  # default value
status_options = OptionMenu(master, status_variable, *status2)
status_options.place(y=16, x=0)

# Severity Dropdown Menu
severity_label = Label(master, text="Severity", font=("Ariel", 10, "bold"))
severity_label.place(x=165, y=0)
severity_variable = StringVar(master)
severity_variable.set(severity2[0])  # default value
severity_options = OptionMenu(master, severity_variable, *severity2)
severity_options.place(x=165, y=17)

# Escalation Name
name_label = Label(master, text="Escalation Name", font=("Ariel", 10, "bold"))
name_label.place(x=0, y=95)
name = StringVar()
name.set("GPM degradation by XX% affecting <xxx>")
name_entry_box = Entry(master, textvariable=name, width=42)
name_entry_box.place(x=0, y=120, height=25)

# Tier
tier_label = Label(master, text="Tier", font=("Ariel", 10, "bold"))
tier_label.place(x=240, y=0)
tier_variable = StringVar(master)
tier_variable.set(tier2[0])  # default value
tier_options = OptionMenu(master, tier_variable, *tier2)
tier_options.place(x=240, y=17)


def click_clear_entry1(event):
    start_time_entry_box1.delete(0, "end")
    return None


def click_clear_entry2(event):
    start_time_entry_box2.delete(0, "end")
    return None


def click_clear_entry3(event):
    end_time_entry_box1.delete(0, "end")
    return None


def click_clear_entry4(event):
    end_time_entry_box2.delete(0, "end")
    return None

# Get Current Time


sel_date1 = datetime.now().date().strftime("%Y-%m-%d")

sel_date2 = datetime.now().date().strftime("%Y-%m-%d")


def update_time():
    # E_now = datetime.now()
    # E_hour = E_now.hour
    # E_minute = E_now.minute
    end_time1.set("{:02d}".format(datetime.now().hour))
    end_time2.set("{:02d}".format(datetime.now().minute))
    global sel_date2
    sel_date2 = datetime.now().date().strftime("%Y-%m-%d")
    cal_label2.config(text=sel_date2)


# Start Hour 1
start_time_label = Label(
    master, text="Start Time (GMT+8):", font=("Ariel", 10, "bold"))
start_time_label.place(x=65, y=340)
start_time1 = StringVar()
start_time1.set("{:02d}".format(datetime.now().hour))
start_time_entry_box1 = Entry(
    master, textvariable=start_time1, width=4, justify='center')
start_time_entry_box1.bind("<Button-1>", click_clear_entry1)
start_time_entry_box1.place(x=65, y=365, height=25)

# Start Hour 2
start_time2 = StringVar()
start_time2.set("{:02d}".format(datetime.now().minute))
start_time_entry_box2 = Entry(
    master, textvariable=start_time2, width=4, justify='center')
start_time_entry_box2.bind("<Button-1>", click_clear_entry2)
start_time_entry_box2.place(x=95, y=365, height=25)

# End Hour 1
end_time_label = Label(
    master, text="Now/End Time (GMT+8):", font=("Ariel", 10, "bold"))
end_time_label.place(x=65, y=400)
end_time1 = StringVar()
end_time1.set("{:02d}".format(datetime.now().hour))
end_time_entry_box1 = Entry(
    master, textvariable=end_time1, width=4, justify='center')
end_time_entry_box1.bind("<Button-1>", click_clear_entry3)
end_time_entry_box1.place(x=65, y=425, height=25)

# End Hour 2
end_time2 = StringVar()
end_time2.set("{:02d}".format(datetime.now().minute))
end_time_entry_box2 = Entry(
    master, textvariable=end_time2, width=4, justify='center')
end_time_entry_box2.bind("<Button-1>", click_clear_entry4)
end_time_entry_box2.place(x=95, y=425, height=25)


# Time Elapsed
def time_elapsed(year1, month1, day1, hour1, min1, year2, month2, day2, hour2, min2):
    start_time = datetime(int(year1), int(
        month1), int(day1), int(hour1), int(min1))
    end_time = datetime(int(year2), int(month2),
                        int(day2), int(hour2), int(min2))

    c = end_time - start_time
    txt = str(c)[:-3]  # string can change if days are included or not
    z = re.split("\\s", txt)  # splits into "###, days, hh:mm"
    # splits only hh:mm and removes a set of brackets on the hh:mm
    a = re.split(":", ", ".join(z))
    if "-" in txt:
        return 'date error'
    # z length of 3 is equal to "###, days, hh:mm"
    elif len(z) == 3 and z[2] and z[2][-2:] == "00" and z[2][:-3] == "0":
        return z[0] + "d"  # gives #d only
    elif len(z) == 3 and z[2] and z[2][:-3] == "0":
        # gives #d and #m int function removes leading zero
        return z[0] + "d" + " " + str(int(z[2][-2:])) + "m"
    elif len(z) == 3 and z[2] and z[2][-2:] == "0":
        return z[0] + "d" + " " + z[2][:-3] + "h"  # gives #d #h
    elif len(z) == 3 and z[2]:
        return z[0] + "d" + " " + z[2][:-3] + "h" + " " + str(
            int(z[2][-2:])) + "m"  # gives #d #h #m int func removes leading zero

    # z length of 1 is equal to "hh:mm"
    elif len(z) == 1 and a[1] == "00":
        return a[0] + "h"  # gives #h
    elif len(z) == 1 and a[0] == "0":
        # gives #m int function removes leading zero
        return str(int(a[1])) + "m"
    elif len(z) == 1:
        # gives #H #m int function removes leading zero
        return a[0] + "h" + " " + str(int(a[1])) + "m"
    else:
        print('no match')


# Checks if resolved comms is sent
def resolved_checker():
    if status_variable.get() == "Resolved" or status_variable.get() == "New/Resolved" or \
            status_variable.get() == "Re-occurring/Resolved":
        return str(sel_date2[0:4]) + "-" + str(sel_date2[5:7]) + "-" + str(sel_date2[8:10]) + " " + \
            str((end_time1.get().rjust(2, '0'))) + ":" + \
            str((end_time2.get().rjust(2, '0'))) + " (GMT+8)"
    else:
        return "N/A"


# Calendar1
def get_date1():
    splash_window = Tk()
    splash_window.title("Select Start Date")
    splash_window.winfo_screenwidth()
    splash_window.winfo_screenheight()
    login_width = 300
    login_height = 300
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    splash_window.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')
    cal = Calendar(splash_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=20)
    Button(splash_window, text="Select", command=lambda: select_date1()).pack()

    # Select Date Within Calendar
    def select_date1():
        global sel_date1
        cal_label1.config(text=cal.get_date())
        sel_date1 = cal.get_date()
        splash_window.destroy()
        return sel_date1


button = Button(master, text="Start Date", command=lambda: get_date1())
button.place(x=0, y=340)

cal_label1 = Label(master, text=sel_date1)
cal_label1.place(x=0, y=369)


# Calendar2
def get_date2():
    splash_window = Tk()
    splash_window.title("Select End Date")
    splash_window.winfo_screenwidth()
    splash_window.winfo_screenheight()
    login_width = 300
    login_height = 300
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    splash_window.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')
    cal = Calendar(splash_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=20)
    Button(splash_window, text="Select", command=lambda: select_date2()).pack()

    # Select Date Within Calendar
    def select_date2():
        global sel_date2
        cal_label2.config(text=cal.get_date())
        sel_date2 = cal.get_date()
        splash_window.destroy()
        return sel_date2


button = Button(master, text="End Date", command=lambda: get_date2())
button.place(x=0, y=400)

cal_label2 = Label(master, text=sel_date2)
cal_label2.place(x=0, y=430)


# Service Degradation
service_degradation_label = Label(
    master, text="Service Degradation", font=("Ariel", 10, "bold"))
service_degradation_label.place(x=160, y=45)
service_degradation_variable = []
# service_degradation_variable = StringVar(master)
# service_degradation_variable.set(service_degradation2[0])  # default value
# service_degradation_options = OptionMenu(
#     master, service_degradation_variable, *service_degradation2)
# service_degradation_options.place(x=160, y=65)

# Service Degradation V2

s1 = Entry(master, width=4, justify='center')
s2 = Entry(master, width=4, justify='center')
s3 = Entry(master, width=4, justify='center')
s4 = Entry(master, width=4, justify='center')
s5 = Entry(master, width=4, justify='center')
s6 = Entry(master, width=4, justify='center')
s7 = Entry(master, width=4, justify='center')
s8 = Entry(master, width=4, justify='center')
s9 = Entry(master, width=4, justify='center')
s10 = Entry(master, width=4, justify='center')
s11 = Entry(master, width=4, justify='center')
s12 = Entry(master, width=4, justify='center')

all_degradation = []


def showPercent():
    global all_degradation
    all_degradation = []
    service_degradation_variable = [s1.get(), s2.get(), s3.get(), s4.get(), s5.get(
    ), s6.get(), s7.get(), s8.get(), s9.get(), s10.get(), s11.get(), s12.get()]
    try:
        for i in range(0, len(service_degradation_variable)):
            if not service_degradation_variable[0]:
                all_degradation.append("N/A")
                all_degradation[1:] = []
            elif int(service_degradation_variable[i]) > 0:
                all_degradation.append(service_degradation_variable[i] + "%")
    except ValueError:
        print("not number")


s1.place(x=160, y=65)
s2.place(x=190, y=65)
s3.place(x=220, y=65)
s4.place(x=250, y=65)
s5.place(x=280, y=65)
s6.place(x=310, y=65)
s7.place(x=160, y=85)
s8.place(x=190, y=85)
s9.place(x=220, y=85)
s10.place(x=250, y=85)
s11.place(x=280, y=85)
s12.place(x=310, y=85)


# Degradation Calculation %
def select_all(event):
    cal_degradation_entry_box1.select_range(0, 'end')  # 選取所有文字
    cal_degradation_entry_box2.select_range(0, 'end')
    return 'break'


cal_degradation_label = Label(
    master, text="Percent Calculation %", font=("Ariel", 10, "bold"))
cal_degradation_label.place(x=0, y=300)

cal_degradation1 = StringVar()
cal_degradation1.set("NN")
cal_degradation_entry_box1 = Entry(
    master, textvariable=cal_degradation1, width=4, justify='center')
cal_degradation_entry_box1.place(x=0, y=320, height=20)

cal_degradation2 = StringVar()
cal_degradation2.set("NN")
cal_degradation_entry_box2 = Entry(
    master, textvariable=cal_degradation2, width=4, justify='center')
cal_degradation_entry_box2.place(x=40, y=320, height=20)

cal_degradation_entry_box1.bind('<FocusIn>', select_all)
cal_degradation_entry_box2.bind('<FocusIn>', select_all)


cal_P = Button(master, text="Calculator",
               command=lambda: degradationP())
cal_P_font = font.Font(size=0, weight='bold')
cal_P['font'] = cal_P_font
cal_P.place(x=80, y=320, height=20)

PercentE = StringVar()


def degradationP():
    if float(cal_degradation1.get()) > float(cal_degradation2.get()):
        Percent_result = ((float(cal_degradation1.get())-float(cal_degradation2.get())
                           ) / float(cal_degradation1.get()))*100
        PercentE = str(Percent_result).split(".")
        if int(PercentE[0]) > 49:
            Presult = Label(master, text=PercentE[0], font=(
                "Ariel", 10, "bold"), fg="red")
            pp = Label(master, text="%", font=("Ariel", 10, "bold"), fg="red")
        elif int(PercentE[0]) <= 49 and int(PercentE[0]) >= 25:
            Presult = Label(master, text=PercentE[0], font=(
                "Ariel", 10, "bold"), fg="orange")
            pp = Label(master, text="%", font=(
                "Ariel", 10, "bold"), fg="orange")
        else:
            Presult = Label(master, text=PercentE[0], font=(
                "Ariel", 10, "bold"), fg="black")
            pp = Label(master, text="%", font=(
                "Ariel", 10, "bold"), fg="black")
    else:
        Percent_result = ((float(cal_degradation2.get())-float(cal_degradation1.get())
                           ) / float(cal_degradation2.get()))*100
        PercentE = str(Percent_result).split(".")
        if int(PercentE[0]) > 49:
            Presult = Label(master, text=PercentE[0], font=(
                "Ariel", 10, "bold"), fg="red")
            pp = Label(master, text="%", font=("Ariel", 10, "bold"), fg="red")
        elif int(PercentE[0]) <= 49 and int(PercentE[0]) >= 25:
            Presult = Label(master, text=PercentE[0], font=(
                "Ariel", 10, "bold"), fg="orange")
            pp = Label(master, text="%", font=(
                "Ariel", 10, "bold"), fg="orange")
        else:
            Presult = Label(master, text=PercentE[0], font=(
                "Ariel", 10, "bold"), fg="black")
            pp = Label(master, text="%", font=(
                "Ariel", 10, "bold"), fg="black")
    Presult.place(x=180, y=320, height=20)
    pp.place(x=200, y=320, height=20)


# Symptoms
symptoms_label = Label(master, text="Symptoms", font=("Ariel", 10, "bold"))
symptoms_label.place(x=0, y=450)
symptoms = Text(master, undo=True, wrap=WORD)
symptoms.insert("3.0", "")
symptoms.place(x=0, y=470, height=100, width=390)


# Fills in escalation name by default if blank
def symptoms_checker():
    if symptoms.get('1.0', 'end-1c') == "" or symptoms.get('1.0', 'end-1c') == name.get():
        return name.get()
    else:
        return symptoms.get('1.0', 'end-1c')


# Action Taken
action_taken_label = Label(
    master, text="Action Taken", font=("Ariel", 10, "bold"))
action_taken_label.place(x=550, y=0)
action_taken = Text(master, undo=True, wrap=WORD)
action_taken.insert("3.0", action_taken_text)
action_taken.place(x=400, y=20, width=390, height=130)
action_taken.get("1.0", "end-1c")

# Root Cause
root_cause_label = Label(master, text="Root Cause", font=("Ariel", 10, "bold"))
root_cause_label.place(x=0, y=45)
root_cause_variable = StringVar(master)
root_cause_variable.set(root_cause2[0])  # default value
root_cause_options = OptionMenu(master, root_cause_variable, *root_cause2)
root_cause_options.place(x=0, y=65)

# Comms Manager
comms_manager_label = Label(
    master, text="Comms Manager", font=("Ariel", 10, "bold"))
comms_manager_label.place(x=400, y=150)
comms_manager_variable = StringVar(master)
comms_manager_variable.set(comms_manager2[0])  # default value
comms_manager_options = OptionMenu(
    master, comms_manager_variable, *comms_manager2)
comms_manager_options.place(x=400, y=170)

# Crisis Manager
crisis_manager_label = Label(
    master, text="Crisis Manager", font=("Ariel", 10, "bold"))
crisis_manager_label.place(x=400, y=200)
crisis_manager_variable = StringVar(master)
crisis_manager_variable.set("Comms Manager")
crisis_manager_entry_box = Entry(
    master, textvariable=crisis_manager_variable, width=50)
crisis_manager_entry_box.place(x=400, y=220, height=25)


def crisis_man_checker():
    if crisis_manager_variable.get().lower() == "comms manager" or crisis_manager_variable.get().lower() == "comms" \
            or crisis_manager_variable.get() == "communication manager" or crisis_manager_variable.get() == "":
        return comms_manager_variable.get()
    else:
        return crisis_manager_variable.get()


# Escalated by
escalated_by_label = Label(master, text="Escalated by:", font=("Ariel", 10, "bold"))
escalated_by_label.place(x=400, y=250)
escalated_by = StringVar()
escalated_by.set(str(list(data.values())[12]))
escalated_by_entry_box = Entry(master, textvariable=escalated_by, width=50)
escalated_by_entry_box.place(x=400, y=270, height=25)

# Clik ID
clik_id_label = Label(master, text="Clik ID SUPL-XXXX",
                      font=("Ariel", 10, "bold"))
clik_id_label.place(x=460, y=300)
clik_id = StringVar()
clik_id.set("N/A")
clik_id_entry_box = Entry(master, textvariable=clik_id, width=40)
clik_id_entry_box.place(x=460, y=320, height=25)

# Jira
supl_button = Button(master, text="Create \nSUPL",
                     command=lambda: jira_generator())
supl_button.place(x=400, y=305)

# Jira Login from config file
user = str(list(data.values())[9])
apikey = str(list(data.values())[10])
server = str(list(data.values())[11])

options = {
    'server': server
}
jira = JIRA(options, basic_auth=(user, apikey))


def jira_generator():
    showPercent()
    global single_issue
    try:
        if shortener(bitly_url) == "Invalid URL":
            messagebox.showinfo('Bitly Error', 'Invalid URL\n無效URL')
        elif sel_date1 is None or sel_date2 is None:
            messagebox.showinfo('Error',
                                'There was an error! Please check the minimum required fields for an escalation!\n'
                                '發生錯誤! 請確認各欄位!')
        elif time_elapsed(int(sel_date1[0:4]), int(sel_date1[5:7]), int(sel_date1[8:10]),
                          int(start_time1.get()), int(
                start_time2.get()), int(sel_date2[0:4]),
                int(sel_date2[5:7]), int(
                sel_date2[8:10]), int(end_time1.get()),
                int(end_time2.get())) == 'date error':
            messagebox.showinfo('Date Error', 'Check the date! \n'
                                              '     確認日期')
        elif items is None or op_items is None or items == [] or op_items == []:
            messagebox.showinfo('Error',
                                'There was an error! Please check the minimum required fields for an escalation!\n'
                                '發生錯誤! 請確認各欄位!')
        else:
            issue_dict = {
                'project': {'id': 10002},  # TSB project ID
                'summary': name.get(),
                'description': f'Status: {status_variable.get()}\n'
                               f'Severity: {severity_variable.get()}\n'
                               f'Name: {name.get()}\n'
                               f'Affecting System: {", ".join(items)}\n'
                               f'Tier: {tier_variable.get()}\n'
                               f'Operator: {", ".join(op_items)}\n'
                               f"""Time Elapsed: {time_elapsed(int(sel_date1[0:4]), int(sel_date1[5:7]), int(sel_date1[8:10]), int(start_time1.get()), int(start_time2.get()), int(sel_date2[0:4]), int(sel_date2[5:7]), int(sel_date2[8:10]), int(end_time1.get()), int(end_time2.get()))}\n"""
                               f'Start Time: '
                               f"""{sel_date1[0:4]}-{sel_date1[5:7]}-{sel_date1[8:10]} {(start_time1.get().rjust(2, '0'))}:{(start_time2.get().rjust(2, '0'))} (GMT+8)\n"""
                               f'End Time: {resolved_checker()}\n'
                               f'Service Degradation: {", ".join(all_degradation)}\n'
                               f'Symptoms: {symptoms_checker()}\n'
                               f'Action Taken: {action_taken.get("1.0", "end-1c")}\n'
                               f'Root Cause: {root_cause_variable.get()}\n'
                               f'Comms Manager: {comms_manager_variable.get()}\n'
                               f'Crisis Manager: {crisis_man_checker()}\n'
                               f'Escalated by: {escalated_by.get()}\n'
                               f'\n\n'
                               f'Clik ID: {clik_id.get()}\n'
                               f'Customer Ref#: {customer_ref.get()}\n'
                               f'\n\n'
                               f'Join Microsoft Teams Chat: {shortener(bitly_url)}',
                'issuetype': {'name': 'MG+ Support Ticket'},
                'customfield_10053': {'value': 'Alert'},  # Call Type
                'components': [{"name": "General Failure"}],  # Components
                'customfield_10051': {'value': 'K2'},  # Provider
                'customfield_10037': {'value': 'K2'},  # Head Office
            }
            new_issue = jira.create_issue(fields=issue_dict)
            single_issue = jira.issue(new_issue.key)
            clik_id.set(str(single_issue))
            root = Tk()
            T = Text(root, font='Ariel 10', height=15,
                     width=35, undo=True, wrap=WORD)
            T.pack()
            T.insert("end", "Ticket created successfully!\n\n" + str(single_issue) +
                     "\n\nhttps://asiasupport247.atlassian.net/browse/" + str(single_issue))
            return f'{single_issue}'
    except TypeError:
        messagebox.showinfo('Error', 'Please fill out the escalation fields first.\n'
                                     '發生錯誤! 請確認各欄位.')
    except ValueError:
        messagebox.showinfo('Error', 'Please fill out the escalation fields first.\n'
                                     '發生錯誤! 請確認各欄位.')
    except JIRAError as eM:
        print(eM.status_code, eM.text)
        if eM.status_code == 401:
            messagebox.showinfo('Error', 'Your API key might be expired. Please get a New API key for Atlassian via https://id.atlassian.com/manage-profile/security/api-tokens.\n\n'
                                'API Key可能已過期,請獲取新的API Key.\n\nError code: ' + str(eM.status_code) + '\n' + str(eM.text))
        else:
            messagebox.showinfo('Error', str(
                eM.status_code) + '\n' + str(eM.text))


# Customer Ref
customer_ref_label = Label(
    master, text="Customer Ref# (AS Jira) SUPL-XXXX", font=("Ariel", 10, "bold"))
customer_ref_label.place(x=400, y=350)
customer_ref = StringVar()
customer_ref.set("N/A")
customer_ref_entry_box = Entry(master, textvariable=customer_ref, width=50)
customer_ref_entry_box.place(x=400, y=380, height=25)

# Teams Chat/Bitly shorten to list
teams_chat_label = Label(master, text='Shorten to Bitly URL (needs "https://"): \n'
                         'Join Microsoft Teams Chat', justify="left", font=("Ariel", 10, "bold"))
teams_chat_label.place(x=400, y=430, anchor="w")
bitly_url = StringVar()
bitly_url.set("N/A")
teams_chat_entry_box = Entry(master, textvariable=bitly_url, width=50)
teams_chat_entry_box.place(x=400, y=460, height=25)


# Bitly Setup
def shortener(url):
    bitly_url_fix = []
    bitly_url_fix = str(bitly_url.get()).split("/", 3)
    url = bitly_url.get()
    # Use your own API key
    tokens_pool = ['d2375064d1ef535690914f2d2d96d7390b41fb10']
    shortener = bitlyshortener.Shortener(
        tokens=tokens_pool, max_cache_size=256)

    if url == "N/A" or bitly_url_fix[2] == "bit.ly":
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


# Setup error statement in print function
items = None


# Select Affecting System from listbox
def select_affecting_system():
    splash_window = Tk()
    splash_window.title("Select Affecting System")
    splash_window.winfo_screenwidth()
    splash_window.winfo_screenheight()
    login_width = 300
    login_height = 300
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    splash_window.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')

    yscrollbar = Scrollbar(splash_window)
    yscrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(splash_window, height=10,
                      selectmode='multiple', yscrollcommand=yscrollbar.set)
    yscrollbar.config(command=listbox.yview)

    for item in affecting_system2:
        listbox.insert(affecting_system2.index(item), item)

    # Creates the list and label inside the window
    def listbox_used(event):
        global items
        items = []
        curselection = listbox.curselection()
        for index in curselection:
            # Gets current selection from listbox
            items.append(listbox.get(index))

    listbox.bind("<<ListboxSelect>>", listbox_used)
    listbox.pack(padx=10, pady=10, expand=YES, fill="both")

    # Displays current selection
    def select():
        global af_label
        af_label = Label(af_frame, text=(', '.join(items)),
                         wraplength=100, justify="center")
        af_label.pack()
        splash_window.destroy()

    Button(splash_window, text="Select", command=lambda: select()).pack(pady=0)
    items.clear()
    af_label.destroy()

    splash_window.mainloop()


# Affecting System Buttons
af_button = Button(master, text="Affecting System:",
                   command=lambda: select_affecting_system())
af_button.place(x=0, y=147)

# Affecting System Frame
af_frame = Frame(master)
af_frame.place(x=0, y=180)

# Setup error statement in print function
op_items = None


# Select Operators from listbox
def select_operators():
    splash_window = Tk()
    splash_window.title("Select Operators")
    splash_window.winfo_screenwidth()
    splash_window.winfo_screenheight()
    login_width = 300
    login_height = 300
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    splash_window.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')

    yscrollbar = Scrollbar(splash_window)
    yscrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(splash_window, height=10,
                      selectmode='multiple', yscrollcommand=yscrollbar.set)
    yscrollbar.config(command=listbox.yview)

    for item in operator2:
        listbox.insert(operator2.index(item), item)

    # Creates the list and label inside the window
    def listbox_used(event):
        global op_items
        op_items = []
        curselection = listbox.curselection()
        for index in curselection:
            # Gets current selection from listbox
            op_items.append(listbox.get(index))

    listbox.bind("<<ListboxSelect>>", listbox_used)
    listbox.pack(padx=10, pady=10, expand=YES, fill="both")

    def select():
        global op_label
        op_label = Label(op_frame, text=(', '.join(op_items)), wraplength=120)
        op_label.pack()
        splash_window.destroy()

    Button(splash_window, text="Select", command=lambda: select()).pack(pady=0)
    op_items.clear()
    op_label.destroy()

    splash_window.mainloop()

# Operator Buttons
operator_button = Button(master, text="Operators:",command=lambda: select_operators())
operator_button.place(x=150, y=147)

# Operator Frame
op_frame = Frame(master)
op_frame.place(x=130, y=180)


# Prints the fully sent escalation comms
def print_template():
    showPercent()
    global T
    klembord.set_text('Nothing to copy!')
    try:
        if shortener(bitly_url) == "Invalid URL":
            messagebox.showinfo('Bitly Error', 'Invalid URL\n無效URL')
        elif sel_date1 is None or sel_date2 is None:
            messagebox.showinfo('Error',
                                'There was an error! Please check the minimum required fields for an escalation!\n'
                                '發生錯誤! 請確認各欄位!')
        elif time_elapsed(int(sel_date1[0:4]), int(sel_date1[5:7]), int(sel_date1[8:10]),
                          int(start_time1.get()), int(
                              start_time2.get()), int(sel_date2[0:4]),
                          int(sel_date2[5:7]), int(
                              sel_date2[8:10]), int(end_time1.get()),
                          int(end_time2.get())) == 'date error':
            messagebox.showinfo('Date Error', 'Check the date! \n'
                                              '     確認日期')
        elif items is None or op_items is None or items == [] or op_items == []:
            messagebox.showinfo('Error',
                                'There was an error! Please check the minimum required fields for an escalation!\n'
                                '發生錯誤! 請確認各欄位!')
        else:
            root = Tk()
            root.title("High Sev Escalation")
            T = Text(root, font='Ariel 10', height=25, width=80, undo=True)
            l = Label(root, text="Template")
            note = Label(
                root, text="Note: Can only copy bold text to an HTML editor.")
            l.config(font=("Courier", 14))
            b2 = Button(root, text="Exit",command=root.destroy )
            clipboard_button = Button(
                root, text="Copy Text", command=lambda: copy())
            l.pack()
            T.pack()
            note.pack()
            clipboard_button.pack(ipadx=20)
            b2.pack()

            T.tag_configure('bold', font='Ariel 10 bold')
            TAG_TO_HTML = {
                ('tagon', 'bold'): '<b>',
                ('tagoff', 'bold'): '</b>',
            }

            # Lets you copy and paste bold to HTML editors
            def copy():
                klembord.set_with_rich_text('Status', f'<b>Status: </b>{status_variable.get()}'
                                                      f'<br><b>Severity: </b>{severity_variable.get()}'
                                                      f'<br><b>Name: </b>{name.get()}'
                                                      f'<br><b>Affecting System: </b>{", ".join(items)}'
                                                      f'<br><b>Tier: </b>{tier_variable.get()}'
                                                      f'<br><b>Operator: </b>{", ".join(op_items)}'
                                                      f"""<br><b>Time Elapsed:</b> {time_elapsed(int(sel_date1[0:4]), int(sel_date1[5:7]), int(sel_date1[8:10]), int(start_time1.get()), int(start_time2.get()), int(sel_date2[0:4]), int(sel_date2[5:7]), int(sel_date2[8:10]), int(end_time1.get()), int(end_time2.get()))}"""
                                                      f'<br><b>Start Time: </b>'
                                                      f"""{sel_date1[0:4]}-{sel_date1[5:7]}-{sel_date1[8:10]} {(start_time1.get().rjust(2, '0'))}:{(start_time2.get().rjust(2, '0'))} (GMT+8)"""
                                                      f'<br><b>End Time: </b>{resolved_checker()}'
                                                      f'<br><b>Service Degradation: </b>{", ".join(all_degradation)}'
                                                      f'<br><b>Symptoms: </b>{symptoms_checker()}'
                                                      f'<br><b>Action Taken: </b>{action_taken.get("1.0", "end-1c")}'
                                                      f'<br><b>Root Cause: </b>{root_cause_variable.get()}'
                                                      f'<br><b>Comms Manager: </b>{comms_manager_variable.get()}'
                                                      f'<br><b>Crisis Manager: </b>{crisis_man_checker()}'
                                                      f'<br><b>Escalated by: </b>{escalated_by.get()}'
                                                      f'<br>'
                                                      f'<br><b>Clik ID: </b>{clik_id.get()}'
                                                      f'<br><b>Customer Ref#: </b>{customer_ref.get()}'
                                                      f'<br>'
                                                      f'<br><b>Join Microsoft Teams Chat: </b>{shortener(bitly_url)}')

            # Shows bold in the print template
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
            T.insert("end",
                     f"""{time_elapsed(int(sel_date1[0:4]), int(sel_date1[5:7]), int(sel_date1[8:10]),
                                       int(start_time1.get()), int(
                                           start_time2.get()), int(sel_date2[0:4]),
                                       int(sel_date2[5:7]), int(
                                           sel_date2[8:10]), int(end_time1.get()),
                                       int(end_time2.get()))}\n""")
            T.insert("end", "Start Time: ", "bold")
            T.insert("end",
                     f"{sel_date1[0:4]}-{sel_date1[5:7]}-{sel_date1[8:10]} {(start_time1.get().rjust(2, '0'))}:{(start_time2.get().rjust(2, '0'))} (GMT+8)\n")
            T.insert("end", "End Time: ", "bold")
            T.insert("end", f"{resolved_checker()}\n")
            T.insert("end", "Service Degradation: ", "bold")
            T.insert("end", f"{', '.join(all_degradation)}\n")
            T.insert("end", "Symptoms: ", "bold")
            T.insert("end", f"{symptoms_checker()}\n")
            T.insert("end", "Action Taken: ", "bold")
            T.insert("end", f"{action_taken.get('1.0', 'end-1c')}\n")
            T.insert("end", "Root Cause: ", "bold")
            T.insert("end", f"{root_cause_variable.get()}\n")
            T.insert("end", "Comms Manager: ", "bold")
            T.insert("end", f"{comms_manager_variable.get()}\n")
            T.insert("end", "Crisis Manager: ", "bold")
            T.insert("end", f"{crisis_man_checker()}\n")
            T.insert("end", "Escalated by: ", "bold")
            T.insert("end", f"{escalated_by.get()}\n\n")
            T.insert("end", "Clik ID: ", "bold")
            T.insert("end", f"{clik_id.get()}\n")
            T.insert("end", "Customer Ref#: ", "bold")
            T.insert("end", f"{customer_ref.get()}\n\n")
            T.insert("end", "Join Microsoft Teams Chat: ", "bold")
            T.insert("end", f"{shortener(bitly_url)}")

    # Backup Errors
    except NameError:
        messagebox.showinfo('Error', 'Please fill out the escalation fields first.\n'
                                     '發生錯誤! 請確認各欄位.')
        pass
    except ValueError:
        messagebox.showinfo('Error', 'Please fill out the escalation fields first.\n'
                                     '發生錯誤! 請確認各欄位.')

    mainloop()


# Get Current Time Button
gettime_button = Button(master, text="Get Time", command=lambda: update_time())
gettime_button_font = font.Font(size=0, weight='bold')
gettime_button['font'] = gettime_button_font
gettime_button.config(height=2, width=10)
gettime_button.place(x=135, y=425, height=25)

# Big print button
print_button = Button(master, text="Print", command=lambda: printandcount())
print_button_font = font.Font(size=0, weight='bold')
print_button['font'] = print_button_font
print_button.config(height=2, width=10)
print_button.place(x=600, y=500)

# Count down Button
countdown_button = Button(master, text="Countdown", command=lambda: countdown2())
countdown_button_font = font.Font(size=0, weight='bold')
countdown_button['font'] = countdown_button_font
countdown_button.config(height=2, width=10)
countdown_button.place(x=420, y=500)

current_job = None
def countdown2():
    global current_job

    if current_job: #check if theres a running countdown
        master.after_cancel(current_job) #reset status
    if severity_variable.get() == "A":
        seconds = 30 * 60
    else:
        seconds = 60 * 60

    def decrement_time():
        global current_job
        nonlocal seconds
        if seconds > 0:
            minutes, secs = divmod(seconds, 60)
            time_string = "{:02d}:{:02d}".format(minutes, secs)
            countdown_button.config(text=time_string)
            seconds -= 1
            current_job = master.after(1000, decrement_time)
        else:
            # send_email()
            master.attributes("-topmost", True)
            master.attributes("-topmost", False)
            messagebox.showinfo("Time's Up!", "Please draft a updated comms")

    decrement_time()

def printandcount():
    global current_job
    countdown2()
    print_template()
    current_job = None

# def send_email():
#     # Set up the SMTP connection
#     try:
#         smtp = smtplib.SMTP("smtp.gmail.com", 587)  # Replace with your SMTP server and port
#         smtp.starttls()
#         smtp.login("itoperationcentre247@gmail.com","muxzrtysritzoiit")  # Replace with your email and password
#     except smtplib.SMTPException as e:
#         messagebox.showerror("Error", f"Failed to establish SMTP connection: {e}")
#         return
#
#     # Create the email message
#     recipient = "it-operations-centre-email@bigasia.pagerduty.com"  # Replace with the recipient's email address
#     subject = "Please prepare a updated comms for " + clik_id.get()
#     message = name.get()
#
#     email_message = f"Subject: {subject}\n\n{message}"
#
#     # Send the email
#     try:
#         smtp.sendmail("itoperationcentre247@gmail.com", recipient, email_message)  # Replace with your email
#         messagebox.showinfo("Success", "Email sent successfully!")
#     except smtplib.SMTPException as e:
#         messagebox.showerror("Error", f"Failed to send email: {e}")
#
#     # Close the SMTP connection
#     smtp.quit()


#Monitor memory usage
def update_memory_usage():
    pid = psutil.Process().pid
    process = psutil.Process(pid)
    memory_info = process.memory_info()
    memory_usage = memory_info.rss
    memory_usage_readable = psutil._common.bytes2human(memory_usage)
    update_memory_usage_label = Label(
    master, text=f"Memory usage: {memory_usage_readable} ", font=("Ariel", 10, "bold"))
    update_memory_usage_label.place(x=600, y=570)
    update_memory_usage_label.config(text=f"Memory usage: {memory_usage_readable} ")
    update_memory_usage_label.after(60000, update_memory_usage)

update_memory_usage()


mainloop()
